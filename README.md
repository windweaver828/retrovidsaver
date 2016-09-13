# Video-Screensaver


Any donations for the continued development of this program are welcome
https://www.paypal.me/windweaver828/

# README #

### What is this repository for? ###

* Plays videos from a given directory at random after specified number of seconds of system idle time, and goes away upon user input, with an optional locking mechanism, just like a normal screensaver.

* Version - 1.0

### How do I get set up? ###

- Note - This program runs with root priveleges
* Dependencies
    - python2.7 - should be preinstalled on most linux systems
    - cron - to run on boot
    - xautolock - starts the screensaver after so long of idle time
    - xtrlock - optionally locks keyboard and mouse on screensaver
    - xbacklight - sets display brightness for screensaver

* Install Dependencies
    - sudo apt-get install python2.7 cron xautolock xtrlock xbacklight

* Clone the repository
    - cd ~
    - git clone https://github.com/windweaver828/Video-Screensaver.git

* At this point before running the installer script, make sure any keyboards/mice, joysticks, or controllers you want to be able to turn off the screensaver, are plugged in at the time of the install. You may run the install as often as you need just remember to delete the /etc/video-screensaver.cfg file before running the install script
* Run the install script
    - cd ~/Video-Screensaver/
    - sudo ./install.sh

* Check your config file in (sudo nano) /etc/video-screensaver.cfg for any changes you may need and reboot. It should be started automatically, the default timer is set for 10 minutes.

* Add videos
    - cd ~/Video-Screensaver/
    - mkdir videos

Copy in any videos you would like to play, making sure the extensions are supported by your player of choice and are listed in your /etc/video-screensaver.cfg file, there is a decent small list of commonly supported extensions pre listed for you.

* Manual starting and stopping of screensaver
    - Use sudo start-video-screensaver to start
    - Use sudo stop-video-screensaver to stop

* To uninstall
    - Simply run uninstall.sh as root, or with sudo
### Contribution guide

* Send a pull request
* Or a well documented email to me with subject "github video-controller"

### Who do I talk to? ###

* Keith Brandenburg - windweaver828@gmail.com

### Todo ###
* Get autocompletion working
* Add in xbacklight, screen brightness settings
* Try to fix input monitor so that a dummy value isn't necessary, some kind of logic to read in x bytes if they are there upon first reading from device
* Add option to mute system volume for a silent screensaver
* Try to minimize emulation station on screensaver and restore it on close
