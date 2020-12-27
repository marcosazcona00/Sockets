import sys
import socket
import threading
from interfaz.Interfaz import Interfaz

interfaz = Interfaz()

HOST = '192.168.1.39'  # The server's hostname or IP address
PORT = 6001        # The port used by the server

def enviar_mensaje(s,mensaje):
    '''
        Se envia el mensaje al servidor
    '''
    mensaje = str(mensaje).encode('utf-8')
    s.send(mensaje)

def output_mensajes(s):
    '''
        Este hilo actualiza el chat cuando se recibe info del server
    '''
    while True:
        mensaje = s.recv(1024).decode('utf-8').rstrip()
        interfaz.mostrar_mensaje_recibido(mensaje) 

def chatear(nombre_usuario):
    threading.Thread(target = output_mensajes, args = (s,)).start()
    interfaz.inicializar_chat()
    enviar_mensaje(s,nombre_usuario)
    while True:
        mensaje = interfaz.enviar_mensaje()
        if not mensaje:
            break
        enviar_mensaje(s,mensaje)
        interfaz.mostrar_mensaje_enviado(mensaje)

    enviar_mensaje(s,'exit')
    interfaz.cerrar_chat()
    
if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        nombre_usuario = interfaz.logueo()
        if nombre_usuario:
            s.connect((HOST, PORT))
            chatear(nombre_usuario)

        sys.exit()
