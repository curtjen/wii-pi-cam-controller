#!/usr/bin/python

import os

# Install gphoto2
print "Installing gphoto2..."
os.system("wget https://raw.githubusercontent.com/curtjen/gphoto2-updater/master/gphoto2-updater.sh && chmod +x gphoto2-updater.sh && sudo ./gphoto2-updater.sh")

# Install Wiimote drivers
print "Installing Wii drivers..."
os.system("sudo apt-get install python-cwiid")

# Change 'shutdown' command permissions
print "Changing permissions to 'shutdown' command for Wiimote use..."
os.system("sudo chmod a+s /sbin/shutdown")
