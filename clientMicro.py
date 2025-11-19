import Pyro4

def main():
    inventario = Pyro4.Proxy("PYRONAME:inventario.servicio")
    
    while True:
        menu = inventario.obtener_menu()
        opcion = input(menu)
        
        if opcion == "1":
            id = input("ID: ")
            nombre = input("Nombre: ")
            stock = int(input("Stock: "))
            resultado = inventario.agregar_producto(id, nombre, stock)
            print(resultado)
        
        elif opcion == "2":
            id = input("ID: ")
            resultado = inventario.obtener_producto(id)
            print(resultado)
        
        elif opcion == "3":
            id = input("ID: ")
            stock = int(input("Nuevo stock: "))
            resultado = inventario.actualizar_stock(id, stock)
            print(resultado)
        
        elif opcion == "4":
            resultado = inventario.listar_productos()
            print(resultado)
        
        elif opcion == "5":
            id = input("ID: ")
            resultado = inventario.eliminar_producto(id)
            print(resultado)
        
        elif opcion == "0":
            print("¡Hasta luego!")
            break
        
        input("\n Presiona Enter para continuar...")

if __name__ == "__main__":
    main()