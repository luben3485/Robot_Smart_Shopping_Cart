import cv2
import time
import threading
import numpy as np

MODE = "COCO"

if MODE is "COCO":
    protoFile = "pose/coco/pose_deploy_linevec.prototxt"
    weightsFile = "pose/coco/pose_iter_440000.caffemodel"
    nPoints = 18
    POSE_PAIRS = [ [1,0],[1,2],[1,5],[2,3],[3,4],[5,6],[6,7],[1,8],[8,9],[9,10],[1,11],[11,12],[12,13],[0,14],[0,15],[14,16],[15,17]]

elif MODE is "MPI":
    protoFile = "pose/mpi/pose_deploy_linevec_faster_4_stages.prototxt"
    weightsFile = "pose/mpi/pose_iter_160000.caffemodel"
    nPoints = 15
    POSE_PAIRS = [[0,1], [1,2], [2,3], [3,4], [1,5], [5,6], [6,7], [1,14], [14,8], [8,9], [9,10], [14,11], [11,12], [12,13] ]


def skeletonDetect(frame):
    # frame = cv2.imread("single.jpeg")
    hasDetect = True
    frameCopy = np.copy(frame)
    frameWidth = frame.shape[1]
    frameHeight = frame.shape[0]
    threshold = 0.1

    net = cv2.dnn.readNetFromCaffe(protoFile, weightsFile)

    t = time.time()
    # input image dimensions for the network
    # inWidth = 368
    # inHeight = 368
    inWidth = 184
    inHeight = 184
    inpBlob = cv2.dnn.blobFromImage(frame, 1.0 / 255, (inWidth, inHeight),
                                    (0, 0, 0), swapRB=False, crop=False)

    net.setInput(inpBlob)

    output = net.forward()
    print("time taken by network : {:.3f}".format(time.time() - t))

    H = output.shape[2]
    W = output.shape[3]

    # Empty list to store the detected keypoints
    points = []

    for i in range(nPoints):
        # confidence map of corresponding body's part.
        probMap = output[0, i, :, :]

        # Find global maxima of the probMap.
        minVal, prob, minLoc, point = cv2.minMaxLoc(probMap)

        # Scale the point to fit on the original image
        x = (frameWidth * point[0]) / W
        y = (frameHeight * point[1]) / H

        if prob > threshold:
            cv2.circle(frameCopy, (int(x), int(y)), 8, (0, 255, 255), thickness=-1, lineType=cv2.FILLED)
            cv2.putText(frameCopy, "{}".format(i), (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, lineType=cv2.LINE_AA)

            # Add the point to the list if the probability is greater than the threshold
            points.append((int(x), int(y)))
        else :
            points.append(None)

    # Draw Skeleton
    for pair in POSE_PAIRS:
        partA = pair[0]
        partB = pair[1]

        if points[partA] and points[partB]:
            cv2.line(frame, points[partA], points[partB], (0, 255, 255), 2)
            cv2.circle(frame, points[partA], 8, (0, 0, 255), thickness=-1, lineType=cv2.FILLED)

    # cv2.imshow('Output-Keypoints', frameCopy)
    # cv2.imshow('Output-Skeleton', frame)

    # Cut lower-body
    lowerBodyPoint = points[9:11] + points[12:14]
    try:
        rect_lt = (min([pt[0] for pt in lowerBodyPoint if pt is not None]), min([pt[1] for pt in lowerBodyPoint if pt is not None]))
        rect_rb = (max([pt[0] for pt in lowerBodyPoint if pt is not None]), max([pt[1] for pt in lowerBodyPoint if pt is not None]))
    except ValueError:
        print("Can't detect any body point")
        hasDetect = False
        rect_lt = (None, None)
        rect_rb = (None, None)
        print("Total time taken : {:.3f}".format(time.time() - t))
        return hasDetect, None, None, None
    # cv2.rectangle(frameCopy, rect_lt, rect_rb, (0, 0, 255), 2)

    # cv2.imwrite('Output-Keypoints.jpg', frameCopy)
    # cv2.imwrite('Output-Skeleton.jpg', frame)

    print("Total time taken : {:.3f}".format(time.time() - t))
    # cv2.waitKey(0)
    skeletonBox = {'x_left': rect_lt[0],
                   'y_top': rect_lt[1],
                   'x_right': rect_rb[0],
                   'y_bottom': rect_rb[1]}
    return hasDetect, skeletonBox, rect_rb[0] - rect_lt[0], rect_rb[1] - rect_lt[1]


if __name__ == '__main__':
    ##### threading test #####
    #
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
        def run(self):
            print ("開始線程：" + self.name)
            self.hasDetect, self.skeletonPoint, self.x_intercept, self.y_intercept = skeletonDetect(self.frame)
            self.detect_finish = True
            print ("退出線程：" + self.name)

    input_source = "video-7.mp4"
    cap = cv2.VideoCapture(input_source)
    hasFrame, frame = cap.read()
    skeleton_thread = skeletonThread(frame, 'Skeleton Thread 1')
    skeleton_thread.start()
    t_start = time.time()
    i = 0
    result_writer = cv2.VideoWriter('skeleton-detect-demo.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 30, (frame.shape[1], frame.shape[0]))
    tmp_frame = None
    while cv2.waitKey(30) < 0:
        hasFrame, frame = cap.read()
        if not hasFrame:
            # cv2.waitKey()
            print('no frame')
            break
        if skeleton_thread.detect_finish:
            skeleton_thread.join()
            print('finish detect')
            cv2.imshow('Normal Video', skeleton_thread.frame)
            tmp_frame = skeleton_thread.frame
            result_writer.write(skeleton_thread.frame)
            skeleton_thread = skeletonThread(frame, 'Skeleton Thread 1')
            skeleton_thread.start()
        else:
            result_writer.write(tmp_frame)
        i += 1
        # hasDetect, skeletonPoint, x_intercept, y_intercept = skeletonDetect(frame)
        time.sleep(0.03)
    print(time.time() - t_start)
    print(i)
    result_writer.release()
    cv2.waitKey(0)

    ###### threading test #####
