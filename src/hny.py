# IMPORTS #
import os
from sys import path
path.append('.\\src')
from lex import *
from yacc import *
import sys
from trans import *
import parser
from zip import *
del main


prf, psf = "", ""
print(f""":::    ::: ::::    :::
:+:    :+: :+:+:   :+:
+:+    +:+ :+:+:+  +:+
+#++:++#++ +#+ +:+ +#+
+#+    +#+ +#+  +#+#+#
#+#    #+# #+#   #+#+#
###    ### ###    ####

pHoney ver 1.9.8a for Microsoft Windows\n""")

if "python" in sys.argv:sys.argv.remove("python")

# prepare save paths

outpath = os.path.splitext(os.path.normpath(os.path.abspath(parse_path_args(sys.argv)[0])))[0]+".exe"

for i in range(len(sys.argv)):
    if sys.argv[i] == '-o':
        outpath = sys.argv[i + 1]
        break
    pass

# attempt to load file
if len(sys.argv) < 2:
    print('Error: file expected')
    raise SystemExit
try:
    with open(os.path.normpath(os.path.abspath(parse_path_args(sys.argv)[0])), 'rt', encoding="utf-8") as _:pass
    pass
except FileNotFoundError:
    print(prf + 'Error: file not found' + psf)
    raise SystemExit
except PermissionError:
    print(prf + 'Error: permission denied' + psf)
    raise SystemExit
except KeyboardInterrupt:raise SystemExit
except SystemExit as E:raise SystemExit
except BaseException as E:
    print(f"Error: internal error. additional info: {E}")
    raise SystemExit

with open(os.path.normpath(os.path.abspath(parse_path_args(sys.argv)[0])), 'rt', encoding="utf-8") as f:lines = f.read()
print(len(lines), 'bytes source, ', end='')
print(len(lines.splitlines()), 'lines.\n')

def fold(data: str):
    return data.replace('\\t', '    ').replace('\\b', ' <backspace> ').replace('\\r', ' <carriage-return> ').replace(' ', ' ').replace('\\n', ' <new-line> ')

try:
    ctx = Hacc().parser.parse(lines)
    pass
except KeyboardInterrupt:raise SystemExit
except SystemExit as E:raise SystemExit
except parser.ParseError as E:
    print(fold(str(E)))
    raise SystemExit
"""
except BaseException as E:
    print(f"Error: internal error. additional info: {E}")
    raise SystemExit
"""

if 1:print(ctx)

trn = Trans()

try:
    trn.walk(ctx, lines)
    print()
    pretty(trn.dump())
    print()
    print(trn.pregen())
    pass
except KeyboardInterrupt:raise SystemExit
except SystemExit as E:raise SystemExit
except parser.ParseError as E:
    print(fold(str(E)))
    raise SystemExit
"""
except BaseException as E:
    print(f"Error: internal error. additional info: {E}")
    raise SystemExit
#
"""