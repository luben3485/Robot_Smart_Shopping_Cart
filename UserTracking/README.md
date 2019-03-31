READ ME!
## Requirement
    * Ubuntu 16.04
    * Python 3.5.2
    * opencv 3.4.3
    * numpy (version relative to opencv)
## How to use
    1. Use getModel.sh to download .caffemodel
    2. Push video file and change input_source to the video name in user_tracking.py 
    3. python3 user_tracking.py then you can get three windows to show the result.
    4. modify ip and port in client.py & server.py
    5. start server.py first and then start client.py

## USB/Pi camera Mode NCS2 SingleStick + Raspberry pi(Synchronous drawing)
### environment
    * Raspbian
    * Python 3.5.2
    * Openvino(opencv 4.0.1)
### How to use
    1. run runSSDPredict.py and it will show detection winow.
### Other
    * SingleStickSSDwithUSBCamera_OpenVINO_NCS2_robot.py contains a funciton which will return a list of object.
    * Each object contains bounding box(box.left,box.top,box.right,box.bottom),class name(There are 21 classes) and confidence.
