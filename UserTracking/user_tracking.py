import os
import cv2
import sys
import time
import threading
import numpy as np
import argparse
from collections import deque

import user_detect

log_file = open("server.log", 'w', encoding='utf-8')
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
        def __init__(self, name, frame):
            threading.Thread.__init__(self)
            self.print_msg('start detect!')
            self.frame = frame
            self.origin_frame = frame
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
            self.print_msg("開始線程：" + self.name)
            start = time.time()
            self.hasDetect, self.skeletonPoint, self.x_intercept, self.y_intercept = user_detect.skeletonDetect(self.cacluate_frame)
            self.draw_box()
            self.detect_finish = True
            self.print_msg("spend time:", time.time() - start)
            self.print_msg("退出線程：" + self.name)

        def draw_box(self):
            frameWidth = self.frame.shape[1]
            frameHeight = self.frame.shape[0]
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

        def print_msg(self, *args):
            print('[' + self.name + ']', " ".join(map(str, args)))
            log_file.write('[' + self.name + '] ' + " ".join(map(str, args)) + '\n')


class trackingThread (threading.Thread):
        def __init__(self, name, frame, bbox, moving_path, tracker=None, rebuild=False, tracker_type_no=2):
            threading.Thread.__init__(self)
            self.print_msg('start tracking!')
            self.bbox = bbox  # (xmin,ymin,boxwidth,boxheight)
            self.tracker_type_no = tracker_type_no
            self.tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
            if rebuild:
                self.tracker = self.creatTracker()
                ok = self.tracker.init(frame, bbox)
            else:
                self.tracker = tracker
            # bbox = (287, 23, 86, 320)  # (xmin,ymin,boxwidth,boxheight)
            self.frame = frame
            self.name = name
            self.hasTracking = False
            self.tracking_finish = False
            self.buffer = 64
            self.pts = deque(maxlen=self.buffer)
            self.moving_path = moving_path

        def run(self):
            self.print_msg("開始線程：" + self.name)
            timer = cv2.getTickCount()
            # Update tracker
            ok, self.bbox = self.tracker.update(self.frame)

            # Calculate Frames per second (FPS)
            fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)

            # Draw bounding box
            if ok:
                # Tracking success
                self.hasTracking = True
                p1 = (int(self.bbox[0]), int(self.bbox[1]))
                p2 = (int(self.bbox[0] + self.bbox[2]), int(self.bbox[1] + self.bbox[3]))
                center = (int(self.bbox[0] + self.bbox[2] / 2), int(self.bbox[1] + self.bbox[3] / 2))
                cv2.rectangle(self.frame, p1, p2, (255, 0, 0), 2, 1)
                path_info = [self.bbox[2], self.bbox[3], self.bbox[2] * self.bbox[3], center]
                self.moving_path.appendleft(path_info)
                self.pts.appendleft(center)
                for i in range(1, len(self.pts)):

                    # if either of the tracked points are None, ignore
                    # them
                    if self.pts[i - 1] is None or self.pts[i] is None:
                        continue

                    # otherwise, compute the thickness of the line and
                    # draw the connecting lines
                    thickness = int(np.sqrt(buffer / float(i + 1)) * 2.5)
                    cv2.line(self.frame, self.pts[i - 1], self.pts[i], (0, 0, 255), thickness)
            else:
                # Tracking failure
                self.hasTracking = False
                self.print_msg("Tracking failed.")
                cv2.putText(self.frame, "Tracking failure detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)

            # Display tracker type on frame
            cv2.putText(self.frame, self.tracker_types[self.tracker_type_no] + " Tracker", (100, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2);

            # Display FPS on frame
            cv2.putText(self.frame, "FPS : " + str(int(fps)), (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2)

            self.tracking_finish = True
            self.print_msg("退出線程：" + self.name)

        def creatTracker(self):
            (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
            tracker_type = self.tracker_types[self.tracker_type_no]
            if int(minor_ver) < 3:
                tracker = cv2.Tracker_create(tracker_type)
            else:
                if tracker_type == 'BOOSTING':
                    tracker = cv2.TrackerBoosting_create()
                elif tracker_type == 'MIL':
                    tracker = cv2.TrackerMIL_create()
                elif tracker_type == 'KCF':
                    tracker = cv2.TrackerKCF_create()
                elif tracker_type == 'TLD':
                    tracker = cv2.TrackerTLD_create()
                elif tracker_type == 'MEDIANFLOW':
                    tracker = cv2.TrackerMedianFlow_create()
                elif tracker_type == 'GOTURN':
                    tracker = cv2.TrackerGOTURN_create()
                elif tracker_type == 'MOSSE':
                    tracker = cv2.TrackerMOSSE_create()
                elif tracker_type == "CSRT":
                    tracker = cv2.TrackerCSRT_create()
                else:
                    tracker = cv2.TrackerMIL_create()  # default MIL
            return tracker

        def print_msg(self, *args):
            print('[' + self.name + ']', " ".join(map(str, args)))
            log_file.write('[' + self.name + '] ' + " ".join(map(str, args)) + '\n')


class decisionThread (threading.Thread):
    def __init__(self, name, tracker_type_no, instruction, frame_queue, show_frame):
        threading.Thread.__init__(self)
        self.name = name
        self.id = '[' + self.name + ']'
        self.tracker = self.creatTracker(tracker_type_no)
        self.instruction = instruction
        self.frame_queue = frame_queue
        self.moving_path = deque(maxlen=10)
        self.print_msg(id(frame_queue))
        self.print_msg(id(self.frame_queue))
        self.show_frame = show_frame
        self.width = 0
        self.height = 0
        print('ID:', id(self.show_frame), id(show_frame))

    def run(self):
        self.print_msg("開始線程：" + self.name)
        init_frame = self.get_frame()
        self.width = init_frame.shape[1]
        self.height = init_frame.shape[0]
        self.origin_writer = cv2.VideoWriter('origin-output.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 30, (init_frame.shape[1], init_frame.shape[0]))
        self.skeleton_writer = cv2.VideoWriter('skeleton-output.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 30, (init_frame.shape[1], init_frame.shape[0]))
        self.tracking_writer = cv2.VideoWriter('tracking-output.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 30, (init_frame.shape[1], init_frame.shape[0]))
        self.skeleton_thread = skeletonThread('Skeleton Thread 1', init_frame)
        self.skeleton_thread.start()
        self.tracking_thread = trackingThread('Tracking Thread 1', init_frame, (0, 0, 0, 0), self.moving_path, rebuild=True)
        self.tracking_thread.start()
        pre_skeleton = []
        c = 0
        tracking_tmp = None
        skeleton_tmp = None
        while True:
            test_start = time.time()
            frame = self.get_frame()
            if frame is False:
                self.origin_writer.release()
                self.skeleton_writer.release()
                self.tracking_writer.release()
                self.print_msg("Release video writer. Close Thread")
                break
            self.origin_writer.write(frame)
            self.show_frame['origin'] = frame  ####
            stop1 = time.time()
            self.print_msg('stop1:', stop1 - test_start)
            if self.skeleton_thread.detect_finish:
                self.skeleton_thread.join()
                self.print_msg('Finish detect')
                if self.skeleton_thread.hasDetect:
                    self.skeleton_writer.write(self.skeleton_thread.frame)
                    self.show_frame['skeleton'] = self.skeleton_thread.frame  ####
                    skeleton_tmp = self.skeleton_thread.frame
                    tracking_box = (self.skeleton_thread.trackingBoxPoints['x_left'], self.skeleton_thread.trackingBoxPoints['y_top'],
                                    self.skeleton_thread.trackingBoxPoints['x_right'] - self.skeleton_thread.trackingBoxPoints['x_left'],
                                    self.skeleton_thread.trackingBoxPoints['y_bottom'] - self.skeleton_thread.trackingBoxPoints['y_top'])
                    pre_skeleton.append([self.skeleton_thread.origin_frame, tracking_box])
                self.skeleton_thread = skeletonThread('Skeleton Thread 1', frame)
                self.skeleton_thread.start()
            else:
                if skeleton_tmp is None:
                    self.skeleton_writer.write(frame)
                    self.show_frame['skeleton'] = frame  ####
                self.skeleton_writer.write(skeleton_tmp)
                self.show_frame['skeleton'] = self.skeleton_thread.frame  ####
            stop2 = time.time()
            self.print_msg('stop2:', stop2 - stop1)
            if self.tracking_thread.tracking_finish:
                self.tracking_thread.join()
                self.print_msg('tracking finish')
                self.tracking_writer.write(self.tracking_thread.frame)
                self.show_frame['tracking'] = self.tracking_thread.frame  ####
                tracking_tmp = self.tracking_thread.frame
                if self.tracking_thread.hasTracking:
                    self.tracking_thread = trackingThread('Tracking Thread 1', frame, self.tracking_thread.bbox, self.moving_path, self.tracking_thread.tracker, rebuild=True)
                    self.make_decision()
                elif len(pre_skeleton) > 0:
                    self.tracking_thread = trackingThread('Tracking Thread 1', pre_skeleton[-1][0], pre_skeleton[-1][1], self.moving_path, rebuild=True)
                    pre_skeleton.clear()
                else:
                    self.tracking_thread = trackingThread('Tracking Thread 1', frame, (0, 0, 0, 0), self.moving_path, rebuild=True)
                    self.print_msg("None tracking")
                self.tracking_thread.start()
            else:
                if tracking_tmp is None:
                    self.tracking_writer.write(frame)
                self.tracking_writer.write(tracking_tmp)
            # time.sleep(0.0333)
            c += 1
            stop3 = time.time()
            self.print_msg('stop3:', stop3 - stop2)
            self.print_msg('total:', time.time() - test_start)
        self.print_msg("退出線程：" + self.name)
        self.print_msg("Total frame:", c)

    def make_decision(self):
        if len(self.moving_path) > 3:
            box_area = 0
            value = 0
            for i in range(len(self.moving_path) - 1):
                box_area += self.moving_path[i+1][2] * (2 - 0.1 * i)
                value += (2 - 0.1 * i)
            box_area /= value
            if self.moving_path[0][2] > box_area * 1.1:
                self.instruction.append([2, 1])
            elif self.moving_path[0][2] < box_area * 0.9:
                self.instruction.append([1, 1])
            else:
                pass

            width_intercept = self.moving_path[0][0] - self.width/2
            height_intercept = self.moving_path[0][1] - self.height/2
            if abs(width_intercept) > self.width/2 * 0.15:
                if width_intercept > 0:
                    self.instruction.append([4, 1])
                else:
                    self.instruction.append([3, 1])
            ### still need improve
            if abs(width_intercept) > self.width/2 * 0.35 and abs(height_intercept) > self.height/2 * 0.35:
                self.moving_path.popleft()
                self.instruction = None
            if self.moving_path[0][3] > box_area * 1.5:
                self.moving_path.popleft()
                self.instruction = None
            if self.moving_path[0][3] < box_area * 0.5:
                self.moving_path.popleft()
                self.instruction = None
        else:
            self.instruction = None  # rewrite the instruction

    def get_frame(self):
        count = 0
        while not self.frame_queue:
            if count > 4000:
                self.print_msg("Wait over 10 sec. Will Close Thread!!!")
                return False
            if count % 200 == 0:
                self.print_msg("Can't get frame. Frame queue is Empty!")
            count += 1
            time.sleep(0.005)
            pass
        frame = self.frame_queue[-1]
        self.frame_queue.clear()
        return frame

    def creatTracker(self, tracker_type_no):
        (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
        tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
        tracker_type = tracker_types[tracker_type_no]
        if int(minor_ver) < 3:
            tracker = cv2.Tracker_create(tracker_type)
        else:
            if tracker_type == 'BOOSTING':
                tracker = cv2.TrackerBoosting_create()
            elif tracker_type == 'MIL':
                tracker = cv2.TrackerMIL_create()
            elif tracker_type == 'KCF':
                tracker = cv2.TrackerKCF_create()
            elif tracker_type == 'TLD':
                tracker = cv2.TrackerTLD_create()
            elif tracker_type == 'MEDIANFLOW':
                tracker = cv2.TrackerMedianFlow_create()
            elif tracker_type == 'GOTURN':
                tracker = cv2.TrackerGOTURN_create()
            elif tracker_type == 'MOSSE':
                tracker = cv2.TrackerMOSSE_create()
            elif tracker_type == "CSRT":
                tracker = cv2.TrackerCSRT_create()
            else:
                tracker = cv2.TrackerMIL_create()  # default MIL
        return tracker

    def print_msg(self, *args):
        print(self.id, " ".join(map(str, args)))
        log_file.write(self.id + ' ' + " ".join(map(str, args)) + '\n')


if __name__ == "__main__":

    input_source = "foot_test3.mp4"
    tracking_box = None
    cap = cv2.VideoCapture(input_source)
    hasFrame, frame = cap.read()
    if not hasFrame:
        print("Video can't open!!!")

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
    skeleton_thread = skeletonThread('Skeleton Thread 1', frame)
    skeleton_thread.start()
    tracking_thread = trackingThread('Tracking Thread 1', frame, (0, 0, 0, 0), rebuild=True)
    tracking_thread.start()
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
            cv2.imshow('Normal Video', skeleton_thread.frame)
            if skeleton_thread.hasDetect:
                tracking_box = (skeleton_thread.trackingBoxPoints['x_left'], skeleton_thread.trackingBoxPoints['y_top'],
                                skeleton_thread.trackingBoxPoints['x_right'] - skeleton_thread.trackingBoxPoints['x_left'],
                                skeleton_thread.trackingBoxPoints['y_bottom'] - skeleton_thread.trackingBoxPoints['y_top'])
                pre_skeleton.append([skeleton_thread.frame, tracking_box])
            skeleton_thread = skeletonThread('Skeleton Thread 1', frame)
            skeleton_thread.start()
        if tracking_thread.tracking_finish:
            tracking_thread.join()
            print('tracking finish')
            cv2.imshow("Tracking", tracking_thread.frame)
            if len(pre_skeleton) > 0:
                tracking_thread = trackingThread('Tracking Thread 1', pre_skeleton[-1][0], pre_skeleton[-1][1], rebuild=True)
                while len(pre_skeleton) <= 0:
                    pre_skeleton.pop()
            else:
                tracking_thread = trackingThread('Tracking Thread 1', frame, tracking_thread.bbox, tracking_thread.tracker, rebuild=True)
            tracking_thread.start()
        time.sleep(0.03)
