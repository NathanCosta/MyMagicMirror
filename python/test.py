import RPi.GPIO as GPIO
import time

GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

pressed = False
lightsOn = False
count = 1
while True:

	if GPIO.input(23):
		if(not pressed):
			pressed = True
		#	if(lightsOn):
		#		turnOffLEDs()
		#		lightsOn = False
		#	else:
		#		turnOnLEDs()
		#		lightsOn = True

	elif(pressed):
		pressed = False

	print(str(count) + str(pressed))
	count += 1
	time.sleep(0.05)
