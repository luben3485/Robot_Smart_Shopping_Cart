import sys
import select
from time import sleep
import termios
import tty
import serial
import determineDistance
import bubbleRebound

ser = serial.Serial('/dev/ttyACM0' , 9600)
old_settings = termios.tcgetattr(sys.stdin)
tty.setcbreak(sys.stdin.fileno())
if(ser.isOpen()):
    print("connent\n")
    file = open("result.txt",'w')
    file.truncate()
    line = ""
    s = ""
    while True:
        sleep(.001)
        if select.select([sys.stdin],[],[],0) == ([sys.stdin], [], []):
            c = sys.stdin.read(1)
            if c == '\x1b':
                ser.write('0'.encode())
                ser.write('\n'.encode())
                ser.close()
                file.close()
                if(~ser.isOpen()):
                    print("closed\n")
                break
			'''	
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
            for i in range(len(determineDistance.distance)):
                print("before sensor %d %f" % (i,determineDistance.distance[i]))	
	
            if bubbleRebound.checkObstacles(determineDistance.distance):
                turnAngle = bubbleRebound.calculateAngle(determineDistance.distance)
                print("turnAngle:%f" % turnAngle)
				line = "0 "+ str(turnAngle)
                ser.write(line.encode())
                ser.write('\n'.encode())

            else:
                print("turnAngle:(safe)")
				line = "0.3 0.3"
                ser.write(line.encode())
                ser.write('\n'.encode())


            sleep(0.1)
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

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
