#!/usr/bin/env python

"Process manipulation and querying module"

import sys
import os


def chgProcessName(processName):
    if sys.platform == 'linux2':
        import ctypes
        libc = ctypes.cdll.LoadLibrary('libc.so.6')
        libc.prctl(15, processName, 0, 0, 0)
        return True

    elif sys.platform == 'win32':
        raise NotImplementedError("Windows is not supported")
    else:
        raise NotImplementedError("Operating System not detected/supported")


def isRunning(processName):
    if sys.platform == 'linux2':
        if not translate(processName):
            return False
        else:
            return True
    elif sys.platform == 'win32':
        raise NotImplementedError("Windows is not supported")
    else:
        raise NotImplementedError("Operating System not detected/supported")


def translate(processName):
    if sys.platform == 'linux2':
        cmd = "ps -A | grep -m 1 -w {pName}".format(pName=processName)
        try:
            ret = os.popen(cmd).readlines()[0].split()
            pid = ret[0]
            pname = ret[-1]
        except IndexError:
            return False
        if pname == processName:
            return str(pid)
        else:
            return pname
    elif sys.platform == 'win32':
        raise NotImplementedError("Windows is not supported")
    else:
        raise NotImplementedError("Operating System not detected/supported")


def getCurPid():
    return str(os.getpid())
