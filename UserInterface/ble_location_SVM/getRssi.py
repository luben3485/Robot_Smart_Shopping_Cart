import numpy as np
import kalman_filter

feature = []
y = []
num = 17
for i in range(30):
	print("Fuck:"+str(i+1))
	R1,R2,R3,R4,R5,R6 = kalman_filter.rssi_kalman_filter()
	feature.append([R1,R2,R3,R4,R5,R6])
	y.append([num])
x = np.array(feature)
y = np.array(y)
print(x)
print(x.shape)

print(y)
print(y.shape)

np.save( "npy_0115/x_" + str(num) + ".npy" , x )
np.save( "npy_0115/y_" + str(num) + ".npy" , y )
