from . import determineDistance
from . import bubbleRebound
from . import kalman
ini = 0
pre = [0]*6
def obstacleAvoidance(init = False):  
    
    determineDistance.get_distance()
    distanceKalman = kalman.kalmanFilter(determineDistance.distance)
    
    if bubbleRebound.checkObstacles(distanceKalman):
        turnAngle = bubbleRebound.calculateAngle(distanceKalman)
        return turnAngle
    else:
        return 0 
