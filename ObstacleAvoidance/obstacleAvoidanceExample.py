import time
import determineDistance
import bubbleRebound
import kalman
while True:
	determineDistance.get_distance()
	for i in range(len(determineDistance.distance)):
		print("cm=%f" % determineDistance.distance[i])
	
	distanceKalman = kalman.kalmanFilter(determineDistance.distance)
	print(distanceKalman[0])
	print(distanceKalman[1])
	if bubbleRebound.checkObstacles(distanceKalman):
		turnAngle = bubbleRebound.calculateAngle(distaceKalman)
		print("turnAngle:%f" % turnAngle)
	else:
		print("turnAngle:(safe)")
	time.sleep(1)                   
