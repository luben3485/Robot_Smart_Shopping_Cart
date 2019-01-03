import cv2
import sys
import time
import socket
import threading
from collections import deque
import pickle
import struct

import user_tracking

log_file = open("server_thread.log", 'w', encoding='utf-8')
class clientListenThread (threading.Thread):
    def __init__(self, name, ip, port, instruction, frame_queue):
        threading.Thread.__init__(self)
        self.name = name
        self.id = '[' + self.name + ']'
        self.ip = ip
        self.port = port
        self.listen_socket = creat_host_TCP_socket(self.ip, self.port)
        self.print_msg("Seccessfully creat %s listening thread." % self.name)
        self.instruction = instruction
        self.frame_queue = frame_queue
        self.print_msg("client Listen get id ", id(instruction))
        self.print_msg("client Listen id ", id(self.instruction))

    def run(self):
        self.print_msg("開始線程：" + self.name)
        self.listen_socket.listen(1)
        self.client_socket, (self.client_ip, self.client_port) = self.listen_socket.accept()
        self.print_msg("Connection accepted from %s:%d" % (self.client_ip, self.client_port))
        # self.instruction[0] = (b"TTTTTTTTTTest inst")  # TEST
        payload_size = struct.calcsize("L")
        data = self.client_socket.recv(1024)
        self.print_msg("Server received:", data)
        self.client_socket.send(b"Welcome to Cloud Computing Server.")
        data = b""
        c = 0
        while True:
            start = time.time()
            # self.print_msg("Start receive image!")
            while len(data) < payload_size:
                data += self.client_socket.recv(4096)
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("L", packed_msg_size)[0]
            while len(data) < msg_size:
                data += self.client_socket.recv(1048576)
            frame_data = data[:msg_size]
            data = data[msg_size:]

            frame = pickle.loads(frame_data)
            # self.print_msg("Successfully get image :", frame.shape)
            self.frame_queue.append(frame)
            c += 1
            end = time.time()
            self.print_msg("frame:", c)
            # self.print_msg('spend time:', end - start)
        self.print_msg("退出線程：" + self.name)

    def print_msg(self, *args):
        print(self.id, " ".join(map(str, args)))
        log_file.write(self.id + ' ' + " ".join(map(str, args)) + '\n')


class clientSendThread (threading.Thread):
    def __init__(self, name, ip, port, instruction):
        threading.Thread.__init__(self)
        self.name = name
        self.id = '[' + self.name + ']'
        self.ip = ip
        self.port = port
        self.send_socket = creat_host_TCP_socket(self.ip, self.port)
        self.print_msg("Seccessfully creat %s listening thread." % self.name)
        self.instruction = instruction
        self.print_msg("client send get id ", id(instruction))
        self.print_msg("client send id ", id(self.instruction))

    def run(self):
        self.send_socket.listen(1)
        self.client_socket, (self.client_ip, self.client_port) = self.send_socket.accept()
        self.print_msg("Connection accepted from %s:%d" % (self.client_ip, self.client_port))
        self.print_msg("開始線程：" + self.name)
        data = self.client_socket.recv(1024)
        self.print_msg("Server received:", data)
        self.client_socket.send(b"Welcome to Cloud Computing Server.")
        while True:
            if self.instruction[0] is not None:
                start = time.time()
                self.client_socket.send(self.instruction[0])
                self.print_msg("Server send instruction", self.instruction[0], "spend time:", time.time() - start)
                self.instruction.clear()
            else:
                pass
            time.sleep(0.01)
        self.print_msg("退出線程：" + self.name)

    def print_msg(self, *args):
        print(self.id, " ".join(map(str, args)))
        log_file.write(self.id + ' ' + " ".join(map(str, args)) + '\n')


class host():
    def __init__(self, name, ip_listen, port_listen, ip_send, port_send):
        self.name = name
        self.show_frame = {'origin': None,
                           'skeleton': None,
                           'tracking': None}
        self.instruction = [None]
        print("HOST id ", id(self.instruction))
        self.frame_queue = deque(maxlen=10)
        self.listen_thread = clientListenThread(name + "_listen", ip_listen, port_listen, self.instruction, self.frame_queue)
        self.send_thread = clientSendThread(name + "_send", ip_send, port_send, self.instruction)
        self.decision_thread = user_tracking.decisionThread(name + "_decision", 2, self.instruction, self.frame_queue, self.show_frame)
        self.listen_thread.start()
        self.send_thread.start()
        self.decision_thread.start()

    def send_instruction(self, instruction):
        self.instruction[0] = instruction

    def get_frame(self):
        if self.frame_queue:
            return self.frame_queue[-1]
        else:
            return None


def creat_host_TCP_socket(ip, port):
    HOST_IP = ip
    HOST_PORT = port
    print("IP:", HOST_IP)
    print("Port:", HOST_PORT)
    print("Create socket:")
    socket_tcp = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM, proto=0, fileno=None)
    socket_tcp.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    host_addr = (HOST_IP, HOST_PORT)
    socket_tcp.bind(host_addr)
    return socket_tcp


if __name__ == '__main__':
    print(1)
    # cart_server = host("Host", "127.0.0.1", 8899, "127.0.0.1", 8889)
    cart_server = host("Host", "127.0.0.1", 8899, "127.0.0.1", 8889)
    time.sleep(2)
    cart_server.instruction[0] = (b"TTTTest inst")
    print(id(cart_server.frame_queue))
    print(id(cart_server.listen_thread.frame_queue))
    print(id(cart_server.decision_thread.frame_queue))

    input_source = "video-1.mp4"
    cap = cv2.VideoCapture(input_source)
    hasFrame, frame = cap.read()
    cv2.namedWindow("Origin", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Origin", (int(frame.shape[1] / 2), int(frame.shape[0] / 2)))
    cv2.namedWindow("Skeleton", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Skeleton", (int(frame.shape[1] / 2), int(frame.shape[0] / 2)))
    cv2.namedWindow("Tracking", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Tracking", (int(frame.shape[1] / 2), int(frame.shape[0] / 2)))
    while cart_server.show_frame['origin'] is None:
        time.sleep(0.1)
    print('ID:', id(cart_server.show_frame))
    while cv2.waitKey(30) < 0:
        cv2.imshow("Origin", cart_server.show_frame['origin'])
        cv2.imshow('Skeleton', cart_server.show_frame['skeleton'])
        cv2.imshow("Tracking", cart_server.show_frame['tracking'])
