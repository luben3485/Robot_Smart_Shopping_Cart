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
        
scanner = Scanner().withDelegate(ScanDelegate())
devices = scanner.scan(1)
for i in devices:
	print("%s:%d"%(i.addr,i.rssi))
	print("---------------------")
