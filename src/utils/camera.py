import cv2

class Camera:
	'''
	Read camera module cv2 and
	run command v4l2 config
	Args:
		num_device(int): number device camera
	'''
	def __init__(self, url_stream):
		self.url_stream = url_stream
		self.camera = cv2.VideoCapture(self.url_stream)

	def camera_streaming(self):
		if not self.camera.isOpened(): self.__init__(self.url_stream)
		return self.camera