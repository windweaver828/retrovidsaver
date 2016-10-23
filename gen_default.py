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

# Edit your config file as needed - sudo nano /etc/retrovidsaver.cfg
# Any donations for the continued development of this program are welcome
# https://www.paypal.me/windweaver828/

"""

supervisor_text = """[program:retrovidsaver]
command=/usr/local/bin/retrovidsaver-start
user={username}
environment=HOME="/home/{username}/",USER="{username}",DISPLAY=":0"
autostart=true
"""


def get_users():
    users = list()
    if os.path.isdir("/root/"):
        users.append("root")
    if os.path.isdir("/home/"):
        users.extend(os.listdir("/home/"))
    return users


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


def choice(header, choices_list, footer):
    print(header)
    choices_dict = dict()
    for num, item in enumerate(choices_list):
        print("{}) {}".format(num + 1, item))
        choices_dict[num + 1] = item

    while True:
        try:
            choice_num = raw_input(footer)
            choice_num = int(choice_num)
            if not 0 < choice_num <= len(choices_dict.keys()):
                print("Choice not in range [{}-{}]".format(1, len(choices_dict.keys())))
                continue
            choice = choices_dict[choice_num]
            break
        except ValueError:
            print("You must input a number")
            continue
        except Exception as e:
            print(e)
            sys.exit(1)
    return choice

if __name__ == '__main__':
    # Remove default.cfg if it exists
    if os.path.isfile("./default.cfg"):
        os.remove("./default.cfg")

    # Enumerate smart default settings
    users = get_users()
    header = "Which user would you like to use? Note - Do not use root unless you have to, typically you would want to use your standard user name"
    footer = "User Number: "
    username = choice(header, users, footer)
    video_directory = os.path.expanduser("~/retrovidsaver/videos/")
    if os.path.isdir("/dev/input/by-path/"):
        input_devices = get_nondirs("/dev/input/by-path/")
    elif os.path.isdir("/dev/input/by-id/"):
        input_devices = get_nondirs("/dev/input/by-id/")
    elif os.path.isdir("/dev/input/"):
        input_devices = get_nondirs("/dev/input/")
    else:
        print("Couldn't find any suitable devices to monitor, edit /etc/retrovidsaver.cfg manually")
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
        print("Or you can configure /etc/retrovidsaver.cfg manually.")
        print("Going with defaults for omxplayer. Note -- this will not run unless you install omxplayer.\n\n")
        player_command = "omxplayer"
        player_args = ""
    elif len(player_commands.keys()) == 1:
        player_command, player_args = player_commands[player_commands.keys()[0]]
    else:
        header = "Multiple player programs detected, which would you like to use?"
        footer = "Program number: "
        player_command = choice(header, player_commands.keys(), footer)
        player_command, player_args = player_commands[player_command]

    # Format the default text with sane values
    default_text = default_text.format(username=username,
                                       input_devices=input_devices,
                                       video_directory=video_directory,
                                       player_command=player_command,
                                       player_args=player_args)

    with open("./default.cfg", 'w') as f:
        f.write(default_text)
        f.flush()

    supervisor_text = supervisor_text.format(username=username)
    
    with open("./supervisor.conf", "w") as f:
        f.write(supervisor_text)
        f.flush()
