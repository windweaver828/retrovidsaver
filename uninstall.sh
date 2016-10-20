#!/bin/bash

INSTALL_DIR="/usr/local/bin/Video-Screensaver"

# Make sure we are root
if [[ $EUID -ne 0 ]]; then
    echo "You must be a root user" 2>&1
    echo "Use sudo $0" 2>&1
    exit 1
fi

# Remove whole install directory if needed
if [[ -d $INSTALL_DIR ]]; then
    echo "Removing $INSTALL_DIR/"
    rm -rf $INSTALL_DIR
fi

# Remove configuration file
if [[ -f /etc/video-screensaver.cfg ]]; then
    echo "Removing /etc/video-screensaver.cfg"
    rm /etc/video-screensaver.cfg
fi

# Remove starter and stopper function
starter="/usr/local/bin/video-screensaver"
if [[ -f $starter ]]; then
    echo "Removing link to starter and stopper function"
    rm $starter
fi

echo
echo "Uninstall completed."
