import time
import os
from datetime import datetime
import take_photo
import RPi.GPIO as GPIO
from picamera2 import Picamera2
import pathlib
import subprocess
import pyudev
from picamera2 import Picamera2
from libcamera import controls

cam0 = Picamera2(0)
cam1 = Picamera2(1)
cam2 = Picamera2(2)
cam3 = Picamera2(3)

folder_name="/mnt/Lexar/Photos"

GPIO.setmode(GPIO.BOARD)
greenPin=36
yellowPin=38
inPin=40

GPIO.setup(inPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(yellowPin, GPIO.OUT)
GPIO.setup(greenPin, GPIO.OUT)

wait_for_release = False
MONITORING = True

#start = time.time()

USB_name = '/mnt/Lexar'

def check_usb():
    context = pyudev.Context()

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

def get_time():
        
        now = datetime.now()
        return now.strftime("%b. %-d, %Y, %-I.%M.%S %p")
        
def process_timer(stage):
        if stage == 'stop':
                print(f'time elapsed: {time.time()-start} seconds.')
                
def capture():

        try:
                
                # create folder
                
                ftime = get_time()
                
                folderName = f"{USB_name}/Photos/'{ftime}'"
                pathlib.Path.mkdir(folderName)
                
                # take photos

                cam0.configure(cam0.create_still_configuration())
                
                cam0.start()
                cam0.capture_file(f"{folderName}/photo 1.jpeg")
                cam0.close()

                cam1.configure(cam1.create_still_configuration())
                
                cam1.start()
                cam1.capture_file(f"{folderName}/photo 2.jpeg")
                cam1.close()
                
                cam2.configure(cam2.create_still_configuration())
                
                cam2.start()
                cam2.capture_file(f"{folderName}/photo 3.jpeg")
                cam2.close()

                cam3.configure(cam3.create_still_configuration())
                
                cam3.start()
                cam3.capture_file(f"{folderName}/photo 4.jpeg")
                cam3.close()
                
        except FileExistsError:
                print("\nPlease wait before taking another photo.\n")

#if __name__ == "__main__":

#	try:
#		capture()

#	finally:
#		process_timer('stop')

try:
	GPIO.output(greenPin, 0)
	GPIO.output(yellowPin, 0)
	
	time.sleep(2)

	while MONITORING == True:
		
		button_state = GPIO.input(inPin)
		
		if button_state == GPIO.LOW:

			wait_for_release = True
			GPIO.output(greenPin, 1)
			
		if wait_for_release == False and button_state == GPIO.HIGH:
			pass
		
		if wait_for_release == True and button_state == GPIO.HIGH:

			GPIO.output(greenPin, 0)

			usb_is_there = check_usb()

			if usb_is_there == 0:

				flash_led(yellowPin, 3)
				print("USB is not connected")
				
			else:
        
				capture()

			GPIO.output(yellowPin, 0)
			wait_for_release = False

except KeyboardInterrupt:
	print("interrupted")

finally:
	GPIO.cleanup()
