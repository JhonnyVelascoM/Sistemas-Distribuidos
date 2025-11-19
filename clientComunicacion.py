import Pyro4

def main():
    write = Pyro4.Proxy("PYRONAME:inventario.write")
    read = Pyro4.Proxy("PYRONAME:inventario.readonly")

    while True:
        print("""
1. Agregar producto
2. Actualizar stock
3. Eliminar producto
4. Consultar producto
5. Listar productos
0. Salir
        """)
        opcion = input("Opción: ")

        if opcion == "1":
            id = input("ID: ")
            nombre = input("Nombre: ")
            stock = int(input("Stock: "))
            print(write.agregar_producto(id, nombre, stock))

        elif opcion == "2":
            id = input("ID: ")
            stock = int(input("Nuevo stock: "))
            print(write.actualizar_stock(id, stock))

        elif opcion == "3":
            id = input("ID: ")
            print(write.eliminar_producto(id))

        elif opcion == "4":
            id = input("ID: ")
            print(read.obtener_producto(id))

        elif opcion == "5":
            print(read.listar_productos())

        elif opcion == "0":
            break

        input("\nPresiona Enter para continuar...")

if __name__ == "__main__":
    main()
