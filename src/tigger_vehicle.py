import socket
from datetime import datetime

from .app.vehicle_classification import VehicleClassification

from .utils.tracker import EuclideanDistTracker

from config.config import (
	MIN_CONFIDENCE,
	API_BLITZ,
	POSITION_CAM,
	TOLERANT_TIME,
	A, B,
	WIDTH, HEIGH,
	UDP, IP_BLITZ,
	PORT_BLITZ, MESSAGE
)


class TriggerVehicle:
	def __init__(self):
		self.classification     = VehicleClassification()
		self.tracker			= EuclideanDistTracker()
		self.unique_id			= list()
		self.current_timestamp  = int()
		self.position_restarea	= POSITION_CAM.split(' ')[1]
		self.sock				= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	def __classification_vehicle(self, image):
		'''
		Classification vehicle
		and filter clasess, confidence
		Args:
			image(np.array): image for classification
		Return:
			result(tuple): (
				clasess(str): clases name
				confidence(float): confidence level
				bbox(list): bbox object [x_min, y_min, x_max, y_max]
			)
		'''
		result_classification 	= self.classification.detection(image, image_size=640)
		results_vehicle_list 	= self.classification.filter_and_crop(
			results=result_classification, min_confidence=MIN_CONFIDENCE+0.2
		)
		return results_vehicle_list

	def tigger_vehicle(self, image):
		# Vehicle detection and classification
		try: vehicle_classification_list	= self.__classification_vehicle(image)
		except: vehicle_classification_list = list()
		
		# Object tracking
		if vehicle_classification_list:
			boxes_ids = self.tracker.update(vehicle_classification_list)
			for i in boxes_ids:
				x_min, y_min, x_max, y_max, classes, conf, id = i
				'''
				CONDITION TRACKER
				'''
				print(id)
		# Reset value tracker_id
		if self.tracker.id_count > 1000: self.tracker.id_count = int()
		return vehicle_classification_list
		
	def _conditions_tigger(self, x_min, y_min, x_max, y_max):
		if self.position_restarea == '88a':
			return x_min in range(A[0], B[0]) and \
				(y_max in range(A[1], A[1]+170) or y_max in range(B[1], B[1]+170))

		elif self.position_restarea == '88b':
			return False

		elif self.position_restarea == '207':
			return x_max in range(A[0], B[0]) and \
				(y_max in range(B[1],B[1]+40) or y_max in range(A[1],A[1]+40))

		elif self.position_restarea == '379':
			# return y_max in range(A[1], HEIGH) and \
			# 	(x_min in range(A[0]-170,A[0]+40) or x_min in range(B[0]-300,B[0]))

			return x_min in range(A[0], HEIGH) and \
				(y_max in range(A[1],A[1]+80) or y_max in range(B[1],B[1]+80))

	def _conditions_blitz(self, x_min, y_min, x_max, y_max):
		# Condition lamp blitz in night
		hour_now = datetime.now().hour
		if not hour_now in range(17, 25) and not hour_now in range(1, 6): return False

		if self.position_restarea == '88a':
			return x_min in range(A[0], B[0]) and \
				(y_max in range(A[1], A[1]+130) or y_max in range(B[1], B[1]+130))

		elif self.position_restarea == '88b':
			return False

		elif self.position_restarea == '207':
			return x_max in range(A[0], B[0]) and \
				(y_max in range(B[1]-30,B[1]) or y_max in range(A[1]-30,A[1]))

		elif self.position_restarea == '379':
			# return y_max in range(A[1], HEIGH) and \
			# 	(x_min in range(A[0]-200,A[0]+40) or x_min in range(B[0]-300,B[0]))
			return x_min in range(A[0], HEIGH) and \
				(y_max in range(A[1]-70,A[1]) or y_max in range(B[1]-70,B[1]))