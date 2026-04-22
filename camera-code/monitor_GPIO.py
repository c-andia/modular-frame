import time
from datetime import datetime
import take_photo
import RPi.GPIO as GPIO
from picamera2 import Picamera2
import pathlib

GPIO.setmode(GPIO.BOARD)
greenPin=36
yellowPin=38
inPin=40

GPIO.setup(inPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(yellowPin, GPIO.OUT)
GPIO.setup(greenPin, GPIO.OUT)

wait_for_release = False
MONITORING = True

def flash_led(colPin, flashDuration):

	GPIO.output(greenPin, 0)
	GPIO.output(yellowPin, 0)

	for i in range(flashDuration):
		
		GPIO.output(colPin, 1)
		time.sleep(0.2)
		GPIO.output(colPin, 0)
		time.sleep(0.2)

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
			GPIO.output(yellowPin, 1)
			take_photo.capture()
			GPIO.output(yellowPin, 0)
			wait_for_release = False

except KeyboardInterrupt:
	print("interrupted")

finally:
	GPIO.cleanup()
