from sklearn.externals import joblib
import numpy as np
import kalman_filter
svc_fit = joblib.load('model/svc_20190605.pkl') 
for i in range(30):
	R1,R2,R3,R4,R5,R6,R7,R8,R9,R10,R11,R12 = kalman_filter.rssi_kalman_filter()
	x=np.array([[R1,R2,R3,R4,R5,R6,R7]])
	print(svc_fit.predict(x))
