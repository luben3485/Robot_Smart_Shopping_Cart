import bubble
import random
import time

distance = [0]*6
while 1:
	for i in range(6):
		distance[i] = random.randint(60, 100)
	if bubble.checkObstacles(distance):
		result = bubble.calculateAngle(distance)
		print(result)
	time.sleep(1)
