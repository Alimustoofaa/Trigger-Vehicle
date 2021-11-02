import os
import json
import socket
import numpy as np

HOSTNAME = socket.gethostname()

POSITION_CAM = 'RA 207' #f'RA {HOSTNAME.split("restarea")[1].upper()}'

#========================== DIRECTORY =====================================
ROOT 					= os.path.normpath(os.path.dirname(__file__))

DIRECTORY_MODEL         = os.path.expanduser('~/.Halotec-LPR/Model')

DIRECTORY_LOGGER        = os.path.expanduser('~/.Halotec-LPR/Logger')

DIRECTORY_SAVE_CAPTURE  = os.path.join(ROOT, 'captures')


#============================ MODELS ======================================
DETECTION_MODEL = {
	'license_plate' : {
		'filename': 'model_license_plate_iso_code.pt',
		'url' : 'https://github.com/Alimustoofaa/1-PlateDetection/releases/download/model_yolov5/license_plat_indonesia_best.pt',
		'file_size' : 14753191
	},
	'yolov5s': {
		'filename': 'model_yolov5s.pt',
		'url' : 'https://github.com/Alimustoofaa/1-PlateDetection/releases/download/model_yolov5/yolov5s.pt',
		'file_size' : 14796495
	}
}


#============================ URL CAMERA ======================================
CAMERA_URL = 'http://54.151.233.173:8080/restarea/km207a.flv'

#============================ DETECTION ======================================
COLOR = {
	'car'	: (0, 153, 0),
	'truck'	: (204,0,102),
	'bus'	: (204, 102, 0)
}

MIN_CONFIDENCE = 0.1

CLASESS_MODEL_SSDNET = [
	'unlabeled', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 
	'traffic light', 'fire hydrant', 'street sign', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 
	'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'hat', 'backpack', 'umbrella', 
	'shoe', 'eye glasses', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball', 
	'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket', 'bottle', 'plate', 
	'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli', 
	'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'mirror', 
	'dining table', 'window', 'desk', 'toilet', 'door', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 
	'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'blender', 'book', 'clock', 'vase',
	'scissors', 'teddy bear', 'hair drier', 'toothbrush'
]

CLASESS_MODEL_YOLOV5 = [
	'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 
	'traffic light', 'fire hydrant', 'street sign', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 
	'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'hat', 'backpack', 'umbrella', 
	'shoe', 'eye glasses', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball', 
	'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket', 'bottle', 'plate', 
	'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli', 
	'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'mirror', 
	'dining table', 'window', 'desk', 'toilet', 'door', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 
	'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'blender', 'book', 'clock', 'vase',
	'scissors', 'teddy bear', 'hair drier', 'toothbrush'
]

VEHICLE_CLASESS 			= ['car', 'bus', 'truck']


#========================= TRIGGER VEHICLE ====================================
'''
Line Trigger
	A------------B
'''
RESOLUTIONS_DICT = {
	# 16:9
	'270p'   : (480, 270),
	'360p'	 : (640, 360),
	'720p'   : (1280, 720),
	'1080p'  : (1920, 1080),

	# 4:3
	'1944p'	: (2592, 1944)
}

if POSITION_CAM.split(" ")[1] == '88A':
	TOLERANT_TIME = 1
	BLITZ_TIME = 20
	WIDTH = RESOLUTIONS_DICT['360p'][0]
	HEIGH = RESOLUTIONS_DICT['360p'][1]
	A = int((15/100) * WIDTH), int((28/100) * HEIGH)
	B = int((100/100) * WIDTH), int((42/100) * HEIGH)

elif POSITION_CAM.split(" ")[1] == '88B':
	TOLERANT_TIME = 2
	BLITZ_TIME = 20
	WIDTH = RESOLUTIONS_DICT['360p'][0]
	HEIGH = RESOLUTIONS_DICT['360p'][1]
	A = int((2/100) * WIDTH), int((79/100) * HEIGH)
	B = int((94/100) * WIDTH), int((57/100) * HEIGH)

elif POSITION_CAM.split(" ")[1] == '207':
	TOLERANT_TIME 	= 2
	BLITZ_TIME 		= 20
	WIDTH = RESOLUTIONS_DICT['360p'][0]
	HEIGH = RESOLUTIONS_DICT['360p'][1]
	A = int((5/100) * WIDTH), int((88/100) * HEIGH)
	B = int((95/100) * WIDTH), int((73/100) * HEIGH)

elif POSITION_CAM.split(" ")[1] == '379':
	TOLERANT_TIME 	= 1
	BLITZ_TIME 		= 20
	WIDTH = RESOLUTIONS_DICT['360p'][0]
	HEIGH = RESOLUTIONS_DICT['360p'][1]
	A = int((11/100) * WIDTH), int((33/100) * HEIGH)
	B = int((88/100) * WIDTH), int((53/100) * HEIGH)
else:
	TOLERANT_TIME 	= 1
	BLITZ_TIME 		= 20


#========================= STREAMING & API WEB & BLITZ =================================
API_BLITZ			= f'http://192.168.8.65/blitz/{BLITZ_TIME}'
_IP_URL 			=  '54.151.233.122'
PORT 				= 8001
URL_VEHICLE_API 	= f'http://{_IP_URL}/list_vehicles/add'
if POSITION_CAM.split(" ")[1] 	== '88A': _URL_STREAMING_RTMP = f'rtmp://{_IP_URL}/km88a/2021/10/21'
elif POSITION_CAM.split(" ")[1] == '88B': _URL_STREAMING_RTMP = f'rtmp://{_IP_URL}/km88b/2021/10/21'
elif POSITION_CAM.split(" ")[1] == '207': _URL_STREAMING_RTMP = f'rtmp://{_IP_URL}/km207a/2021/10/21'
elif POSITION_CAM.split(" ")[1] == '379': _URL_STREAMING_RTMP = f'rtmp://{_IP_URL}/km379a/2021/10/21'
else: _URL_STREAMING_RTMP = f'rtmp://{_IP_URL}/km379a/2021/10/21'
#========================= UDP BLITZ =================================
UDP 		= True
IP_BLITZ 	= '192.168.8.65'
PORT_BLITZ 	= 4210
MESSAGE 	= b'blitz 20'

COMMAND_FFMPEG = [
	'ffmpeg',
	'-y',
	'-f', 'rawvideo',
	# '-stream_loop', '-1',
	'-vcodec', 'rawvideo',
	'-pix_fmt', 'bgr24',
	'-s', f'{str(RESOLUTIONS_DICT["270p"][0])}x{str(RESOLUTIONS_DICT["270p"][1])}',
	'-r', '10',
	'-i', '-',
	'-c:v', 'libx264',
	'-b:v', '300K',
	'-pix_fmt', 'yuv420p',
	# '-preset', 'medium',
	'-f', 'flv',
	'-flvflags', 'no_duration_filesize',
	_URL_STREAMING_RTMP
]

# Straming camera
FPS = 30
# -> Lounch string
LAUNCH_STRING = 'appsrc name=source is-live=true block=true format=GST_FORMAT_TIME ' \
				'caps=video/x-raw,format=BGR, '\
				f'width={str(RESOLUTIONS_DICT["720p"][0])},height={str(RESOLUTIONS_DICT["720p"][1])},framerate={FPS}/1 ' \
				'! videoconvert ! video/x-raw,format=I420 ' \
				'! x264enc speed-preset=ultrafast tune=zerolatency ' \
				'! rtph264pay config-interval=1 name=pay0 pt=96'