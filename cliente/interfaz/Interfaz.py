import threading
import PySimpleGUI as sg

class Interfaz(object):
    def __init__(self):
        self._layout_chat = [      
                                [sg.InputText()],
                                [sg.Multiline(size=(70, 30), disabled = True,key='Multi')],      
                                [sg.Submit('Enviar'), sg.Cancel()]
                            ]      
        self.layout_logueo = [
                                [sg.Text('Ingrese su nombre de usuario')],
                                [sg.InputText()],
                                [sg.Submit('Enviar'), sg.Cancel()]
                             ]

        self.texto_chat = ''
        self._multiline_object = None
        self.sem_mostrar_mensajes = threading.Semaphore()

    def inicializar_chat(self):
        self._window_chat = sg.Window('Chat', self._layout_chat)    
        self._multiline_object = self._window_chat['Multi'] #Devuelve un objeto de tipo Multiline

    def cerrar_chat(self):
        self._window_chat.close()

    def enviar_mensaje(self):
        event, values = self._window_chat.read()    
        if event == 'Cancel' or event is None:
            return False
        mensaje = values[0]    
        return mensaje

    def logueo(self):
        self.window_logueo = sg.Window('Chat', self.layout_logueo)    
        while True:
            event, values = self.window_logueo.read()
            if event is None or event == 'Cancel':
                return False
            if values[0].rstrip() == '':
                sg.popup('El usuario no puede ser vacio')                    
            else:
                break

        self._usuario = values[0]
        self.window_logueo.close()
        return values[0]

    def mostrar_mensaje_enviado(self,mensaje):
        mensaje =  'Vos: ' + mensaje
        
        self.sem_mostrar_mensajes.acquire()
        self.texto_chat = self.texto_chat + mensaje + '\n'        
        self._multiline_object.Update(value = self.texto_chat)
        self.sem_mostrar_mensajes.release()

    def mostrar_mensaje_recibido(self,mensaje_recibido):
        self.sem_mostrar_mensajes.acquire()
        self.texto_chat = self.texto_chat + mensaje_recibido + '\n'
        self._multiline_object.Update(value = self.texto_chat)
        self.sem_mostrar_mensajes.release()
