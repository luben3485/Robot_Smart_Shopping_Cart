from sklearn.externals import joblib
import numpy as np
import kalman_filter_six
svc_fit = joblib.load('model/svc_20190605.pkl') 
for i in range(30):
	R1,R2,R3,R4,R5,R6,R7 = kalman_filter_six.rssi_kalman_filter_six()
	x=np.array([[R1,R2,R3,R4,R5,R6,R7]])
	print(svc_fit.predict(x))
