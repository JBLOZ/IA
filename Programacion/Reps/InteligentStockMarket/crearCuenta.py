import constantesVariables as c
import random
from datetime import datetime
import funcionesGenericas as g

#FUNCION PRINCIPAL PARA CREAR CUENTA 

def crearCuenta():
    g.linea(y=2)
    g.linea(c='¯')

    nombre_usuario = pedirNombre()
    nombre_usuario = comprobarUsuario(nombre_usuario)

    g.linea(c='¯')

    passw = pedirPassw()
    passw = comprobarPassw(passw,nombre_usuario)
    
    g.linea()
    g.linea(c='_')
    g.bienvenida(nombre_usuario,passw)



    pedirDatos()
    saveUserPassw(nombre_usuario,passw)
    generaInfBancaria()
    

    return



#PIDE UN NOMBRE DE USUARIO Y COMPRUEBA QUE CUMPLA CON LOS REQUISITOS

def pedirNombre():
    nombre_usuario = input('Introduce un nombre de usuario: ')
    return nombre_usuario

def comprobarUsuario(nombre_usuario):

    while len(nombre_usuario) < 3 or nombre_usuario in c.informacion_clientes['usuario']:

        if len(nombre_usuario) < 3:
            print('El nombre de usuario tiene que tener mas de 3 caracteres')
        else:
            print('Este nombre de usuario ya ha sido usado')

        g.linea(c='_')    
        nombre_usuario = pedirNombre()

    return nombre_usuario

#PIDE UNA CONTRASEÑA Y COMPRUEBA QUE CUMPLA CON LOS REQUISITOS


def pedirPassw():
    passw = input('Introduce una contrasena para la cuenta: ')
    return passw


def comprobarPassw(passw,user):
    while len(passw) < 8 or not any(i.isupper() for i in passw) or not any(i.isdigit() for i in passw) or user.lower() in passw.lower():
        g.linea(c='_')

        if len(passw) < 8:
            print ('La contrasena debe de tener 8 o mas caracteres')
        if not any(i.isupper() for i in passw):
            print('La contrasena debe de tener almenos una mayuscula')
        if not any(i.isdigit() for i in passw):
            print ('La contrasena debe de tener al menos un numero')
        if user.upper() in passw.upper():
            print ('La contrasena no puede contener tu nombre de usuario')
        g.linea(c='¯')
        passw = pedirPassw()


    return passw



#PEDIR EL CONTENIDO DE LOS DATOS PERSONALES Y AUTOMATICAMENTE COMPROBAR QUE CUMPLEN CON LOS REQUISITOS 

def pedirDatos():
    print('DATOS PERSONALES')
    g.linea(c='¯')

    pide (x='nombre',y='Nombre: ',z=[3,10])
    pide (x='apellidos',y='Apellidos: ',z=[6,25],carc='ap')
    pide(x='DNI',y='DNI: ',z=[9,9],carc='ln')
    #FUNCION MAS COMPLICADA YA QUE TENEMOS QUE COMPROBAR QUE LOS PRIMEROS 8 CARACTERES SEAN NUMEROS Y 
    #QUE EL ULTIMO SEA UNA LETRA, ADEMAS DE QUE EN TOTAL TIENEN QUE SER 9 CIFRAS
    while not (g.comprobarStringCarcEsp(c.usuarioNuevo['DNI'][:8],tipo='n') and 
               g.comprobarStringCarcEsp(c.usuarioNuevo['DNI'][8],tipo='l')):
        
        print('DNI no válido')

        c.usuarioNuevo['DNI'] = input('DNI: ')
        pide(x='DNI',y='DNI: ',z=[9,9],carc='ln',first=False)
    
    pide (x='telefono',y='Telefono: ',z=[9,9],carc='n')
    pide (x='email', y='Correo electronico: ', z=[5,35],carc='e')
    pide (x='CP', y='Codigo postal: ', z=[5,5],carc='n')
    pide (x='direccion', y='Direccion: ', z=[6,30], carc='ln')

    guardarUserNuevo()


# COMPRUEBA SI EL ATRIBUTO CONTIENE UNA S AL FINAL PARA ESCRIBIR SI ES VALIDO O NO USANDO LA FUNCION DE COMPROBAR STRINGS

def pide(x,y,carc='l',z=None,first=True):

    if first:
        c.usuarioNuevo[x] = input(y).lower()

    while not g.comprobarStringCarcEsp(c.usuarioNuevo[x],long=z,tipo=carc):
        
        if x[-1] == 's':
            print(x.capitalize() + ' invalidos')
        else:
            print(x.capitalize() + ' no valido')
        g.linea(c='¯')

        c.usuarioNuevo[x] = input(y).lower()

    return c.usuarioNuevo[x]


#FUNCIONES PARA GUARDAR LA INFORMACION DE INICIO DE SESION 

def saveUserPassw(user,passw):
    with open ('informacionUsuarios/contrasena.txt', 'ta') as passwtx:
        passwtx.write(passw + '\n')
     
    with open ('informacionUsuarios/user.txt', 'ta') as usertx:
        usertx.write(user + '\n')

#GENERA LA INFORMACION BANCARIA ALEATORIA COMO EL NUMERO DE LA TARJETA Y INICALIZA LOS VALORES DE SALDO Y BALANCE A 0,
# GUARDA TODO EN LOS FICHEROS

def generaInfBancaria():
    with open ('informacionUsuarios/saldo.txt', 'ta') as saldotx:
        saldotx.write('0' + '\n')
    with open ('informacionUsuarios/balance.txt', 'ta') as balancetx:
        balancetx.write('0' + '\n')

    #UTILIZA LA FECHA DE HOY PARA AÑADIRLE 7 AÑOS Y ASI DATAR EL AÑO DE CADUCIDAD DE LA TARJETA TAL COMO SE HACE EN LOS BANCOS

    fechaHoy = datetime.now()
    fechaAñoStr = (int(fechaHoy.strftime('%Y')) + 7)
    fechaMesStr = (fechaHoy.strftime('%m'))
    fechaMesAñoStr = fechaMesStr + '/' + str(fechaAñoStr)[2:]

    with open ('informacionUsuarios/fechaCaducidad.txt', 'ta') as fechCadtx:
        fechCadtx.write(fechaMesAñoStr + '\n')
    with open ('informacionUsuarios/numTarjeta.txt', 'ta') as numTartx:
        numTartx.write(g.aleatorio(16) + '\n')
    with open ('informacionUsuarios/IBAN.txt', 'ta') as IBANtx:
        IBANtx.write('ES' + g.aleatorio(22) + '\n')

#GUARDA LA INFORMACION RESTANTE EN LOS FICHEROS
def guardarUserNuevo(user=c.usuarioNuevo):
    with open ('informacionUsuarios/nombreApellidos.txt', 'ta') as nApll:
        nApll.write(user['nombre'] + ' ' + user['apellidos'] + '\n')
    with open ('informacionUsuarios/DNI.txt', 'ta') as DNItx:
        DNItx.write(user['DNI'] + '\n')
    with open ('informacionUsuarios/telefono.txt', 'ta') as tel:
        tel.write(user['telefono'] + '\n')
    with open ('informacionUsuarios/email.txt', 'ta') as email:
        email.write(user['email'] + '\n')