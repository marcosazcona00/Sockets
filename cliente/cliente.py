import socket
import threading
HOST = '192.168.1.39'  # The server's hostname or IP address
PORT = 6001        # The port used by the server


def output_mensajes(s):
    while True:
        mensaje = s.recv(1024).decode('utf-8').rstrip()
        print(mensaje) 

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    nombre_usuario = input('Ingrese su nombre de usuario: ')
    s.send(nombre_usuario.encode('utf-8'))
    threading.Thread(target = output_mensajes, args = (s,)).start()
    
    while True:
        mensaje = input('Ingrese un mensaje: ')
        s.send(mensaje.encode('utf-8'))
