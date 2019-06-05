bubbleBoundary = [30, 30, 80, 80, 30, 30]
def checkObstacles(distance):
	
	for i in range(6):
		if distance[i] <= bubbleBoundary[i]:
			#print("Obstacle detected!!")
			return True
	#print("It's safe!!")
	return False

def calculateAngle(distance):
	angle = [-90, -60, -30, 30, 60, 90] #left to right
	
	sum1 = 0
	sum2 = 0

	for i in range(6):
		if distance[i] >= 70:
			distance[i] = bubbleBoundary[i]
		sum1 = sum1 + angle[i]*distance[i]
		sum2 = sum2 + distance[i]

	turn = sum1/sum2

	return turn