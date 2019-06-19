import numpy as np
from filterpy.kalman import KalmanFilter
from filterpy.common import Q_discrete_white_noise
import random
import time
import kalman
import kalman_object as ko

def rssi_kalman_filter():
	#while True:
	total1 = 0
	total2 = 0
	total3 = 0
	total4 = 0
	total5 = 0
	total6 = 0
	total7 = 0
	total8 = 0
	total9 = 0
	total10 = 0
	total11 = 0
	total12 = 0
	num  = 1
	for i in range(num):
		print(i)
		ko.f1.predict()
		ko.f2.predict()
		ko.f3.predict()
		ko.f4.predict()
		ko.f5.predict()
		ko.f6.predict()
		ko.f7.predict()
		ko.f8.predict()
		ko.f9.predict()
		ko.f10.predict()
		ko.f11.predict()
		ko.f12.predict()
	
		R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12 = kalman.RSSI_ave()
		if R1 != 0:
			ko.f1.update(R1)
			# do something with the output
		a = ko.f1.x
	
		if R2 != 0:
			ko.f2.update(R2)
			# do something with the output
		b = ko.f2.x

		if R3 != 0:
			ko.f3.update(R3)
			# do something with the output
		c = ko.f3.x
		
		if R4 != 0:
			ko.f4.update(R4)
			# do something with the output
		d = ko.f4.x
		
		if R5 != 0:
			ko.f5.update(R5)
			# do something with the output
		e = ko.f6.x
		
		if R6 != 0:
			ko.f6.update(R6)
			# do something with the output
		f = ko.f6.x
		
		if R7 != 0:
			ko.f7.update(R7)
			# do something with the output
		g = ko.f7.x
		
		if R8 != 0:
			ko.f8.update(R8)
			# do something with the output
		h = ko.f8.x
		
		if R9 != 0:
			ko.f9.update(R9)
			# do something with the output
		i = ko.f9.x
		
		if R10 != 0:
			ko.f10.update(R10)
			# do something with the output
		j = ko.f10.x
		
		if R11 != 0:
			ko.f11.update(R11)
			# do something with the output
		k = ko.f11.x
		
		if R12 != 0:
			ko.f12.update(R12)
			# do something with the output
		l = ko.f12.x
		#time.sleep(1)
		total1 += a[0]
		total2 += b[0]
		total3 += c[0]
		total4 += d[0]
		total5 += e[0]
		total6 += f[0]
		total7 += g[0]
		total8 += h[0]
		total9 += i[0]
		total10 += j[0]
		total11 += k[0]
		total12 += l[0]
		#print("Beacon 1: Before:%d, After:%d, Current Average:%d" %(R1, a[0], total1/(i+1)))
		#print("Beacon 2: Before:%d, After:%d, Current Average:%d" %(R2, b[0], total2/(i+1)))
		#print("Beacon 3: Before:%d, After:%d, Current Average:%d" %(R3, c[0], total3/(i+1)))
	print("Average:%d, %d, %d, %d ,%d ,%d, %d, %d, %d, %d, %d, %d" %(total1/num, total2/num, total3/num, total4/num, total5/num, total6/num, total7/num, total8/num, total9/num, total10/num, total11/num, total12/num))
	return total1/num, total2/num, total3/num, total4/num, total5/num, total6/num, total7/num, total8/num, total9/num, total10/num, total11/num, total12/num



