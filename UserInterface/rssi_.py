import time
import math
from bluepy.btle import Scanner, DefaultDelegate

class ScanDelegate(DefaultDelegate):
	def __init__(self):
		DefaultDelegate.__init__(self)

	def HandleDiscovery(self,dev,new_dev,new_dat):
		if new_dev:
			pass
		if new_dat:
			pass
        


def RSSI(ble):
	scanner = Scanner().withDelegate(ScanDelegate())
	time_diff = 0
	first_time =1

	while 1:
		try:
			devices = scanner.scan(1)
##        print("Amount of Devices = "+str(len(devices)))
			for ii in devices:
				
				if ii.addr == u'20:c3:8f:8d:82:d3' or ii.addr == u'20:c3:8f:8d:7e:40' \
				or ii.addr==u'20:c3:8f:8d:7c:55':
					if ii.addr == u'20:c3:8f:8d:82:d3':

						print("Device 1, RSSI=%d dB " % (ii.rssi))
						#return li.rssi
						#txPower = -30
						#ratio = ii.rssi*1.0/txPower
						#distance1 = 0.02255*math.pow(ratio,6.00016)-0.39841
						#print(distance1)
					#if ble == 2 and ii.addr == u'20:c3:8f:8d:7e:40':
						#count2 = count2 +1
						#RSSI2 = RSSI2 + li.rssi
						#print("Device 2, RSSI=%d dB ,count=%d" % (ii.rssi,count2))
						#txPower = -30
						#ratio = ii.rssi*1.0/txPower
						#distance2 = 0.02255*math.pow(ratio,6.00016)-0.39841
						#print(distance2)
					#if ble == 3 and ii.addr == u'20:c3:8f:8d:7c:55':
						#count3 = count3 +1
						#RSSI3 = RSSI3 + li.rssi
						#print("Device 3, RSSI=%d dB ,count=%d" % (ii.rssi,count3))
						#txPower = -30
						#ratio = ii.rssi*1.0/txPower
						#distance3 = 0.02255*math.pow(ratio,6.00016)-0.39841
						#print(distance3)
					

					
					if first_time == 1:
						first_time = 0
						pass
					else:
						time_diff = time.time()-time_prev
                    

						
                
					time_prev = time.time()
					rssi_prev = ii.rssi
					continue
					
		except:
			continue

