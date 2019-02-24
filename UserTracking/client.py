# coding=utf-8
import cv2
import sys
import time
import socket
import pickle
import struct
import threading
from collections import deque

import object_avoid


class serverListenThread (threading.Thread):
    def __init__(self, name, ip, port, from_sonic=False):
        threading.Thread.__init__(self)
        self.name = name
        self.id = '[' + self.name + ']'
        self.ip = ip
        self.port = port
        self.listen_socket = creat_TCP_socket(self.ip, self.port)
        self.recv_data = b""
        self.print_msg("Seccessfully creat %s listening thread." % self.name)
        self.instruction = deque(maxlen=3)
        self.from_sonic = from_sonic

    def run(self):
        self.print_msg("開始線程：" + self.name)
        while True:
            # print("Receiving data...")
            data = self.listen_socket.recv(1024)
            # print("data size: %d", len(data))
            # self.print_msg("listen get data", data)
            self.recv_data += data
            if len(self.recv_data) < 1024:
                # self.print_msg("Update instruction from server %s:%d" % (self.ip, self.port))
                #print(data)
                self.instruction.appendleft(self.recv_data)
                #print("--receive")
                self.recv_data = b''
            time.sleep(0.1)
        self.print_msg("退出線程：" + self.name)

    def get_instruction(self, from_sonic=False):
        if len(self.instruction) > 0:
            return self.instruction[0]
        else:
            return None

    def clean_instruction(self):
        self.instruction.clear()

    def print_msg(self, *args):
        print(self.id, " ".join(map(str, args)))


class serverSendThread (threading.Thread):
    def __init__(self, name, ip, port):
        threading.Thread.__init__(self)
        self.name = name
        self.id = '[' + self.name + ']'
        self.ip = ip
        self.port = port
        self.send_socket = creat_TCP_socket(self.ip, self.port)
        self.print_msg("Seccessfully creat %s sending thread." % self.name)
        self.frame_queue = deque(maxlen=10)

    def run(self):
        self.print_msg("開始線程：" + self.name)
        while True:
            if len(self.frame_queue) > 0:
                self.sendImg(self.frame_queue.pop())
            else:
                pass
            time.sleep(0.01)
        self.print_msg("退出線程：" + self.name)

    def sendImg(self, img):
        '''
        data = img.read(1024)
        while data:
            # print("Sending data...")
            self.send_socket.send(data)
            # print("data size: %d", len(data))
            data = img.read(1024)
        '''
        t_data = pickle.dumps(img)  # new
        self.print_msg(len(t_data))
        start = time.time()
        self.send_socket.sendall(struct.pack("I", len(t_data)) + t_data)  # new
        print("size:", len(t_data))
        self.print_msg(time.time() - start)
        self.print_msg("Successfully send frame" + str(time.time() - start))

    def print_msg(self, *args):
        print(self.id, " ".join(map(str, args)))


class client():
    def __init__(self, name, ip_listen, port_listen, ip_send, port_send):
        self.name = name
        self.listen_thread = serverListenThread(name + "_listen", ip_listen, port_listen)
        self.send_thread = serverSendThread(name + "_send", ip_send, port_send)
        pins = [[23, 24], [15, 16]]
        degrees = [-60, -45, -30, 30, 45, 60]
        self.avoid_thread = object_avoid.avoidThread('Sonic', pins, degrees)
        self.avoid_thread.start()
        self.sonic_thread = serverListenThread(name + "_listen", '127.0.0.1', 7788, from_sonic=True)
        self.listen_thread.start()
        self.send_thread.start()
        self.sonic_thread.start()

    def send_frame(self, img):
        self.send_thread.frame_queue.append(img)

    def get_instruction(self):
        if self.listen_thread.instruction:
            return self.listen_thread.instruction[-1]
        else:
            return None


def creat_TCP_socket(ip, port):
    SERVER_IP = ip
    SERVER_PORT = port
    print("IP:", SERVER_IP)
    print("Port:", SERVER_PORT)
    print("Create socket:")
    socket_tcp = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM, proto=0, fileno=None)
    socket_tcp.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    socket_tcp.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1024 * 1024)
    socket_tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_addr = (SERVER_IP, SERVER_PORT)
    while True:
        try:
            print("Conneting to server at %s:%s..." % server_addr)
            socket_tcp.connect(server_addr)
            print("connect")
            socket_tcp.send(b"Hello server")
            print("Successfully connect to server %s:%d" % (SERVER_IP, SERVER_PORT))
            data = socket_tcp.recv(1024)
            print("Server send:", data)
            break
        except Exception:
            print("Can't connect to server %s:%s, try it after %d second." % (SERVER_IP, SERVER_PORT, 1))
            time.sleep(0.5)
            continue
    return socket_tcp


def creat_motor_socket(ip, port):  # create socket
    SERVER_IP = ip
    SERVER_PORT = port
    print("IP:", SERVER_IP)
    print("Port:", SERVER_PORT)
    print("Create motor socket:")
    socket_tcp = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM, proto=0, fileno=None)
    print("motor tcp socket")
    socket_tcp.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    socket_tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("set socket")
    server_addr = (SERVER_IP, SERVER_PORT)
    while True:
        try:
            print("Conneting to server at %s:%s..." % server_addr)
            socket_tcp.connect(server_addr)
            print("connect")
            socket_tcp.send(b"Hello server")
            print("Successfully connect to server %s:%d" % (SERVER_IP, SERVER_PORT))
            data = socket_tcp.recv(1024)
            print("Server send:", data)
            break
        except Exception:
            print("Can't connect to server %s:%s, try it after %d second." % (SERVER_IP, SERVER_PORT, 1))
            time.sleep(1)
            continue
    print("get motor")
    return socket_tcp


if __name__ == '__main__':
    print(1)
    # cart_client = client("Cart 1", "127.0.0.1", 8889, "127.0.0.1", 8899)
    # cart_client = client("Cart 1", "140.116.102.106", 8889, "140.116.102.106", 8899)
    cart_client = client("Cart 1", "192.168.0.4", 8889, "192.168.0.4", 8899)
    # cart_client = client("Cart 1", "192.168.137.147", 8889, "192.168.137.147", 8899)
    motor_socket = creat_motor_socket("127.0.0.1", 7878)  # create socket: connect to 127.0.0.1 at port:7878
    input_source = "video.avi"
    # cap = cv2.VideoCapture(input_source)
    cap = cv2.VideoCapture(0)
    frame_count = 0
    hasFrame, frame = cap.read()
    if not hasFrame:
        print("Video can't open!!!")
    while True:
        hasFrame, frame = cap.read()
        if not hasFrame:
            break
        frame_count += 1
        cart_client.send_frame(frame)
        print("get instruction")
        final_instruction = None
        tracking_instruction = cart_client.listen_thread.get_instruction()
        # sonic_instruction = cart_client.sonic_thread.get_instruction()
        print("check instruction")
        if tracking_instruction:
            print("tracking instruction")
            cart_client.listen_thread.clean_instruction()
            final_instruction = tracking_instruction
        # if sonic_instruction:
            # print("sonic instruction")
            # cart_client.sonic_thread.clean_instruction()
            # final_instruction = sonic_instruction
        if final_instruction is None:
            print()
            print("None instruction")
            print()
            # motor_socket.send(b"4 0")
        else:
            msg = str(final_instruction[0])
            print()
            print("final instruction", msg)
            print()
            motor_socket.send(msg.encode())
        if frame_count > 150:
            break
        else:
           print(frame_count)
        print("finish 1 cycle")
        time.sleep(1)
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(length)
    # fps = cap.get(cv2.CAP_PROP_FPS)
    # print("Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps))

    #origin_img = "test.jpg"
    #img = cv2.imread(origin_img)
    #cart_client.send_frame(img)
    #cart_client.send_frame(img)
    #cart_client.send_frame(img)
    #cart_client.send_frame(img)
    # cart_client.send_frame(img)
    '''
    with open(origin_img, 'rb') as f:
        print("Send data from %s" % origin_img)
        data = f.read(1024)
        while data:
            # print("Sending data...")
            cart_client.send_frame(data)
            # print("data size: %d", len(data))
            data = f.read(1024)
        print("Successfully send %s" % origin_img)
    '''
    # mess = cart_client.get_instruction()
    # print("get mess", mess)
