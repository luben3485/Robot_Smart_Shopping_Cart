kalman_filter.py and kalman_filter_six.py almost the same
kalman_six get rssi from R1 to R6 and calculate the averages
getRssi.py gets rssi numbers after kalman filter and save as numpy
kalman_filter.py calls kalman but it's not in the folder
rssi_six.py scan the old six beacons

svm.py trains ble RSSI data with fingerprint method
load_svm.py predicts region where you are given the six RSSI values.
load_svm_test.py test the model
