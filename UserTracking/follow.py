#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2
import time
import math
import socket
import threading
from collections import deque
import SingleStickSSDwithUSBCamera_OpenVINO_NCS2_robot as SSD

class TargetFeature(SSD.DetectionObject):
    center = [0, 0]
    area = 0
    img = None
    gray_img = None
    keypoints = None
    def __init__(self, target, target_img, kps):
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
        self.keypoints = kps

class Follow(threading.Thread):
    def __init__(self, name, ip, port, camera_id = 0):
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

    def run(self):
     #    self.decison_socket = self.creat_TCP_socket(self.decision_socket_ip, self.decision_socket_port)
        # input_source = "test.avi"
        #self.camera_init(camera_id=input_source)
        self.camera_init(camera_id = self.camera_id)
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
            target = self.target_search(frame, objects)
            # call function make_instruction() make final insturction to control cart
            #      include: momentum calculate & compare with previous position
            #               judge the rationality of the position
            #               according to (x,y), target size, center position make instruction
            if target is None:
                continue
            else:
                instruction = self.make_instruction(target)
                # send instruction
                data = instruction[0] + ' ' + str(instruction[1])
           #    self.decison_socket.send(bytes(data.encode('utf-8')))
                self.print_msg("Send follow instruction to server!", data)
                cv2.rectangle(frame, (target.box_left, target.box_top), (target.box_right, target.box_bottom), (0,0,255))
                cv2.rectangle(frame, (self.prev_position[-1].box_left, self.prev_position[-1].box_top),
                        (self.prev_position[-1].box_right, self.prev_position[-1].box_bottom), (0,255,0))
                cv2.putText(frame, data, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 1, cv2.LINE_AA)
            cv2.nameWindow("Follow", cv2.WINDOW_NORMAL)
            cv2.imshow("Follow", frame)
            cv2.waitKey(30)
        pass

    def make_instruction(self, target):
        direction = "straight"
        value = 0
        weight = 1
        if target.area > self.x * self.y * 0.6:
            diection = "stop"
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


    def feature_calculate(self, target):
        target_center = [(target.box_right + target.box_left)/2,
                         (target.box_bottom + target.box_top)/2]
        # temp condition
        # displacement between previous frame and current frame must smaller than 20% of weight and height
        if (target_center[0] <= self.prev_position[-1].center[0] + self.x * 0.2) and (target_center[0] >= self.prev_position[-1].center[0] - self.x * 0.2):
            return True
        else:
            return False

    def keypoint_detect(self, gray):
        detector = cv2.FastFeatureDetector_create() # FAST
        kps = detector.detect(gray)
        return kps

    def SURF(self, grayImg, kpsData):
        extractor = cv2.DescriptorExtractor_create("SURF")
        # extractor = cv2.xfeatures2d.SURF_create()
        (kps, descs) = extractor.compute(grayImg, kpsData)
        if len(kps) > 0:
            return (kps, descs)
        else:
            return ([], None)

    def feature_matching(self, prevImg, targetImg, prevFeature, targetFeature):
        # resize to width = 600px
        #prevImg = imutils.resize(prevImg, width = 600)
        #targetImg = imutils.resize(targetImg, width = 600)
        matcher = cv2.DescriptorMatcher_create("BruteForce")
        rawMatches = matcher.knnMatch(prevFeature[1], targetFeature[1], 2)
        matches = []
        # match each pair of keypoints
        for m in rawMatches:
            print("#1:{} , #2:{}".format(m[0].distance, m[1].distance))
            if len(m) == 2 and m[0].distance < m[1].distance * 0.8:
                matches.append((m[0].trainIdx, m[0].queryIdx))
        # temp condition
        # It should be some rate of match keypoints
        if len(matches) > 5:
            return 1
        else:
            return 0

    def target_search(self, frame, objects):
        target_objects = []
        for obj in objects:
            if obj.class_name is 'person':
                target_objects.append(obj)
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
                    kps = self.keypoint_detect(cv2.cvtColor(target_img, cv2.COLOR_BGR2GRAY))
                    self.prev_position.append(TargetFeature(target, target_img, kps))
                    return None
            return None
        else:
            for target in target_objects:
                if target.confidence < 0.7:
                    continue
                # reduce computing time of compare
                # delete some impossible objects
                if not self.feature_calculate(target):
                    continue
                # compare with previous image
                target_img = frame[target.box_top:target.box_bottom, target.box_left:target.box_right]
                print(target_img.shape)
                if (target_img.shape[0] == 0 or target_img.shape[1] == 0):
                    continue
                gray = cv2.cvtColor(target_img, cv2.COLOR_BGR2GRAY)
                kps = self.keypoint_detect(gray)
                # temp condition
                '''
                result1 = self.feature_matching(self.prev_position[-1].gray_img, gray,
                                      self.SURF(self.prev_position[-1].gray_img, self.prev_position[-1].keypoints), self.SURF(gray, kps))
                result2 = self.feature_matching(self.prev_position[-2].gray_img, gray,
                                      self.SURF(self.prev_position[-2].gray_img, self.prev_position[-2].keypoints), self.SURF(gray, kps))
                result3 = self.feature_matching(self.prev_position[-3].gray_img, gray,
                                      self.SURF(self.prev_position[-3].gray_img, self.prev_position[-3].keypoints), self.SURF(gray, kps))
                if result1 + result2 + result3 >= 2:
                    self.prev_position.append(TargetFeature(target, target_img, kps))
                    return TargetFeature(target, target_img, kps)
                '''
                self.prev_position.append(TargetFeature(target, target_img, kps))
                return TargetFeature(target, target_img, kps)
            return None

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
        self.x = camera_width
        self.y = camera_height
        self.frame_center = [camera_width / 2, camera_height / 2]

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
if __name__ == "__main__":
    follow_test = Follow('Follow_test', '127.0.0.1', 8888, 'video.avi')
    print("Start Follow")
    follow_test.start()
