kalman_filter.py: 		old version of kalman_filter_six.py
kalman_filter_six.py: 	return the new RSSI after kalman filter
kalman_six:				get rssi from R1 to R6 and calculate the averages
getRssi.py:				gets rssi numbers after kalman filter and save as numpy
rssi_six.py:			scan the old six beacons

4 -> 2 -> 3 -> 5

svm.py:					trains ble RSSI data with fingerprint method
load_svm.py:			predicts region where you are given the six RSSI values.
load_svm_test.py:		test the model

