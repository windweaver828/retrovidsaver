#!/usr/bin/env python2

import os
import sys

default_text = """[UserSettings]
# Influences which username's password must be typed, where
# logs end up, and the username that the player is executed
# under. You generally want to change this to your username
username = {username}

# Input devices to monitor to stop the screensaver
input_devices = {input_devices}

# Directory to play videos from
# You would want to change to a folder you can easily
# put and remove video files from. Typically a folder
# inside /home/username/ somewhere
video_directory = {video_directory}

# Extensions to consider for video files
video_extensions = mp4 mkv avi mov mpeg
                   mpeg2 mpeg1 mpg wmv

# Whether to play videos at random or in order
shuffle = True

# Player command to play videos with
player_command = {player_command}

# For custom player options
player_args = {player_args}

# How many minutes of idle time before screensaver starts
timer = 10

# Some input devices immediately give input whether your
# using them or not. Increase this slowly to increase the
# tolerance if it seems to immediately exit when videos
# start to play, and decrease it when you have to input
# more than you would like before it exits
input_dummy_amt = 7

# Whether to place a lock on the keyboard/mouse using xtrlock
# Enter your user password and press enter to unlock
lock = False

# Edit your config file as needed - sudo nano /etc/video-screensaver.cfg
# Any donations for the continued development of this program are welcome
# https://www.paypal.me/windweaver828/

"""


def get_nondirs(path):
    devices = list()
    if not path.endswith(os.sep):
        path += os.sep
    if not os.path.isdir(path):
        return devices
    for device in os.listdir(path):
        if os.path.exists(path + device) and not os.path.isdir(path + device):
            devices.append(path + device)
    return devices


def which(name):
    return [line.strip() for line in os.popen("which {}".format(name)).readlines()]


if __name__ == '__main__':
    # Remove default.cfg if it exists
    if os.path.isfile("./default.cfg"):
        os.remove("./default.cfg")

    # Enumerate smart default settings
    username = os.path.expanduser("~").split(os.sep)[-1]
    video_directory = os.path.expanduser("~/Video-Screensaver/videos/")
    if os.path.isdir("/dev/input/by-path/"):
        input_devices = get_nondirs("/dev/input/by-path/")
    elif os.path.isdir("/dev/input/by-id/"):
        input_devices = get_nondirs("/dev/input/by-id/")
    elif os.path.isdir("/dev/input/"):
        input_devices = get_nondirs("/dev/input/")
    else:
        print("Couldn't find any suitable devices to monitor, edit /etc/video-screensaver.cfg manually")
        sys.exit(1)
    input_devices = " ".join(input_devices)
    omxplayer = which("omxplayer")
    mplayer = which("mplayer")
    vlc = which("vlc")
    player_commands = dict()
    if omxplayer:
        player_args = ""
        player_commands["omxplayer"] = (omxplayer[0], player_args)
    if mplayer:
        player_args = "-fs"
        player_commands["mplayer"] = (mplayer[0], player_args)
    if vlc:
        player_args = "--play-and-exit --fullscreen"
        player_commands["vlc"] = (vlc[0], player_args)

    if len(player_commands.keys()) == 0:
        print("\n\nNo supported default players found.")
        print("Install omxplayer mplayer or vlc and run install.sh again.")
        print("Or you can configure /etc/video-screensaver.cfg manually.")
        print("Going with defaults for omxplayer. Note -- this will not run unless you install omxplayer.\n\n")
        player_command = "omxplayer"
        player_args = ""
    elif len(player_commands.keys()) == 1:
        player_command, player_args = player_commands[player_commands.keys()[0]]
    else:
        print("Multiple player programs detected, which would you like to use?")

        choices = dict()
        for num, program_name in enumerate(player_commands.keys()):
            print("{}) {}".format(num + 1, program_name))
            choices[num + 1] = program_name

        while True:
            try:
                choice = raw_input("Program number: ")
                choice = int(choice)
                if not 0 < choice <= len(choices.keys()):
                    print("Choice not in range [{}-{}]".format(1, len(choices.keys())))
                    continue
                player_command, player_args = player_commands[choices[choice]]
                break
            except ValueError:
                print("You must input a number")
                continue
            except Exception as e:
                print(e)
                sys.exit(1)
    default_text = default_text.format(username=username,
                                       input_devices=input_devices,
                                       video_directory=video_directory,
                                       player_command=player_command,
                                       player_args=player_args)

    with open("./default.cfg", 'w') as f:
        f.write(default_text)
        f.flush()
