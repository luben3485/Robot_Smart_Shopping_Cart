import cv2
import sys
import time
import socket
import pickle
import struct
import threading
from collections import deque


class serverListenThread (threading.Thread):
    def __init__(self, name, ip, port):
        threading.Thread.__init__(self)
        self.name = name
        self.ip = ip
        self.port = port
        self.listen_socket = creat_TCP_socket(self.ip, self.port)
        self.recv_data = b""
        print("Seccessfully creat %s listening thread." % self.name)
        self.instruction = deque(maxlen=3)

    def run(self):
        print("開始線程：" + self.name)
        while True:
            # print("Receiving data...")
            data = self.listen_socket.recv(1024)
            # print("data size: %d", len(data))
            print("listen get data", data)
            self.recv_data += data
            if not data or len(data) < 1024:
                print("Update instruction from server %s:%d" % (self.ip, self.port))
                self.instruction.append(self.recv_data)
                break
            time.sleep(0.01)
        print("退出線程：" + self.name)


class serverSendThread (threading.Thread):
    def __init__(self, name, ip, port):
        threading.Thread.__init__(self)
        self.name = name
        self.ip = ip
        self.port = port
        self.send_socket = creat_TCP_socket(self.ip, self.port)
        print("Seccessfully creat %s sending thread." % self.name)
        self.frame_queue = deque(maxlen=10)

    def run(self):
        print("開始線程：" + self.name)
        while True:
            if len(self.frame_queue) > 0:
                self.sendImg(self.frame_queue.pop())
            else:
                pass
            time.sleep(0.01)
        print("退出線程：" + self.name)

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
        print(len(t_data))
        start = time.time()
        self.send_socket.sendall(struct.pack("L", len(t_data)) + t_data)  # new
        print(time.time() - start)
        print("Successfully send frame")


class client():
    def __init__(self, name, ip_listen, port_listen, ip_send, port_send):
        self.name = name
        self.listen_thread = serverListenThread(name + "_listen", ip_listen, port_listen)
        self.send_thread = serverSendThread(name + "_send", ip_send, port_send)
        self.listen_thread.start()
        self.send_thread.start()

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
    return socket_tcp


if __name__ == '__main__':
    print(1)
    # cart_client = client("Cart 1", "127.0.0.1", 8889, "127.0.0.1", 8899)
    cart_client = client("Cart 1", "140.116.102.99", 8889, "140.116.102.99", 8899)
    origin_img = "test.jpg"
    img = cv2.imread(origin_img)
    cart_client.send_frame(img)
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
    mess = cart_client.get_instruction()
    print("get mess", mess)
