import determineDistance
import bubbleRebound
import kalman
ini = 0
pre = [0]*6
def obstacleAvoidance():  
    determineDistance.get_distance()
    distanceKalman = kalman.kalmanFilter(determineDistance.distance)
    if(ini ==0):
        pre = determineDistance.distance
        ini +=1
    else:
        for i in range(len(distanceKalman)):
            if abs(pre[i]-determineDistance.distance[i]) >=70:
                distanceKalman[i] = pre[i] 
            pre[i] = distanceKalman[i]
            
    if bubbleRebound.checkObstacles(distanceKalman):
        turnAngle = bubbleRebound.calculateAngle(distanceKalman)
        return turnAngle
    else:
        return 0 
