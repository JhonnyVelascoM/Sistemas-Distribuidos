import Pyro4
import threading
import json
import os

@Pyro4.expose
class Inventario:
    def __init__(self, archivo_json="inventario.json"):
        self.archivo_json = archivo_json
        self.lock = threading.Lock()
        self.productos = self._cargar_inventario()
    
    def _cargar_inventario(self):
        """Carga el inventario desde el archivo JSON"""
        try:
            if os.path.exists(self.archivo_json):
                with open(self.archivo_json, 'r') as f:
                    return json.load(f)
            else:
                print("Creando nuevo archivo de inventario")
                return {}
        except Exception as e:
            print(f"Error cargando inventario: {e}")
            return {}
    
    def _guardar_inventario(self):
        """Guarda el inventario en el archivo JSON"""
        try:
            with open(self.archivo_json, 'w') as f:
                json.dump(self.productos, f, indent=2)
        except Exception as e:
            print(f"Error guardando inventario: {e}")
    
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
            
            self.productos[id] = {
                "nombre": nombre, 
                "stock": stock
            }
            
            self._guardar_inventario()  # Guardar en JSON
            return "Producto agregado"
    
    def obtener_producto(self, id):
        with self.lock:
            if id in self.productos:
                producto = self.productos[id]
                return f"{id}: {producto['nombre']} - Stock: {producto['stock']}"
            return "Error: Producto no encontrado"
    
    def actualizar_stock(self, id, nuevo_stock):
        with self.lock:
            if id in self.productos:
                self.productos[id]["stock"] = nuevo_stock
                self._guardar_inventario()  # Guardar en JSON
                return "Stock actualizado"
            return " Error: Producto no encontrado"
    
    def listar_productos(self):
        if not self.productos:
            return " Inventario vacío"
        
        resultado = "📋 Productos:\n"
        for id, info in self.productos.items():
            resultado += f"  {id}: {info['nombre']} - Stock: {info['stock']}\n"
        return resultado
    
    def eliminar_producto(self, id):
        with self.lock:
            if id in self.productos:
                del self.productos[id]
                self._guardar_inventario()  # Guardar en JSON
                return "✅ Producto eliminado"
            return "❌ Error: Producto no encontrado"

def main():
    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS()
    
    inventario = Inventario()
    uri = daemon.register(inventario)
    ns.register("inventario.servicio", uri)
    
    print("🚀 Servidor Pyro4 iniciado - Persistencia JSON activada")
    daemon.requestLoop()

if __name__ == "__main__":
    main()