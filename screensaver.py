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


def monitor_input(input_device, queue, dummy):
    FORMAT = "llHHI"
    EVENT_SIZE = struct.calcsize(FORMAT)
    f = open(input_device, 'rb')
    for _ in range(dummy):
        f.read(EVENT_SIZE)
    f.close()
    queue.put("DONE")


def monitor_inputs(input_devices, dummy):
    queue = multiprocessing.Queue()
    processes = list()
    for input_device in input_devices:
        proc = multiprocessing.Process(target=monitor_input, args=(input_device, queue, dummy))
        proc.daemon = True
        proc.start()
        processes.append(proc)

    while True:
        if not queue.empty():
            for proc in processes:
                proc.terminate()
            break


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
        input_devices = ["/dev/input/event4",
                         "/dev/input/mouse0",
                         "/dev/input/js0",
                         ]
        video_directory = "/root/Video-Screensaver/videos/"
        video_extensions = ["mp4", ]
        shuffle = True
        player_command = "omxplayer"
        player_args = ""
        timer = 10
        lock = False
        lock_username = "root"
        input_dummy_amt = 7
        message = "{} does not exist. Assuming defaults.".format(CONFIGPATH)
        log(message, lock_username)
    else:
        config = ConfigParser.ConfigParser()
        config.read(CONFIGPATH)

        input_devices = config.get("UserSettings", "input_devices").split()
        video_directory = config.get("UserSettings", "video_directory")
        video_extensions = config.get("UserSettings", "video_extensions").split()
        shuffle = config.getboolean("UserSettings", "shuffle")
        player_command = config.get("UserSettings", "player_command")
        player_args = config.get("UserSettings", "player_args").split()
        timer = config.getint("UserSettings", "timer")
        lock = config.getboolean("UserSettings", "lock")
        lock_username = config.get("UserSettings", "lock_username")
        input_dummy_amt = config.getint("UserSettings", "input_dummy_amt")

    # Exit if an instance of this script is already running
    ProcessName = "Video-Screensav"
    if Process.isRunning(ProcessName):
        message = "{} already running".format(ProcessName)
        log(message, lock_username)
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
        log(message, lock_username)
        sys.exit(1)
    # Load the video list
    video_list = get_videos(video_directory, video_extensions)
    if not video_list:
        msg = "No videos found, put some in {}".format(video_directory)
        log(msg)
        sys.exit(1)

    # Play videos on a loop
    end_signal = threading.Event()
    thread = threading.Thread(target=play_videos, args=(video_list, player_command, player_args, lock_username, shuffle, end_signal))
    thread.start()

    # Lock the keyboard and mouse if enabled
    if lock:
        os.popen("sudo -u {} xtrlock".format(lock_username))
    locked = True  # Loop will check if it is really locked

    try:
        while locked:
            # Wait for a device to have input
            monitor_inputs(input_devices, input_dummy_amt)
            if not Process.isRunning("xtrlock"):
                locked = False
            if not locked:
                break
    except KeyboardInterrupt, SystemExit:
        pass
    except Exception as e:
        log(e, lock_username)
    finally:
        end_signal.set()
        thread.join()
