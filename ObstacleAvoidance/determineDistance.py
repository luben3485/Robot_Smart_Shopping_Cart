import RPi.GPIO as GPIO
import time
#trigger_pin = 23
#echo_pin = 24
#trigger_pin = 14
#echo_pin = 15
trigger_pin = [23,10,16,17,25,2]
echo_pin = [24,9,20,27,8,3]
numOfSensor = 6
distance = [0]*numOfSensor
count = 1
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
for i in range(len(trigger_pin)):
	GPIO.setup(trigger_pin[i], GPIO.OUT)
for i in range(len(trigger_pin)):
	GPIO.setup(echo_pin[i], GPIO.IN)

def send_trigger_pulse(i):
	GPIO.output(trigger_pin[i], True)
	time.sleep(0.001)
	GPIO.output(trigger_pin[i], False)

def wait_for_echo(value, timeout,i):
	count = timeout
	while GPIO.input(echo_pin[i]) != value and count > 0:
		count = count - 1

def get_distance():
	for i in range(len(distance)):
		send_trigger_pulse(i)
		wait_for_echo(True, 5000,i)
		start = time.time()
		wait_for_echo(False, 5000,i)
		finish = time.time()
		pulse_len = finish - start
		distance[i] = pulse_len * 340 *100 /2
		time.sleep(0.1)

if __name__ == "__main__":
    while True:
	    get_distance()
	    print("count:%d" % count)
	    count+=1
	    for i in range(len(distance)):
		    print("cm=%f" % distance[i])
	    time.sleep(0.1)

