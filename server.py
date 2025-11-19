import socket
import os

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('172.17.44.232', 7777))  # IP de tu servidor
serversocket.listen(5)

print("Servidor escuchando en el puerto 7777...")

while True:
    connection, address = serversocket.accept()
    print("Conexión establecida desde:", address)

    try:
        menu = """
        # a. listar los archivos
        # b. Abrir el navegador
        # c. Guardar las teclas pulsadas en un .txt
        # d. copiar el archivo del cliente al servidor
        # e. Girar la pantalla a 90° (opcional)"""

        connection.sendall(menu.encode())

        while True:
            data = connection.recv(1024).decode().strip()
            if not data:
                break # El cliente se desconectó
            print(f"Datos recibidos del cliente:,{data}")

            if data == 'a':
                files = os.listdir('.')
                file_list_str = "\n".join(files)
                connection.sendall(f"Archivos en el servidor:\n{file_list_str}".encode())
            elif data == 'b':
                connection.sendall(b"Comando para abrir navegador enviado al cliente")
            elif data == 'c':
                connection.sendall(b"Comando para enviar teclas enviado al cliente")
            elif data == 'd':
                connection.sendall(b"Comando para copiar archivo del cliente al servidor")
            else:
                connection.sendall(b"seleccione un comando de la lista")
    except Exception as e:
        print("Error de comunicacion con el servidor")
    finally:
        connection.close()
        print(f"Conexion con {address} cerrada")