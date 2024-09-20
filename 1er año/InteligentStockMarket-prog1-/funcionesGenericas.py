import constantesVariables as c
import random


#AQUI SE GUARDAN TODAS LAS FUNCIOONES GENERALES




#BIENVENIDA A USUARIOS QUE ACABAN DE REISTRARSE

def bienvenida(user,passw):

    frase = ('| BIENVENIDO A SU BANCO DE CONFIANZA (ISM) ' + user + ', NO COMPARTA NUNCA SU CONTRASEÑA ' + ocultarStrings(passw))
    print(' ' + ('_'*(len(frase)-1)))
    print(frase + '|')
    print(' ' + ('¯'*(len(frase)-1)))

#BIENVENIDA A USUARIOS QUE ACABAN DE INICIAR SESION

def bienvenida2(user):
    frase = ('| BIENVENIDO DE NUEVO ' + str(user) + ' A INTELIGENT STOCK MARKET, TE ECHABAMOS DE MENOS')
    print(' ' + ('_'*(len(frase)-1)))
    print(frase + '|')
    print(' ' + ('¯'*(len(frase)-1)))

#GENERADOR DE LINEAS AL GUSTO, OPCION DE MODIFICAR EL TAMAÑO Y LA CANTIDAD DE LAS LINEAS, ASI COMO EL CARACTER QUE LA COMPONGA
def linea(c='',y=1,x=80):
    linea = c
    for i in range (y):
        for i in range (x):
            linea = linea + c
        print(linea)
        linea = c
    return linea



#OCULTA CADENAS DE TEXTO AL GUSTO, OPCION DE MODIFICAR EL CARACTER QUE LAS OCULTA, LA POSICION Y LA CANTIDAD DE CARACTERES OCULTOS 

def ocultarStrings(strn, numCaract=None, caracter="*", posicion="aleatoria"):
    if numCaract is None:
        numCaract = len(strn) // 2

    nuevaStr = strn

    if posicion == "aleatoria":
        for i in range(numCaract):
            index = random.randint(0, len(nuevaStr) - 1)
            nuevaStr = nuevaStr[:index] + caracter + nuevaStr[index + 1:]
    else:

        if posicion == "final":
            nuevaStr = strn[:len(strn)-numCaract]  


        if posicion == "inicio":        
            nuevaStr = strn[numCaract:]
        for i in range(numCaract):
            nuevaStr = caracter + nuevaStr 

    return nuevaStr

#FUNCION QUE SE HIZO PRINCIPALMENTE PARA COMPROBAR SI UNA STRING TENIA CARACTERES ESPECIALES Y CON FORME 
# HEMOS NECESITADO MAS COMPROBACIONES Y FUNCIONES LAS HEMOS INSERTADO COMO LA DE LONIGTUD DE UNA STRINGS O 
# LA DE COMPROBAR SI UNA ESTRING ES NUMERICA O SI CONTIENE UNA ARROBA Y UN PUNTO PARA LOS EMAILS

def comprobarStringCarcEsp(strn,tipo = 'l',long = None):

    if long == None:
        long = [0,50]
    
    valido = False
    for i in range(len(strn)):
        if tipo == 'l' and (97 <= ord(strn[i].lower()) <= 122 or ord(strn[i].lower()) == 32):
            valido = True
        elif tipo == 'ap' and (97 <= ord(strn[i].lower()) <= 122 or ord(strn[i].lower()) == 32) and ' ' in strn:
            valido = True
            
        elif tipo == 'n' and 47 <= ord(strn[i]) <= 57:
            valido = True
        
        elif tipo == 'ln' and (47 <= ord(strn[i]) <= 57 or 97 <= ord(strn[i].lower()) <= 122 or ord(strn[i].lower()) == 32):
            valido = True

        else:           
            valido = False
            break
    if tipo == 'e' and '@' in strn and '.' in strn:
        valido = True

    if (long[0] <= len(strn) <= long[1]) and valido:
        valido = True
    else:
        valido = False

    return valido

#FUNCION QUE GENERA STRINGS DE X CIFRAS NUMERICAS 

def aleatorio(x):
    num=''
    for i in range(x):
        num=num + str(random.randint(0,9))
    return num

def stringEsp(strn,salto=4):
    strnEsp = ' '.join([strn[i:i+salto] for i in range(0, len(strn), salto)])
    return strnEsp

