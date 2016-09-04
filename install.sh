#!/bin/bash

INSTALL_DIR="/usr/local/bin/Video-Screensaver"

# Make sure we are root
if [[ $EUID -ne 0 ]]; then
    echo "You must be a root user" 2>&1
    echo "Use sudo $0" 2>&1
    exit 1
fi

# Create directory if needed
if [[ ! -d $INSTALL_DIR ]]; then
    echo "Creating $INSTALL_DIR/"
    mkdir $INSTALL_DIR
fi

# Copy over program files
echo "Copying files"
/bin/cp -v ./screensaver.py ./Process.py ./start.py ./stop.sh $INSTALL_DIR/
echo
echo "Setting program permissions"
chown -Rv root:root $INSTALL_DIR/
chmod -Rv 700 $INSTALL_DIR/
chmod 755 $INSTALL_DIR/

# Copy new default configuration
echo
echo "Installing new default configuration"
/bin/cp -v ./video-screensaver.cfg $INSTALL_DIR/default.cfg
echo
echo "Setting config file permissions"
chown -v root:root $INSTALL_DIR/default.cfg
chmod -v 644 $INSTALL_DIR/default.cfg
# and put it in /etc/video-screensaver.cfg
if [[ ! -f /etc/video-screensaver.cfg ]]; then
    echo
    echo "No configuration file detected"
    echo "Creating default configuration /etc/video-screensaver.cfg"
    /bin/cp -v $INSTALL_DIR/default.cfg /etc/video-screensaver.cfg
fi

echo
echo "Edit your config file as needed - sudo nano /etc/video-screensaver.cfg"
echo "Any donations for the continued development of this program are welcome"
echo "https://www.paypal.me/windweaver828/"
