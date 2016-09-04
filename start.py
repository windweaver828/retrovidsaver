#!/usr/bin/env python2

import os
import sys
import ConfigParser
import Process


def log(message, username):
    print(message)
    path = "/home/{}/".format(username)
    if not os.path.isdir("/home/{}/".format(username)):
        path = "/root/"
    path += "Video-Screensaver-ERROR.log"
    with open(path, 'a+') as f:
        f.write(message + "\n")
        f.flush()

if __name__ == '__main__':
    # Load config settings
    CONFIGPATH = "/etc/video-screensaver.cfg"
    if not os.path.isfile(CONFIGPATH):
        timer = 10
        lock_username = "root"
        message = "{} does not exist. Assuming defaults.".format(CONFIGPATH)
        log(message, lock_username)
    else:
        config = ConfigParser.ConfigParser()
        config.read(CONFIGPATH)
        timer = config.getint("UserSettings", "timer")
        lock_username = config.get("UserSettings", "lock_username")

    # Exit if an instance of xautolock is already running
    ProcessName = "xautolock"
    if Process.isRunning(ProcessName):
        message = "{} already running".format(ProcessName)
        log(message, lock_username)
        sys.exit(1)

    cmd = 'xautolock -time {} -locker "sudo python2 /usr/local/bin/Video-Screensaver/screensaver.py" &'

    os.popen(cmd)
    print("xautolock started")
