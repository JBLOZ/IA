import random
import string

#AQUI SE GUARDAN TODAS LAS CLAVES DEL DICCIONARIO DE LISTAS QUE LUEGO VAN A SER USADAS PARA GUARDAR,
#LEER Y MANIPULAR INFORMACION DE UNA MANERA MAS SENCILLA
claves = [
    'usuario',
    'contraseña',
    'nombreApellidos',
    'numero de tarjeta',
    'fechaCaducidad',
    'IBAN',
    'saldo',
    'balance del mes',
    'DNI',
    'telefono',
    'email'
]
#AQUI SE GUARDAN LOS FICHEROS EN LOS QUE SE GUARDARA TODA LA INFORMACION, LA LISTA TIENE QUE SER DEL MISMO
#TAMAÑO QUE EL DE LAS CLAVES YA QUE CADA CLAVE CORRESPONDE A UN FICHERO

archivos = [
    'informacionUsuarios/user.txt',
    'informacionUsuarios/contrasena.txt',
    'informacionUsuarios/nombreApellidos.txt',
    'informacionUsuarios/numTarjeta.txt',
    'informacionUsuarios/fechaCaducidad.txt',
    'informacionUsuarios/IBAN.txt',
    'informacionUsuarios/saldo.txt',
    'informacionUsuarios/balance.txt',
    'informacionUsuarios/DNI.txt',
    'informacionUsuarios/telefono.txt',
    'informacionUsuarios/email.txt'
]

#SE INICIALIZA EL DICCINARIO CON TANTAS CLAVES COMO LARGA SEA LA LISTA 

informacion_clientes = {clave: [] for clave in claves}

# ESTA VARIABLE SE USA SOLO PARA EL USUARIO QUE INICIA SESION YA QUE AL NO GUARDAR DATOS COMO EL CODIGO POSTAL 
# O LA DIRECCION DE CORREO RESULTABA MAS FACIL QUE AÑADIRLO AL ANTERIOR DICCIONARIO
usuarioNuevo = {'nombre':'',
                'apellidos':'',
                'CP':'',
                'telefono':'',
                'provincia':'',
                'localidad':'',
                'direccion':'',
                'email':'',
                'DNI':''}

salgo = False

#FUNCION QUE RECORRE CADA LINEA DE CADA ARCHIVO Y GUARDA LAS STRINGS CONFORME A LAS CLAVES QUE HAYA GUARDADAS EN EL DICCIONARIO CON LOS VALORES EN FORMA DE LISTA
def leerArchivos():

    for archivo, clave in zip(archivos, claves):
        with open(archivo, 'r') as archivo_actual:
            lineas = archivo_actual.readlines()
            informacion_clientes[clave] = [linea.strip() for linea in lineas]

#FUNCION QUE ESCRIBE CADA VALOR DEL DICCIONARIO DE LISTAS DE CLIENTES Y LAS SOBRE ESCRIBE EN LOS FICHEROS LINEA POR LINEA
def escribir_en_archivos():
    for clave, archivo in zip(informacion_clientes.keys(), archivos):
        with open(archivo, 'w') as archivo_actual:
            for elemento in informacion_clientes[clave]:
                archivo_actual.write(f"{elemento}\n")





                
