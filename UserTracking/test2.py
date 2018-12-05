import cv2
import sys
import time
import socket
import numpy as np
import pickle
import struct

origin_img = "origin_img.jpg"
HOST_IP = "127.0.0.1"
HOST_PORT = 8889
print("IP:", HOST_IP)
print("Port:", HOST_PORT)
print("Starting socket:")

# creat socket object
socket_tcp = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM, proto=0, fileno=None)
print("TCP server listen at %s:%d" % (HOST_IP, HOST_PORT))
host_addr = (HOST_IP, HOST_PORT)

# bind socket to host_ip and host_port
socket_tcp.bind(host_addr)

# listen connection request
socket_tcp.listen(1)

socket_client, (client_ip, client_port) = socket_tcp.accept()
print("Connection accepted from %s" % client_ip)

# wait for client connect
# new
data = ""
payload_size = struct.calcsize("L")
# new
while True:
    start = time.time()
    data = socket_client.recv(4096)
    print("Server received:", data)
    socket_client.send(b"Welcome to Cloud Computing Server.")
    print("Start receive image!")
    data = b""
    print(len(data), payload_size)
    while len(data) < payload_size:
        print(1, len(data))
        data += socket_client.recv(4096)
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("L", packed_msg_size)[0]
    print(msg_size)
    while len(data) < msg_size:
        print(2, len(data))
        data += socket_client.recv(4096)
    frame_data = data[:msg_size]
    data = data[msg_size:]

    frame = pickle.loads(frame_data)
    print(frame.shape)
    cv2.imshow('SERVER', frame)
    cv2.waitKey(0)
    '''
    img_length = socket_client.recv(16)
    count = int(img_length)
    buf = b''
    while count:
        data = socket_client.recv(1024)
        if not data:
            break
        buf += data
        count -= len(data)
    data = np.fromstring(buf, dtype='uint8')
    print(data.shape)
    decimg = cv2.imdecode(data, 1)
    print(decimg.shape)
    '''
    # cv2.imshow('SERVER', decimg)
    # cv2.waitKey(0)
    '''
    with open(origin_img, 'wb') as f:
        print("Write data to %s" % origin_img)
        while True:
            # print("Receiving data...")
            data = socket_client.recv(1024)
            # print("data size: %d", len(data))
            if not data or len(data) < 1024:
                break
            f.write(data)
    print("Successfully get %s" % origin_img)
    success_mess = "Successfully get " + origin_img
    socket_client.send(success_mess.encode())
    data = socket_client.recv(1024)
    print("Server received:", data)
    '''
    end = time.time()
    print(end - start)
    break
