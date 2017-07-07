#!/usr/bin/env python
import os, sys
if len(sys.argv) != 2:
    print("Usage: compile-file.py *byte-compiled-file*")
    sys.exit(1)
source = sys.argv[1]

assert source.endswith('.py')
basename = source[:-3]

# We do this crazy way to support Python 2.6 which
# doesn't support version_major, and has a bug in
# floating point so we can't divide 26 by 10 and get
# 2.6
PY_VERSION = sys.version_info[0] + (sys.version_info[1] / 10.0)

ver_prefix = "%s-%s" % (basename, PY_VERSION)
bytecode = "%s-good.pyc" % (ver_prefix)

import py_compile
print("compiling %s to %s" % (source, bytecode))
py_compile.compile(source, bytecode, 'exec')
asm_file = "%s.pyasm" % ver_prefix
cmd = "pydisasm --asm %s > %s" % (bytecode, asm_file)
print(cmd)
os.system(cmd)
cmd = "../xasm/cli.py %s" % asm_file
print(cmd)
os.system(cmd)
