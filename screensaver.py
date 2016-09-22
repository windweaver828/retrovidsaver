#!/usr/bin/env python2

import sys
import os
import time
import datetime
import random
import subprocess
import signal
import struct
import threading
import Queue
import ConfigParser
import Process


def play_videos(paths, user, player_command, player_args, shuffle, end_signal):
    while True:
        if shuffle:
            random.shuffle(paths)
        for path in paths:
            if end_signal.is_set():
                return
            if os.path.isfile(path):
                try:
                    cmd = ["sudo", "-u", user, player_command]
                    cmd.extend(player_args)
                    cmd.append(path)
                    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
                except Exception as e:
                    print player_command
                    print player_args
                    print path
                    print(e)
                    return
                while process.poll() is None:
                    if end_signal.is_set():
                        process.terminate()
                        time.sleep(.3)
                        if process.poll() is None:
                            cmd = "pkill " + player_command.split(os.sep)[-1]
                            os.popen(cmd)
                    end_signal.wait(.5)


def get_videos(path, extensions):
    if os.path.exists(path):
        if not path.endswith(os.sep):
            path += os.sep
        return [path + x for x in sorted(os.listdir(path), key=alphanum_key) if x.split('.')[-1] in extensions]


def monitor_input(input_device, queue, end_signal):
    FORMAT = "llHHI"
    EVENT_SIZE = struct.calcsize(FORMAT)
    f = open(input_device, 'rb')
    while not end_signal.is_set():
        f.read(EVENT_SIZE)
        queue.put("RESET")
    f.close()


def log(message, username):
    print(message)
    path = "/home/{}/".format(username)
    if not os.path.isdir("/home/{}/".format(username)):
        path = "/root/"
    path += "Video-Screensaver-ERROR.log"
    with open(path, 'a+') as f:
        f.write(message + "\n")
        f.flush()


# Used for sorting
def alphanum_key(s):
    from re import split as resplit
    """ Turn a string into a list of string and number chunks.
        "z23a" -> ["z", 23, "a"]
    """
    def tryint(s):
        try:
            return int(s)
        except:
            return s

    return [tryint(c) for c in resplit('([0-9]+)', s)]


if __name__ == '__main__':
    # Set this signal off at any point in the program to tell all threads and processes to end
    end_signal = threading.Event()
    locked = False  # Start off unlocked

    # Load config settings
    CONFIGPATH = "/etc/video-screensaver.cfg"
    if not os.path.isfile(CONFIGPATH):
        username = "root"
        input_devices = ["/dev/input/event4",
                         "/dev/input/mouse0",
                         "/dev/input/js0",
                         ]
        video_directory = "/root/Video-Screensaver/videos/"
        video_extensions = ["mp4", ]
        shuffle = True
        player_command = "omxplayer"
        player_args = list()
        timer = 10 * 60
        lock = False
        message = "{} does not exist. Assuming defaults.".format(CONFIGPATH)
        log(message, username)
    else:
        config = ConfigParser.ConfigParser()
        config.read(CONFIGPATH)

        username = config.get("UserSettings", "username")
        input_devices = config.get("UserSettings", "input_devices").split()
        video_directory = config.get("UserSettings", "video_directory")
        video_extensions = config.get("UserSettings", "video_extensions").split()
        shuffle = config.getboolean("UserSettings", "shuffle")
        player_command = config.get("UserSettings", "player_command")
        player_args = config.get("UserSettings", "player_args").split()
        timer = config.getint("UserSettings", "timer") * 60
        lock = config.getboolean("UserSettings", "lock")

    # Exit if we are not root
    if os.geteuid() != 0:
        message = ("This script must be ran as root, try using sudo")
        log(message, username)
        sys.exit(1)

    # Exit if an instance of this script is already running
    ProcessName = "Video-Screensav"
    if Process.isRunning(ProcessName):
        message = "{} already running".format(ProcessName)
        log(message, username)
        sys.exit(1)
    # And change our process name so we are easily identifiable
    Process.chgProcessName(ProcessName)

    # Catch kill signal if we happen to get one
    def signal_term_handler(signal, frame):
        raise SystemExit
    signal.signal(signal.SIGTERM, signal_term_handler)

    # Only use devices that exist
    for device in input_devices:
        if not os.path.exists(device):
            input_devices.remove(device)
    # Exit if no devices left
    if not input_devices:
        message = "None of the given input devices are available, check {}".format(CONFIGPATH)
        log(message, username)
        sys.exit(1)
    # Load the video list
    video_list = get_videos(video_directory, video_extensions)
    if not video_list:
        msg = "No videos found, put some in {}".format(video_directory)
        log(msg)
        sys.exit(1)

    # Create input watcher threads and start tracking time
    control_time = datetime.datetime.now()
    threads = list()
    queue = Queue.Queue()  # Queue to watch to know when we have input devices active
    for device in input_devices:
        thread = threading.Thread(target=monitor_input, args=(device, queue, end_signal))
        thread.start()
        threads.append(thread)

    try:
        while True:
            if end_signal.is_set():
                break
            if not queue.empty():  # Input received
                queue.get()
                if locked:
                    # Check if xtrlock has been unlocked yet
                    if not Process.isRunning("xtrlock"):
                        locked = False
                else:
                    # Reset the timer on every input unless already running videos
                    if not locked:
                        control_time = datetime.datetime.now()
            else:
                # Target time reached, play videos
                if (datetime.datetime.now() - control_time).total_seconds() >= timer:
                    thread = threading.Thread(target=play_videos, args=(video_list, username, player_command, player_args, shuffle, end_signal))
                    thread.start()
                    threads.append(thread)
                    if lock:
                        os.popen("sudo -u {} xtrlock".format(username))
                    locked = True
            time.sleep(.7)

            if not Process.isRunning("xtrlock"):
                locked = False
            if not locked:
                break
    except KeyboardInterrupt, SystemExit:
        pass
    except Exception as e:
        log(e, username)
    finally:
        # Wait for all threads to end cleanly
        end_signal.set()
        for thread in threads:
            thread.join()
