import socket
import os
import threading

class VideoServer:
    def __init__(self, host='localhost', port=7777):
        self.host = host
        self.port = port
        self.videos = {
            '1': 'video1.mp4',
            '2': 'video2.mp4', 
            '3': 'video3.mp4',
            '4': 'video4.mp4'
        }
    
    def create_menu(self):
        menu = "\n=== SERVIDOR DE VIDEOS ===\n"
        for key, video in self.videos.items():
            exists = "OK" if os.path.exists(video) else "Error"
            menu += f"{key}. {video} {exists}\n"
        menu += "5. Salir\nSelecciona opción: "
        return menu
    
    def handle_client(self, connection, address):
        print(f"Cliente conectado: {address}")
        try:
            while True:
                connection.send(self.create_menu().encode())
                data = connection.recv(1024).decode().strip()
                
                if not data or data == '5':
                    break
                
                if data in self.videos:
                    video = self.videos[data]
                    if os.path.exists(video):
                        connection.send(f"PLAY:{video}".encode())
                        print(f"Enviando: {video} a {address}")
                    else:
                        connection.send(b"ERROR:Video no encontrado")
                else:
                    connection.send(b"ERROR:Opcion No valida")
        finally:
            connection.close()
    
    def start(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((self.host, self.port))
        server.listen(5)
        print(f"Servidor en {self.host}:{self.port}")
        
        try:
            while True:
                conn, addr = server.accept()
                threading.Thread(target=self.handle_client, args=(conn, addr)).start()
        except KeyboardInterrupt:
            print("\nServidor cerrado")
        finally:
            server.close()

if __name__ == "__main__":
    VideoServer().start()