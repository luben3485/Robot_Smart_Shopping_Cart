import numpy as np
from filterpy.kalman import KalmanFilter
from filterpy.common import Q_discrete_white_noise
import random
import time
import kalman

my_filter1 = KalmanFilter(dim_x=2, dim_z=1)
my_filter1.x = np.array([-60., -60.])       # initial state (location and velocity)
my_filter1.F = np.array([[1.,1.], [0.,1.]])    # state transition matrix
my_filter1.H = np.array([[1.,0.]])    # Measurement function
my_filter1.P *= 1023.                 # covariance matrix
my_filter1.R = 32                      # state uncertainty
my_filter1.Q = Q_discrete_white_noise(2, 1, .125) # process uncertainty

my_filter2 = KalmanFilter(dim_x=2, dim_z=1)
my_filter2.x = np.array([-60., -60.])       # initial state (location and velocity)
my_filter2.F = np.array([[1.,1.], [0.,1.]])    # state transition matrix
my_filter2.H = np.array([[1.,0.]])    # Measurement function
my_filter2.P *= 1023.                 # covariance matrix
my_filter2.R = 32                      # state uncertainty
my_filter2.Q = Q_discrete_white_noise(2, 1, .125) # process uncertainty
	
my_filter3 = KalmanFilter(dim_x=2, dim_z=1)
my_filter3.x = np.array([-60., -60.])       # initial state (location and velocity)
my_filter3.F = np.array([[1.,1.], [0.,1.]])    # state transition matrix
my_filter3.H = np.array([[1.,0.]])    # Measurement function
my_filter3.P *= 1023.                 # covariance matrix
my_filter3.R = 32                      # state uncertainty
my_filter3.Q = Q_discrete_white_noise(2, 1, .125) # process uncertainty

total1 = 0
total2 = 0
total3 = 0

#while True:
for i in range(30):
	my_filter1.predict()
	my_filter2.predict()
	my_filter3.predict()
	R1, R2, R3 = kalman.RSSI_ave()
	
	if R1 != 0:
		my_filter1.update(R1)
		# do something with the output
	a = my_filter1.x
	
	if R2 != 0:
		my_filter2.update(R2)
		# do something with the output
	b = my_filter2.x

	if R3 != 0:
		my_filter3.update(R3)
		# do something with the output
	c = my_filter3.x
	#time.sleep(1)
	total1 += a[0]
	total2 += b[0]
	total3 += c[0]
	print("Beacon 1: Before:%d, After:%d, Current Average:%d" %(R1, a[0], total1/(i+1)))
	print("Beacon 2: Before:%d, After:%d, Current Average:%d" %(R2, b[0], total2/(i+1)))
	print("Beacon 3: Before:%d, After:%d, Current Average:%d" %(R3, c[0], total3/(i+1)))
print("Average:%d, %d, %d" %(total1/30, total2/30, total3/30))
