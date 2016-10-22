#!/bin/bash

INSTALL_DIR="/usr/local/bin/retrovidsaver"

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
/bin/cp ./screensaver.py ./Process.py ./retrovidsaver-start ./retrovidsaver-stop $INSTALL_DIR/
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
# and put it in /etc/retrovidsaver.cfg if there isn't one
if [[ ! -f /etc/retrovidsaver.cfg ]]; then
    echo
    echo "No configuration file detected"
    echo "Creating default configuration /etc/retrovidsaver.cfg"
    /bin/cp $INSTALL_DIR/default.cfg /etc/retrovidsaver.cfg
fi

# Create accessible starter and stopper service function
echo "Creating link to starter function"
starter="/usr/local/bin/retrovidsaver-start"
if [[ -L $starter ]]; then
    rm $starter
fi
ln -sv $INSTALL_DIR/retrovidsaver-start $starter

# Create accessible starter and stopper service function
echo "Creating link to stopper function"
stopper="/usr/local/bin/retrovidsaver-stop"
if [[ -L $stopper ]]; then
    rm $stopper
fi
ln -sv $INSTALL_DIR/retrovidsaver-stop $stopper

# # Create upstart job to start screensaver on boot
# echo "Creating upstart job to start screensaver on boot"
# /bin/cp ./retrovidsaverinitd /etc/init.d/retrovidsaver
# chmod 755 /etc/init.d/retrovidsaver
# upstartfile="/etc/rc2.d/S99retrovidsaver"
# if [[ -L $upstartfile ]]; then
#     rm $upstartfile
# fi
# ln -sv /etc/init.d/retrovidsaver $upstartfile

# Make service usable with sudo by anyone without authentication
echo
echo "Adding screensaver script to sudoers file so xautolock can run it with sudo"
printf "Cmnd_Alias SCREENSAVER=/usr/local/bin/retrovidsaver/screensaver.py\nALL ALL=NOPASSWD: SCREENSAVER" | (EDITOR="tee -a" visudo)
