import os
import cv2
import sys
import time
import socket
import pickle
import struct
import threading
import numpy as np
from collections import deque

#cap = cv2.VideoCapture(1)
#ret, frame = cap.read()
#cv2.imwrite("test.jpg", frame)

def create_TCP_socket(ip, port):
    SERVER_IP = ip
    SERVER_PORT = port
    print("IP:", SERVER_IP)
    print("Port:", SERVER_PORT)
    print("Create socket:")
    socket_tcp = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM, proto=0, fileno=None)
    socket_tcp.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    socket_tcp.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1024 * 400)
    server_addr = (SERVER_IP, SERVER_PORT)
    while True:
        try:
            print("Connecting to server at %s:%d..." % (SERVER_IP, SERVER_PORT))
            socket_tcp.connect(server_addr)
            print("connect")
            socket_tcp.send(b"Hellow")
            print("Successfully connect to server %s:%d" % (SERVER_IP, SERVER_PORT))
            data = socket_tcp.recv(1024)
            print("Server send:", data)
            return socket_tcp
        except Exception:
            print("Can't connect to server %s:%d, try it after %d second" %(SERVER_IP, SERVER_PORT, 1))
            time.sleep(1)
            continue
    return socket_tcp


send_socket = create_TCP_socket("140.116.102.106", 8899)
t = 0
while t < 15:
    print("Start")
    cap = cv2.VideoCapture(0)
    #ret, frame = cap.read()
    ret, img = cap.read()
    #cv2.imwrite('send.jpg', frame)
    #img = cv2.imread("send.jpg")
    #img = open("send.jpg", 'rb')
    #f = img.read()
    #print(len(img))
    if ret is False:
        print("No image")
        print()
        print('--------------')
        print()
        t += 1
        continue
    start = time.time()
    # t_data = pickle.dumps(img)  # new
    filename = "img.npy"
    sendname = b"img.npy"
    np.save(filename, img)
    fileinfo_size = struct.calcsize('128sI')
    fhead = struct.pack('128sI', sendname, os.stat(filename).st_size)
    send_socket.send(fhead)
    print("start send...")
    fp = open(filename, 'rb')
    while True:
        data = fp.read(1024 * 200)
        if not data:
            print("end send")
            break
        send_socket.send(data)
    fp.close()

    '''
    t_data = np.load("img.npy")
    print("data size", len(t_data))
    send_socket.sendall(struct.pack("I", len(t_data)) + t_data)  # new
    '''
    print("frame:", t)
    print("size:", os.stat(filename).st_size)
    print("send time:", time.time() - start)
    # img.close()
    t += 1
    print("Successfully send frame")
    print()
    print("-----------------------")
    print()
    time.sleep(0.1)
send_socket.close()
