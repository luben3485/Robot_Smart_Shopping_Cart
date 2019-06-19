from sklearn.externals import joblib
import numpy as np

def load_svm(R1,R2,R3,R4,R5,R6,R7):
	fit = joblib.load('ble_location_SVM/model/svc_20190605.pkl') 
	x=np.array([[R1,R2,R3,R4,R5,R6,R7]])
	region = fit.predict(x)[0]
	print("predict region: %d "%(region))
	x = 1
	y = 4
	if region == 1:
		x=1
		y=4
	if region == 2:
		x=1
		y=3
	if region == 3:
		x=1
		y=2
	if region == 4:
		x=1
		y=1
	if region == 5:
		x=2
		y=1
	if region == 6:
		x=3
		y=1
	if region == 7:
		x=4
		y=1
	if region == 8:
		x=5
		y=1
	if region == 9:
		x=6
		y=1
	if region == 10:
		x=7
		y=1
	if region == 11:
		x=7
		y=2
	if region == 12:
		x=7
		y=3
	if region == 13:
		x=7
		y=4
	if region == 14:
		x=6
		y=4
	if region == 15:
		x=5
		y=4
	if region == 16:
		x=4
		y=4
	if region == 17:
		x=3
		y=4
	if region == 18:
		x=2
		y=4
	return x,y 
