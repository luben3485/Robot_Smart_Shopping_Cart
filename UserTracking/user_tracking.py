import os
import cv2
import sys
import time
import threading
import numpy as np
import argparse
from collections import deque

import user_detect

ap = argparse.ArgumentParser()
ap.add_argument("-i", "-image", required=False, help="Path to the image",
                dest='image')
args = vars(ap.parse_args())

################################################################
# video = cv2.VideoCapture(args['image'])
# frame = cv2.imread('test3.jpg')
def SkeletonCheck(frameWidth, frameHeight, skeletonPoint, x_intercept, y_intercept):
    # pass contition:
    aspect_ratio = 8
    pass_status = {'vertical': False,
                   'aspect_ratio': False}
    if x_intercept < y_intercept:
        pass_status['vertical'] = True
    if x_intercept > 0 and y_intercept / x_intercept < aspect_ratio:
        pass_status['aspect_ratio'] = True
    final_status = True
    for status in pass_status.values():
        if status is not True:
            final_status = False
            break
    return final_status


class skeletonThread (threading.Thread):
        def __init__(self, frame, name):
            threading.Thread.__init__(self)
            print('start detect!')
            self.frame = frame
            self.name = name
            self.detect_finish = False
            self.hasDetect = None
            self.skeletonPoint = None
            self.x_intercept = None
            self.y_intercept = None
            rectangle = np.zeros(frame.shape[:2], dtype="uint8")
            cv2.rectangle(rectangle, (300, 0), (900, 1080), 255, -1)
            mask = rectangle
            self.cacluate_frame = cv2.bitwise_and(frame, frame, mask=mask)

        def run(self):
            print("開始線程：" + self.name)
            self.hasDetect, self.skeletonPoint, self.x_intercept, self.y_intercept = user_detect.skeletonDetect(self.cacluate_frame)
            self.draw_box()
            self.detect_finish = True
            print("退出線程：" + self.name)

        def draw_box(self):
            frameWidth = frame.shape[1]
            frameHeight = frame.shape[0]
            self.trackingBoxPoints = {'x_left': frameWidth * 0.4,
                                      'y_top': frameHeight * 0.4,
                                      'x_right': frameWidth * 0.6,
                                      'y_bottom': frameHeight * 0.8}
            if self.hasDetect:
                self.trackingBoxPoints['x_left'] = int(self.skeletonPoint['x_left'] - self.x_intercept * 0.25)
                self.trackingBoxPoints['x_right'] = int(self.skeletonPoint['x_right'] + self.x_intercept * 0.25)
                self.trackingBoxPoints['y_top'] = int(self.skeletonPoint['y_top'] - self.y_intercept * 0.4)
                self.trackingBoxPoints['y_bottom'] = int(self.skeletonPoint['y_bottom'] + self.y_intercept * 0.3)

                cv2.rectangle(self.frame,
                              (self.skeletonPoint['x_left'], self.skeletonPoint['y_top']),
                              (self.skeletonPoint['x_right'], self.skeletonPoint['y_bottom']),
                              (0, 0, 255), 2)
                if SkeletonCheck(frameWidth, frameHeight, self.skeletonPoint, self.x_intercept, self.y_intercept):
                    cv2.rectangle(self.frame,
                                  (self.trackingBoxPoints['x_left'], self.trackingBoxPoints['y_top']),
                                  (self.trackingBoxPoints['x_right'], self.trackingBoxPoints['y_bottom']),
                                  (0, 255, 0), 2)
            # cv2.imshow('Output Tracking Box', self.frame)


class trackingThread (threading.Thread):
        def __init__(self, name, frame, bbox, tracker=None, rebuild=False):
            threading.Thread.__init__(self)
            print('start tracking!')
            self.bbox = bbox  # (xmin,ymin,boxwidth,boxheight)
            if rebuild:
                self.tracker = creatTracker()
                ok = self.tracker.init(frame, bbox)
            else:
                self.tracker = tracker
            # bbox = (287, 23, 86, 320)  # (xmin,ymin,boxwidth,boxheight)
            self.frame = frame
            self.name = name
            self.tracking_finish = False

        def run(self):
            print("開始線程：" + self.name)
            timer = cv2.getTickCount()
            # Update tracker
            ok, self.bbox = self.tracker.update(self.frame)

            # Calculate Frames per second (FPS)
            fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)

            # Draw bounding box
            if ok:
                # Tracking success
                p1 = (int(self.bbox[0]), int(self.bbox[1]))
                p2 = (int(self.bbox[0] + self.bbox[2]), int(self.bbox[1] + self.bbox[3]))
                center = (int(self.bbox[0] + self.bbox[2] / 2), int(self.bbox[1] + self.bbox[3] / 2))
                cv2.rectangle(self.frame, p1, p2, (255, 0, 0), 2, 1)
                pts.appendleft(center)
                for i in range(1, len(pts)):

                    # if either of the tracked points are None, ignore
                    # them
                    if pts[i - 1] is None or pts[i] is None:
                        continue

                    # otherwise, compute the thickness of the line and
                    # draw the connecting lines
                    thickness = int(np.sqrt(buffer / float(i + 1)) * 2.5)
                    cv2.line(self.frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
            else:
                # Tracking failure
                cv2.putText(self.frame, "Tracking failure detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)

            # Display tracker type on frame
            cv2.putText(self.frame, tracker_type + " Tracker", (100, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2);

            # Display FPS on frame
            cv2.putText(self.frame, "FPS : " + str(int(fps)), (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);

            # Display result
            # cv2.imshow("Tracking", self.frame)
            self.tracking_finish = True
            print("退出線程：" + self.name)


input_source = "foot_test3.mp4"
tracking_box = None
cap = cv2.VideoCapture(input_source)
hasFrame, frame = cap.read()
if not hasFrame:
    print("Video can't open!!!")
skeleton_thread = skeletonThread(frame, 'Skeleton Thread 1')
skeleton_thread.start()

# vid_writer = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame.shape[1], frame.shape[0]))

##### Object Tracking #####

(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
tracker_type = tracker_types[2]


def creatTracker():
    if int(minor_ver) < 3:
        tracker = cv2.Tracker_create(tracker_type)
    else:
        if tracker_type == 'BOOSTING':
            tracker = cv2.TrackerBoosting_create()
        if tracker_type == 'MIL':
            tracker = cv2.TrackerMIL_create()
        if tracker_type == 'KCF':
            tracker = cv2.TrackerKCF_create()
        if tracker_type == 'TLD':
            tracker = cv2.TrackerTLD_create()
        if tracker_type == 'MEDIANFLOW':
            tracker = cv2.TrackerMedianFlow_create()
        if tracker_type == 'GOTURN':
            tracker = cv2.TrackerGOTURN_create()
        if tracker_type == 'MOSSE':
            tracker = cv2.TrackerMOSSE_create()
        if tracker_type == "CSRT":
            tracker = cv2.TrackerCSRT_create()
    return tracker


buffer = 64
pts = deque(maxlen=buffer)
tracking_thread = trackingThread('Tracking Thread 1', frame, (0, 0, 0, 0), rebuild=True)
tracking_thread.start()
'''
tracker = creatTracker()
# bbox = (287, 23, 86, 320)  # (xmin,ymin,boxwidth,boxheight)
bbox = (0, 0, 0, 0)  # (xmin,ymin,boxwidth,boxheight)
ok = tracker.init(frame, bbox)
buffer = 64
pts = deque(maxlen=buffer)
'''
cv2.namedWindow("Origin", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Origin", (int(frame.shape[1] / 2), int(frame.shape[0] / 2)))
cv2.namedWindow("Normal Video", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Normal Video", (int(frame.shape[1] / 2), int(frame.shape[0] / 2)))
cv2.namedWindow("Tracking", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Tracking", (int(frame.shape[1] / 2), int(frame.shape[0] / 2)))
##### Object Tracking #####
pre_skeleton = []
while cv2.waitKey(30) < 0:
    hasFrame, frame = cap.read()
    if not hasFrame:
        cv2.waitKey()
        break
    cv2.imshow("Origin", frame)
    if skeleton_thread.detect_finish:
        skeleton_thread.join()
        print('finish detect')
        #cv2.resizeWindow("Normal Video", (int(frame.shape[1] / 2), int(frame.shape[0] / 2)))
        cv2.imshow('Normal Video', skeleton_thread.frame)
        if skeleton_thread.hasDetect:
            tracking_box = (skeleton_thread.trackingBoxPoints['x_left'], skeleton_thread.trackingBoxPoints['y_top'],
                            skeleton_thread.trackingBoxPoints['x_right'] - skeleton_thread.trackingBoxPoints['x_left'],
                            skeleton_thread.trackingBoxPoints['y_bottom'] - skeleton_thread.trackingBoxPoints['y_top'])
            pre_skeleton.append([skeleton_thread.frame, tracking_box])
            # tracking_thread.join()
            # cv2.resizeWindow("Tracking", (int(frame.shape[1] / 2), int(frame.shape[0] / 2)))
            # cv2.imshow("Tracking", tracking_thread.frame)
            # tracking_thread = trackingThread('Tracking Thread 1', skeleton_thread.frame, tracking_box, rebuild=True)
            # tracking_thread.start()
            # tracker = creatTracker()
            # ok = tracker.init(skeleton_thread.frame, tracking_box)
        skeleton_thread = skeletonThread(frame, 'Skeleton Thread 1')
        skeleton_thread.start()
    if tracking_thread.tracking_finish:
        tracking_thread.join()
        print('tracking finish')
        #cv2.resizeWindow("Tracking", (int(frame.shape[1] / 2), int(frame.shape[0] / 2)))
        cv2.imshow("Tracking", tracking_thread.frame)
        if len(pre_skeleton) > 0:
            tracking_thread = trackingThread('Tracking Thread 1', pre_skeleton[-1][0], pre_skeleton[-1][1], rebuild=True)
            while len(pre_skeleton) <= 0:
                pre_skeleton.pop()
        else:
            tracking_thread = trackingThread('Tracking Thread 1', frame, tracking_thread.bbox, tracking_thread.tracker, rebuild=True)
        tracking_thread.start()
    ##### Object Tracking #####
    '''
    timer = cv2.getTickCount()
    # Update tracker
    ok, bbox = tracker.update(frame)

    # Calculate Frames per second (FPS)
    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)

    # Draw bounding box
    if ok:
        # Tracking success
        p1 = (int(bbox[0]), int(bbox[1]))
        p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
        center = (int(bbox[0] + bbox[2] / 2), int(bbox[1] + bbox[3] / 2))
        cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
        pts.appendleft(center)
        for i in range(1, len(pts)):

            # if either of the tracked points are None, ignore
            # them
            if pts[i - 1] is None or pts[i] is None:
                continue

            # otherwise, compute the thickness of the line and
            # draw the connecting lines
            thickness = int(np.sqrt(buffer / float(i + 1)) * 2.5)
            cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
    else:
        # Tracking failure
        cv2.putText(frame, "Tracking failure detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)

    # Display tracker type on frame
    cv2.putText(frame, tracker_type + " Tracker", (100, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2);

    # Display FPS on frame
    cv2.putText(frame, "FPS : " + str(int(fps)), (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);

    # Display result
    cv2.imshow("Tracking", frame)
    '''
    ##### Object Tracking #####
    time.sleep(0.03)
    '''
    frameWidth = frame.shape[1]
    frameHeight = frame.shape[0]
    # trackingBoxPoints = [frameWidth * 0.4, frameHeight * 0.4, frameWidth * 0.6, frameHeight * 0.8]
    trackingBoxPoints = {'x_left': frameWidth * 0.4,
                         'y_top': frameHeight * 0.4,
                         'x_right': frameWidth * 0.6,
                         'y_bottom': frameHeight * 0.8}
    hasDetect, skeletonPoint, x_intercept, y_intercept = user_detect.skeletonDetect(frame)
    if hasDetect:
        trackingBoxPoints['x_left'] = int(skeletonPoint['x_left'] - x_intercept * 0.25)
        trackingBoxPoints['x_right'] = int(skeletonPoint['x_right'] + x_intercept * 0.25)
        trackingBoxPoints['y_top'] = int(skeletonPoint['y_top'] - y_intercept * 0.4)
        trackingBoxPoints['y_bottom'] = int(skeletonPoint['y_bottom'] + y_intercept * 0.3)

        cv2.rectangle(frame,
                      (skeletonPoint['x_left'], skeletonPoint['y_top']),
                      (skeletonPoint['x_right'], skeletonPoint['y_bottom']),
                      (0, 0, 255), 2)
        if SkeletonCheck(frameWidth, frameHeight, skeletonPoint, x_intercept, y_intercept):
            cv2.rectangle(frame,
                          (trackingBoxPoints['x_left'], trackingBoxPoints['y_top']),
                          (trackingBoxPoints['x_right'], trackingBoxPoints['y_bottom']),
                          (0, 255, 0), 2)
    cv2.imshow('Output Tracking Box', frame)

    # cv2.waitKey(0)

    vid_writer.write(frame)
    '''

# vid_writer.release()
