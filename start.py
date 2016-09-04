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
        username = "root"
        timer = 10
        message = "{} does not exist. Assuming defaults.".format(CONFIGPATH)
        log(message, username)
    else:
        config = ConfigParser.ConfigParser()
        config.read(CONFIGPATH)

        username = config.get("UserSettings", "username")
        timer = config.getint("UserSettings", "timer")

    # Exit if we are not
    if os.geteuid() != 0:
        message = ("This script must be ran as root, try using sudo")
        log(message, username)
        sys.exit(1)

    # Exit if an instance of xautolock is already running
    ProcessName = "xautolock"
    if Process.isRunning(ProcessName):
        message = "{} already running".format(ProcessName)
        log(message, username)
        sys.exit(1)

    cmd = 'xautolock -time {} -locker "sudo python2 /usr/local/bin/Video-Screensaver/screensaver.py" &'

    os.popen(cmd)
    print("xautolock started")
