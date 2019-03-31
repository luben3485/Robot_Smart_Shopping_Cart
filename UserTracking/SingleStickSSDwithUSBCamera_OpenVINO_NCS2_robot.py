import sys
import numpy as np
import cv2
from os import system
import io, time
from os.path import isfile, join
import re

class DetectionObject():
	box_left = 0
	box_top = 0
	box_right = 0
	box_bottom = 0
	class_name = ""
	confidence = 0.0
	
	def __init__(self,box_left,box_top,box_right,box_bottom,class_name,confidence):
		self.box_left = box_left
		self.box_top = box_top
		self.box_right = box_right
		self.box_bottom = box_bottom
		self.class_name = class_name
		self.confidence = confidence

net = cv2.dnn.readNet('lrmodel/MobileNetSSD/MobileNetSSD_deploy.xml', 'lrmodel/MobileNetSSD/MobileNetSSD_deploy.bin')
net.setPreferableTarget(cv2.dnn.DNN_TARGET_MYRIAD)

def SSD_predict(frame):

	LABELS = ('background',
          'aeroplane', 'bicycle', 'bird', 'boat',
          'bottle', 'bus', 'car', 'cat', 'chair',
          'cow', 'diningtable', 'dog', 'horse',
          'motorbike', 'person', 'pottedplant',
          'sheep', 'sofa', 'train', 'tvmonitor')



	try:
		objects = []
		height = frame.shape[0]
		width = frame.shape[1]
		
		blob = cv2.dnn.blobFromImage(frame, 0.007843, size=(300, 300), mean=(127.5,127.5,127.5), swapRB=False, crop=False)
		net.setInput(blob)
		out = net.forward()
		out = out.flatten()

		for box_index in range(100):
			if out[box_index + 1] == 0.0:
				break
			base_index = box_index * 7
			if (not np.isfinite(out[base_index]) or
			not np.isfinite(out[base_index + 1]) or
			not np.isfinite(out[base_index + 2]) or
			not np.isfinite(out[base_index + 3]) or
			not np.isfinite(out[base_index + 4]) or
			not np.isfinite(out[base_index + 5]) or
			not np.isfinite(out[base_index + 6])):
				continue


			x1 = max(0, int(out[base_index + 3] * height))
			y1 = max(0, int(out[base_index + 4] * width))
			x2 = min(height, int(out[base_index + 5] * height))
			y2 = min(width, int(out[base_index + 6] * width))

			object_info_overlay = out[base_index:base_index + 7]

			min_score_percent = 60
			source_image_width = width
			source_image_height = height

			base_index = 0
			class_id = object_info_overlay[base_index + 1]
			percentage = int(object_info_overlay[base_index + 2] * 100)
			if (percentage <= min_score_percent):
				continue

			box_left = int(object_info_overlay[base_index + 3] * source_image_width)
			box_top = int(object_info_overlay[base_index + 4] * source_image_height)
			box_right = int(object_info_overlay[base_index + 5] * source_image_width)
			box_bottom = int(object_info_overlay[base_index + 6] * source_image_height)
			class_name = LABELS[int(class_id)]
			obj = DetectionObject(box_left,box_top,box_right,box_bottom,class_name,percentage)
			objects.append(obj)
		return objects

	except:
		import traceback
		traceback.print_exc()
