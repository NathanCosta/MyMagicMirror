#!/usr/bin/env python3

import time
import socket
import select
import RPi.GPIO as GPIO
import threading
import json
import traceback
from neopixel import *
from classes.LedStripController import LedStripController
from classes.DisplayController import DisplayController
from classes.FacialRecognitionController import FacialRecognitionController

# LED strip configuration:
LED_COUNT      = 110     # Number of LED pixels.
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

#network configuration
UDP_IP = "127.0.0.1"
UDP_PORT = 12123 

#tunning response times (in seconds)
BUTTON_DOWN_TIME = 0.5

#seconds to disable the PIR sensor when the display is shut off by the button
PIR_SENSOR_TIMEOUT = 60

#directory storing anything related to facial recognition
FACIAL_RECOGNITION_DIR = "../facialRecognition/"

#tracking variables, nothing to see here, move along
BUTTON_ONE_LAST = 0.0
BUTTON_TWO_LAST = 0.0
PIR_SENSOR_DISABLED = False

#used to interrupt the program
RUN_PROGRAM = True

GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)

GPIO.setup(BUTTON_ONE_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BUTTON_TWO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(PIR_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

strip = Adafruit_NeoPixel(LED_COUNT, LED_STRIP_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

ledStripController = LedStripController(strip, LED_COUNT, MAX_INTENSITY)
displayController = DisplayController()
facialRecognitionController = FacialRecognitionController(FACIAL_RECOGNITION_DIR)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

def handleButtonOne():
	global BUTTON_ONE_LAST
	if time.time() - BUTTON_ONE_LAST > BUTTON_DOWN_TIME:
		BUTTON_ONE_LAST = time.time()
		ledStripController.toggleLeds()

def handleButtonTwo():
	global BUTTON_TWO_LAST, PIR_SENSOR_DISABLED
	if time.time() - BUTTON_TWO_LAST > BUTTON_DOWN_TIME:
		BUTTON_TWO_LAST = time.time()

		toggledTo = displayController.toggleDisplay()
		if not toggledTo:
			timeoutPirSensor()

def timeoutPirSensor():
	global PIR_SENSOR_DISABLED

	if not PIR_SENSOR_DISABLED:
		PIR_SENSOR_DISABLED = True
		timer = threading.Timer(PIR_SENSOR_TIMEOUT, endPirSensorTimeout)
		timer.daemon = True
		timer.start()

def endPirSensorTimeout():
	global PIR_SENSOR_DISABLED
	PIR_SENSOR_DISABLED = False

def handlePirSensor():
	if not PIR_SENSOR_DISABLED:
		displayController.turnOnDisplay()

def handleUDPCall(data):
	if "command" in data:
		if "setLightsColor" == data["command"]:
			r, g, b = hexToRGB(data["color"])
			ledStripController.setAllLedsNow(r, g, b)

		if "capture" == data["command"]:
			facialRecognitionController.capture(data["user"])

def hexToRGB(hex):
	hex = hex.lstrip('#')
	return tuple(int(hex[i:i+2], 16) for i in (0, 2 ,4))

def listenToUDP():
	global RUN_PROGRAM

	while RUN_PROGRAM:
		ready = select.select([sock], [], [], 1)
		if ready[0]:
			data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
			try:
				handleUDPCall(json.loads(data))
			except Exception as e:
				traceback.print_exc()
			
		time.sleep(0.005)

def listenToGPIO():
	global RUN_PROGRAM, BUTTON_ONE_PIN, BUTTON_TWO_PIN, PIR_SENSOR_PIN

	while RUN_PROGRAM:

		if(GPIO.input(BUTTON_ONE_PIN)):
			handleButtonOne()

		if(GPIO.input(BUTTON_TWO_PIN)):
			handleButtonTwo()

		if(GPIO.input(PIR_SENSOR_PIN)):
			handlePirSensor()

		time.sleep(0.05)

if __name__ == '__main__':
	ledStripController.resetAll()

	run_event = threading.Event()
	run_event.set()

	udpThread = threading.Thread(target=listenToUDP)
	gpioThread = threading.Thread(target=listenToGPIO)

	udpThread.start()
	gpioThread.start()

	try:
		#keep the main thread alive
		while RUN_PROGRAM:
			time.sleep(0.5)

	except KeyboardInterrupt:
		RUN_PROGRAM = False

		run_event.clear()
		udpThread.join()
		gpioThread.join()

		ledStripController.resetAll()
		displayController.clearDisplayTimeout()
		displayController.turnOnDisplay()
		sock.close()