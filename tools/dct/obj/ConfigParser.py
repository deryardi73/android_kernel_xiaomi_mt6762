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
import configparser as _configparser

# Some of MediaTek's .cmp config files (e.g. config/YuSu.cmp) contain
# duplicate option names within the same section. Python 2's
# ConfigParser silently let the last occurrence win; Python 3's
# ConfigParser defaults to strict=True and raises DuplicateOptionError
# instead. Subclassing here to default strict=False restores the old,
# lenient Python 2 behavior everywhere this module is used, without
# having to edit every ConfigParser.ConfigParser(...) call site.
class ConfigParser(_configparser.ConfigParser):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('strict', False)
        _configparser.ConfigParser.__init__(self, *args, **kwargs)

RawConfigParser = _configparser.RawConfigParser
SafeConfigParser = ConfigParser