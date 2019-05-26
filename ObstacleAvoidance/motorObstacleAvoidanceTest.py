import sys
import select
from time import sleep
import termios
import tty
import serial
import determineDistance
import bubbleRebound
import kalman
ser = serial.Serial('/dev/ttyACM0' , 9600)
old_settings = termios.tcgetattr(sys.stdin)
tty.setcbreak(sys.stdin.fileno())
if(ser.isOpen()):
    print("connent\n")
    file = open("result.txt",'w')
    file.truncate()
    line = ""
    s = ""
    pre = [0]*6
    ini = 0
    while True:
        sleep(.001)
        try:
        #if select.select([sys.stdin],[],[],0) == ([sys.stdin], [], []):
            '''
            c = sys.stdin.read(1)
            if c == '\x1b':
                ser.write('0'.encode())
                ser.write('\n'.encode())
                ser.close()
                file.close()
                if(~ser.isOpen()):
                    print("closed\n")
                break
            	
            if c != '\n' :
                line += c
                sys.stdout.write(c)
                sys.stdout.flush()
            else:
                sys.stdout.write('\n')
                sys.stdout.write(line + '\n')
                sys.stdout.flush()
            '''
            
            determineDistance.get_distance()
            distanceKalman = kalman.kalmanFilter(determineDistance.distance)
            
            #distanceKalman = determineDistance.distance
            
            if(ini ==0):
                pre = determineDistance.distance
                ini +=1
            else:
                for i in range(len(distanceKalman)):
                    if abs(pre[i]-determineDistance.distance[i]) >=70:
                        distanceKalman[i] = pre[i] 
                    pre[i] = distanceKalman[i]
            
            for i in range(len(distanceKalman)):
                print("after sensor %d %f" % (i,distanceKalman[i]))	
            if bubbleRebound.checkObstacles(distanceKalman):
                turnAngle = bubbleRebound.calculateAngle(distanceKalman)
                print("turnAngle:%f" % turnAngle)
                line = "0 "+ str(turnAngle)
                ser.write(line.encode())
                ser.write('\n'.encode())

            else:
                print("turnAngle:(safe)")
                line = "0.4 0"
                ser.write(line.encode())
                ser.write('\n'.encode())


            sleep(0.05)
            line = ""
            if ser.in_waiting:
                #print("received")
                cin = ser.read(1)
                if cin != b'\n':
                    cin = cin.decode(encoding='utf-8' , errors='ignore')
                    s += cin
                else:
                    print("received:" + s)
                    file.write(s + '\n')
                    s = ""
        except KeyboardInterrupt:

            ser.write('0'.encode())
            ser.write('\n'.encode())
            ser.close()
            file.close()
            if(~ser.isOpen()):
                print("closed\n")
            break
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
