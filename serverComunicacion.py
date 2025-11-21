# server1_write.py
import Pyro4
import threading

@Pyro4.expose
class InventarioWrite:
    def __init__(self):
        self.lock = threading.Lock()
        self.productos = {}

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
            if id not in self.productos:
                return "Error: Producto no encontrado"

            self.productos[id]["stock"] = stock
            self.sincronizar_server2()
            return "Stock actualizado"

    def eliminar_producto(self, id):
        with self.lock:
            if id not in self.productos:
                return "Error: Producto no encontrado"

            del self.productos[id]
            self.sincronizar_server2()
            return "Producto eliminado"

    def sincronizar_server2(self):
        """Envía los datos actualizados al servidor de solo lectura."""
        try:
            self.server2.sincronizar(self.productos)
        except Exception as e:
            print("ERROR sincronizando con Server2:", e)


def main():
    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS()
    servidor = InventarioWrite()
    uri = daemon.register(servidor)
    ns.register("inventario.write", uri)
    print("Server1 iniciado")
    daemon.requestLoop()

if __name__ == "__main__":
    main()
