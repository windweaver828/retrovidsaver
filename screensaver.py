#!/usr/bin/env python2

import sys
import os
import struct
import random
import ConfigParser
import Process

default_config = """[UserSettings]

# Directory to play videos from
video_directory = /home/pi/Video-Screensaver/videos/

# Extensions to look at for video files
video_extensions = mp4

# Player command to play videos with - for custom use so you can specify hdmi devices or windows size etc if the default options dont work well
player_command = omxplayer

# How many seconds of idle time before screensaver starts
timer = 600

# Whether to place a lock on the keyboard/mouse using xtrlock
# Enter your user password and press enter to unlock
lock = False
"""

# Check if config exists and generate one if not
# CONFIGPATH = os.path.expanduser("~/Video-Screensaver/screensaver.cfg")
CONFIGPATH = os.path.expanduser("~/Projects/Video-Screensaver/screensaver.cfg")
if not os.path.isfile(CONFIGPATH):
    with open(CONFIGPATH, 'w') as f:
        f.write(default_config)
        f.flush()

ProcessName = "Video-Screensaver"

if Process.isRunning(ProcessName):
    print("{} already running".format(ProcessName))
    sys.exit(1)

Process.chgProcessName(ProcessName)


def get_videos(path, extensions):
    video_list = list()
    if os.path.exists(path):
        if not path.endswith(os.sep):
            path += os.sep
        video_list = [path + x for x in os.listdir(path) if x.split('.')[-1] in extensions]
        return video_list


def monitor_inputs(input_devices):
    FORMAT = "llHHI"
    EVENT_SIZE = struct.calcsize(FORMAT)
    in_files = [open(x, "rb") for x in input_devices]
    events = list()
    for f in in_files:
        events.append(f.read(EVENT_SIZE))

    while True:
        for f in in_files:
            events.append(f.read(EVENT_SIZE))

        if len(events):
            break
        # for event in events[:]:
        #     events.remove(event)
        #     (tv_sec, tv_usec, type, code, value) = struct.unpack(FORMAT, event)

        #     if type != 0 or code != 0 or value != 0:
        #         print("Event type %u, code %u, value %u at %d.%d" % (type, code, value, tv_sec, tv_usec))
        #     else:
        #         # Events with code, type and value == 0 are "separator" events
        #         print("===========================================")


if __name__ == '__main__':
    input_devices = ["/dev/input/event4"]
    # Load config settings
    config = ConfigParser.ConfigParser()
    config.read(CONFIGPATH)

    video_directory = config.get("UserSettings", "video_directory")
    video_extensions = config.get("UserSettings", "video_extensions").split()
    player_command = config.get("UserSettings", "player_command")
    timer = config.getint("UserSettings", "timer")
    lock = config.getboolean("UserSettings", "lock")

    video_list = get_videos(video_directory, video_extensions)
    random.shuffle(video_list)
    for vid in video_list:
        print(vid)
