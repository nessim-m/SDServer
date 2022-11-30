from picamera import PiCamera
from picamera.array import PiRGBArray
import time 
import cv2
import sys
# initialize the camera and grab a reference to the raw camera capture
#camera = PiCamera()
#camera.resolution = (640, 480)
#camera.framerate = 32
#cap = PiRGBArray(camera, size=(640, 480))
# allow the camera to warmup
time.sleep(0.1)

#img = cv2.imread('sampleimg_nn.jpg')

thres = 0.6 # Threshold to detect object

cap = cv2.VideoCapture(0)
#cap = img
cap.set(3,640) #for id'ing
cap.set(4,480)
#cap.set(10,70)

sys.path.append('../adeept_picarpro/server/')
#from testprog import go_get_it
classNames= []
classFile = 'coco.names'
with open(classFile,'rt') as f:
	classNames = f.read().rstrip('\n').split('\n')

configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
weightsPath = 'frozen_inference_graph.pb'

net = cv2.dnn_DetectionModel(weightsPath,configPath)
net.setInputSize(320,320)
net.setInputScale(1.0/ 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)
found = False
def gen_frame():
	while True:
		success,img = cap.read() #gives us the image from feed
		classIds, confs, bbox = net.detect(img,confThreshold=thres)
		print(classIds,bbox)

		if len(classIds) != 0:
			for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
				if True:
					cv2.rectangle(img,box,color=(0,255,0),thickness=2)
					cv2.putText(img,classNames[classId-1],(box[0]+10,box[1]+30),
					cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
					cv2.putText(img,str(round(confidence*100,2)),(box[0]+200,box[1]+30),
					cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
		#			found = True
		ret, buffer = cv2.imencode('.jpg', img)
		frame = buffer.tobytes()
		yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
		#if found:
			#pass
			#go_get_it()
			#found = False
			#classIds, confs, bbox = net.detect(img,confThreshold=thres)
