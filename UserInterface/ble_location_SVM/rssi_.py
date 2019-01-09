import time
import math
from bluepy.btle import Scanner, DefaultDelegate
import sys
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

	devices = scanner.scan(1)
	devices_selected = []
	for device in devices:
		if device.addr == u'20:c3:8f:8d:82:d3' or device.addr == u'20:c3:8f:8d:7e:40' or device.addr==u'20:c3:8f:8d:7c:55'or device.addr==u'20:c3:8f:8d:7e:31'or device.addr==u'20:c3:8f:8d:91:7e'or device.addr==u'20:c3:8f:8d:82:d0':
			devices_selected.append(device)
	return devices_selected
