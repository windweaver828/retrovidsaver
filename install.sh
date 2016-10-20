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
/bin/cp ./screensaver.py ./Process.py ./video-screensaver $INSTALL_DIR/
echo
echo "Setting program permissions"
chown -R root:root $INSTALL_DIR/
chmod -R 700 $INSTALL_DIR/
chmod 755 $INSTALL_DIR/

# Generate new default configuration
./gen_default.py

# Copy new default configuration
/bin/cp ./default.cfg $INSTALL_DIR/default.cfg
chown root:root $INSTALL_DIR/default.cfg
chmod 644 $INSTALL_DIR/default.cfg
# and put it in /etc/video-screensaver.cfg if there isn't one
if [[ ! -f /etc/video-screensaver.cfg ]]; then
    echo
    echo "No configuration file detected"
    echo "Creating default configuration /etc/video-screensaver.cfg"
    /bin/cp $INSTALL_DIR/default.cfg /etc/video-screensaver.cfg
fi

# Create accessible starter and stopper function
echo "Creating link to starter and stopper function"
starter="/usr/local/bin/video-screensaver"
if [[ -f $starter ]]; then
    rm $starter
fi
ln -sv $INSTALL_DIR/video-screensaver $starter

echo
echo "Your default config looks like ---"
cat "./default.cfg"
