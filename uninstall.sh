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

# Remove starter and stopper functions
starter="/usr/local/bin/start-video-screensaver"
if [[ -f $starter ]]; then
    echo "Removing links to starter function"
    rm $starter
fi
stopper="/usr/local/bin/stop-video-screensaver"
if [[ -f $stopper ]]; then
    echo "Removing links to stopper function"
    rm $stopper
fi

# Remove files for autocomplete of starter and stopper scripts
if [[ -f /etc/bash_completion.d/start-video-screensaver ]]; then
    echo "Remove autocompletion starter file"
    rm /etc/bash_completion.d/start-video-screensaver
fi
if [[ -f /etc/bash_completion.d/stop-video-screensaver ]]; then
    echo "Remove autocompletion stopper file"
    rm /etc/bash_completion.d/stop-video-screensaver
fi

# Recommend manual removal of cron job if it exists
echo
crontab -l > /tmp/curcronfile.txt
if grep -R "@reboot /usr/local/bin/start-video-screensaver" /tmp/curcronfile.txt; then
    echo "You should run sudo crontab -e and remove the line above"
fi

rm /tmp/curcronfile.txt

echo
echo "Uninstall completed."
