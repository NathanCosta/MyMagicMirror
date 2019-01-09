#!/usr/bin/env python3

import time
from neopixel import *
import RPi.GPIO as GPIO
from classes.LedStripController import LedStripController
from classes.DisplayController import DisplayController

# LED strip configuration:
LED_COUNT      = 112     # Number of LED pixels.
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
MAX_INTENSITY  = 50

#GPIO pin configuration
LED_STRIP_PIN	= 18
PIR_SENSOR_PIN	= 16
BUTTON_ONE_PIN	= 12
BUTTON_TWO_PIN	= 6

#tunning response times (in seconds)
BUTTON_DOWN_TIME = 0.5

#tracking variables, nothing to see here, move along
BUTTON_ONE_LAST = 0.0
BUTTON_TWO_LAST = 0.0

GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)

GPIO.setup(BUTTON_ONE_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BUTTON_TWO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(PIR_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

strip = Adafruit_NeoPixel(LED_COUNT, LED_STRIP_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

ledStripController = LedStripController(strip, LED_COUNT, MAX_INTENSITY)
displayController = DisplayController()

def handleButtonOne():
	global BUTTON_ONE_LAST
	if time.time() - BUTTON_ONE_LAST > BUTTON_DOWN_TIME:
		BUTTON_ONE_LAST = time.time()

		ledStripController.toggleLeds()

def handleButtonTwo():
	global BUTTON_TWO_LAST
	if time.time() - BUTTON_TWO_LAST > BUTTON_DOWN_TIME:
		BUTTON_TWO_LAST = time.time()

		displayController.toggleDisplay()

def handlePirSensor():
	displayController.turnOnDisplay()

if __name__ == '__main__':
	ledStripController.resetAll()

	while True:

		if(GPIO.input(BUTTON_ONE_PIN)):
			handleButtonOne()

		if(GPIO.input(BUTTON_TWO_PIN)):
			handleButtonTwo()

		if(GPIO.input(PIR_SENSOR_PIN)):
			handlePirSensor()

		time.sleep(0.05)