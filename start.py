#!/usr/bin/env python2

import os
import sys
import ConfigParser
import Process

if Process.isRunning("xautolock"):
    print("xautolock is already running")
    sys.exit(0)


CONFIGPATH = os.path.expanduser("~/Video-Screensaver/screensaver.cfg")
config = ConfigParser.ConfigParser()
config.read(CONFIGPATH)
timer = config.getint("UserSettings", "timer")
cmd = 'xautolock -time {} -locker "sudo python2 '.format(timer)
cmd += os.path.expanduser("~/Video-Screensaver/")
cmd += 'screensaver.py" &'

os.popen(cmd)
print("xautolock started")
