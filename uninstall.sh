#!/bin/bash

INSTALL_DIR="/usr/local/bin/retro-vidsaver"

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
if [[ -f /etc/retrovidsaver.cfg ]]; then
    echo "Removing /etc/retrovidsaver.cfg"
    rm /etc/retrovidsaver.cfg
fi

# Remove starter and stopper function
starter="/usr/local/bin/retrovidsaver"
if [[ -f $starter ]]; then
    echo "Removing link to starter and stopper function"
    rm $starter
fi

echo
echo "Do sudo visudo and remove a line near the bottom that looks like below"
printf "Cmnd_Alias SCREENSAVER=/usr/local/bin/retrovidsaver/retrovidsaver\nALL ALL=NOPASSWD: SCREENSAVER" | (EDITOR="tee -a" visudo)

echo
echo "Uninstall completed."
