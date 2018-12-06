import cv2
import sys
import time
import socket
import threading
from collections import deque
import pickle
import struct


class clientListenThread (threading.Thread):
    def __init__(self, name, ip, port, instruction, frame_queue):
        threading.Thread.__init__(self)
        self.name = name
        self.id = '[' + self.name + ']'
        self.ip = ip
        self.port = port
        self.listen_socket = creat_host_TCP_socket(self.ip, self.port)
        print(self.id, "Seccessfully creat %s listening thread." % self.name)
        self.instruction = instruction
        self.frame_queue = frame_queue
        print(self.id, "client Listen get id ", id(instruction))
        print(self.id, "client Listen id ", id(self.instruction))

    def run(self):
        self.listen_socket.listen(1)
        self.client_socket, (self.client_ip, self.client_port) = self.listen_socket.accept()
        print(self.id, "Connection accepted from %s:%d" % (self.client_ip, self.client_port))
        # self.instruction[0] = (b"TTTTTTTTTTest inst")  # TEST
        origin_img = "origin_img.jpg"
        payload_size = struct.calcsize("L")
        while True:
            data = self.client_socket.recv(1024)
            print(self.id,"Server received:", data)
            self.client_socket.send(b"Welcome to Cloud Computing Server.")
            start = time.time()
            print(self.id, "開始線程：" + self.name)
            print(self.id, "Start receive image!")
            data = b""
            print(self.id, len(data), payload_size)
            while len(data) < payload_size:
                print(self.id, 1, len(data))
                data += self.client_socket.recv(4096)
            stop1 = time.time()
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("L", packed_msg_size)[0]
            stop2 = time.time()
            print(self.id, msg_size)
            while len(data) < msg_size:
                data += self.client_socket.recv(1048576)
            frame_data = data[:msg_size]
            data = data[msg_size:]
            stop3 = time.time()
            print(self.id, len(data))

            frame = pickle.loads(frame_data)
            print(self.id, frame.shape)
            stop4 = time.time()
            # cv2.imwrite('output.jpg', frame)
            # cv2.imshow('SERVER', frame)
            '''
            with open(origin_img, 'wb') as f:
                print("Write data to %s" % origin_img)
                while True:
                    # print("Receiving data...")
                    data = self.client_socket.recv(1024)
                    # print("data size: %d", len(data))
                    if not data or len(data) < 1024:
                        break
                    f.write(data)
            '''
            print(self.id, "Successfully get %s" % origin_img)
            self.frame_queue.append(frame)
            # success_mess = "Successfully get " + origin_img
            # self.client_socket.send(success_mess.encode())
            # data = self.client_socket.recv(1024)
            # print("Server received:", data)
            end = time.time()
            print(stop1 - start)
            print(stop2 - start)
            print(stop3 - start)
            print(stop4 - start)
            print(end - start)
            break
        print(self.id, "退出線程：" + self.name)


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
                self.client_socket.send(self.instruction[0])
                self.print_msg("Server send instruction", self.instruction[0])
                self.instruction[0] = None
            else:
                pass
            time.sleep(0.01)
        self.print_msg("退出線程：" + self.name)

    def print_msg(self, *args):
        print(self.id, " ".join(map(str, args)))


class host():
    def __init__(self, name, ip_listen, port_listen, ip_send, port_send):
        self.name = name
        self.instruction = [None]
        print("HOST id ", id(self.instruction))
        self.frame_queue = deque(maxlen=10)
        self.listen_thread = clientListenThread(name + "_listen", ip_listen, port_listen, self.instruction, self.frame_queue)
        self.send_thread = clientSendThread(name + "_send", ip_send, port_send, self.instruction)
        self.listen_thread.start()
        self.send_thread.start()

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
    cart_server = host("Host", "140.116.102.99", 8899, "140.116.102.99", 8889)
    # time.sleep(4)
    cart_server.instruction[0] = (b"TTTTest inst")
    print(id(cart_server.instruction))
    print(id(cart_server.listen_thread.instruction))
    print(id(cart_server.send_thread.instruction))
