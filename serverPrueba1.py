import Pyro4
import threading
import json
import os

RUTA_DB = "tareas.json"

@Pyro4.expose
class GestorTareas:
    def __init__(self):
        self.lock = threading.Lock()
        self.tareas = []
        self.cargar_desde_archivo()

    
    def guardar_en_archivo(self):
        """Guarda la lista de tareas en tareas.json."""
        with open(RUTA_DB, "w") as f:
            json.dump(self.tareas, f, indent=4)

    def cargar_desde_archivo(self):
        """Carga tareas desde el archivo si existe, de lo contrario lo crea."""
        if os.path.exists(RUTA_DB):
            try:
                with open(RUTA_DB, "r") as f:
                    self.tareas = json.load(f)
            except json.JSONDecodeError:
                print("Archivo corrupto. Creando nuevo.")
                self.tareas = []
                self.guardar_en_archivo()
        else:
            self.tareas = []
            self.guardar_en_archivo()

  
    def agregar_tarea(self, descripcion):
        """Agrega una nueva tarea y devuelve su ID."""
        with self.lock:
            nueva_tarea = {
                "id": len(self.tareas) + 1,
                "descripcion": descripcion,
                "estado": "pendiente"
            }
            self.tareas.append(nueva_tarea)
            self.guardar_en_archivo()
            return nueva_tarea["id"]

    def listar_tareas(self):
        """Retorna todas las tareas en formato JSON."""
        return json.dumps(self.tareas, indent=4)

    def completar_tarea(self, id):
        """Marca una tarea como completada."""
        with self.lock:
            for tarea in self.tareas:
                if tarea["id"] == id:
                    tarea["estado"] = "completada"
                    self.guardar_en_archivo()
                    return "Tarea completada"
            return "Error: ID no encontrado"

    def eliminar_tarea(self, id):
        """Elimina una tarea de la lista."""
        with self.lock:
            for tarea in self.tareas:
                if tarea["id"] == id:
                    self.tareas.remove(tarea)
                    self.guardar_en_archivo()
                    return "Tarea eliminada"
            return "Error: ID no encontrado"

    def contar_tareas_pendientes(self):
        """Devuelve cuántas tareas están pendientes."""
        return sum(1 for t in self.tareas if t["estado"] == "pendiente")


def main():
    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS()

    gestor = GestorTareas()
    uri = daemon.register(gestor)
    ns.register("tareas.gestor", uri)

    print("Servidor de tareas iniciado.")
    print(f"Usando base de datos: {RUTA_DB}")

    daemon.requestLoop()


if __name__ == "__main__":
    main()
