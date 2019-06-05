import numpy as np
from filterpy.kalman import KalmanFilter
from filterpy.common import Q_discrete_white_noise

f = KalmanFilter(dim_x=6, dim_z=1)
f1.x = np.array([0., 0., 0., 0., 0., 0.])       # initial state (location and velocity)
f1.F = np.array([[1.,1.], [0.,1.]])    # state transition matrix
f1.H = np.array([[1.,0.]])    # Measurement function
f1.P *= 1023.                 # covariance matrix
f1.R = 32                      # state uncertainty
f1.Q = Q_discrete_white_noise(2, 1, .125) # process uncertainty


def kalmanFilter(distance):
	f.predict()
	f.update(distance)
	
	newDistance = [f.x]
	
	return newDistance
