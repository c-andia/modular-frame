**The following is a reference for navigating the device's code structure.**

**monitor_GPIO.py** Watches the input pins and describes the main feedback behaviour. It verifies that a viable USB storage device is connected, and then it then calls the take_photos program.
  Edit this file if: 
- The control behaviour must be changed.

**take_photos.py** configures the cameras, takes photos and sends them to the USB drive.
  Edit this file if:
- The USB must be changed or replaced.
- The cameras must be changed (not replaced).
- The camera configuration must be altered.

**bootErrorLog.txt** logs... boot errors...

**camera-launcher.sh** initiates monitor_GPIO at boot time.

*local files to be aware of:*

**crontab** is edited by typing 'crontab -e' into the terminal. It points the machine to where camera-launcher.sh is so it runs.

**bashrc** I'm not actually sure if it is used, but it might be a place to check if things aren't working. Type 'sudo nano ~/.bashrc' and look at the bottom line.

if a new USB is being attached, you need to set it up:

1. Find the UUID and type of the drive.
2. Create a mount point.
3. Mount the drive to the mount point (should be something like 'mount /mnt/mntname /dev/usbname/'
4. I think there is another step here that I forgot 😿 probably to do with cron or bashrc
5. Edit the variable 'USB_name' in take_photos.py to the new mountpoint name.
