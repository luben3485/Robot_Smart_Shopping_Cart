#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
import socket
import threading
import queue
from collections import deque

class DecisionMaker(threading.Thread):
    def __init__(self, name, ip, port):
        threading.Thread.__init__(self)
        self.id = '[' + name + ']'
        self.ip = ip
        self.port = port # dict type
        self.follow_lock = threading.Lock() # Synchronize
        self.avoid_lock = threading.Lock() # Synchronize
        self.motor_lock = threading.Lock() # Synchronize
        self.follow_instruction = deque(maxlen = 15)
        self.avoid_instruction = deque(maxlen = 15)
        self.motor_instruction = deque(maxlen = 15)
        self.follow_socket = self.creat_TCP_socket(self.ip, self.port['follow'])
        self.avoid_socket = self.creat_TCP_socket(self.ip, self.port['avoid'])
        self.motor_socket = self.creat_TCP_socket(self.ip, self.port['motor'])
    
    def run(self):
        follow_socket_thread = FollowSocketThread("FST", self.follow_socket, self.follow_instruction, self.follow_lock)
        avoid_socket_thread = AvoidSocketThread("AST", self.avoid_socket, self.avoid_instruction, self.avoid_lock)
        motor_socket_thread = MotorSocketThread("MST", self.motor_socket, self.motor_instruction, self.motor_lock)
        self.print_msg("Checking follow connection...")
        follow_socket_thread.start()
        self.print_msg("Follow connection is OK!")
        self.print_msg("Checking avoid connection...")
        avoid_socket_thread.start()
        self.print_msg("Avoid connection is OK!")
        self.print_msg("Checking motor connection...")
        motor_socket_thread.start()
        self.print_msg("Motor connection is OK!")
        while(True):
            data = None
            self.follow_lock.acquire()
            if len(self.follow_instruction) > 0 and self.follow_instruction[0] is not None:
                data = self.follow_instruction[0]
                self.follow_instruction.clear()
            self.follow_lock.release()
            self.avoid_lock.acquire()
            if len(self.avoid_instruction) > 0 and self.avoid_instruction[0] is not None:
                data = self.avoid_instruction[0]
                self.avoid_instruction.clear()
            self.avoid_lock.release()
            if data is not None:
                self.motor_lock.acquire()
                self.motor_instruction.appendleft(data)
                self.motor_lock.release()

        pass
    
    def creat_TCP_socket(self, ip, port):
        HOST_IP = self.ip
        HOST_PORT = self.port
        self.print_msg("IP:", HOST_IP)
        self.print_msg("Port:", HOST_PORT)
        self.print_msg("Create socket:")
        socket_tcp = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM, proto=0, fileno=None)
        socket_tcp.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        socket_tcp.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1024*200)
        host_addr = (HOST_IP, HOST_PORT)
        socket_tcp.bind(host_addr)
        return socket_tcp
        # remember socket.listen(1) and socket.accept()

    def print_msg(self, *args):
        print(self.id, " ".join(map(str, args)))

class FollowSocketThread(threading.Thread):
    def __init__(self, name, follow_socket, follow_instruction, lock):
        threading.Thread.__init__(self)
        self.id = '[' + name + ']'
        self.server_socket = follow_socket
        self.instruction = follow_instruction
        self.lock = lock
    def run(self):
        self.server_socket.listen(1)
        self.client_socket, (self.client_ip, self.client_port) = self.server_socket.accept() 
        self.print_msg("Follow Socket Thread Start!")
        while True:
            data = self.client_socket.recv(1024).decode('utf-8')
            self.lock.acquire() # Synchronize
            self.instruction.appendleft(data)
            self.print_msg("Recv instruction from follow")
            self.lock.release() # Synchronize
        self.client_socket.close()
    def print_msg(self, *args):
        print(self.id, " ".join(map(str, args)))

class AvoidSocketThread(threading.Thread):
    def __init__(self, name, avoid_socket, avoid_instruction, lock):
        threading.Thread.__init__(self)
        self.id = '[' + name + ']'
        self.server_socket = avoid_socket
        self.instruction = avoid_instruction
        self.lock = lock
    def run(self):
        self.server_socket.listen(1)
        self.client_socket, (self.client_ip, self.client_port) = self.server_socket.accept() 
        self.print_msg("Avoid Socket Thread Start!")
        while True:
            data = self.client_socket.recv(1024).decode('utf-8')
            self.lock.acquire() # Synchronize
            self.instruction.appendleft(data)
            self.print_msg("Recv instruction from avoid")
            self.lock.release() # Synchronize
        self.client_socket.close()
    def print_msg(self, *args):
        print(self.id, " ".join(map(str, args)))

class MotorSocketThread(threading.Thread):
    def __init__(self, name, motor_socket, motor_instruction, lock):
        threading.Thread.__init__(self)
        self.id = '[' + name + ']'
        self.server_socket = motor_socket
        self.instruction = motor_instruction
        self.lock = lock
    def run(self):
        self.server_socket.listen(1)
        self.client_socket, (self.client_ip, self.client_port) = self.server_socket.accept() 
        self.print_msg("Motor Socket Thread Start!")
        while True:
            if len(self.instruction) > 0 and self.instruction[0] is not None:
                self.lock.acquire() # Synchronize
                data = self.instruction[0]
                self.instruction.clear()
                self.client_socket.send(bytes(data.encode('utf-8')))
                self.print_msg("Send instruction to motor")
                self.lock.release() # Synchronize
    def print_msg(self, *args):
        print(self.id, " ".join(map(str, args)))
