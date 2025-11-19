import Pyro4
import threading
import json
import os
import time

RUTA_DB = "inventario.json"

@Pyro4.expose
class InventarioReadOnly:
    def __init__(self):
        self.lock = threading.Lock()
        self.productos = {}
        self.cargar_desde_archivo()

    def cargar_desde_archivo(self):
        if os.path.exists(RUTA_DB):
            with open(RUTA_DB, "r") as f:
                try:
                    self.productos = json.load(f)
                except:
                    self.productos = {}
        else:
            self.productos = {}

    def sincronizar(self, nuevos_productos):
        """Server1 enviará los datos actualizados para mantener consistencia eventual"""
        with self.lock:
            self.productos = nuevos_productos
            with open(RUTA_DB, "w") as f:
                json.dump(self.productos, f, indent=4)

    # Métodos solo de lectura
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

# Arranque
def main():
    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS()
    server2 = InventarioReadOnly()
    uri = daemon.register(server2)
    ns.register("inventario.readonly", uri)
    print("Server2 iniciado (solo lectura / persistencia JSON)")
    daemon.requestLoop()

if __name__ == "__main__":
    main()
