import constantesVariables as c
import funcionesGenericas as g
import crearCuenta as CC
import random


#FUNCION PRINCIPAL DE INICIAR SESION, COMPRUEBA QUE LA CONTRASEÑA COINCIDA CON EL USUARIO Y 
#DEVUELVE EL NUMERO DE CLIENTE QUE CORRESPONDERÁ AL HUECO DE LA LISTA DE LOS VALORES DEL DICCIONARIO EN LA QUE 
# ESTARAN GUARDADOS LOS DATOS DE LOS USUARIOS

def iniciarSesion():
    
    cliente = comprobarCredenciales()
    if cliente == None:
        return
    
    g.linea()
    g.bienvenida2(c.informacion_clientes['usuario'][cliente])
    infoCuenta(cliente)
    
    g.linea()
    menu(cliente)







def comprobarCredenciales():
    n = 0
    

    while n < 3:
        print('╔══════════════════════════════════════════════════════════════════')    
        usuario_iniciando = input('║ Introduce el usuario para iniciar sesión: ')
        contrasena_iniciando = input('║ Introduce la contraseña para iniciar sesión: ')
        print('╚══════════════════════════════════════════════════════════════════')

        for i in range (len(c.informacion_clientes['usuario'])):
            if c.informacion_clientes['usuario'][i] == usuario_iniciando and c.informacion_clientes['contraseña'][i] == contrasena_iniciando:
                cliente = i

                


                return cliente
     
        print('Usuario o contraseña incorrectos.')
        n = n + 1      

    return None    
                

#PROPORCIONA LA INFORMACION DE LA CUENTA DEL CLIENTE QUE HA INICIADO SESION 

def infoCuenta(cliente,oculto=True,operacion=False):
    print("INFORMACION DEL USUARIO")
    print(c.informacion_clientes['nombreApellidos'][cliente].upper())
    g.linea()
    
    print('╔═════════════════════════════════════════════════════════════════╗')
    
    print('║' + 'USUARIO: ' + c.informacion_clientes['usuario'][cliente], end = ' ') 
    print((64-(len('USUARIO: ') + len(c.informacion_clientes['usuario'][cliente]))) * ' ' + '║')
    if not operacion:
        print('║' +'CONTRASEÑA: ' + g.ocultarStrings(c.informacion_clientes['contraseña'][cliente]),end='')
        print((65-(len('CONTRASEÑA: ') + len(c.informacion_clientes['contraseña'][cliente]))) * ' ' + '║')

    print('║' +'SALDO: ' + str(round(float(c.informacion_clientes['saldo'][cliente]),2)) + '€',end='')
    print((64-(len('SALDO: ') + len(str(round(float(c.informacion_clientes['saldo'][cliente]),2))))) * ' ' + '║')
    if not operacion:
        if oculto:
            print('║' +'NUMERO DE TARJETA: ' + g.stringEsp(g.ocultarStrings(c.informacion_clientes['numero de tarjeta'][cliente],posicion='inicio',numCaract=12)),end='')
            print((62-(len('NUMERO DE TARJETA: ') + len(c.informacion_clientes['numero de tarjeta'][cliente]))) * ' ' + '║')

            print('║' +'FECHA DE CADUCIDAD: ' + g.ocultarStrings(c.informacion_clientes['fechaCaducidad'][cliente],posicion='inicio',numCaract=5),end='')
            print((65-(len('FECHA DE CADUCIDAD: ') + len(c.informacion_clientes['fechaCaducidad'][cliente]))) * ' ' + '║')

            print('║' +'IBAN: ' + c.informacion_clientes['IBAN'][cliente][:4] + ' **** **** **** **** ' + c.informacion_clientes['IBAN'][cliente][20::],end='')
            print((60-(len('IBAN: ') + len(c.informacion_clientes['IBAN'][cliente]))) * ' ' + '║')
        else:
            print('║' +'NUMERO DE TARJETA: ' + g.stringEsp(c.informacion_clientes['numero de tarjeta'][cliente]),end='')
            print((62-(len('NUMERO DE TARJETA: ') + len(c.informacion_clientes['numero de tarjeta'][cliente]))) * ' ' + '║')

            print('║' +'FECHA DE CADUCIDAD: ' + c.informacion_clientes['fechaCaducidad'][cliente],end='')
            print((65-(len('FECHA DE CADUCIDAD: ') + len(c.informacion_clientes['fechaCaducidad'][cliente]))) * ' ' + '║')
        
            print('║' +'IBAN: ' + g.stringEsp(c.informacion_clientes['IBAN'][cliente],salto=4),end='')
            print((60-(len('IBAN: ') + len(c.informacion_clientes['IBAN'][cliente]))) * ' ' + '║')
        
    print('║' +'BALANCE DEL MES: ' + str(round(float(c.informacion_clientes['balance del mes'][cliente]),2)) + '€',end='')
    print((64-(len('BALANCE DEL MES: ') + len(str(round(float(c.informacion_clientes['balance del mes'][cliente]),2))))) * ' ' + '║')
    
    print('╚═════════════════════════════════════════════════════════════════╝')


#MUESTRA EL MENU DE OPCIONES PARA EL USUARIO Y LLAMA A LAS FUNCIONES QUE EL USUARIO TIENE A SU DISPOSICION

def menu(cliente): 
    while c.salgo==False:

        c.escribir_en_archivos()
        g.linea()
        print('╔═════════════════════════════════════════════════════════════════╗')
        print('║                       MENU DE OPCIONES                          ║')
        print('╠═════════════════════════════════════════════════════════════════╣')
        print('║                (1)     Ingresar dinero                          ║')
        print('║                (2)      Sacar dinero                            ║')
        print('║                (3)    Transferir dinero                         ║')
        print('║                (4) Informacion de la cuenta                     ║')
        print('║                (5)    Cambiar contraseña                        ║')
        print('║                (6)          Salir                               ║')
        print('╚═════════════════════════════════════════════════════════════════╝')
        opcion=input('Elige una opción: ')

        g.linea()

        if opcion=='1':
            op1_ingreso(cliente)
        elif opcion=='2':
            op2_sacar(cliente)
        elif opcion=='3':
            if(float(c.informacion_clientes['saldo'][cliente]) > 0):
                op3_transferir(cliente)
            else:
                #Referencia a SIRI
                print('No se pueden hacer trasferencias sin dinero, imagínate que tienes cero galletas y la repartes entre cero amigos.')
                print('¿Cuántas galletas le tocan a cada amigo? No tiene sentido, ¿lo ves? Intenta conseguir alguna galleta antes de que') 
                print('el mounstruo de las galletas se coma a los pocos amigos que te quedan por no tener galletas para darle.')
            
        elif opcion=='4':
            op4_info(cliente)
        elif opcion == '5':
            op5_cambiar_contraseña(cliente)
        elif opcion == '6':
            c.salgo = True
        else:
            print('Opción incorrecta.')
    return




#A CONTINUACION ESTAN TODAS LAS OPCIONES DEL MENU, HACEN OPERACIONES CON EL DICCIONARIO DE LISTAS (INFORMACION_CLIENTES) Y 
#VUELVEN AL MENU PRINCIPAL DONDE SE ESCRIBEN EN LOS FICHEROS LA INFORMACION RECOLECTADA  

def op1_ingreso(cliente):
    ingreso = float(input('Introduce la cantidad a ingresar: '))
    while ingreso < 0:
        print('no puedes introducir una cantidad negativa')
        ingreso = float(input('Introduce la cantidad a ingresar: '))

    g.linea('_')

    c.informacion_clientes['saldo'][cliente] = str(float(c.informacion_clientes['saldo'][cliente]) + ingreso)
    c.informacion_clientes['balance del mes'][cliente]= str(float(c.informacion_clientes['balance del mes'][cliente]) + ingreso)

    infoCuenta(cliente,operacion=True)
    g.linea()

    return
    
    



           
        
def op2_sacar (cliente):
    
   
    cantidad = float(input('Introduce la cantidad a sacar: '))
    g.linea('_')
    while (cantidad > float(c.informacion_clientes['saldo'][cliente]) or cantidad < 0):
        if cantidad < 0:
            print('no puedes introducir una cantidad negativa')
        else:
            print('Fondos insuficientes')

        cantidad = float(input('Vuelva a introducir el importe, siempre menor a su saldo de ' + str(c.informacion_clientes['saldo'][cliente])+ '€: '))

    if cantidad >= float(c.informacion_clientes['saldo'][cliente])/2:
        print('Disculpa pero al intentar obtener una cantidad que iguala o supera el 50% de dinero')
        print('de tu cuenta necesitamos una confirmación.')
        g.linea(c='¯')
        if falloContraseñas(cliente):
            return
        else:
            sacarDinero(cliente,cantidad)
                 
    else:
        sacarDinero(cliente,cantidad)

    return


def sacarDinero(cliente,cantidad):
    c.informacion_clientes['saldo'][cliente] = str(float(c.informacion_clientes['saldo'][cliente]) - cantidad)
    c.informacion_clientes['balance del mes'][cliente]= str(float(c.informacion_clientes['balance del mes'][cliente]) - cantidad)

    infoCuenta(cliente,operacion=True)
    g.linea()    

    return




    

def op3_transferir (cliente):

    cobrador = bizumTransferencia(cliente)
    s = input('Desea transferir dinero a ' + c.informacion_clientes['nombreApellidos'][cobrador].upper() + ' ? (s/n): ')
    if s.upper() == 'S':

        cantidad = float(input('Introduce el dinero que se va a transferir: '))

        g.linea('_')

        while (cantidad >= float(c.informacion_clientes['saldo'][cliente]) or cantidad < 0):
            if cantidad < 0:
                print('no puedes introducir una cantidad negativa')
            else:
                print('Fondos insuficientes')

            cantidad = float(input('Vuelva a introducir el importe, siempre menor a su saldo de ' + str(c.informacion_clientes['saldo'][cliente])+ '€: '))


        if cantidad >= float(c.informacion_clientes['saldo'][cliente])/2:
            print('Disculpa pero al intentar transferir una cantidad que iguala o supera el 50% de dinero')
            print('de tu cuenta necesitamos una confirmación.')
            g.linea(c='¯')

            if falloContraseñas(cliente):
                return
            else:
                traspaso(cliente,cobrador,cantidad)
            
        else:
            traspaso(cliente,cobrador,cantidad)
    return


#FUNCION QUE SIRVE PARA COMPARAR Y BUSCAR POR NUMERO O POR IBAN PARA HACER UN TRASPASO DE DINERO A OTRA CUENTA

def bizumTransferencia(cliente):

    encontrado = False
    tipo=''

    while tipo != 'b' and tipo != 't':
        tipo=input('Que desea realizar, bizum o transferencia? (b/t): ')

    if tipo == 'b':
        while encontrado == False:
            tel=input('Introduce el numero de telefono del cobrador del bizum: ')
            for i in range (len(c.informacion_clientes['telefono'])):

                if tel == c.informacion_clientes['telefono'][i] and c.informacion_clientes['telefono'][cliente] != c.informacion_clientes['telefono'][i]:
                    cobrador = i
                    encontrado = True
                

    elif tipo == 't':

        while encontrado == False:
            IBAN=input('Introduce el numero IBAN (de ISM) de la cuenta del cobrador de la transferencia: ')
            for i in range (len(c.informacion_clientes['IBAN'])):

                if IBAN == c.informacion_clientes['IBAN'][i] and c.informacion_clientes['IBAN'][cliente] != c.informacion_clientes['IBAN'][i]:
                    cobrador = i
                    encontrado = True
                

    return cobrador


def traspaso (cliente,cobrador,cantidad):
    
    c.informacion_clientes['saldo'][cliente] = str(float(c.informacion_clientes['saldo'][cliente]) - cantidad)
    c.informacion_clientes['balance del mes'][cliente]= str(float(c.informacion_clientes['balance del mes'][cliente]) - cantidad)


    c.informacion_clientes['saldo'][cobrador]= str(float(c.informacion_clientes['saldo'][cobrador]) + cantidad)
    c.informacion_clientes['balance del mes'][cobrador]= str(float(c.informacion_clientes['balance del mes'][cobrador]) + cantidad)

    
    infoCuenta(cliente,operacion=True)
 

    return   
        
def op4_info(cliente):

    sensible = input('Desea ver informacion sensible de la cuenta, como el numero de cuenta, etc? (s/n)')
    if sensible == 's':

        if falloContraseñas(cliente):
            return
        else:
            infoCuenta(cliente,oculto=False)    
            return

    else:
        infoCuenta(cliente,oculto=True)


def op5_cambiar_contraseña(cliente):
   if falloContraseñas(cliente):
       return
   else:
        passw = CC.pedirPassw()
        passw = CC.comprobarPassw(passw,c.informacion_clientes['usuario'][cliente])
        c.informacion_clientes['contraseña'][cliente] = passw
   


#FUNCION PARA CUANDO QUERAMOS COMPROBAR QUE EL USUARIO SE SABE LA CONTRASEÑA Y TIENE PERMITIDO HACER CIERTAS OPERACIONES

def falloContraseñas(cliente,fallos=3):
    passw=input('Introduce tu contraseña porfavor: ')
    n = 0
    while passw != c.informacion_clientes['contraseña'][cliente]:

        print('Contraseña incorrecta.')
        g.linea('_')
        if n == (fallos-1):
            g.linea()
            g.linea('<>',x=39)
            g.linea('═')
            print('  FALLASTE DEMASIADAS VECES LA CONTRASEÑA, TENDRAS QUE VOLVER A INICIAR SESION')
            g.linea('═')
            g.linea('<>',x=39)
            c.salgo = True
            return True
            
        passw=input('Introduce tu contraseña por favor: ')
        n = n + 1
    return False
