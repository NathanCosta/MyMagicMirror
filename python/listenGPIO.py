#!/usr/bin/env python3

import time
from neopixel import *
import RPi.GPIO as GPIO

# LED strip configuration:
LED_COUNT      = 112      # Number of LED pixels.
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
MAX_INTENSITY  = 255

#GPIO pin configuration
LED_STRIP_PIN	= 18
PIR_SENSOR_PIN	= 16
SWITCH_ONE_PIN	= 12
SWITCH_TWO_PIN	= 6

GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)
GPIO.setup(SWITCH_ONE_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def turnOnLEDs():
	while intensity < MAX_INTENSITY:
		led = 0
		
		while led < LED_COUNT:
			strip.setPixelColor(led, Color(intensity, intensity, intensity))
			led += 1

		strip.show()
		time.sleep(0.005)
		intensity += 1

if __name__ == '__main__':
	while True:
		print(GPIO.input(SWITCH_ONE_PIN))
		time.sleep(0.05)


