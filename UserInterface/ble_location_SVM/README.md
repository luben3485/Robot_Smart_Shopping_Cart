kalman_filter.py: 	return the new RSSI after kalman filter
kalman.py:				get rssi from R1 to R6 and calculate the averages
getRssi.py:			gets rssi numbers after kalman filter and save as numpy
rssi.py:			scan the old six beacons
kalman_object.py	initialize filter1 to filter12

3 -> 1 -> 2 -> 4

svm.py:					trains ble RSSI data with fingerprint method
load_svm.py:			predicts region where you are given the six RSSI values.
load_svm_test.py:		test the model

