####################################################################
#                                                                  #
#   file: lexyac.py                                                #
#                                                                  #
#   This module contains functions which                           #
#   generates lexers and parsers (translators too) for my          #
#   programming language individually                              #
#                                                                  #
#   Credits: Chetchasov Ivan                                       #
#   (chetvano@gmail.com, talismanchet@vk.com, +7(965)353-32-22)    #
#                                                                  #
####################################################################

from typing import Sized, TextIO, Iterable

try:
    from lex import *
    from yacc import *
    from trans import *
    from zip import *
    pass
except ImportError:
    from src.lex import *
    from src.yacc import *
    from src.trans import *
    from src.zip import *
    pass
del main


# setup color output prefix/suffix
prf, psf = '', ''
stdrub = TextIO()
#
def clearzip(data: Iterable[tuple[Any, Any]]) -> Iterable[tuple[Any, Any]] | Sized:
    mx, my = len(list(data)), len(data[0])
    ret = []
    for x in range(my):
        ret.append([])
        for y in range(mx):
            ret[-1].append([])
            ret[x][y] = data[y][x]
            pass
        pass
    return ret

#
def hny_lexx():
    class TokenSheet(object):
        def __init__(self: object, value: Iterable[Iterable[LexToken]] = []) -> None:
            self.V = value
            pass
        def __repr__(self):
            return f'CTS \"{self.__name__}\"\n' + '{' + str(self.V)[1:][:-1].replace(', ', '\n').replace('\n', '\n\t') + '\n}'
        def __str__(self):
            ret: str = ''
            for l in self.V:
                for t in l:
                    ret += t.value() + ' '
                    pass
                ret += '\n'
                pass
            return ret
        __len__ = lambda self: len(self.V)
        def __getitem__(self, k):
            return self.V[k]
        def __setitem__(self, v, l, c):
            self.V[l][c] = v
            pass
        pass
    HNYRULES = [
    ['str', r'(\'[.^\']*\'|\"[.^\"]*\")'],
    ['comment', r'//.*|/\*.*/'],
    ['name', r'[A-Za-zА-Яа-яЁё_]\w*'],
    ['int', r'[+-]?(0[Xx][A-Za-z0-9][A-Za-z0-9_]*|\d+|1[01]*[Bb]|0[Bb])'],
    ['float', r'[+-]?\d*\.\d+'],
    ['plus', r'\+'],
    ['minus', r'\-'],
    ['star', r'\*'],
    ['slash', r'/'],
    ['back', r'\\'],
    ['colon', r'\:'],
    ['semi', r'\;'],
    ['dot', r'\.'],
    ['comma', r'\,'],
    ['amper', r'\&'],
    ['sharp', r'\#'],
    ['expl', r'\!'],
    ['dog', r'\@'],
    ['bux', r'\$'],
    ['percent', r'\%'],
    ['flex', r'\^'],
    ['lpar', r'\('],
    ['rpar', r'\)'],
    ['lblc', r'\['],
    ['rblc', r'\]'],
    ['lfig', r'\{'],
    ['rfig', r'\}'],
    ['lang', r'\<'],
    ['rang', r'\>'],
    ['equ', r'='],
    #['apos', r'\`'],
    ['tilde', r'\~'],       # Note:
    ['ignore', ' |\r|\f|\t'],  #   'ignore' and 'newline' token types
    ['newline', '\n']       #   must be listed in rules for correct
]                           #   <Lexer> type lexer work.
#                           #   upd: 'multilinecomment' too.
    let = Lex(HNYRULES)
    def ret(code):
        let.input(code)
        uwu = let.tokens()
        owo = [[]]
        comment = 0
        for i in uwu:
            # Note:
            #   This code made for trace
            #   comments or other ignoring
            #   tokens and discarding it
            # Upd:
            #   Now, this code also traces
            #   and handling newlines
            # Upd:
            #   This code is patch too:
            #   fixes strange bug that
            #   makes lexer catcantanate
            #   name and next left-block
            #   so, pr_in_t] = LexToken{name:"pr_in_t]":0}
            #   should:
            #       pr_in_t] = [LexToken{name:"pr_in_t":0}, LexToken{lblc:"]":7}]
            # Upd:
            #   Handles and discarding null lines
            if i.type() in ('ignore', 'comment', 'multilinecomment') or comment:
                pass
            elif i.type() == 'multilinecommentstart':
                comment = 1
                pass
            elif i.type() == 'multilinecommentendin':
                comment = 0
                pass
            elif i.type() == 'newline':
                owo.append([])
                pass
            elif i.type() != 'rblc' and i.value().endswith(']'):
                owo[-1].append([LexToken(i.type(), i.value()[:-1], i.pos()), LexToken('rblc', ']', i.pos()+len(i.value())-1)])
                pass
            else:
                owo[-1].append(i)
                pass
            pass
        # for more clear discarding null lines
        while [] in owo:
            owo.remove([])
            pass
        return TokenSheet(owo)
    return ret

#
hny_yacc = lambda: lambda code: Hacc().parser.parse(code)
