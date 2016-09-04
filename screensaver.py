#!/usr/bin/env python2

import sys
import os
import random
import subprocess
import signal
import struct
import threading
import multiprocessing
import ConfigParser
import Process


def play_videos(paths, player_command, player_args, end_signal):
    user = os.path.expanduser("~").split(os.sep)[-1]
    while True:
        random.shuffle(paths)
        for path in paths:
            if end_signal.is_set():
                return
            if os.path.isfile(path):
                try:
                    cmd = ["sudo", "-u", user, player_command]
                    cmd.extend(player_args)
                    cmd.append(path)
                    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                except OSError as e:
                    print player_command
                    print player_args
                    print path
                    print(e)
                    return
                while process.poll() is None:
                    if end_signal.is_set():
                        process.terminate()
                    end_signal.wait(.5)


def get_videos(path, extensions):
    if os.path.exists(path):
        if not path.endswith(os.sep):
            path += os.sep
        return [path + x for x in os.listdir(path) if x.split('.')[-1] in extensions]


def monitor_input(input_device, queue):
    FORMAT = "llHHI"
    EVENT_SIZE = struct.calcsize(FORMAT)
    f = open(input_device, 'rb')
    f.read(EVENT_SIZE)
    f.close()
    queue.put("DONE")


def monitor_inputs(input_devices):
    queue = multiprocessing.Queue()
    processes = list()
    for input_device in input_devices:
        proc = multiprocessing.Process(target=monitor_input, args=(input_device, queue))
        proc.daemon = True
        proc.start()
        processes.append(proc)

    while True:
        if not queue.empty():
            for proc in processes:
                proc.terminate()
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

# How many minutes of idle time before screensaver starts
timer = 10

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
    ProcessName = "Video-Screensav"
    if Process.isRunning(ProcessName):
        print("{} already running".format(ProcessName))
        sys.exit(1)
    # And change our process name so we are easily identifiable
    Process.chgProcessName(ProcessName)

    # Catch kill signal if we happen to get one
    def signal_term_handler(signal, frame):
        raise SystemExit
    signal.signal(signal.SIGTERM, signal_term_handler)

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
    if not video_list:
        print("No videos found, put some in {}".format(video_directory))
        sys.exit(1)

    # Play videos on a loop
    end_signal = threading.Event()
    thread = threading.Thread(target=play_videos, args=(video_list, player_command, player_args, end_signal))
    thread.start()

    # Lock the keyboard and mouse if enabled
    if lock:
        os.popen("xtrlock")
    locked = True  # Loop will check if it is really locked

    try:
        while locked:
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
