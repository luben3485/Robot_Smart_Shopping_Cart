import time
import determineDistance
import bubbleRebound
#import kalman
while True:
    determineDistance.get_distance()

#	distanceKalman = kalman.kalmanFilter(determineDistance.distance)
	
    for i in range(len(determineDistance.distance)):
        print("before sensor %d %f" % (i,determineDistance.distance[i]))	
	
#	for i in range(len(distanceKalman)):
#		print("after sensor %d %f" % (i,distanceKalman[i]))	
#	if bubbleRebound.checkObstacles(distanceKalman):
#		turnAngle = bubbleRebound.calculateAngle(distanceKalman)
    if bubbleRebound.checkObstacles(determineDistance.distance):
        turnAngle = bubbleRebound.calculateAngle(determineDistance.distance)
        print("turnAngle:%f" % turnAngle)
    else:
        print("turnAngle:(safe)")
    time.sleep(1)                   
