import numpy as np
import kalman_filter

feature = []
y = []
num = 18
for i in range(100):
	print("Count:"+str(i+1)+ "Now:"+str(num))
	R1,R2,R3,R4,R5,R6,R7,R8,R9,R10,R11,R12 = kalman_filter.rssi_kalman_filter()
	feature.append([R1,R2,R3,R4,R5,R6,R7,R8,R9,R10,R11,R12])
	y.append([num])
x = np.array(feature)
y = np.array(y)
print(x)
print(x.shape)

print(y)
print(y.shape)

np.save( "npy_0619/x_" + str(num) + ".npy" , x )
np.save( "npy_0619/y_" + str(num) + ".npy" , y )
