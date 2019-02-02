#Code pulled from MMM-Facial-Recognition-OCV3 - MagicMirror Module

from __future__ import division
from   builtins import input
import os
import sys
import re
import cv2

sys.path.append((os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))+ '/MMM-Facial-Recognition-OCV3/lib/common/'))
import webcam
from face import FaceDetection

sys.path.append((os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))+ '/MMM-Facial-Recognition-OCV3/lib/tools/'))
from config import ToolsConfig


class FacialRecognitionController:

	def __init__(self, facialRecognitionDir):
		self.face = ToolsConfig.getFaceDetection()
		ToolsConfig.TRAINING_DIR = facialRecognitionDir

	def capture(self, captureName):

		camera = FacialRecognitionController.getCamera()
		toolsConfig = ToolsConfig(captureName)
		image = camera.read()
		camera._camera.release()
		# Convert image to grayscale.
		image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
		# Get coordinates of single face in captured image.
		result = self.face.detect_single(image)

		if result is None:
			return None
		x, y, w, h = result
		# Crop image as close as possible to desired face aspect ratio.
		# Might be smaller if face is near edge of image.
		crop = self.face.crop(image, x, y, w, h,int(ToolsConfig.getFaceFactor() * w))
		# Save image to file.
		filename, count = toolsConfig.getNewCaptureFile()
		cv2.imwrite(filename, crop)

		return filename

	@staticmethod
	def getCamera():
		return webcam.OpenCVCapture(device_id=0)