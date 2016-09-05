#!/usr/bin/env python2

import os

default_text = """[UserSettings]
# Influences which username's password must be typed, where
# logs end up, and the username that the player is executed
# under. You generally want to change this to your username
username = {username}

# Input devices to monitor to stop the screensaver
input_devices = /dev/input/event4
                /dev/input/mouse0
                /dev/input/js0

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


def which(name):
    return [line.strip() for line in os.popen("which {}".format(name)).readlines()]


if __name__ == '__main__':
    username = os.path.expanduser("~").split(os.sep)[-1]
    video_directory = os.path.expanduser("~/Video-Screensaver/videos/")
    omxplayer = which("omxplayer")
    mplayer = which("mplayer")
    vlc = which("vlc")
    if omxplayer:
        player_command = omxplayer[0]
        player_args = ""
    elif vlc:
        player_command = vlc[0]
        player_args = "--play-and-exit --fullscreen"
    elif mplayer:
        player_command = mplayer[0]
        player_args = ""
    else:
        print("No supported players found. Install omxplayer mplayer or vlc or configure /etc/video-screensaver.cfg manually. Going with defaults for omxplayer. Note -- this will not run unless you install omxplayer")
        player_command = "omxplayer"
        player_args = ""

    default_text = default_text.format(username=username,
                                       video_directory=video_directory,
                                       player_command=player_command,
                                       player_args=player_args)


    with open("./default.cfg", 'w') as f:
        f.write(default_text)
        f.flush()

