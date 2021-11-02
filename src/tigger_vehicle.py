import time
import socket
from datetime import datetime

from .utils.tracker import EuclideanDistTracker
from .app.vehicle_classification_v2 import VehicleClassification

from config.config import (
	MIN_CONFIDENCE,
	POSITION_CAM,
	TOLERANT_TIME,
	A, B, HEIGH,
	IP_JETSON, PORT_JETSON
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
		try:
			result_classification 	= self.classification.detection(image)
			results_vehicle_list 	= self.classification.filter_and_crop(
				results=result_classification, min_confidence=MIN_CONFIDENCE
			)
		except: results_vehicle_list = list()
		return results_vehicle_list

	def __send_udp_trigger_vehicle(self, message_str_send):
		try:
			self.sock.sendto(str.encode(message_str_send), (IP_JETSON, PORT_JETSON))
			self.sock.settimeout(0.2)
			message = self.sock.recvfrom(1024)
			self.sock.settimeout(0.2)
			print(message[0])
		except: pass

	def tigger_vehicle(self, image):
		# Vehicle detection and classification
		vehicle_classification_list	= self.__classification_vehicle(image)
		
		# Object tracking
		if vehicle_classification_list:
			boxes_ids = self.tracker.update(vehicle_classification_list)
			for i in boxes_ids:
				x_min, y_min, x_max, y_max, classes, conf, id = i
				if self._conditions_tigger(x_min, y_min, x_max, y_max):
					if not id in self.unique_id:
						timestamp_now = int(time.time())
						if (timestamp_now-self.current_timestamp) >= TOLERANT_TIME:
							self.current_timestamp = timestamp_now
							self.__send_udp_trigger_vehicle(f'{classes} {round(conf, 2)}')
							if len(self.unique_id) > 10: self.unique_id = list()
						else: self.current_timestamp = self.current_timestamp

		# Reset value tracker_id
		if self.tracker.id_count > 40: self.tracker.id_count = int()
		return vehicle_classification_list
		
	def _conditions_tigger(self, x_min, y_min, x_max, y_max):
		if self.position_restarea == '88a':
			return x_min in range(A[0], B[0]) and \
				(y_max in range(A[1], A[1]+170) or y_max in range(B[1], B[1]+170))

		elif self.position_restarea == '88b':
			return False

		elif self.position_restarea == '207':
			return y_max in range(180, 199)
				
		elif self.position_restarea == '379':
			return x_min in range(A[0], HEIGH) and \
				(y_max in range(A[1],A[1]+80) or y_max in range(B[1],B[1]+80))