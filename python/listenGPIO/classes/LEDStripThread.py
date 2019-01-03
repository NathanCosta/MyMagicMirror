import time
import StoppableThread
import copy
from neopixel import *

class LEDStripThread(StoppableThread.StoppableThread):

	TRANSITION_STEPS = 100 #how many steps needed to get the LEDs to their final value
	TRANSITION_TIME = 2	#the amount of seconds to get the LEDs to their final value
	TRANSITION_STEP_TIME = TRANSITION_TIME / float(TRANSITION_STEPS) #this is what's actually being used to decide the total time used

	def __init__(self, strip, ledCount, maxIntensity=255):
		super(LEDStripThread, self).__init__()
		self.strip = strip
		self.maxIntensity = maxIntensity
		self.ledCount = ledCount
		
		self.togglingLeds = False
		self.ledsOn = False
		self.ledValues = self.getLEDInitialVal()

	def toggleLEDs(self):
		if not self.togglingLeds:
			if self.ledsOn:
				self.turnOffLEDs()
			else:
				self.turnOnLEDs()

	def turnOnLEDs(self):
		self.ledsOn = True
		self.togglingLeds = True
		self.setAllLEDs(self.maxIntensity)
		self.togglingLeds = False

	def turnOffLEDs(self):
		self.ledsOn = False
		self.togglingLeds = True
		self.setAllLEDs(0)
		self.togglingLeds = False

	def setAllLEDs(self, finalValue):
		initialValues = copy.deepcopy(self.ledValues)

		for step in range(1, self.TRANSITION_STEPS + 1):
			startTime = time.time()

			for led in range(self.ledCount) :
				r = self.getPixelColorVal(initialValues[led][0], step, finalValue)
				g = self.getPixelColorVal(initialValues[led][1], step, finalValue)
				b = self.getPixelColorVal(initialValues[led][2], step, finalValue)

				self.setLEDValue(led, r, g, b)

			self.strip.show()

			#going to need to take into consideration the run time so that we can get as close to TRANSITION_TIME as possible
			sleepTime = self.TRANSITION_STEP_TIME - (time.time() - startTime)
			time.sleep(sleepTime if sleepTime > 0 else 0)

	def setLEDValue(self, led, r, g, b):
		self.ledValues[led][0] = r
		self.ledValues[led][1] = g
		self.ledValues[led][2] = b
		self.strip.setPixelColor(led, Color(g,r,b))

	def getLEDInitialVal(self):
		initialValues = []
		for led in range(self.ledCount) :
			initialValues.append([0,0,0])

		return initialValues

	def getPixelColorVal(self, initialValue, currentStep, finalValue):
		return int(round(initialValue + ((finalValue - initialValue) / float(self.TRANSITION_STEPS)) * currentStep))