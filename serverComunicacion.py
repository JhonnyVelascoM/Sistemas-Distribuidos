import Pyro4
import threading
import time

@Pyro4.expose
class InventarioWrite:
    def __init__(self):
        self.lock = threading.Lock()
        self.productos = {}

        # Conectar con Server2 para sincronización eventual
        self.server2 = Pyro4.Proxy("PYRONAME:inventario.readonly")

    def agregar_producto(self, id, nombre, stock):
        with self.lock:
            if id in self.productos:
                return "Error: Producto ya existe"
            self.productos[id] = {"nombre": nombre, "stock": stock}
            self.sincronizar_server2()
            return "Producto agregado"

    def actualizar_stock(self, id, stock):
        with self.lock:
            if id in self.productos:
                self.productos[id]["stock"] = stock
                self.sincronizar_server2()
                return "Stock actualizado"
            return "Error: Producto no encontrado"

    def eliminar_producto(self, id):
        with self.lock:
            if id in self.productos:
                del self.productos[id]
                self.sincronizar_server2()
                return "Producto eliminado"
            return "Error: Producto no encontrado"

    # Sincronización eventual: enviar copia completa a Server2
    def sincronizar_server2(self):
        try:
            self.server2.sincronizar(self.productos)
        except Exception as e:
            print("Error sincronizando con Server2:", e)

# Arranque
def main():
    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS()
    server1 = InventarioWrite()
    uri = daemon.register(server1)
    ns.register("inventario.write", uri)
    print("Server1 iniciado (modificaciones)")
    daemon.requestLoop()

if __name__ == "__main__":
    main()
