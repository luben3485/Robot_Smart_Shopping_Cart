# UserInterface

## Function including audio recognition & barcode scan & Beacon indoor location

### Audio recognition
audio_regonition.py

### barcode scan
barcode.py: scan barcode and QR code

### Beancon indoor location
**All files in folder "ble_location_SVM"**

#### Beacon RSSI
blue_test.py: scan bluetooth devices


#### Fingerprint method
* we use machine learning(SVM) to predict where you are
* Train data is in ble_location_SVM/npy
* SVM model is in ble_location_SVM/model

