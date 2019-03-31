import SingleStickSSDwithUSBCamera_OpenVINO_NCS2_robot as SSD
import cv2
import time

#camera_width = 320
#camera_height = 240
camera_width = 960
camera_height = 720

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 30)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, camera_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, camera_height)

while True:
	ret, frame = cap.read()
	if not ret:
		break
	t = time.time()
	objects = SSD.SSD_predict(frame)
	diff_t = time.time()-t
	#print("It takes " + str(diff_t) + "s for running the model.\n")
	if objects != None:
		
		#print(str(len(objects))+" objects\n")
		for object in objects:
			color = (255, 128, 0)
			box_thickness = 1
			label_text = object.class_name + " (" + str(object.confidence) + "%)"

			cv2.rectangle(frame,(object.box_left,object.box_top),(object.box_right,object.box_bottom),color,box_thickness)
			cv2.putText(frame,label_text,(object.box_left,object.box_top),cv2.FONT_HERSHEY_SIMPLEX, 0.5,color, 1)
	
	cv2.namedWindow('Camera', cv2.WINDOW_AUTOSIZE)
	cv2.imshow('Camera', cv2.resize(frame, (frame.shape[1],frame.shape[0])))
	if cv2.waitKey(1)&0xFF == ord('q'):
		break

