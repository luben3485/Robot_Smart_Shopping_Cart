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

	devices = scanner.scan(0.3)
	devices_selected = []
	for device in devices:
		if device.addr == u'12:3b:6a:1b:bb:05' or device.addr == u'12:3b:6a:1b:bb:13' or device.addr==u'12:3b:6a:1b:ba:a5'or device.addr==u'12:3b:6a:1b:bd:c7'or device.addr==u'12:3b:6a:1b:bb:06'or device.addr==u'12:3b:6a:1b:bd:e4' or device.addr == u'12:3b:6a:1b:b5:d8':
			devices_selected.append(device)
	return devices_selected