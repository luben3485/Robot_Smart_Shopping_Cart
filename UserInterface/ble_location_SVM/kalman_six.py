import random
import rssi_six
import math

def RSSI_ave_six():
	iteration = 0
	count1 = 0
	count2 = 0
	count3 = 0
	count4 = 0
	count5 = 0
	count6 = 0
	count7 = 0
	R1 = 0
	R2 = 0
	R3 = 0
	R4 = 0
	R5 = 0
	R6 = 0
	R7 = 0
	while 1:
		iteration +=1
		devices = rssi_six.RSSI()
		for device in devices:
			if device.addr == u'12:3b:6a:1b:bb:05':
				count1 += 1
				R1 += device.rssi
			if device.addr == u'12:3b:6a:1b:bb:13':
				count2 += 1
				R2 += device.rssi
			if device.addr == u'12:3b:6a:1b:ba:a5':
				count3 += 1
				R3 += device.rssi
			if device.addr == u'12:3b:6a:1b:bd:c7':
				count4 += 1
				R4 += device.rssi
			if device.addr == u'12:3b:6a:1b:bb:06':
				count5 += 1
				R5 += device.rssi
			if device.addr == u'12:3b:6a:1b:bd:e4':
				count6 += 1
				R6 += device.rssi
			if device.addr == u'12:3b:6a:1b:b5:d8':
				count7 += 1
				R7 += device.rssi
			print(count1,count2,count3,count4,count5,count6,count7)
		if iteration >=20:
			if count1 == 0:
				R1 = -80
				count1 = 1
			if count2 == 0:
				R2 = -80
				count2 = 1
			if count3 == 0:
				R3 = -80
				count3 = 1
			if count4 == 0:
				R4 = -80
				count4 = 1
			if count5 == 0:
				R5 = -80
				count5 = 1
			if count6 == 0:
				R6 = -80
				count6 = 1
			if count7 == 0:
				R7 = -80
				count7 = 1
			break
		if count1 >= 1 and count2 >= 1 and count3 >= 1 and count4 >=1 and count5 >=1 and count6 >=1 and count7>=1:
			break
	
	R1_ave = R1/count1
	R2_ave = R2/count2
	R3_ave = R3/count3
	R4_ave = R4/count4
	R5_ave = R5/count5
	R6_ave = R6/count6
	R7_ave = R7/count7
	#print( "RSSI R1:%d R2:%d R3:%d" %(R1,R2,R3))
	#print( "RSSI R1:%d" %R1)
	return R1_ave, R2_ave, R3_ave,R4_ave, R5_ave, R6_ave, R7_ave
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
