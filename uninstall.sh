#!/bin/bash

INSTALL_DIR="/usr/local/bin/retrovidsaver"

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

# # Remove configuration file
# if [[ -f /etc/retrovidsaver.cfg ]]; then
#     echo "Removing /etc/retrovidsaver.cfg"
#     rm /etc/retrovidsaver.cfg
# fi

# Remove starter and stopper function
starter="/usr/local/bin/retrovidsaver-start"
if [[ -L $starter ]]; then
    echo "Removing link to starter function"
    rm $starter
fi

# Remove starter and stopper function
stopper="/usr/local/bin/retrovidsaver-stop"
if [[ -L $stopper ]]; then
    echo "Removing link to stopper function"
    rm $stopper
fi

# # Remove upstart job
# upstartfile="/etc/init.d/retrovidsaver"
# if [[ -f $upstartfile ]]; then
#     echo "Removing upstart job"
#     rm $upstartfile
# fi
# upstartfile="/etc/rc2.d/S99retrovidsaver"
# if [[ -L $upstartfile ]]; then
#     rm $upstartfile
# fi

echo
echo "Do sudo visudo and remove a line near the bottom that looks like below"
printf "Cmnd_Alias SCREENSAVER=/usr/local/bin/retrovidsaver/screensaver.py\nALL ALL=NOPASSWD: SCREENSAVER"

echo
echo "Uninstall completed."
