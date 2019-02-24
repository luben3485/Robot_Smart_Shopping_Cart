import socket
import time


def creat_TCP_socket(ip, port):  # create socket
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


send_socket = creat_TCP_socket("127.0.0.1", 7878)  # create socket: connect to 127.0.0.1 at port:7878
send_socket.send(b"1")  # send test data
time.sleep(2)
#send_socket.send(b"1 2")  # send test data
#time.sleep(3)
#send_socket.send(b"3 5")  # send test data
#time.sleep(5)
#send_socket.send(b"4 4")  # send test data
