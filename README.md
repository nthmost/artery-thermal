# artery-thermal
a library that helps us pump out stupid shit on a receipt printer, for art



## Requirements

Python3.10

a thermal printer that uses ESC-POS protocol

CPU/RAM min:  Intel i3 with 4GB RAM


## Setting Up udev Rules for USB Receipt Printer on Linux

You will probably need to create a `udev` rule for a USB receipt printer so that all users on your Linux system can access it. 

### Add entry to udev rules

sudo nano /etc/udev/rules.d/99-receipt-printer.rules

Add the following line to the file:

SUBSYSTEM=="usb", ATTR{idVendor}=="6868", ATTR{idProduct}=="0200", MODE="0666", GROUP="plugdev"
SUBSYSTEM=="usb": Ensures the rule applies only to USB devices.


ATTR{idVendor} and ATTR{idProduct}: Match the VID and PID of your printer.
MODE="0666": Grants read and write permissions to all users.
GROUP="plugdev": Sets the device's group to plugdev. Replace plugdev with another group if needed.

Save and close the file.

### Reload udev Rules
Run the following commands to reload the udev rules and apply them:

sudo udevadm control --reload
sudo udevadm trigger

### Verify Permissions
Unplug and replug the receipt printer, then check the permissions of the device node (likely under /dev/):

ls -l /dev/bus/usb/005/074

You should see output similar to this:

crw-rw-rw- 1 root plugdev 189, 74 Jan 19 15:00 /dev/bus/usb/005/074

If the rw permissions are present for all users, the setup is complete.

Notes
Replace the group plugdev with another group if it better suits your system configuration.
If the printer doesn't work as expected, verify the VID and PID using lsusb again to ensure they match.
