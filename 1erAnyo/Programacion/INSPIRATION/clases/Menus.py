import User
import Inspirations
def menuPrincipal():
    print("Bienvenido a Inspiration")
    print("1. Iniciar sesión")
    print("2. Registrarse")
    print("3. Salir")
    opcion = input("Ingrese una opción: ")
    if opcion == "1":
        userActivo = User.iniciar_sesion()
        menuUsuario(userActivo)
    elif opcion == "2":
        User.crear_usuario()
        menuPrincipal()
    elif opcion == "3":
        return
    else:
        print("Opción inválida")
        menuPrincipal()

def menuUsuario(userActivo):
    print("1. Ver inspirations")
    print("2. Crear inspiration")
    print("3. Buscar usuarios")
    print("4. Ver perfil")
    print("5. Cerrar sesión")
    opcion = input("Ingrese una opción: ")
    if opcion == "1":
        Inspirations.mostrar_inspirations(userActivo)
    elif opcion == "2":
        Inspirations.crear_inspiration(userActivo)
    elif opcion == "3":
        pass
    elif opcion == "4":
        userActivo.mostrar_perfil()
    elif opcion == "5":
        return
    else:
        print("Opción inválida")
        menuUsuario()


menuPrincipal()