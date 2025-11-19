import Pyro4
import threading
import json
import os

RUTA_DB = "inventario.json"

@Pyro4.expose
class Inventario:
    def __init__(self):
        self.lock = threading.Lock()
        self.productos = {}
        self.cargar_desde_archivo()

    # ------------------------------
    #      MANEJO DEL ARCHIVO JSON
    # ------------------------------
    def guardar_en_archivo(self):
        """Crea o actualiza el archivo JSON con los productos."""
        with open(RUTA_DB, "w") as f:
            json.dump(self.productos, f, indent=4)

    def cargar_desde_archivo(self):
        """Carga los datos del JSON solo si existe."""
        if os.path.exists(RUTA_DB):
            try:
                with open(RUTA_DB, "r") as f:
                    self.productos = json.load(f)
            except:
                # Archivo corrupto o ilegible → se inicia vacío
                self.productos = {}
        else:
            self.productos = {}

    # ------------------------------
    #        MÉTODOS DEL SISTEMA
    # ------------------------------
    def obtener_menu(self):
        return """
=== SISTEMA DE INVENTARIO ===
1. Agregar producto
2. Obtener producto  
3. Actualizar stock
4. Listar productos
5. Eliminar producto
0. Salir
Selecciona una opción: """

    def agregar_producto(self, id, nombre, stock):
        with self.lock:
            if id in self.productos:
                return "Error: Producto ya existe"

            self.productos[id] = {"nombre": nombre, "stock": stock}

            # Crear JSON automáticamente si no existe
            self.guardar_en_archivo()

            return "Producto agregado"

    def obtener_producto(self, id):
        with self.lock:
            if id in self.productos:
                p = self.productos[id]
                return f"{id}: {p['nombre']} - Stock: {p['stock']}"
            return "Error: Producto no encontrado"

    def actualizar_stock(self, id, nuevo_stock):
        with self.lock:
            if id in self.productos:
                self.productos[id]["stock"] = nuevo_stock
                self.guardar_en_archivo()
                return "Stock actualizado"
            return "Error: Producto no encontrado"

    def listar_productos(self):
        if not self.productos:
            return "Inventario vacío"

        texto = "Productos:\n"
        for id, p in self.productos.items():
            texto += f"  {id}: {p['nombre']} - Stock: {p['stock']}\n"
        return texto

    def eliminar_producto(self, id):
        with self.lock:
            if id in self.productos:
                del self.productos[id]
                self.guardar_en_archivo()
                return "Producto eliminado"
            return "Error: Producto no encontrado"


# ------------------------------
#             MAIN
# ------------------------------
def main():
    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS()

    inventario = Inventario()
    uri = daemon.register(inventario)
    ns.register("inventario.servicio", uri)

    print("Servidor Pyro4 iniciado")
    print(f"Archivo de inventario: {RUTA_DB}")
    daemon.requestLoop()


if __name__ == "__main__":
    main()
