import random
import rssi_
import math

def RSSI_ave():
	count1 = 0
	count2 = 0
	count3 = 0
	count4 = 0
	count5 = 0
	count6 = 0
	R1 = 0
	R2 = 0
	R3 = 0
	R4 = 0
	R5 = 0
	R6 = 0
	while 1:
		devices = rssi_.RSSI()
		for device in devices:
			if device.addr == u'20:c3:8f:8d:82:d3':
				count1 += 1
				R1 += device.rssi
			if device.addr == u'20:c3:8f:8d:7e:40':
				count2 += 1
				R2 += device.rssi
			if device.addr == u'20:c3:8f:8d:7c:55':
				count3 += 1
				R3 += device.rssi
			if device.addr == u'20:c3:8f:8d:7e:31':
				count4 += 1
				R4 += device.rssi
			if device.addr == u'20:c3:8f:8d:91:7e':
				count5 += 1
				R5 += device.rssi
			if device.addr == u'20:c3:8f:8d:82:d0':
				count6 += 1
				R6 += device.rssi
			print(count1,count2,count3,count4,count5,count6)
		if count1 >= 1 and count2 >= 1 and count3 >= 1 and count4 >=1 and count5 >=1 and count6>=1:
			break
	
	R1_ave = R1/count1
	R2_ave = R2/count2
	R3_ave = R3/count3
	R4_ave = R4/count4
	R5_ave = R5/count5
	R6_ave = R6/count6
	
	#print( "RSSI R1:%d R2:%d R3:%d" %(R1,R2,R3))
	#print( "RSSI R1:%d" %R1)
	return R1_ave, R2_ave, R3_ave,R4_ave, R5_ave, R6_ave
def RssiToDistance(rssi):
	txPower = -30
	ratio = rssi*1.0/txPower
	distance = 0.02255*math.pow(ratio,6.00016)-0.39841
	return distance
	
	
def getRandomXY(a,b,c,d):
	x = random.randint(a,b)
	y = random.randint(c,d) 

	return x,y

def trilateration(r1,r2,r3):
	'''
	set P1(0,0),P2(d,0),P3(i,j)
	'''
	#d = 10.5
	d = 4
	i = 0
	#j = 6.6
	j = 4
	x = (r1*r1 - r2*r2 + d*d)/(2*d)
	y = (r1*r1 -r3*r3-x*x +(x-i)*(x-i) +j*j)/(2*j)
	return x ,y
