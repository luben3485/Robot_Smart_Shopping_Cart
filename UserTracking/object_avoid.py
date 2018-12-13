import numpy
import time
import math
import threading
import RPi.GPIO as GPIO


log_file = open("avoid.log", 'w', encoding='utf-8')


class Ultrasonic():
    def __init__(self, pins):
        # pins = [(trigger_pin, echo_pin), (trigger_pin, echo_pin)]
        self.pins = pins

    def send_tigger_pulse(trigger_pin):
        GPIO.output(trigger_pin, True)
        time.sleep(0.001)
        GPIO.output(trigger_pin, False)

    def wait_for_echo(echo_pin, value, timeout):
        count = timeout
        while GPIO.input(echo_pin) != value and count > 0:
            count -= 1

    def get_distance(self):
        distance = []
        for pair in self.pins:
            self.send_tigger_pulse(pair[0])
            self.wait_for_echo(pair[1], True, 5000)
            start = time.time()
            self.wait_for_echo(pair[1], False, 5000)
            finish = time.time()
            pulse_len = finish - start
            distance_cm = pulse_len * 340 * 100 / 2
            distance.append(distance_cm)
        return distance


class avoidThread(threading.Thread):
    """docstring for avoidThread
        sensor = [  0,   1,   2,  3,  4,  5]
        degree = [-60, -45, -30, 30, 45, 60]
    """
    def __init__(self, name, pins, degree):
        threading.Thread.__init__(self)
        self.name = name
        # self.pins = [(23, 24)]
        self.pins = pins
        self.degree = degree
        self.ultrasonic = Ultrasonic(pins)
        self.minDistance = 60
        self.dangerDistance = 30
        self.distance = None
        self.decision = None

    def run(self):
        self.print_msg("開始線程：" + self.name)
        while True:
            self.distance = self.ultrasonic.get_distance()
            self.decision = self.make_decision()
            time.sleep(0.1)
        self.print_msg("退出線程：" + self.name)

    def make_decision(self):
        hori_dist = []
        vert_dist = []
        for distance, degree in self.distance, self.degree:
            hori_dist.append(distance * math.sin(degree))  # use rad don't use deg
            vert_dist.append(distance * math.cos(degree))  # use rad don't use deg
        min_left = min(hori_dist[:len(hori_dist) / 2])
        min_right = min(hori_dist[len(hori_dist) / 2:])
        if min_left > 60 and min_right > 60:
            return 0  # keep straight
        elif min_left <= 60 and min_right > 60:
            return 1  # turn right
        elif min_left > 60 and min_right <= 60:
            return -1  # turn left
        elif min_left < 60 and min_right < 60:
            if min_left == min_right:
                return 0  # keep straight
            elif min_left < min_right:
                return 1  # turn right
            else:
                return -1  # turn left
        else:
            print("Something Error when make decision!")
            return None

    def print_msg(self, *args):
        print('[' + self.name + ']', " ".join(map(str, args)))
        log_file.write('[' + self.name + '] ' + " ".join(map(str, args)) + '\n')


if __name__ == "__main__":
    print()