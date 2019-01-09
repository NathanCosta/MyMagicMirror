from subprocess import check_output, call

class MonitorController():

	def __init__(self):
		self.updatePowerState()

	def toggleMonitor(self):
		self.setMonitorPower(not self.displayPower)

	def setMonitorPower(self, powerState):
		call(["vcgencmd", "display_power " + ("1" if powerState else "0")])
		self.updatePowerState()

	def updatePowerState(self):
		response = check_output(["vcgencmd", "display_power"])
		name, val = response.partition("=")[::2]

		self.displayPower = val.strip() == "1"