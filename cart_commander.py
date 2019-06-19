#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import tty
import time
from collections import deque
import serial
import termios
from argparse import ArgumentParser
from UserTracking import follow
from ObstacleAvoidance import utils as avoid

class Commander(object):
    def __init__(self, name, display, log):
        self.id = '[' + name + ']'
        self.display = display
        self.log = log
    
    def start(self):
        self.ser = serial.Serial('/dev/ttyACM0' , 9600)
        self.old_settings = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin.fileno())
        follow_instruction = deque(maxlen = 5)
        self.follow_thread = follow.Follow(args.name + '_follow', follow_instruction, 0, self.display, self.log)
        self.follow_thread.start()
        avoid.obstacleAvoidance(init=True)
        final_instruction = []
        self.print_msg('Start!!!')
        t1 = time.time()
        avoidance = 0
        while True:
            try:
                if len(follow_instruction) > 0:
                    final_instruction.append(follow_instruction[0])
                    follow_instruction.clear()
                                
                #avoidance = avoid.obstacleAvoidance()
                if avoidance != 0:
                    final_instruction.clear()
                    final_instruction.append([0, avoidance])
                    self.print_msg('Avoidance:', 'turn left' if avoidance > 0 else 'turn right')
                
                if len(final_instruction) > 0:
                    self.motor_control(final_instruction[-1])
                    final_instruction.clear()
                time.sleep(0.05)

            except KeyboardInterrupt:
                self.ser.write('0'.encode())
                self.ser.write('\n'.encode())
                self.ser.close()
                # file.close()
                if(~self.ser.isOpen()):
                    self.print_msg("Serial is closed\n")
                self.follow_thread.join()
                break
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)
    
    def motor_control(self, instruction):
        try:
            # combine motor instruction
            s = ''
            line = str(instruction[0]) + ' ' + str(instruction[1])
            self.ser.write(line.encode())
            self.ser.write('\n'.encode())
            self.print_msg('Instruction send to motor:', line)

            time.sleep(0.02)
            line = ""
            if self.ser.in_waiting:
                cin = self.ser.read(1)
                if cin != b'\n':
                    cin = cin.decode(encoding='utf-8' , errors='ignore')
                    s += cin
                else:
                    self.print_msg("Serial is received:" + s)
                    # file.write(s + '\n')
                    s = ""
        except KeyboardInterrupt:
            self.ser.write('0'.encode())
            self.ser.write('\n'.encode())
            self.ser.close()
            # file.close()
            if(~self.ser.isOpen()):
                self.print_msg("Serial is closed\n")
            self.follow_thread.join()
    
    def print_msg(self, *args):
        print(self.id, " ".join(map(str, args)))


if __name__ == "__main__":
    parser = ArgumentParser(description='Manage Follow & Avoidence')
    parser.add_argument("-l", "--log", dest="log", default=True)
    parser.add_argument("-n", "--name", dest="name", default='Cart')
    parser.add_argument("-d", "--display", dest="display", default=True)
    args = parser.parse_args()
    commander = Commander(name=args.name, display=args.display, log=args.log)
    commander.start()
