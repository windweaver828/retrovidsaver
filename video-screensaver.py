#!/usr/bin/env python2

import os
import sys
import ConfigParser
import Process

CONFIGPATH = os.path.expanduser("~/Video-Screensaver/screensaver.cfg")
ProcessName = "Video-Screensaver"

if Process.isActive(ProcessName):
    print("{} already running".format(ProcessName))
    sys.exit(1)

Process.chgProcessName(ProcessName)

config = ConfigParser.ConfigParser()
config.read(CONFIGPATH)

video_directory = config.get("UserSettings", "video_directory")
video_extensions = config.get("UserSettings", "video_extensions").split()
player_command = config.get("UserSettings", "player_command")
timer = config.getint("UserSettings", "timer")
lock = config.getboolean("UserSettings", "lock")

