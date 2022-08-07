####################################################################
#                                                                  #
#   file: yacc2.py                                                 #
#                                                                  #
#   This module contains classes for parser code analisys          #
#   also for tracing unexpected structures(e.g. comma after comma) #
#   and creating code context table(AST)                           #
#                                                                  #
#   Credits: Chetchasov Ivan                                       #
#   (chetvano@gmail.com, talismanchet@vk.com, +7(965)353-32-22)    #
#                                                                  #
####################################################################

import re, sys
from types import GeneratorType, NoneType
from typing import Any, Iterable, Sized

from parser.parser import LRStackNode

try:
    from parser import Grammar, Parser
    pass
except ModuleNotFoundError:
    from src.parser import Grammar, Parser

try:
    from zip import *
    pass
except ImportError:
    from src.zip import *

    pass

def clearflat(array: list|tuple):
    ret = []
    for i in array:
        if isinstance(i, (tuple, list)):
            i = clearflat(i)
            ret += i
            pass
        else:ret.append(i)
        pass
    return ret

class YaccNode(object):
    par: tuple|list
    nod: LRStackNode
    #
    def __init__(self, parts: tuple | list = [], typ='${node}', node=None):
        self.typ = typ
        self.par = parts
        self.nod = node
        pass
    def __getitem__(s, k):
        return s.par[k]
    def __setitem__(s, k, v):
        s.par[k] = v
        pass
    def strvalue(self):
        if not self.par:
            return "{}"
        for i in self.par:
            yield str(i)
        pass
    __str__  = lambda s: s.typ + '\n{\n    ' + ('\n----------------\n'.join(s.strvalue())).replace('\n', '\n    ') + '\n}'
    __repr__ = __str__
    pass

def _root(_, n):
    return YaccNode(n[0], 'root', _)

def _line(_, n):
    return n[0]

def _comment(_, n):
    n=n[:-1]
    return YaccNode([n], "comment", _)

def _param(_, n):
    return YaccNode([n[1]], "param", _)

def _aka(_, n):
    return YaccNode([n[1]], "aka", _)

def _const(_, n):
    return YaccNode([n[1], n[3], n[5]], "const", _)

def _class(_, n):
    parent = n[1]
    name = n[3]
    body = n[4]
    return YaccNode([name,parent,body], "class", _)

def _member(_, n):
    if n[1] == "def":
        name = n[2]
        args = YaccNode([], "args", _) if n[4] is None else n[4]
        restype = YaccNode(["void"], "restype", _) if n[6] is None else n[6]
        return YaccNode([YaccNode([name,args,restype],"funcpreinit")],"member", _)
    name = n[1]
    typo = n[3]
    return YaccNode([YaccNode([name,typo], "define")], "member", _)

def _define(_, n):
   return YaccNode([n[0][0],n[0][1]],"define", _)

def _assign(_, n):
    return YaccNode([n[0],n[2]],"assign", _)

def _adefine(_, n):
    return YaccNode([n[0], YaccNode([n[0][0], n[2]], "assign", _)],"adefine", _)

def _private(_, n):
    return YaccNode([*n], "private", _)

def _public(_, n):
    return YaccNode([*n], "public", _)

def _function(_, n):
    name = n[1]
    args = args = n[3] if n[3] is not None else YaccNode([], "args", _)
    restype = n[5] if n[5] is not None else YaccNode(["void"], "restype", _)
    body = n[6]
    return YaccNode([name,args,restype,body],"function", _)

def _return(_, n):
    return YaccNode(["void" if n[1] is None else n[1]],"return", _)

def _call(_, n):
    name = n[0]
    args = n[2] if n[2] is not None else YaccNode(["void"], "argarray", _)
    return YaccNode([name,args],"call", _)

def _funcpreinit(_, n):
    return YaccNode(["void"], "nop", _)

def _interface(_, n):
    return YaccNode(n[1:], "interface", _)

def _block(_, n):
    return YaccNode(n[1:][:-1],"block", _)

def _rawinit(_, n):
    return YaccNode([n[0],n[2]],"rawinit", _)

def _args(_, n):
    return YaccNode(clearflat(n), "args", _)

def _typesign(_, n):
    return YaccNode([n[1]], "restype", _)

def _float(_, n):
    return YaccNode([n[0][0], n[0][2]], "float", _)

def _name(_, n):
    n = clearflat(n)
    while "." in n:n.remove(".")
    return YaccNode([n], "name", _)

def _arraycontent(_, n):
    while "," in n:n.remove(",")
    return YaccNode([n], "array", _)

def _array(_, n):
    return n[1]

def _dictentry(_, n):
    return YaccNode([n[0], n[2]], "dictmember", _)

def _dictcontent(_, n):
    while "," in n:n.remove(",")
    return YaccNode(clearflat(n), "dict", _)

def _dict(_, n):
    return n[1]

def _index(_, n):
    return YaccNode([n[1]], "index", _)

def _for(_, n):
    name = n[1]
    start = n[3]
    stop = n[5]
    block = n[6]
    return YaccNode([name,start,stop,YaccNode(["1"], "expr-int"),block], 'for', _)

def _forby(_, n):
    name = n[1]
    start = n[3]
    stop = n[5]
    step = n[7]
    block = n[8]
    return YaccNode([name,start,stop,step,block], 'for', _)

def _while(_, n):
    cond = n[1]
    body = n[2]
    return YaccNode([cond,body], 'while', _)

def _whiledo(_, n):
    cond = n[1]
    body = n[3]
    return YaccNode([cond,body], 'while', _)

def _dowhile(_, n):
    body = n[1]
    cond = n[3]
    return YaccNode([cond,body], 'dowhile', _)

def _foreach(_, n):
    name = n[1]
    itrn = n[3]
    body = n[4]
    return YaccNode([name,itrn,body], 'foreach', _)

_expression = [
    lambda _, n: YaccNode([n[1]],       "expr-neg", _),
    lambda _, n: n[1],
    lambda _, n: n[1],
    lambda _, n: YaccNode([n[0]],       "expr-int", _),
    lambda _, n: YaccNode([n[0]],       "expr-flt", _),
    lambda _, n: YaccNode([n[0]],       "expr-str", _),
    lambda _, n: YaccNode([n[0]],       "expr-nam", _),
    lambda _, n: YaccNode([n[0]],       "expr-arr", _),
    lambda _, n: YaccNode([n[0]],       "expr-dct", _),
    lambda _, n: YaccNode([n[0]],       "expr-cll", _),
    lambda _, n: YaccNode([n[0],n[2]],  "expr-lor", _),
    lambda _, n: YaccNode([n[0],n[2]],  "expr-lor", _),
    lambda _, n: YaccNode([n[0],n[2]],  "expr-and", _),
    lambda _, n: YaccNode([n[0],n[2]],  "expr-and", _),
    lambda _, n: YaccNode([n[0],n[2]],  "expr-equ", _),
    lambda _, n: YaccNode([n[0],n[2]],  "expr-neq", _),
    lambda _, n: YaccNode([n[0],n[2]],  "expr-xor", _),
    lambda _, n: YaccNode([n[0],n[2]],  "expr-xor", _),
    lambda _, n: YaccNode([n[0],n[2]],  "expr-sub", _),
    lambda _, n: YaccNode([n[0],n[2]],  "expr-mod", _),
    lambda _, n: YaccNode([n[0],n[2]],  "expr-add", _),
    lambda _, n: YaccNode([n[0],n[2]],  "expr-div", _),
    lambda _, n: YaccNode([n[0],n[2]],  "expr-fit", _),
    lambda _, n: YaccNode([n[0],n[2]],  "expr-mul", _),
    lambda _, n: YaccNode([n[0],n[2]],  "expr-pow", _),
    lambda _, n: YaccNode([n[0],n[2]],  "expr-fil", _),
    lambda _, n: YaccNode([n[1]],       "expr-not", _),
    lambda _, n: YaccNode([n[1]],       "expr-not", _),
    lambda _, n: YaccNode([n[1]],       "expr-not", _),
    lambda _, n: YaccNode([n[0], n[1]], "expr-get", _)
]

class Hacc:
    with open("grammar_0.txt") as f:
        grammar = f.read()
        pass
    actions = {
        'Sroot': _root,
        'Sline': _line,
        'Tcomment': _comment,
        "Sparam": _param,
        "Saka": _aka,
        "Sconst": _const,
        "Sclass": _class,
        "Smember": _member,
        "Sdefine": _define,
        "Sassign": _assign,
        "Sadefine": _adefine,
        "Sprivate": _private,
        "Spublic": _public,
        "Sfunction": _function,
        "Sreturn": _return,
        "Scall": _call,
        "Sfuncpreinit": _funcpreinit,
        "Sinterface": _interface,
        "Sblock": _block,
        "Srawinit": _rawinit,
        "Sargs": _args,
        "Stypesign": _typesign,
        "Sfloat": _float,
        "Sname": _name,
        "Sarraycontent": _arraycontent,
        "Sarray": _array,
        "Sdictentry": _dictentry,
        "Sdictcontent": _dictcontent,
        "Sdict": _dict,
        "Sindex": _index,
        "Sexpression": _expression,
        "Sfor": _for,
        "Swhile": _while,
        "Swhiledo": _whiledo,
        "Sdowhile": _dowhile,
        "Sforeach": _foreach,
        "Sforby": _forby
    }
    g = Grammar.from_string(grammar, re_flags = re.MULTILINE)
    parser = Parser(g, debug = False, actions = actions)
    pass
#
