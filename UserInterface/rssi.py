import time
from bluepy.btle import Scanner, DefaultDelegate

class ScanDelegate(DefaultDelegate):
	def __init__(self):
		DefaultDelegate.__init__(self)

	def HandleDiscovery(self,dev,new_dev,new_dat):
		if new_dev:
			pass
		if new_dat:
			pass
        


def RSSI():
	scanner = Scanner().withDelegate(ScanDelegate())
	time_diff = 0
	first_time =1
	while 1:
		print("new")
		try:
			devices = scanner.scan(1)
##        print("Amount of Devices = "+str(len(devices)))
			for ii in devices:
				print(ii.addr)
				'''
				if ii.addr == u'17:a4:ce:e4:60:f1' or ii.addr == u'72:c1:b1:a3:69:ee' \
				or ii.addr == 'c0:28:8d:36:d2:c3' or ii.addr=='10:bb:35:51:74:b2' \
				or ii.addr== u'd4:36:39:dc:11:47':
				'''
				print("Device %s, RSSI=%d dB" % (ii.addr,ii.rssi))
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
