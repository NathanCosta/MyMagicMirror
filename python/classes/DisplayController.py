from subprocess import check_output, call
from threading import Timer

class DisplayController():

	DISPLAY_TIMEOUT_TIME = 60 * 10

	def __init__(self):
		self.updatePowerState()

	def toggleDisplay(self):
		return self.setDisplayPower(not self.displayPower)

	def setDisplayPower(self, powerState):
		call(["vcgencmd", "display_power " + ("1" if powerState else "0")])
		self.updatePowerState()
		return self.displayPower

	def updatePowerState(self):
		response = check_output(["vcgencmd", "display_power"])
		name, val = response.partition("=")[::2]

		self.displayPower = val.strip() == "1"
		self.resetDisplayTimeout()

	def turnOnDisplay(self):
		self.setDisplayPower(True)

	def turnOffDisplay(self):
		self.setDisplayPower(False)

	def clearDisplayTimeout(self):
		if hasattr(self, "timeoutThread") and not self.timeoutThread.finished.isSet():
			self.timeoutThread.cancel()

	def resetDisplayTimeout(self):
		self.clearDisplayTimeout()

		if self.displayPower:
			self.timeoutThread = Timer(self.DISPLAY_TIMEOUT_TIME, self.turnOffDisplay)
			self.timeoutThread.daemon = True
			self.timeoutThread.start()