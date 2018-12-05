import cv2
import sys
import time
import numpy as np
import socket
import pickle
import struct

origin_img = "test.jpg"
SERVER_IP = "127.0.0.1"
SERVER_PORT = 8889
print("IP:", SERVER_IP)
print("Port:", SERVER_PORT)
print("Starting socket:")

# creat socket object
socket_tcp = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM, proto=0, fileno=None)
server_addr = (SERVER_IP, SERVER_PORT)

start = time.time()
while True:
    try:
        print("Conneting to server at %s:%s..." % server_addr)
        socket_tcp.connect(server_addr)
        print("connect")
        socket_tcp.send(b"Hello server")
        print("Successfully connect to server.")
        data = socket_tcp.recv(1024)
        print("Server send:", data)
        break
    except Exception:
        print("Can't connect to server, try it after %d second." % 1)
        time.sleep(1)
        continue

maxlength = 1024
img = cv2.imread(origin_img)
print(img.shape)
t_data = pickle.dumps(img)  # new
print(len(t_data))
socket_tcp.sendall(struct.pack("L", len(t_data)) + t_data)  # new
''' # new
print(img.shape)
# cv2.imshow('CLIENT', img)
data = np.array(img)
stringData = data.tostring()
length = len(stringData)
socket_tcp.send(str(len(stringData)).ljust(16).encode())
socket_tcp.send(stringData)
''' # new
end = time.time()
print(end - start)
# cv2.waitKey(0)
'''
with open(origin_img, 'rb') as f:
    print("Send data from %s" % origin_img)
    data = f.read(1024)
    while data:
        # print("Sending data...")
        socket_tcp.send(data)
        # print("data size: %d", len(data))
        data = f.read(1024)
    print("Successfully send %s" % origin_img)
    success_mess = "Successfully send " + origin_img
    data = socket_tcp.recv(1024)
    print("Server send:", data)
    socket_tcp.send(success_mess.encode())
'''
