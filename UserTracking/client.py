import sys
import time
import socket
import threading
from collections import deque


class serverListenThread (threading.Thread):
    def __init__(self, name, ip, port):
        threading.Thread.__init__(self)
        self.name = name
        self.ip = ip
        self.port = port
        self.listen_socket = creat_TCP_scoket(self.ip, self.port)
        self.recv_data = None
        print("Seccessfully creat %s listening thread." % self.name)
        self.instruction = deque(maxlen=3)

    def run(self):
        print("開始線程：" + self.name)
        while True:
            # print("Receiving data...")
            data = self.listen_socket.recv(1024)
            # print("data size: %d", len(data))
            self.recv_data += data
            if not data or len(data) < 1024:
                print("Update instruction from server %s:%d" % (self.ip, self.port))
                self.instruction.append(self.recv_data)
                break
        print("退出線程：" + self.name)


class serverSendThread (threading.Thread):
    def __init__(self, name, ip, port):
        threading.Thread.__init__(self)
        self.name = name
        self.ip = ip
        self.port = port
        self.send_socket = creat_TCP_scoket(self.ip, self.port)
        print("Seccessfully creat %s sending thread." % self.name)
        self.frame_queue = deque(maxlen=10)

    def run(self):
        print("開始線程：" + self.name)
        while True:
            if len(self.frame_queue) > 0:
                self.sendImg(self.frame_queue.pop())
            else:
                pass

        print("退出線程：" + self.name)

    def sendImg(self, img):
        data = img.read(1024)
        while data:
            # print("Sending data...")
            self.send_socket.send(data)
            # print("data size: %d", len(data))
            data = img.read(1024)
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


def creat_TCP_scoket(ip, port):
    SERVER_IP = ip
    SERVER_PORT = port
    print("IP:", SERVER_IP)
    print("Port:", SERVER_PORT)
    print("Create socket:")
    socket_tcp = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM, proto=0, fileno=None)
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


'''
origin_img = "test.jpg"
SERVER_IP = "127.0.0.1"
SERVER_PORT = 8889
print("IP:", SERVER_IP)
print("Port:", SERVER_PORT)
print("Starting socket:")

# creat socket object
socket_tcp = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM, proto=0, fileno=None)
server_addr = (SERVER_IP, SERVER_PORT)

start = time.time()
while True:
    try:
        print("Conneting to server at %s:%s..." % server_addr)
        socket_tcp.connect(server_addr)
        print("connect")
        socket_tcp.send(b"Hello server")
        print("Successfully connect to server.")
        data = socket_tcp.recv(1024)
        print("Server send:", data)
        break
    except Exception:
        print("Can't connect to server, try it after %d second." % 1)
        time.sleep(1)
        continue

with open(origin_img, 'rb') as f:
    print("Send data from %s" % origin_img)
    data = f.read(1024)
    while data:
        # print("Sending data...")
        socket_tcp.send(data)
        # print("data size: %d", len(data))
        data = f.read(1024)
    print("Successfully send %s" % origin_img)
    success_mess = "Successfully send " + origin_img
    data = socket_tcp.recv(1024)
    print("Server send:", data)
    socket_tcp.send(success_mess.encode())
end = time.time()
print(end - start)
'''
