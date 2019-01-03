import time
import StoppableThread
from neopixel import *

class LEDStripThread(StoppableThread.StoppableThread):

	def __init__(self, strip, ledCount, maxIntensity=255):
		super(LEDStripThread, self).__init__()
		self.strip = strip
		self.maxIntensity = maxIntensity
		self.ledCount = ledCount

	def turnOnLEDs(self):
		intensity = 0
		print("Turning on LEDs")
		while intensity < self.maxIntensity:
			led = 0

			while led < self.ledCount:
				self.strip.setPixelColor(led, Color(intensity, intensity, intensity))
				led += 1

			self.strip.show()
			time.sleep(0.005)
			intensity += 1

	def turnOffLEDs(self):
		intensity = self.maxIntensity
	
		while intensity >= 0:
			led = 0
	
			while led < self.ledCount:
				self.strip.setPixelColor(led, Color(intensity, intensity, intensity))
				led += 1

			self.strip.show()
			time.sleep(0.005)
			intensity -= 1