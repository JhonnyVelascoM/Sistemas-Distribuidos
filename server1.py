import socket

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('172.17.44.232', 7777))  # IP de tu servidor
serversocket.listen(5)

print("Servidor escuchando en el puerto 7777...")

while True:
    connection, address = serversocket.accept()
    print("Conexión establecida desde:", address)
    
    data = connection.recv(1024).decode().strip()
    if data:
        print("Datos recibidos del cliente:", data)
        
        # Comando seguro para crear archivo
        if data.startswith("creararchivo "):
            filename = data.split(" ", 1)[1]
            try:
                with open(filename, "w") as f:
                    f.write("Archivo creado desde cliente remoto\n")
                connection.send(f"Archivo '{filename}' creado exitosamente.".encode())
            except Exception as e:
                connection.send(f"Error al crear archivo: {e}".encode())
        else:
            connection.send(b"Comando no permitido")

    connection.close()
