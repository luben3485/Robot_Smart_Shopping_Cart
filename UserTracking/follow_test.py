#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2
import time
import math
import socket
import threading
import numpy as np
from collections import deque
import SingleStickSSDwithUSBCamera_OpenVINO_NCS2_robot as SSD
import sys
import termios
import tty
import serial

class TargetFeature(SSD.DetectionObject):
    center = [0, 0]
    area = 0
    img = None
    gray_img = None
    keypoints = None
    def __init__(self, target, target_img, keypoint_list):
        self.box_left = target.box_left
        self.box_top = target.box_top
        self.box_right = target.box_right
        self.box_bottom = target.box_bottom
        self.class_name = target.class_name
        self.confidence = target.confidence
        self.center = [(target.box_left + target.box_right)/2, (target.box_top + target.box_bottom)/2]
        self.area = (target.box_right - target.box_left) * (target.box_bottom - target.box_top)
        self.img = target_img
        self.gray_img = cv2.cvtColor(target_img, cv2.COLOR_BGR2GRAY)
        self.keypoints = keypoint_list

class Follow(threading.Thread):
    def __init__(self, name, ip, port, testing=False, camera_id = 0):
        threading.Thread.__init__(self)
        self.id = '[' + name + ']'
        self.camera_id = camera_id
        self.decision_socket_ip = ip
        self.decision_socket_port = port
        self.decison_socket = None
        self.prev_position = deque(maxlen = 10)
        self.x = 0
        self.y = 0
        self.frame_center = [0, 0] # [x, y] frame center point
        self.timer = 0
        self.orb = cv2.ORB.create()
        self.bf = cv2.BFMatcher(normType=cv2.NORM_HAMMING)
        self.testing = testing

    def run(self):
     #    self.decison_socket = self.creat_TCP_socket(self.decision_socket_ip, self.decision_socket_port)
        # input_source = "test.avi"
        #self.camera_init(camera_id=input_source)

        # Testing connect with motor
        ser = ''
        old_settings = ''
        file = ''
        line = ""
        s = ""

        if self.testing is True:
            ser = serial.Serial('/dev/ttyACM0' , 9600)
            old_settings = termios.tcgetattr(sys.stdin)
            tty.setcbreak(sys.stdin.fileno())
            if(ser.isOpen()):
                print("connent\n")
                file = open("result.txt",'w')
                file.truncate()
        # Testing connect with motor

        self.camera_init(camera_width=960, camera_height=540, camera_fps=30, camera_id = self.camera_id)
        # (320, 200)
        self.timer = time.time()
        frame = self.get_frame()
        if frame is None:
            self.print_msg("Camera or Video can't open!!!")

        while(True):
            # get camera image
            start_time = time.time()
            frame = self.get_frame()
            # call function person_detect() get result
            objects = self.person_detect(frame)
            # test tracking
            # self.target_tracking(objects, frame)
            # call function target_search() analysis target position
            #      include: characteristic_compare() select target from people
            #               feature_calculate() calculate target feature
            #               return features
            target = self.target_search(frame, objects)
            # call function make_instruction() make final insturction to control cart
            #      include: momentum calculate & compare with previous position
            #               judge the rationality of the position
            #               according to (x,y), target size, center position make instruction
            diff_time = time.time() - start_time
            self.print_msg("It takes %s second to find target.\n" % str(diff_time))
            if target is None:
                # continue
                cv2.imshow("Follow", frame)
                print()
            else:
                instruction = self.make_instruction(target)
                # send instruction
                data = instruction[0] + ' ' + str(instruction[1])
                # self.decison_socket.send(bytes(data.encode('utf-8')))

                # Testing connect with motor
                try:
                    # speed(stop:0) , angle(left:positive; right:negative; straight:0)
                    turnAngle = 0
                    speed = 1.4
                    constant_angle = 5
                    # parse instruction from follow.py 
                    if instruction[0] is 'straight':
                        turnAngle = 0
                        speed = 30
                    elif instruction[0] is 'left':
                        turnAngle = constant_angle
                        speed = 3
                    elif instruction[0] is 'right':
                        turnAngle = -constant_angle
                        speed = 3
                    elif instruction[0] is 'stop':
                        turnAngle = 0
                        speed = 0
                    else:
                        turnAngle = 0
                        speed = 0
            
                    # combine motor instruction
                    line = str(speed) + ' ' + str(turnAngle)
                    ser.write(line.encode())
                    ser.write('\n'.encode())
                    print(line)

                    time.sleep(0.05)
                    line = ""
                    if ser.in_waiting:
                        #print("received")
                        cin = ser.read(1)
                        if cin != b'\n':
                            cin = cin.decode(encoding='utf-8' , errors='ignore')
                            s += cin
                        else:
                            print("received:" + s)
                            file.write(s + '\n')
                            s = ""
                except KeyboardInterrupt:

                    ser.write('0'.encode())
                    ser.write('\n'.encode())
                    ser.close()
                    file.close()
                    if(~ser.isOpen()):
                        print("closed\n")
                        break
                # Testing connect with motor

                self.print_msg("Send follow instruction to server!", data)
                cv2.rectangle(frame, (target.box_left, target.box_top), (target.box_right, target.box_bottom), (0,0,255), 2)
                cv2.rectangle(frame, (self.prev_position[-2].box_left, self.prev_position[-2].box_top),
                                     (self.prev_position[-2].box_right, self.prev_position[-2].box_bottom), (0,255,0), 2)
                cv2.putText(frame, data, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 1, cv2.LINE_AA)
                cv2.circle(frame, (int(target.center[0]), int(target.center[1])), 7, (0,0,255), -1)
            cv2.line(frame, (int(self.x/2), 0), (int(self.x/2), self.y), (0,232,240), 3)
            cv2.line(frame, (int(self.x * 0.4), 0), (int(self.x * 0.4), self.y), (27,211,218), 2)
            cv2.line(frame, (int(self.x * 0.6), 0), (int(self.x * 0.6), self.y), (27,211,218), 2)
            for i in range(len(self.prev_position)-1, -1, -1):
                if self.prev_position[i-1] is None or self.prev_position[i] is None:
                    continue
                thickness = int(np.sqrt(10/float(i+1)) * 2.5)
                center1 = (int(self.prev_position[i].center[0]), int(self.prev_position[i].center[1]))
                center2 = (int(self.prev_position[i-1].center[0]), int(self.prev_position[i-1].center[1]))
                cv2.line(frame, center2, center1, (0,0,255), thickness)
            cv2.namedWindow("Follow", cv2.WINDOW_NORMAL)
            cv2.resizeWindow("Follow", 640, 360)
            #cv2.imshow("Follow", frame)
            #cv2.waitKey(30)
        pass

    def make_instruction(self, target):
        direction = "straight"
        value = 0
        weight = 1
        if target.area > self.x * self.y * 0.6:
            direction = "stop"
            return (direction, int(value))
        standard_area = self.x * self.y * 0.3
        current_position = target.center
        if current_position[0] < self.x * 0.4:
            value = math.log2((1 / (1 - target.area / (self.x * self.y))) * (self.x * 0.5 - current_position[0])) * weight
            direction = "left"
        elif current_position[0] > self.x * 0.6:
            value = math.log2((1 / (1 - target.area / (self.x * self.y))) * (current_position[0] - self.x * 0.5)) * weight
            direction = "right"
        else:
            # sigmoid function to scale the difference of area
            value = (1 / (1 + math.exp(-(1 - (target.area / standard_area)) * 4)) + 1) * 5
        return (direction, int(value))

    def keypoint_detect(self, gray):
        # orb = cv2.ORB.create()
        kps, des = self.orb.detectAndCompute(gray, None)
        return kps, des

    def keypoints_match(self, kp1, des1, kp2, des2):
        # bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        # bf = cv2.BFMatcher(normType=cv2.NORM_HAMMING)
        if des1 is None or des2 is None:
            return 0, 0
        raw_matches = self.bf.knnMatch(des1, des2, k=2)
        if raw_matches is None or raw_matches[0] is None or raw_matches[1] is None:
            return 0, 0
        try:
            good_matches = [m for (m, n) in raw_matches if m.distance < 0.65 * n.distance]
        except:
            return 0, 0

        #raw_number = len(raw_matches)
        good_number = len(good_matches)
        #ratio = good_number / raw_number
        ratio = 0

        #print("Origin matches:", raw_number)
        #print("After matches:", good_number)
        #print("Match ratio:", ratio)
        return ratio, good_number

    def target_search(self, frame, objects):
        target_objects = []
        for obj in objects:
            if obj.class_name is 'person':
                target_objects.append(obj)
        if target_objects is None:
            return None
        # when number of previous position is less 5
        if len(self.prev_position) < 5:
            for target in target_objects:
                if target.confidence < 0.7:
                    continue
                target_center = [(target.box_right + target.box_left)/2,
                                 (target.box_bottom + target.box_top)/2]
                # when target center between x-center of frame +- 20%
                if (target_center[0] <= self.frame_center[0] + self.x * 0.2) and (target_center[0] >= self.frame_center[0] - self.x * 0.2):
                    # crop target reigon in frame
                    target_img = frame[target.box_top:target.box_bottom, target.box_left:target.box_right]
                    print(target_img.shape)
                    if (target_img.shape[0] == 0 or target_img.shape[1] == 0):
                        continue
                    kps, des = self.keypoint_detect(cv2.cvtColor(target_img, cv2.COLOR_BGR2GRAY))
                    self.prev_position.append(TargetFeature(target, target_img, [kps, des]))
                    return None
            return None
        else:
            limit_match_points = 4
            result_list = []
            for j in range(len(target_objects)):
                target = target_objects[j]
                if target.confidence < 0.7:
                    continue
                target_img = frame[target.box_top:target.box_bottom, target.box_left:target.box_right]
                print(target_img.shape)
                if (target_img.shape[0] == 0 or target_img.shape[1] == 0):
                    continue
                gray = cv2.cvtColor(target_img, cv2.COLOR_BGR2GRAY)
                time1 = time.time()
                kps, des = self.keypoint_detect(gray)
                print("keypoint detect time:", time.time()-time1)
                # temp condition
                count = 0
                total_points = 0
                distance = 0
                center = [(target.box_left + target.box_right)/2, (target.box_top + target.box_bottom)/2]
                time1 = time.time()
                for i in range(1, 3, 1):
                    match_points = self.keypoints_match(self.prev_position[-i].keypoints[0], self.prev_position[-i].keypoints[1], kps, des)
                    total_points += match_points[1]
                    if match_points[1] > limit_match_points:
                        count += 1
                    if i <= 3:
                        distance += (np.square(center[0] - self.prev_position[-i].center[0]) + np.square(center[1] - self.prev_position[-i].center[1]))
                result_list.append((j, distance, total_points, count, target_img, [kps, des]))
                print("keypoint match time", time.time() - time1)
            if result_list is None:
                return None
            distance_list = sorted(result_list, key=lambda x: x[1])
            points_list = []
            for i in range(len(distance_list)):
                if distance_list[0][1] / distance_list[i][1] > 0.85:
                    points_list.append(distance_list[i])
            final_list = sorted(points_list, key=lambda x: x[2], reverse=True)
            if len(final_list) > 0:
                index = final_list[0][0]
                self.prev_position.append(TargetFeature(target_objects[index], final_list[0][4], final_list[0][5]))
                return TargetFeature(target_objects[index], final_list[0][4], final_list[0][5])
            return None

    def person_detect(self, frame):
        objects = SSD.SSD_predict(frame)
        return objects

    def camera_init(self, camera_width = 960, camera_height = 720, camera_fps = 30, camera_id = 0):
        self.cap = cv2.VideoCapture(camera_id)
        self.cap.set(cv2.CAP_PROP_FPS, camera_fps)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, camera_width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, camera_height)
        self.x = int(camera_width / 4 * 3)
        #self.x = 960
        self.y = int(camera_height / 4 * 3)
        #self.y = 540
        self.frame_center = [camera_width / 2, camera_height / 2]

    def get_frame(self):
        hasFrame, frame = self.cap.read()
        if not hasFrame:
            return None
        else:
            frame = cv2.resize(frame, (self.x, self.y))
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
if __name__ == "__main__":
    follow_test = Follow('Follow_test', '127.0.0.1', 8888, testing=True)
    print("Start Follow")
    follow_test.start()
