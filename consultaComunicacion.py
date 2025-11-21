import Pyro4
import threading
import json
import os

RUTA_DB = "inventario.json"

@Pyro4.expose
class InventarioReadOnly:
    def __init__(self):
        self.lock = threading.Lock()
        self.productos = {}
        self.cargar_desde_archivo()

    def cargar_desde_archivo(self):
        """Carga el archivo JSON o lo crea si no existe."""
        if os.path.exists(RUTA_DB):
            try:
                with open(RUTA_DB, "r") as f:
                    self.productos = json.load(f)
            except:
                print("JSON corrupto. Creando uno nuevo.")
                self.productos = {}
                self.guardar()
        else:
            print("JSON no encontrado. Creando nuevo.")
            self.productos = {}
            self.guardar()

    def guardar(self):
        """Guarda los datos en el archivo JSON."""
        with open(RUTA_DB, "w") as f:
            json.dump(self.productos, f, indent=4)

    def sincronizar(self, nuevos_productos):
        """Recibe datos actualizados desde Server1."""
        with self.lock:
            self.productos = nuevos_productos
            self.guardar()

    def listar_productos(self):
        with self.lock:
            if not self.productos:
                return "Inventario vacío"
            texto = "Productos:\n"
            for id, p in self.productos.items():
                texto += f"{id}: {p['nombre']} - Stock: {p['stock']}\n"
            return texto

    def obtener_producto(self, id):
        with self.lock:
            if id in self.productos:
                p = self.productos[id]
                return f"{id}: {p['nombre']} - Stock: {p['stock']}"
            return "Error: Producto no encontrado"


def main():
    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS()
    servidor = InventarioReadOnly()
    uri = daemon.register(servidor)
    ns.register("inventario.readonly", uri)
    print("Server2 iniciado")
    daemon.requestLoop()

if __name__ == "__main__":
    main()
