import numpy as np
from filterpy.kalman import KalmanFilter
from filterpy.common import Q_discrete_white_noise

f1 = KalmanFilter(dim_x=2, dim_z=1)
f1.x = np.array([0., 0.])       # initial state (location and velocity)
f1.F = np.array([[1.,1.], [0.,1.]])    # state transition matrix
f1.H = np.array([[1.,0.]])    # Measurement function
f1.P *= 1023.                 # covariance matrix
f1.R = 32                      # state uncertainty
f1.Q = Q_discrete_white_noise(2, 1, .125) # process uncertainty

f2 = KalmanFilter(dim_x=2, dim_z=1)
f2.x = np.array([0., 0.])       # initial state (location and velocity)
f2.F = np.array([[1.,1.], [0.,1.]])    # state transition matrix
f2.H = np.array([[1.,0.]])    # Measurement function
f2.P *= 1023.                 # covariance matrix
f2.R = 32                      # state uncertainty
f2.Q = Q_discrete_white_noise(2, 1, .125) # process uncertainty

f3 = KalmanFilter(dim_x=2, dim_z=1)
f3.x = np.array([0., 0.])       # initial state (location and velocity)
f3.F = np.array([[1.,1.], [0.,1.]])    # state transition matrix
f3.H = np.array([[1.,0.]])    # Measurement function
f3.P *= 1023.                 # covariance matrix
f3.R = 32                      # state uncertainty
f3.Q = Q_discrete_white_noise(2, 1, .125) # process uncertainty

f4 = KalmanFilter(dim_x=2, dim_z=1)
f4.x = np.array([0., 0.])       # initial state (location and velocity)
f4.F = np.array([[1.,1.], [0.,1.]])    # state transition matrix
f4.H = np.array([[1.,0.]])    # Measurement function
f4.P *= 1023.                 # covariance matrix
f4.R = 32                      # state uncertainty
f4.Q = Q_discrete_white_noise(2, 1, .125) # process uncertainty

f5 = KalmanFilter(dim_x=2, dim_z=1)
f5.x = np.array([0., 0.])       # initial state (location and velocity)
f5.F = np.array([[1.,1.], [0.,1.]])    # state transition matrix
f5.H = np.array([[1.,0.]])    # Measurement function
f5.P *= 1023.                 # covariance matrix
f5.R = 32                      # state uncertainty
f5.Q = Q_discrete_white_noise(2, 1, .125) # process uncertainty

f6 = KalmanFilter(dim_x=2, dim_z=1)
f6.x = np.array([0., 0.])       # initial state (location and velocity)
f6.F = np.array([[1.,1.], [0.,1.]])    # state transition matrix
f6.H = np.array([[1.,0.]])    # Measurement function
f6.P *= 1023.                 # covariance matrix
f6.R = 32                      # state uncertainty
f6.Q = Q_discrete_white_noise(2, 1, .125) # process uncertainty

def kalmanFilter(distance):
	f1.predict()
	f2.predict()
	f3.predict()
	f4.predict()
	f5.predict()
	f6.predict()
	f1.update(distance[0])
	f2.update(distance[1])
	f3.update(distance[2])
	f4.update(distance[3])
	f5.update(distance[4])
	f6.update(distance[5])
	
	newDistance = [f1.x[0], f2.x[0], f3.x[0], f4.x[0], f5.x[0], f6.x[0]]
	
	return newDistance
