import User

def menuPrincipal():
    print("Bienvenido a Inspiration")
    print("1. Iniciar sesión")
    print("2. Registrarse")
    print("3. Salir")
    opcion = input("Ingrese una opción: ")
    if opcion == "1":
        us.iniciar_sesion()
    elif opcion == "2":
        us.crear_usuario()
    elif opcion == "3":
        return
    else:
        print("Opción inválida")
        menuPrincipal()

def menuUsuario():
    print("1. Ver inspirations")
    print("2. Crear inspiration")
    print("3. Buscar usuarios")
    print("4. Ver perfil")
    print("5. Cerrar sesión")
    opcion = input("Ingrese una opción: ")
    if opcion == "1":
        pass
    elif opcion == "2":
        pass
    elif opcion == "3":
        pass
    elif opcion == "4":
        pass
    elif opcion == "5":
        return
    else:
        print("Opción inválida")
        menuUsuario()


