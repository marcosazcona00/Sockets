import sys
import socket
import threading
'''
    The first parameter is AF_INET and the second one is SOCK_STREAM. 
    AF_INET refers to the address family ipv4. 
    The SOCK_STREAM means connection oriented TCP protocol. 
    SOCK_DGRAM is for UDP protocol
'''

class ServerSocket(socket.socket):
    def __init__(self,*args,**kwargs):
        super(ServerSocket,self).__init__(*args,**kwargs)
        self._ip = '192.168.1.39'
        self._puerto = 6001

        self.clientes = []
        self.buffer_mensajes = []

        self.sem = threading.Semaphore()
        self.sem_server = threading.Semaphore(0)
        self.sem_buffer_mensajes = threading.Semaphore()
        self.sem_clientes = threading.Semaphore()

        self._config_server()


    def _config_server(self):
        self.bind((self._ip,self._puerto)) ### Le decimos al servidor que escuche en esta IP:Puerto
        self.listen()   
        self.hilo_principal = threading.Thread(target = self._enviar_mensaje_clientes)
        self.hilo_principal.start()
        print(f'Servidor escuchando en {self._ip}:{self._puerto}')

    def _cerrar_conexion_cliente(self,conn,addr):
        '''
            Esta funcion asociada a un hilo cierra la conexion con un cliente
        '''
        ### Sacamos al cliente de la lista de clientes que escuchar
        ### Como la cola de clientes es compartida hay que manejarla con exclusion mutua
        self.sem.acquire()
        self.clientes.remove((conn,addr))
        self.sem.release()
        
        ### Obtenemos el hilo para matarlo
        hilo_actual = threading.current_thread()
        
        ### Cerramos el socket que escucha a este cliente
        conn.close()

    def _enviar_mensaje_clientes(self):
        '''
            Esta funcion es un hilo del servidor principal que envia mensajes a los clientes conectados
        '''
        while True:
            print('Server esperando mandar mensaje')
            
            ### Esperamos a que algun cliente envie un mensaje que despierte al hilo de envio de mensajes 
            self.sem_server.acquire()
            
            ### Sacamos el mensaje de la cola
            self.sem_buffer_mensajes.acquire()
            info_cliente = self.buffer_mensajes.pop()
            self.sem_buffer_mensajes.release()

            ### Enviamos le mensaje al cliente
            mensaje_enviar = info_cliente[0]
            conn_cliente = info_cliente[1]
            for cliente in self.clientes:
                if conn_cliente != cliente[0]:
                    cliente[0].send(mensaje_enviar.encode('utf-8'))
        

    def _atender_cliente(self,conn,addr):
        '''
            Esta funcion se asocia a un hilo para atender a un cliente particular
            Si recibe exit como mensaje cierra la conexion
        '''
        print(conn)
        print(f'Bienvenido {addr}!')
        nombre_usuario = (conn.recv(1024)).decode('utf-8').rstrip()
        while True:
            data = (conn.recv(1024)).decode('utf-8').rstrip()
            
            mensaje_enviar = f'Mensaje de: {nombre_usuario} --> {data}'
            
            ### Guardamos el mensaje en el buffer
            self.sem_buffer_mensajes.acquire()
            self.buffer_mensajes.append([mensaje_enviar,conn])
            self.sem_buffer_mensajes.release()
            
            ### Le avisamos al hilo del server que envie los mensajes
            self.sem_server.release()
            
            if data == 'exit':
                ### El cliente decide cerrar la conexion
                break
            
        
        self._cerrar_conexion_cliente(conn,addr)
        print(f'Cerrada conexion con {nombre_usuario}')
        print(self.clientes)
        ### Matamos al hilo de este cliente 
        sys.exit()


    def accept(self):
        conn, addr = super(ServerSocket,self).accept() ### Aceptamos la conexion de un cliente
        self.clientes.append((conn,addr)) 
        hilo_cliente = threading.Thread(target = self._atender_cliente, args = (conn,addr))
        hilo_cliente.start()