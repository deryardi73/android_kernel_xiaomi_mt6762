#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (C) 2016 MediaTek Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See http://www.gnu.org/licenses/gpl-2.0.html for more details.	

import os, sys
import getopt
import traceback
import subprocess
import xml.dom.minidom

sys.dont_write_bytecode = True

sys.path.append('.')
sys.path.append('..')
# Python 3 removed implicit relative imports. The obj/*.py files use
# unqualified sibling imports like "from GpioObj import GpioObj" that
# relied on Python 2's package-relative lookup. Adding obj/ itself to
# sys.path lets those legacy imports keep resolving without having to
# patch every file inside obj/ individually.
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'obj'))

from ChipObj import ChipObj
from ChipObj import Everest
from ChipObj import Olympus
from ChipObj import MT6757_P25
from ChipObj import Rushmore
from ChipObj import Whitney
from ChipObj import MT6759
from ChipObj import MT6763
from ChipObj import MT6750S
from ChipObj import MT6758
from ChipObj import MT6739
from ChipObj import MT8695
from ChipObj import MT6771
from ChipObj import MT6775
from ChipObj import MT6779

from utility.util import LogLevel
from utility.util import log

def usage():
    print('''
usage: DrvGen [dws_path] [file_path] [log_path] [paras]...

options and arguments:

dws_path    :    dws file path
file_path   :    where you want to put generated files
log_path    :    where to store the log files
paras        :    parameter for generate wanted file
''')

def is_oldDws(path, gen_spec):
    if not os.path.exists(path):
        log(LogLevel.error, 'Can not find %s' %(path))
        sys.exit(-1)

    try:
        root = xml.dom.minidom.parse(dws_path)
    except Exception as e:
        log(LogLevel.warn, '%s is not xml format, try to use old DCT!' %(dws_path))
        if len(gen_spec) == 0:
            log(LogLevel.warn, 'Please use old DCT UI to gen all files!')
            return True
        old_dct = os.path.join(sys.path[0], 'old_dct', 'DrvGen')
        cmd = old_dct + ' ' + dws_path + ' ' + gen_path + ' ' + log_path + ' ' + gen_spec[0]
        if 0 == subprocess.call(cmd, shell=True):
            return True
        else:
            log(LogLevel.error, '%s format error!' %(dws_path))
            sys.exit(-1)

    return False

if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], '')

    if len(args) == 0:
        msg = 'Too less arguments!'
        usage()
        log(LogLevel.error, msg)
        sys.exit(-1)

    dws_path = ''
    gen_path = ''
    log_path = ''
    gen_spec = []

    # get DWS file path from parameters
    dws_path = os.path.abspath(args[0])

    # get parameters from input
    if len(args) == 1:
        gen_path = os.path.dirname(dws_path)
        log_path = os.path.dirname(dws_path)

    elif len(args) == 2:
        gen_path = os.path.abspath(args[1])
        log_path = os.path.dirname(dws_path)

    elif len(args) == 3:
        gen_path = os.path.abspath(args[1])
        log_path = os.path.abspath(args[2])

    elif len(args) >= 4:
        gen_path = os.path.abspath(args[1])
        log_path = os.path.abspath(args[2])
        for i in range(3,len(args)):
            gen_spec.append(args[i])

    log(LogLevel.info, 'DWS file path is %s' %(dws_path))
    log(LogLevel.info, 'Gen files path is %s' %(gen_path))
    log(LogLevel.info, 'Log files path is %s' %(log_path))

    for item in gen_spec:
        log(LogLevel.info, 'Parameter is %s' %(item))



    # check DWS file path
    if not os.path.exists(dws_path):
        log(LogLevel.error, 'Can not find "%s", file not exist!' %(dws_path))
        sys.exit(-1)

    if not os.path.exists(gen_path):
        log(LogLevel.error, 'Can not find "%s", gen path not exist!' %(gen_path))
        sys.exit(-1)

    if not os.path.exists(log_path):
        log(LogLevel.error, 'Can not find "%s", log path not exist!' %(log_path))
        sys.exit(-1)

    if is_oldDws(dws_path, gen_spec):
        sys.exit(0)

    chipId = ChipObj.get_chipId(dws_path)
    log(LogLevel.info, 'chip id: %s' %(chipId))
    chipObj = None
    if chipId == 'MT6797':
        chipObj = Everest(dws_path, gen_path)
    elif chipId == 'MT6757':
        chipObj = Olympus(dws_path, gen_path)
    elif chipId == 'MT6757-P25':
        chipObj = MT6757_P25(dws_path, gen_path)
    elif chipId == 'KIBOPLUS':
        chipObj = MT6757_P25(dws_path, gen_path)
    elif chipId == 'MT6570':
        chipObj = Rushmore(dws_path, gen_path)
    elif chipId == 'MT6799':
        chipObj = Whitney(dws_path, gen_path)
    elif chipId == 'MT6763':
        chipObj = MT6763(dws_path, gen_path)
    elif chipId == 'MT6759':
        chipObj = MT6759(dws_path, gen_path)
    elif chipId == 'MT6750S':
        chipObj = MT6750S(dws_path, gen_path)
    elif chipId == 'MT6758':
        chipObj = MT6758(dws_path, gen_path)
    elif chipId == 'MT6739':
        chipObj = MT6739(dws_path, gen_path)
    elif chipId == 'MT8695':
        chipObj = MT8695(dws_path, gen_path)
    elif chipId in ('MT6771', 'MT6775', 'MT6765', 'MT3967', 'MT6761'):
        chipObj = MT6771(dws_path, gen_path)
    elif chipId == 'MT6779':
        chipObj = MT6779(dws_path, gen_path)
    else:
        chipObj = ChipObj(dws_path, gen_path)

    if not chipObj.parse():
        log(LogLevel.error, 'Parse %s fail!' %(dws_path))
        sys.exit(-1)

    if not chipObj.generate(gen_spec):
        log(LogLevel.error, 'Generate files fail!')
        sys.exit(-1)

    sys.exit(0)