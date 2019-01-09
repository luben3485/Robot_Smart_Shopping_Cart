import numpy as np
from filterpy.kalman import KalmanFilter
from filterpy.common import Q_discrete_white_noise
import random
import time

my_filter = KalmanFilter(dim_x=2, dim_z=1)

my_filter.x = np.array([[2.], [0.]])       # initial state (location and velocity)

my_filter.F = np.array([[1.,1.], [0.,1.]])    # state transition matrix

my_filter.H = np.array([[1.,0.]])    # Measurement function
my_filter.P *= 1023.                 # covariance matrix
my_filter.R = 32                      # state uncertainty
my_filter.Q = Q_discrete_white_noise(2, 2, .1) # process uncertainty

while True:
    my_filter.predict()
    my_filter.update(random.randint(6,10))

    # do something with the output
    x = my_filter.x
    time.sleep(3)
    print(x)
