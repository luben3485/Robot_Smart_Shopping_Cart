from . import determineDistance
from . import bubbleRebound
from . import kalman
ini = 0
pre = [0]*6
def obstacleAvoidance(init = False):  
    # pre=[0] * 6
    determineDistance.get_distance()
    distanceKalman = kalman.kalmanFilter(determineDistance.distance)
    '''
    if(init):
        pre = determineDistance.distance
    else:
        for i in range(len(distanceKalman)):
            if abs(pre[i]-determineDistance.distance[i]) >=70:
                distanceKalman[i] = pre[i] 
            pre[i] = distanceKalman[i]
    '''     
    
    
    if bubbleRebound.checkObstacles(distanceKalman):
        turnAngle = bubbleRebound.calculateAngle(distanceKalman)
        return turnAngle
    else:
        return 0 
