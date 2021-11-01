import cv2
import base64
from config.config import COLOR

def draw_rectangle(image, bbox_dict, encoded=False):
	'''
	Draw bbox detection vehicle and license plate
	Args:
		image(np.array): image for drawed
		bbox_dict(dict): {'name':value(list)}
		encoded(boolen): True/False retrun image decode
	Return:
		drawed_image(any): image drawed retrun str if decoded else np.array 
	'''
	for name in bbox_dict:
		if bbox_dict[name][1]:
			if name == 'vehicle_type':
				color_reactangle = (0, 204, 0) # Green
			elif name == 'license_plate':
				color_reactangle = (204, 102, 0) # Red
			
			x_min, y_min = bbox_dict[name][1][0], bbox_dict[name][1][1]
			x_max, y_max = bbox_dict[name][1][2], bbox_dict[name][1][3]
			# Draw rectangle
			cv2.rectangle(image, (x_min, y_min), (x_max, y_max), color_reactangle, 2)
			# Add label
			cv2.rectangle(image, (x_min, y_min), (x_min+50, y_min+23), color_reactangle, cv2.FILLED)
			cv2.putText(image, f'{bbox_dict[name][0]} | {bbox_dict[name][2]}', (x_min+2,y_min+12), cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1)

	if encoded: return encode_image(image)
	else: return image

def draw_rectangle_list(image, result_list, encoded=False):
	'''
	Draw bounding box, label and clases detection image
	Args:
		img(numpy.ndarray) : image/frame
		result(list) : [[x_min, y_min, x_max, y_max, classes_name, confidence]]
	return : 
		image(numpy.ndarray)
	'''
	if len(result_list):
		for i in result_list:
			x_min, x_max = i[0], i[2]
			y_min, y_max = i[1], i[3]
			classes_name = i[4]
			confidence   = int(i[5]*100)
			color 		 = COLOR[classes_name]
			# Draw rectangle
			cv2.rectangle(image, (x_min, y_min), (x_max, y_max), color, 1)
			# Add label
			cv2.rectangle(image, (x_min, y_min), (x_min+70, y_min+20), color, cv2.FILLED)
			cv2.putText(image, f'{classes_name.upper()}[{confidence}%]', (x_min+2,y_min+12), cv2.FONT_HERSHEY_PLAIN, 0.7, (255, 255, 255), 1)

	# cv2 image np array to base64
	if encoded: return encode_image(image)
	else: return image

def encode_image(image):
	'''
	Encoding image to base64.
	Args:
		image(numpy.ndarray) : image/frame
	Return:
		image_encoded(str)
	'''
	image_list = cv2.imencode('.jpg', image)[1]
	image_bytes = image_list.tobytes()
	image_encoded = base64.b64encode(image_bytes)
	return image_encoded