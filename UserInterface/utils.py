import random

def getRandomXY(a,b,c,d):
	x = random.randint(a,b)
	y = random.randint(c,d) 

	return x,y

def trilateration(r1,r2,r3):
	'''
	set P1(0,0),P2(d,0),P3(i,j)
	'''
	d = 10
	i = 0
	j = 5
	x = (r1*r1 - r2*r2 + d*d)/(2*d)
	y = (r1*r1 -r3*r3-x*x +(x-i)*(x-i) +j*j)/(2*j)
	return x ,y

	
