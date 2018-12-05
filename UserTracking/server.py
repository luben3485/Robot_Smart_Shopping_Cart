import sys
import time
import socket
import threading
from collections import deque


class clientListenThread (threading.Thread):
    def __init__(self, name, ip, port):
        threading.Thread.__init__(self)
        self.name = name
        self.ip = ip
        self.port = port
        self.listen_socket = creat_host_TCP_scoket(self.ip, self.port)
        print("Seccessfully creat %s listening thread." % self.name)
        self.listen_socket.listen(1)
        self.client_socket, (self.client_ip, self.client_port) = self.listen_socket.accept()
        print("Connection accepted from %s:%d" % (self.client_ip, self.client_port))
        self.frame_queue = deque(maxlen=10)

    def run(self):
        print("開始線程：" + self.name)
        origin_img = "origin_img.jpg"
        while True:
            start = time.time()
            data = self.client_socket.recv(1024)
            print("Server received:", data)
            self.client_socket.send(b"Welcome to Cloud Computing Server.")

            print("Start receive image!")
            with open(origin_img, 'wb') as f:
                print("Write data to %s" % origin_img)
                while True:
                    # print("Receiving data...")
                    data = self.client_socket.recv(1024)
                    # print("data size: %d", len(data))
                    if not data or len(data) < 1024:
                        break
                    f.write(data)
            print("Successfully get %s" % origin_img)
            success_mess = "Successfully get " + origin_img
            self.client_socket.send(success_mess.encode())
            data = self.client_socket.recv(1024)
            print("Server received:", data)
            end = time.time()
            print(end - start)
            break
        print("退出線程：" + self.name)


class clientSendThread (threading.Thread):
    def __init__(self, name, ip, port):
        threading.Thread.__init__(self)
        self.name = name
        self.ip = ip
        self.port = port
        self.send_socket = creat_host_TCP_scoket(self.ip, self.port)
        print("Seccessfully creat %s listening thread." % self.name)
        self.send_socket.listen(1)
        self.client_socket, (self.client_ip, self.client_port) = self.send_socket.accept()
        print("Connection accepted from %s:%d" % (self.client_ip, self.client_port))
        self.instruction = None

    def run(self):
        print("開始線程：" + self.name)
        while True:
            if self.instruction is not None:
                self.client_socket.send(self.instruction)
                self.instruction = None
            else:
                pass
        print("退出線程：" + self.name)


class host():
    def __init__(self, name, ip_listen, port_listen, ip_send, port_send):
        self.name = name
        self.listen_thread = clientListenThread(name + "_listen", ip_listen, port_listen)
        self.send_thread = clientSendThread(name + "_send", ip_send, port_send)
        self.listen_thread.start()
        self.send_thread.start()

    def send_instruction(self, instruction):
        self.send_thread.instruction = instruction

    def get_frame(self):
        if self.listen_thread.frame_queue:
            return self.listen_thread.frame_queue[-1]
        else:
            return None


def creat_host_TCP_scoket(ip, port):
    HOST_IP = ip
    HOST_PORT = port
    print("IP:", HOST_IP)
    print("Port:", HOST_PORT)
    print("Create socket:")
    socket_tcp = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM, proto=0, fileno=None)
    host_addr = (HOST_IP, HOST_PORT)
    socket_tcp.bind(host_addr)
    return socket_tcp


if __name__ == '__main__':
    print(1)


'''
origin_img = "origin_img.jpg"
HOST_IP = "127.0.0.1"
HOST_PORT = 8889
print("IP:", HOST_IP)
print("Port:", HOST_PORT)
print("Starting socket:")

# creat socket object
socket_tcp = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM, proto=0, fileno=None)
print("TCP server listen at %s:%d" % (HOST_IP, HOST_PORT))
host_addr = (HOST_IP, HOST_PORT)

# bind socket to host_ip and host_port
socket_tcp.bind(host_addr)

# listen connection request
socket_tcp.listen(1)

socket_client, (client_ip, client_port) = socket_tcp.accept()
print("Connection accepted from %s" % client_ip)

# wait for client connect
while True:
    start = time.time()
    data = socket_client.recv(1024)
    print("Server received:", data)
    socket_client.send(b"Welcome to Cloud Computing Server.")

    print("Start receive image!")
    with open(origin_img, 'wb') as f:
        print("Write data to %s" % origin_img)
        while True:
            # print("Receiving data...")
            data = socket_client.recv(1024)
            # print("data size: %d", len(data))
            if not data or len(data) < 1024:
                break
            f.write(data)
    print("Successfully get %s" % origin_img)
    success_mess = "Successfully get " + origin_img
    socket_client.send(success_mess.encode())
    data = socket_client.recv(1024)
    print("Server received:", data)
    end = time.time()
    print(end - start)
    break
'''
