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
    - xautolock
    - xtrlock

* Install Dependencies
    - sudo apt-get install python2.7 cron xautolock xtrlock

* Clone the repository
    - cd ~
    - git clone https://github.com/windweaver828/Video-Screensaver.git

* Run the install script
    - cd ~/Video-Screensaver/
    - sudo ./install.sh

* Run sudo /usr/local/bin/start-video-screensaver on boot

* Use sudo /usr/local/bin/stop-video-screensaver to stop it

### Contribution guide

* Send a pull request
* Or a well documented email to me with subject "github video-controller"

### Who do I talk to? ###

* Keith Brandenburg - windweaver828@gmail.com

### Todo ###

* Everything is fully functional and complete at the moment
