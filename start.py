#!/usr/bin/env python2

import os
import sys
import Process

if Process.isRunning("xautolock"):
    print("xautolock is already running")
    sys.exit(0)

cmd = 'xautolock -time 5 -locker "sudo python2 '
cmd += os.path.expanduser("~/Video-Screensaver/")
cmd += 'screensaver.py"'

os.popen(cmd)
print("xautolock started")
