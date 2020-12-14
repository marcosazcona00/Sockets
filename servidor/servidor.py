import socket
from socket_server import ServerSocket

def main():
    socket_server = ServerSocket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        socket_server.accept()


if __name__ == '__main__':
    main()