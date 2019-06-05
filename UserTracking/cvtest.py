import cv2
import numpy as np

img = cv2.imread('test.jpg')
type(img)
print(img.shape)


cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
#fourcc = cv2.VideoWriter_fourcc(*'DIVX')
#out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 360))
c = 0
while (cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        c += 1
#        out.write(frame)
        print(frame.shape)
    else:
        break
    if c > 100:
        break
cap.release()
#out.release()
