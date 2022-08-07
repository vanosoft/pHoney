####################################################################
#                                                                  #
#   file: lex.py                                                   #
#                                                                  #
#   This module contains classes for lexer code analisys           #
#   also for tracing unexpected symbols in code                    #
#   and enstablish token optimizing                                #
#                                                                  #
#   Credits: Chetchasov Ivan                                       #
#   (chetvano@gmail.com, talismanchet@vk.com, +7(965)353-32-22)    #
#                                                                  #
####################################################################

import re
import sys
from types import GeneratorType
from typing import Any
try:
    from zip import *
    pass
except ImportError:
    from src.zip import *
    pass
del main


# situation-specific routine
stdin, stdout, stderr = sys.stdin, sys.stdout, sys.stderr

# LexToken class -
# container for lexems (tokens)
# useful for operations with
# code syntax units
class LexToken(object):
    # Constructor
    def __init__(self, typ, val, pos):
        self.typ = typ
        self.val = val
        self.ps = pos

    def __len__(s):
        return len(str(s))

    # to str (output for user)
    def __str__(self):
        return '{\n\ttype: '+self.typ+',\n\tvalue: \"'+self.val+'\",\n\tpos: '+str(self.ps)+'\n}'
    
    # repr (debug output, or for posthandle)
    def __repr__(self):
        return str('LexToken{'+self.type()+':\"'+self.value()+'\":'+str(self.ps)+'}').replace('\n', '\\n')
    
    # getitem - for make it iterable
    def __getitem__(self, i):
        return [self.type, self.val][i]
    
    # setitem - for make it iterable
    def __setitem__(self, i, value):
        if i == 0:
            self.typ = value
            pass
        elif i == 1:
            self.val = value
            pass
        else:
            raise IndexError('Sequence index out of range: ' + str(i))

    # returns type of token
    def type(self):
        return self.typ
    
    # returns value of token
    def value(self):
        return self.val

    # returns where this token was found
    def pos(self):
        return self.ps
    pass

# LexError class -
# Exception for posthandle
# catching, raises if syntax
# error on lexing stage has
# occured, usual fatal
class LexError(Exception):
    # Constructor
    #
    # Note:
    #   typ - maybe "unexpected" or "missing"
    def __init__(self, token, line, pos, rpos, typ='unexpected'):
        self.token = token
        self.pos = pos
        self.type = typ
        self.line = line
        self.rpos = rpos
        pass
    pass

# Lex class -
# Class for lexer constructing
# uses RegExp for tokens detecting
# universal, can be used anywhere
class Lex(object):
    # Constructor
    #
    # rules - sequence of pairs
    # <typename, regexp>
    def __init__(self, rules):
        # init local variables
        self.pos = None
        self.buf = None
        self.line = None
        idx = 1
        regex_parts = []
        self.group_type = {}

        # loop which generates one big regexp based on groups
        for typ, regex in rules:
            groupname = 'GROUP%s' % idx
            regex_parts.append('(?P<%s>%s)' % (groupname, regex))
            self.group_type[groupname] = typ
            idx += 1

        # cancatanate regexp`s
        self.regex = re.compile('|'.join(regex_parts))

    # method uses for input string to lex
    def input(self, buf):
        self.buf = buf
        self.pos = 0
        self.lpos = 0
        self.line = 0

    # generates once token per call
    def token(self) :
        # end of buf?
        if self.pos >= len(self.buf):
            return None
        else:
            # token detect
            m = self.regex.match(self.buf, self.pos)
            if m:
                if "\n" in m.string:
                    self.line += 1
                    self.lpos = len(m.string.split("\n")[-1])
                    pass
                groupname = m.lastgroup
                tok_type = self.group_type[groupname]
                tok = LexToken(tok_type, m.group(groupname), self.pos)
                self.pos = m.end()
                return tok

            # if we're here, no rule matched
            raise LexError(LexToken('<unexpected>', self.buf[self.pos], self.pos), self.line, self.lpos, self.pos)

    # method to generate multiple tokens per call
    def tokens(self):
        while 1:
            tok = self.token()
            if tok is None: break
            yield tok
        return -1
    pass
