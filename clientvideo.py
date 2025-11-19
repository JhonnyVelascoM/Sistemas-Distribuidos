import socket
import os
import subprocess

class VideoClient:
    def __init__(self, server_ip, port=7777):
        self.server_ip = server_ip
        self.port = port
    
    def play_video(self, video_path):
        try:
            print(f"Reproduciendo: {video_path}")
            subprocess.Popen(['xdg-open', video_path])
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
    
    def start(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.server_ip, self.port))
                print(f"Conectado a {self.server_ip}:{self.port}")
                
                while True:
                    data = s.recv(1024).decode()
                    print(data)
                    
                    choice = input().strip()
                    s.send(choice.encode())
                    
                    if choice == '5':
                        break
                    
                    response = s.recv(1024).decode()
                    if response.startswith("PLAY:"):
                        video = response.split(":")[1]
                        if os.path.exists(video):
                            self.play_video(video)
                            input("Presiona Enter para continuar...")
                        else:
                            print(f"Video no encontrado: {video}")
                    else:
                        print(f"Error: {response}")
                        
        except ConnectionRefusedError:
            print("Error: No se pudo conectar al servidor")
        except KeyboardInterrupt:
            print("\nCliente terminado")

if __name__ == "__main__":
 
    client = VideoClient("localhost")
    client.start()