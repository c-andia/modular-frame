import time
import os
from datetime import datetime
import take_photo
import RPi.GPIO as GPIO
from picamera2 import Picamera2
import pathlib
import subprocess
import pyudev

## Initialize the pins

GPIO.setmode(GPIO.BOARD)

greenPin=36
yellowPin=38
inPin=40

GPIO.setup(inPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(yellowPin, GPIO.OUT)
GPIO.setup(greenPin, GPIO.OUT)

wait_for_release = False
MONITORING = True

def check_usb():
	
    context = pyudev.Context()

	## Check for any usb drive connection (take_photo.py will still only save photos to specific drives)
	
    for device in context.list_devices(subsystem='block', DEVTYPE='partition'):
        if device.get('ID_BUS') == 'usb':
            return True
    return False

def flash_led(colPin, flashDuration):

	GPIO.output(greenPin, 0)
	GPIO.output(yellowPin, 0)

	for i in range(flashDuration):

		GPIO.output(colPin, 1)
		time.sleep(0.2)
		GPIO.output(colPin, 0)
		time.sleep(0.2)

try:

	## Clear any stuck pins and indicate that the device is armed after booting 
	
	GPIO.output(greenPin, 0)
	GPIO.output(yellowPin, 0)

	time.sleep(2)

	flash_led(greenPin, 2)

	while MONITORING == True:

		button_state = GPIO.input(inPin)

		## Allow the user to press and hold the button by only triggering after it has been released
		
		if button_state == GPIO.LOW:

			wait_for_release = True
			GPIO.output(greenPin, 1)

		if wait_for_release == True and button_state == GPIO.HIGH:

			GPIO.output(greenPin, 0)
			GPIO.output(yellowPin, 1)

			## Check USB every time the program is run, to avoid crashes if the user has forgotten to put it back in
			
			usb_is_there = check_usb()

			if usb_is_there == 0:

				flash_led(yellowPin, 3)
				print("USB is not connected")

			else:

				## Call the take_photo script in a subprocess so it can write to the drive, as this requires sudo capability   
				
				subprocess.run(['sudo', 'python3', 'take_photo.py'])

				## Indicate that the cameras are done capturing, and give time for the USB to unmount automatically 

				GPIO.output(yellowPin, 0)
				flash_led(greenPin, 4)
				GPIO.output(greenPin, 1)
				time.sleep(0.4)
				
			GPIO.output(yellowPin, 0)
			GPIO.output(greenPin, 0)

			wait_for_release = False

except KeyboardInterrupt:

	print("interrupted")

finally:

	## Indicate that the program has been interrupted.
	
	for i in range(2):
		flash_led(greenPin, 1)
		flash_led(yellowPin, 1)

	GPIO.cleanup()
