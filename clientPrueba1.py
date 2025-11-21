import Pyro4
import json

def main():
    try:
        tareas = Pyro4.Proxy("PYRONAME:tareas.gestor")
    except Exception as e:
        print("Error al conectar al servidor Pyro4:", e)
        return

    while True:
        print("""
=== GESTOR DE TAREAS ===
1. Agregar tarea
2. Listar tareas
3. Completar tarea
4. Eliminar tarea
5. Contar tareas pendientes
0. Salir
""")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            descripcion = input("Descripción: ")
            if descripcion.strip() == "":
                print("La descripción no puede estar vacía.")
                continue
            id = tareas.agregar_tarea(descripcion)
            print(f"Tarea agregada con ID: {id}")

        elif opcion == "2":
            datos = tareas.listar_tareas()
            lista = json.loads(datos)

            if not lista:
                print("No hay tareas registradas.")
            else:
                print("\n=== LISTA DE TAREAS ===")
                for t in lista:
                    print(f"{t['id']}. {t['descripcion']} — [{t['estado']}]")

        elif opcion == "3":
            try:
                id = int(input("ID de la tarea a completar: "))
                print(tareas.completar_tarea(id))
            except ValueError:
                print("ID inválido. Debe ser un número.")

        elif opcion == "4":
            try:
                id = int(input("ID de la tarea a eliminar: "))
                print(tareas.eliminar_tarea(id))
            except ValueError:
                print("ID inválido. Debe ser un número.")

        elif opcion == "5":
            print("Tareas pendientes:", tareas.contar_tareas_pendientes())

        elif opcion == "0":
            print("Saliendo...")
            break

        else:
            print("Opción inválida.")

        input("\nPresiona Enter para continuar...")


if __name__ == "__main__":
    main()
