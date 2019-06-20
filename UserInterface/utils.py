import random
import sys
sys.path.append('ble_location_SVM')
import kalman_filter
from sklearn.externals import joblib
import numpy as np
svc_fit = joblib.load('ble_location_SVM/model/svc_20190619.pkl')

def getRandomXY(a,b,c,d):
	x = random.randint(a,b)
	y = random.randint(c,d) 

	return x,y

def trilateration(r1,r2,r3):
	'''
	set P1(0,0),P2(d,0),P3(i,j)
	'''
	d = 10
	i = 0
	j = 5
	x = (r1*r1 - r2*r2 + d*d)/(2*d)
	y = (r1*r1 -r3*r3-x*x +(x-i)*(x-i) +j*j)/(2*j)
	return x ,y

def predPosition():
	R1,R2,R3,R4,R5,R6,R7,R8,R9,R10,R11,R12 = kalman_filter.rssi_kalman_filter()
	x = np.array([[R1,R2,R3,R4,R5,R6,R7,R8,R9,R10,R11,R12]])
	return svc_fit.predict(x)[0]
	#return 0

if __name__ == '__main__':
	a= predPosition()
	print(a)
