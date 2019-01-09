import threading
import socket
import time
from neopixel import *
import RPi.GPIO as GPIO

# LED strip configuration:
LED_COUNT	  = 100	  # Number of LED pixels.
LED_PIN		= 18	  # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ	= 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA		= 10	  # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255	 # Set to 0 for darkest and 255 for brightest
LED_INVERT	 = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL	= 0	   # set to '1' for GPIOs 13, 19, 41, 45 or 53
MAX_INTENSITY  = 255

UDP_IP = "127.0.0.1"
UDP_PORT = 12123 
MAX_THREADS = 10
DEATH_TO_THE_THREADS = False


def listenToUDP():
	print("Listening to UDP")

	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind((UDP_IP, UDP_PORT))

	while not DEATH_TO_THE_THREADS:
		data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
		if(threading.activeCount() < MAX_THREADS):
			colors = data.split(",")
			threading.Thread(target=setLEDColor, args=[int(colors[0]), int(colors[1]), int(colors[2])]).start()

def listenToGPIO():
	print("Listening to GPIO")

	GPIO.setwarnings(True)
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

	pressed = False
	lightsOn = False

	while not DEATH_TO_THE_THREADS:

		if GPIO.input(23):
			if(not pressed):
				pressed = True
				if(lightsOn):
					turnOffLEDs()
					lightsOn = False
				else:
					turnOnLEDs()
					lightsOn = True

		elif(pressed):
			pressed = False

		time.sleep(0.05)


def turnOnLEDs():
	intensity = 0
	
	while intensity < MAX_INTENSITY:
		led = 0
		
		while led < LED_COUNT:
			strip.setPixelColor(led, Color(intensity, intensity, intensity))
			led += 1

		strip.show()
		time.sleep(0.005)
		intensity += 1

def turnOffLEDs():
	intensity = MAX_INTENSITY
	
	while intensity >= 0:
		led = 0
		
		while led < LED_COUNT:
			strip.setPixelColor(led, Color(intensity, intensity, intensity))
			led += 1

		strip.show()
		time.sleep(0.005)
		intensity -= 1

def has_live_threads(threads):
	return True in [t.isAlive() for t in threads]

def setLEDColor(red, green, blue):
	led = 0

	while led < LED_COUNT:
		strip.setPixelColor(led, Color(green, red, blue))
		strip.show()
		led += 1
		time.sleep(0.001)

if __name__ == '__main__':
	threads = []

	strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
	strip.begin()

	listenToUDPThread = threading.Thread(target=listenToUDP)
	listenToGPIOThread = threading.Thread(target=listenToGPIO)

	listenToUDPThread.start()
	listenToGPIOThread.start()
	
	threads.append(listenToUDPThread)
	threads.append(listenToGPIOThread)

	while has_live_threads(threads):
		try:
			# synchronization timeout of threads kill
			[t.join(1) for t in threads
			 if t is not None and t.isAlive()]
		except KeyboardInterrupt:
			# Ctrl-C handling and send kill to threads
			print "Sending kill to threads..."
			DEATH_TO_THE_THREADS = True

