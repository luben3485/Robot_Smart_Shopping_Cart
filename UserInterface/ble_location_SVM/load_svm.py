from sklearn.externals import joblib
import numpy as np

def load_svm(R1,R2,R3,R4,R5,R6,R7):
	fit = joblib.load('ble_location_SVM/model/svc_0115.pkl') 
	x=np.array([[R1,R2,R3,R4,R5,R6,R7]])
	region = fit.predict(x)[0]
	print("predict region: %d "%(region))
	x = 0
	y = 0
	if region == 1:
		x=3
		y=80
	if region == 2:
		x=3
		y=62
	if region == 3:
		x=3
		y=40
	if region == 4:
		x=3
		y=20
	if region == 5:
		x=13
		y=20
	if region == 6:
		x=23
		y=20
	if region == 7:
		x=33
		y=20
	if region == 8:
		x=43
		y=20
	if region == 9:
		x=53
		y=20
	if region == 10:
		x=65
		y=20
	if region == 11:
		x=65
		y=40
	if region == 12:
		x=65
		y=62
	if region == 13:
		x=53
		y=62
	if region == 14:
		x=43
		y=62
	if region == 15:
		x=33
		y=62
	if region == 16:
		x=23
		y=62
	if region == 17:
		x=13
		y=62
	return x,y 
