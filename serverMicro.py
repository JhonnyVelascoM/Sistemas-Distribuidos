import Pyro4
import threading

@Pyro4.expose
class Inventario:
    def __init__(self):
        self.productos = {}
        self.lock = threading.Lock()
    
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
                return " Error: Producto ya existe"
            self.productos[id] = {"nombre": nombre, "stock": stock}
            return "Producto agregado"
    
    def obtener_producto(self, id):
        with self.lock:
            if id in self.productos:
                producto = self.productos[id]
                return f" {id}: {producto['nombre']} - Stock: {producto['stock']}"
            return " Error: Producto no encontrado"
    
    def actualizar_stock(self, id, nuevo_stock):
        with self.lock:
            if id in self.productos:
                self.productos[id]["stock"] = nuevo_stock
                return "Stock actualizado"
            return " Error: Producto no encontrado"
    
    def listar_productos(self):
        if not self.productos:
            return "Inventario vacío"
        
        resultado = "Productos:\n"
        for id, info in self.productos.items():
            resultado += f"  {id}: {info['nombre']} - Stock: {info['stock']}\n"
        return resultado
    
    def eliminar_producto(self, id):
        with self.lock:
            if id in self.productos:
                del self.productos[id]
                return "Producto eliminado"
            return "Error: Producto no encontrado"

def main():
    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS()
    
    inventario = Inventario()
    uri = daemon.register(inventario)
    ns.register("inventario.servicio", uri)
    
    print("Servidor Pyro4 iniciado")
    daemon.requestLoop()

if __name__ == "__main__":
    main()