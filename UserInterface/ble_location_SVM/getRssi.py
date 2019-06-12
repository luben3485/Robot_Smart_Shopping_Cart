import numpy as np
import kalman_filter_six

feature = []
y = []
num = 18
for i in range(30):
	print("Order:"+str(i+1))
	R1,R2,R3,R4,R5,R6,R7 = kalman_filter_six.rssi_kalman_filter_six()
	feature.append([R1,R2,R3,R4,R5,R6,R7])
	y.append([num])
x = np.array(feature)
y = np.array(y)
print(x)
print(x.shape)

print(y)
print(y.shape)

#np.save( "npy_20190605/x_" + str(num) + ".npy" , x )
#np.save( "npy_20190605/y_" + str(num) + ".npy" , y )
