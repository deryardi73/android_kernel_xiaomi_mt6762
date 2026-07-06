# Python 3 compatibility shim.
#
# The legacy MediaTek DCT tool (tools/dct/obj/*.py) was written for
# Python 2 and does `import ConfigParser`. In Python 3 this module was
# renamed to `configparser` (lowercase). Placing this file as
# tools/dct/obj/ConfigParser.py lets every old `import ConfigParser`
# statement in the codebase keep working unmodified, instead of having
# to patch each file individually.
#
# `SafeConfigParser` was an alias kept for backward-compat in early
# Python 3, but was removed entirely in Python 3.12 (which is what
# recent Ubuntu GitHub Actions runners ship). We re-add it here as an
# alias to ConfigParser so old code calling
# ConfigParser.SafeConfigParser(...) doesn't crash either.

from configparser import *  # noqa: F401,F403
from configparser import ConfigParser, RawConfigParser

try:
    from configparser import SafeConfigParser
except ImportError:
    SafeConfigParser = ConfigParser
