#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2
import time
import socket
import threading
import SingleStickSSDwithUSBCamera_OpenVINO_NCS2_robot as SSD

class Follow(threading.Thread):
    def __init___(self, name, ip, port):
        threading.Thread.__init__(self)
        self.id = '[' + name + ']'
        self.decision_socket_ip = ip
        self.decision_socket_port = port
        self.decison_socket = None
    
    def run(self):
        self.decison_socket = self.creat_TCP_socket(self.decision_socket_ip, self.decision_socket_port)
        # input_source = "test.avi"
        #self.camera_init(camera_id=input_source)
        self.camera_init()
        frame = self.get_frame()
        if frame is None:
            self.print_msg("Camera or Video can't open!!!")

        while(True):
            # get camera image
            frame = self.get_frame()
            # call function person_detect() get result
            objects = self.person_detect(frame)
            # call function target_search() analysis target position
            #      include: characteristic_compare() select target from people
            #               feature_calculate() calculate target feature
            #               return features 
            # call function make_instruction() make final insturction to control cart
            #      include: momentum calculate & compare with previous position
            #               judge the rationality of the position
            #               according to (x,y), target size, center position make instruction
        
            pass
        pass

    def person_detect(self, frame):
        start_time = time.time()
        objects = SSD.SSD_predict(frame)
        diff_time = time.time() - start_time
        self.print_msg("It takes %s second for detect object.\n" % str(diff_time))
        return objects

    def camera_init(self, camera_width = 960, camera_height = 720, camera_fps = 30, camera_id = 0):
        self.cap = cv2.VideoCapture(camera_id)
        self.cap.set(cv2.CAP_PROP_FPS, camera_fps)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, camera_width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, camera_height)

    def get_frame(self):
        hasFrame, frame = self.cap.read()
        if not hasFrame:
            return None
        else:
            return frame

    def creat_TCP_socket(self, ip, port):
        SERVER_IP = ip
        SERVER_PORT = port
        self.print_msg("IP:", SERVER_IP)
        self.print_msg("Port:", SERVER_PORT)
        self.print_msg("Create socket:")
        socket_tcp = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM, proto=0, fileno=None)
        socket_tcp.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        socket_tcp.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1024 * 1024)
        socket_tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_addr = (SERVER_IP, SERVER_PORT)
        while True:
            try:
                self.print_msg("Conneting to server at %s:%s..." % server_addr)
                socket_tcp.connect(server_addr)
                self.print_msg("Successfully connect to server %s:%d" % (SERVER_IP, SERVER_PORT))
                data = socket_tcp.recv(1024).decode('utf-8')
                self.print_msg("Server send:", data)
                break
            except Exception:
                self.print_msg("Can't connect to server %s:%s, try it after %d second." % (SERVER_IP, SERVER_PORT, 1))
                time.sleep(0.5)
                continue
        return socket_tcp

    def print_msg(self, *args):
        print(self.id, " ".join(map(str, args)))