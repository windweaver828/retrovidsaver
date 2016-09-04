#!/usr/bin/env python2

import sys
import os
import random
import subprocess
import signal
import threading
import struct
import ConfigParser
import Process


def play_videos(paths, player_command, end_signal):
    while True:
        random.shuffle(paths)
        for path in paths:
            if end_signal.is_set():
                return
            if os.path.isfile(path):
                process = subprocess.Popen([player_command, path])
                while process.poll():
                    if end_signal.is_set():
                        process.terminate()
                    end_signal.wait(.5)


def get_videos(path, extensions):
    if os.path.exists(path):
        if not path.endswith(os.sep):
            path += os.sep
        return [path + x for x in os.listdir(path) if x.split('.')[-1] in extensions]


def monitor_inputs(input_devices):
    FORMAT = "llHHI"
    EVENT_SIZE = struct.calcsize(FORMAT)
    in_files = [open(x, "rb") for x in input_devices]
    events = list()
    while True:
        for f in in_files:
            events.append(f.read(EVENT_SIZE))

        # Uncomment below code for help detecting which input devices are actually doing anything

        # for event in events[:]:
        #     events.remove(event)
        #     (tv_sec, tv_usec, type, code, value) = struct.unpack(FORMAT, event)

        #     if type != 0 or code != 0 or value != 0:
        #         print("Event type %u, code %u, value %u at %d.%d" % (type, code, value, tv_sec, tv_usec))
        #     else:
        #         # Events with code, type and value == 0 are "separator" events
        #         print("===========================================")

        # Exit once input is detected
        if events:
            break


if __name__ == '__main__':
    default_config = """[UserSettings]
# Input devices to monitor to stop the screensaver
input_devices = /dev/input/event4
                /dev/input/mouse0

# Directory to play videos from
video_directory = {video_directory}

# Extensions to look at for video files
video_extensions = mp4

# Player command to play videos with
player_command = omxplayer

# For custom use so you can specify hdmi devices or window size etc if the default options dont work well
player_args = ""

# How many seconds of idle time before screensaver starts
timer = 600

# Whether to place a lock on the keyboard/mouse using xtrlock
# Enter your user password and press enter to unlock
lock = False
""".format(video_directory=os.path.expanduser("~/Video-Screensaver/videos/"))

    # Check if config exists and generate one if not
    CONFIGPATH = os.path.expanduser("~/Video-Screensaver/screensaver.cfg")
    if not os.path.isfile(CONFIGPATH):
        with open(CONFIGPATH, 'w') as f:
            f.write(default_config)
        # Make the file usable by normal user - we should be running as root
        os.chmod(CONFIGPATH, 0o664)
        cmd = "chown {0}:{0} {1}".format(os.path.expanduser("~").split(os.sep)[-1], CONFIGPATH)
        os.system(cmd)

    # Exit if an instance of this script is already running
    ProcessName = "Video-Screensaver"
    if Process.isRunning(ProcessName):
        print("{} already running".format(ProcessName))
        sys.exit(1)
    # And change our process name so we are easily identifiable
    Process.chgProcessName(ProcessName)

    # Load config settings
    config = ConfigParser.ConfigParser()
    config.read(CONFIGPATH)

    input_devices = config.get("UserSettings", "input_devices").split()
    video_directory = config.get("UserSettings", "video_directory")
    video_extensions = config.get("UserSettings", "video_extensions").split()
    player_command = config.get("UserSettings", "player_command")
    player_args = config.get("UserSettings", "player_args").split()
    timer = config.getint("UserSettings", "timer")
    lock = config.getboolean("UserSettings", "lock")

    # Verify the input devices exist or exit
    for device in input_devices:
        if not os.path.exists(device):
            print device
            print("Bad device path, check the configuration")
            sys.exit(1)

    # Load the video list
    video_list = get_videos(video_directory, video_extensions)

    # Lock the keyboard and mouse if enabled
    if lock:
        subprocess.Popen(["xtrlock"])
        locked = True
    else:
        locked = False

    # Play videos on a loop
    end_signal = threading.Event()
    thread = threading.Thread(target=play_videos, args=(video_list, player_command, end_signal))
    thread.start()

    def signal_term_handler(signal, frame):
        raise SystemExit
    signal.signal(signal.SIGTERM, signal_term_handler)

    try:
        while True:
            # Wait for a device to have input
            monitor_inputs(input_devices)
            if not Process.isRunning("xtrlock"):
                locked = False
            if not locked:
                break
    except KeyboardInterrupt, SystemExit:
        pass
    except Exception as e:
        with open(os.path.expanduser("~/Video-Screensaver/error.log"), 'a+') as f:
            f.write(e)
            f.flush()
        print(e)
    finally:
        print("Exiting cleanly")
        end_signal.set()
        thread.join()
