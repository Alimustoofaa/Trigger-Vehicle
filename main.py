import cv2
import time
from src.utils.camera import  Camera
from src.tigger_vehicle import TriggerVehicle
from src.utils.draw_rectangle import draw_rectangle_list

from config.config import (
	CAMERA_URL, HEIGH, WIDTH
)

class RunAplication:
	def __init__(self):
		self.trigger    	= TriggerVehicle()
		self.camera_url		= Camera(url_stream=CAMERA_URL)
		self.cap			= self.camera_url.camera_streaming()

	def __crop_image(self, image):
		return image[0:HEIGH, 250:WIDTH]

	def run(self):
		print('Starting Aplication')
		while True:
			ret, frame = self.cap.read()
			if not ret:
				self.cap.release()
				time.sleep(2)
				self.cap = self.camera_url.camera_streaming()
			else:
				frame = self.__crop_image(frame)
				vehicle_classification_list = self.trigger.tigger_vehicle(frame)
				frame = draw_rectangle_list(
					frame, vehicle_classification_list,
					encoded=False
				)
				cv2.imshow("frame", frame)

				key = cv2.waitKey(30)
				if key == 27:
					break

		self.cap.release()
		cv2.destroyAllWindows()

if __name__ == '__main__':
	aplication = RunAplication()
	aplication.run()			
