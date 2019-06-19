import numpy as np
from filterpy.kalman import KalmanFilter
from filterpy.common import Q_discrete_white_noise

f1 = KalmanFilter(dim_x=2, dim_z=1)
f1.x = np.array([-60., -60.])       # initial state (location and velocity)
f1.F = np.array([[1.,1.], [0.,1.]])    # state transition matrix
f1.H = np.array([[1.,0.]])    # Measurement function
f1.P *= 1023.                 # covariance matrix
f1.R = 32                      # state uncertainty
f1.Q = Q_discrete_white_noise(2, 1, .125) # process uncertainty

f2 = KalmanFilter(dim_x=2, dim_z=1)
f2.x = np.array([-60., -60.])       # initial state (location and velocity)
f2.F = np.array([[1.,1.], [0.,1.]])    # state transition matrix
f2.H = np.array([[1.,0.]])    # Measurement function
f2.P *= 1023.                 # covariance matrix
f2.R = 32                      # state uncertainty
f2.Q = Q_discrete_white_noise(2, 1, .125) # process uncertainty
	
f3 = KalmanFilter(dim_x=2, dim_z=1)
f3.x = np.array([-60., -60.])       # initial state (location and velocity)
f3.F = np.array([[1.,1.], [0.,1.]])    # state transition matrix
f3.H = np.array([[1.,0.]])    # Measurement function
f3.P *= 1023.                 # covariance matrix
f3.R = 32                      # state uncertainty
f3.Q = Q_discrete_white_noise(2, 1, .125) # process uncertainty

f4 = KalmanFilter(dim_x=2, dim_z=1)
f4.x = np.array([-60., -60.])       # initial state (location and velocity)
f4.F = np.array([[1.,1.], [0.,1.]])    # state transition matrix
f4.H = np.array([[1.,0.]])    # Measurement function
f4.P *= 1023.                 # covariance matrix
f4.R = 32                      # state uncertainty
f4.Q = Q_discrete_white_noise(2, 1, .125) # process uncertainty

f5 = KalmanFilter(dim_x=2, dim_z=1)
f5.x = np.array([-60., -60.])       # initial state (location and velocity)
f5.F = np.array([[1.,1.], [0.,1.]])    # state transition matrix
f5.H = np.array([[1.,0.]])    # Measurement function
f5.P *= 1023.                 # covariance matrix
f5.R = 32                      # state uncertainty
f5.Q = Q_discrete_white_noise(2, 1, .125) # process uncertainty
	
f6 = KalmanFilter(dim_x=2, dim_z=1)
f6.x = np.array([-60., -60.])       # initial state (location and velocity)
f6.F = np.array([[1.,1.], [0.,1.]])    # state transition matrix
f6.H = np.array([[1.,0.]])    # Measurement function
f6.P *= 1023.                 # covariance matrix
f6.R = 32                      # state uncertainty
f6.Q = Q_discrete_white_noise(2, 1, .125) # process uncertainty

f7 = KalmanFilter(dim_x=2, dim_z=1)
f7.x = np.array([-60., -60.])       # initial state (location and velocity)
f7.F = np.array([[1.,1.], [0.,1.]])    # state transition matrix
f7.H = np.array([[1.,0.]])    # Measurement function
f7.P *= 1023.                 # covariance matrix
f7.R = 32                      # state uncertainty
f7.Q = Q_discrete_white_noise(2, 1, .125) # process uncertainty

f8 = KalmanFilter(dim_x=2, dim_z=1)
f8.x = np.array([-60., -60.])       # initial state (location and velocity)
f8.F = np.array([[1.,1.], [0.,1.]])    # state transition matrix
f8.H = np.array([[1.,0.]])    # Measurement function
f8.P *= 1023.                 # covariance matrix
f8.R = 32                      # state uncertainty
f8.Q = Q_discrete_white_noise(2, 1, .125) # process uncertainty

f9 = KalmanFilter(dim_x=2, dim_z=1)
f9.x = np.array([-60., -60.])       # initial state (location and velocity)
f9.F = np.array([[1.,1.], [0.,1.]])    # state transition matrix
f9.H = np.array([[1.,0.]])    # Measurement function
f9.P *= 1023.                 # covariance matrix
f9.R = 32                      # state uncertainty
f9.Q = Q_discrete_white_noise(2, 1, .125) # process uncertainty
	
f10 = KalmanFilter(dim_x=2, dim_z=1)
f10.x = np.array([-60., -60.])       # initial state (location and velocity)
f10.F = np.array([[1.,1.], [0.,1.]])    # state transition matrix
f10.H = np.array([[1.,0.]])    # Measurement function
f10.P *= 1023.                 # covariance matrix
f10.R = 32                      # state uncertainty
f10.Q = Q_discrete_white_noise(2, 1, .125) # process uncertainty

f11 = KalmanFilter(dim_x=2, dim_z=1)
f11.x = np.array([-60., -60.])       # initial state (location and velocity)
f11.F = np.array([[1.,1.], [0.,1.]])    # state transition matrix
f11.H = np.array([[1.,0.]])    # Measurement function
f11.P *= 1023.                 # covariance matrix
f11.R = 32                      # state uncertainty
f11.Q = Q_discrete_white_noise(2, 1, .125) # process uncertainty

f12 = KalmanFilter(dim_x=2, dim_z=1)
f12.x = np.array([-60., -60.])       # initial state (location and velocity)
f12.F = np.array([[1.,1.], [0.,1.]])    # state transition matrix
f12.H = np.array([[1.,0.]])    # Measurement function
f12.P *= 1023.                 # covariance matrix
f12.R = 32                      # state uncertainty
f12.Q = Q_discrete_white_noise(2, 1, .125) # process uncertainty

