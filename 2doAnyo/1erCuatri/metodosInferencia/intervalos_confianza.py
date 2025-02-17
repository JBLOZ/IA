import numpy as np

def ejercicio1(lista, Zpr_derecha_alpha_medios, var):
    media = np.mean(lista)
    
    # Guardar el número de elementos en la lista
    n = len(lista)

    # Calcular los valores de a y b
    a = media - Zpr_derecha_alpha_medios * (var / np.sqrt(n))
    b = media + Zpr_derecha_alpha_medios * (var / np.sqrt(n))

    return a, b

lista = [4.74,1.51,3.93,3.06,0.47,0.21,1.77,0.6,0.63,4.2,1.13,0.02,2.23,1.18,2.9,2.05]
Zpr_derecha_alpha_medios = 1.7506860712522 # normal 0, 1, cola derecha, alpha medios
var = 8/5

print(ejercicio1(lista, var,Zpr_derecha_alpha_medios))


def ejercicio2(lista, cola_izquierda, cola_derecha):
       media = np.mean(lista)
       cuasivarianza = np.var(lista, ddof=1)
       n = len(lista)
       a = ((n - 1)*(cuasivarianza)) / cola_derecha
       b = ((n - 1)*(cuasivarianza)) / cola_izquierda
       return a, b


lista = [4.25,0.09,1.22,2.27,3.35,3.42,0.04,4.06,0.34,4.75,0.57,3.52,0.37,2.02,3.45]
cola_izquierda = 5.0572413340227 #chi cuadr, glib = n - 1, area = alpha medios
cola_derecha = 27.8267769432232
print(ejercicio2(lista, cola_izquierda, cola_derecha))





def ejercicio3(lista, tstudent):
     media = np.mean(lista)
     n = len(lista)
     square_cuasivarianza = np.sqrt(np.var(lista, ddof=1))
     a = media - (tstudent * (square_cuasivarianza/np.sqrt(n)))
     b = media + (tstudent * (square_cuasivarianza/np.sqrt(n)))

     return a, b

lista = [4.98,1.91,2.36,3.99,1.6,1.21,0.84,2.16,2.53,0.51,0.46,1.28,3.78,3.52]
tstudent = 1.831699767895 #Cola derecha glib = n-1 ,Glib = alpha medios 
print(ejercicio3(lista, tstudent))



def ejercicio4(lista1, lista2, Z):
     media1 = np.mean(lista1)
     media2 = np.mean(lista2)
     n1 = len(lista1)
     n2 = len(lista2)
     cuasivarianza1 = np.var(lista1, ddof=1)
     cuasivarianza2 = np.var(lista2, ddof=1)

     amplitud = Z * np.sqrt((cuasivarianza1/n1) + (cuasivarianza2/n2))
     centro = media1 - media2

     a = centro - amplitud #limite inferior
     b = centro + amplitud #limite superior

     return a, b



Z = 2.5758293035489 #normal 0, 1, cola derecha, alpha medios
lista1 = [0.82,0.22,2.65,3.72,0.84,4.18,4.74,2.82,1.07,1.26,1.56,4.88,4.11,0.7,4.27,0.12,1.54,3.59]
lista2 = [3.17,3.06,4.4,1.48,2.54,3.68,0.7,4.84,1.77,3.29,0.11,1.07,0.75,1.46]
print(ejercicio4(lista1, lista2, Z))






def ejercicio5(lista1, lista2, tstudent):
     media1 = np.mean(lista1)
     media2 = np.mean(lista2)
     n1 = len(lista1)
     n2 = len(lista2)
     cuasivarianza1 = np.var(lista1, ddof=1)
     cuasivarianza2 = np.var(lista2, ddof=1)
     
     ST_cuadrado = ((n1 - 1) * cuasivarianza1 + (n2 - 1) * cuasivarianza2) / (n1 + n2 - 2)
     ST = np.sqrt(ST_cuadrado)
     amplitud = tstudent * ST * np.sqrt(1/n1 + 1/n2)
     centro = media1 - media2
     
     a = centro - amplitud
     b = centro + amplitud

     return a, b

tstudent = 2.4671400978338 #tsutend Glib = n1 + n2 - 2, area = alpha medios, cola derecha
lista1 = [0.23,4.83,3.49,3.4,0.83,3.14,0.37,4.94,1.56,2.1,0.7,2.52,0.23]
lista2 = [4.91,3.79,3.24,1.15,4.7,1.1,4.73,1.79,4.85,4.62,0.23,0.16,2.8,0.65,2.12]
print(ejercicio5(lista1, lista2, tstudent))



def ejercicio6(favorable, muestratotal, Z):
     p = favorable / muestratotal
     n = muestratotal

     a = p - (Z * (np.sqrt((p * (1-p))/n)))
     b = p + (Z * (np.sqrt((p * (1-p))/n)))

     return a, b



Z = 1.8119106729526 #Normal cola derecha, 0, 1, area = alpha medios
favorable = 155
muestratotal = 171
print(ejercicio6(favorable, muestratotal, Z))



def ejercicio7(Z, L):
     valor_raro = 0.25

     n = ((Z ** 2) * valor_raro)/ (L ** 2)
     numero_redondeado = int(n) + (1 if n % 1 != 0 else 0)

     return numero_redondeado




Z = -1.8807936081513 #Cola izquierda normal 0, 1, alpha medios
L = 0.111

print(ejercicio7(Z, L))