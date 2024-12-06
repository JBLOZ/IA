import numpy as np
from scipy import stats

# Configuración de la población
NUM_INDIVIDUOS = 1010
MU_EDAD = 40
SIGMA_EDAD = 11
PROPORCION_MUJERES = 0.41

# Probabilidades de contagio según edad y sexo
PROB_CONTAGIO_MUJER = {
    'joven': 0.07,   # Menor de 30 años
    'adulto': 0.10,  # Entre 31 y 60 años
    'mayor': 0.13    # Mayor de 60 años
}

PROB_CONTAGIO_HOMBRE = {
    'joven': 0.03,
    'adulto': 0.07,
    'mayor': 0.11
}

# Probabilidad de mortalidad después de la infección
PROB_MORTALIDAD = 0.02  # 2%

# Tiempo que un individuo permanece infectado antes de recuperarse o fallecer
TIEMPO_INFECCION = 15

# Función para asignar el grupo de edad
def grupo_edad(edad):
    if edad < 30:
        return 'joven'
    elif 31 <= edad <= 60:
        return 'adulto'
    else:
        return 'mayor'

# Clase que representa a un individuo
class Individuo:
    def __init__(self, id):
        self.id = id
        self.edad = np.clip(np.random.normal(MU_EDAD, SIGMA_EDAD), 0, 104)
        self.sexo = np.random.choice(['Mujer', 'Hombre'], p=[PROPORCION_MUJERES, 1 - PROPORCION_MUJERES])
        self.estado = 'sano'  # sano, infectado, recuperado, fallecido
        self.tiempo_infectado = 0

    def probabilidad_contagio(self):
        grupo = grupo_edad(self.edad)
        if self.sexo == 'Mujer':
            return PROB_CONTAGIO_MUJER[grupo]
        else:
            return PROB_CONTAGIO_HOMBRE[grupo]

# Clase que representa la población
class Poblacion:
    def __init__(self, num_individuos):
        self.individuos = [Individuo(i) for i in range(num_individuos)]
        # Inicializar con un infectado aleatorio
        infectado_inicial = np.random.choice(self.individuos)
        infectado_inicial.estado = 'infectado'
        infectado_inicial.tiempo_infectado = 0
        self.tiempo = 0
        self.total_contagiados = 1  # Inicialmente un infectado

    def ciclo(self):
        while any(ind.estado == 'infectado' for ind in self.individuos):
            self.tiempo += 1
            nuevos_infectados = []
            for ind in self.individuos:
                if ind.estado == 'infectado':
                    ind.tiempo_infectado += 1
                    # Intentar contagiar a otros individuos sanos
                    for otro_ind in self.individuos:
                        if otro_ind.estado == 'sano':
                            if np.random.rand() < ind.probabilidad_contagio():
                                nuevos_infectados.append(otro_ind)
                    # Verificar si debe recuperarse o fallecer
                    if ind.tiempo_infectado >= TIEMPO_INFECCION:
                        if np.random.rand() < PROB_MORTALIDAD:
                            ind.estado = 'fallecido'
                        else:
                            ind.estado = 'recuperado'
            # Actualizar estados de los nuevos infectados
            for ind in nuevos_infectados:
                ind.estado = 'infectado'
                ind.tiempo_infectado = 0
                self.total_contagiados += 1

        # Contar resultados finales
        num_fallecidos = sum(1 for ind in self.individuos if ind.estado == 'fallecido')
        num_recuperados = sum(1 for ind in self.individuos if ind.estado == 'recuperado')
        num_sanos = sum(1 for ind in self.individuos if ind.estado == 'sano')
        return self.tiempo, num_fallecidos, self.total_contagiados, num_sanos

# Función para calcular el intervalo de confianza al 90%
def intervalo_confianza(data, confianza=0.90):
    n = len(data)
    media = np.mean(data)
    error_estandar = stats.sem(data)
    h = error_estandar * stats.t.ppf((1 + confianza) / 2., n - 1)
    return media, media - h, media + h

# Simulación de 200 repeticiones
num_simulaciones = 200
resultados_iteraciones = []
resultados_fallecidos = []
resultados_contagiados = []
resultados_sanos = []

for _ in range(num_simulaciones):
    poblacion = Poblacion(NUM_INDIVIDUOS)
    iteraciones, fallecidos, contagiados, sanos = poblacion.ciclo()
    resultados_iteraciones.append(iteraciones)
    resultados_fallecidos.append(fallecidos)
    resultados_contagiados.append(contagiados)
    resultados_sanos.append(sanos)

# Calcular intervalos de confianza para cada valor
media_iter, inf_iter, sup_iter = intervalo_confianza(resultados_iteraciones)
media_fallecidos, inf_fallecidos, sup_fallecidos = intervalo_confianza(resultados_fallecidos)
media_contagiados, inf_contagiados, sup_contagiados = intervalo_confianza(resultados_contagiados)
media_sanos, inf_sanos, sup_sanos = intervalo_confianza(resultados_sanos)

# Imprimir resultados
print("Intervalos de confianza al 90%:")
print(f"Numero de iteraciones hasta 0 infectados: Media={media_iter:.5f}, IC=[{inf_iter:.5f}, {sup_iter:.5f}]")
print(f"Numero de fallecidos: Media={media_fallecidos:.5f}, IC=[{inf_fallecidos:.5f}, {sup_fallecidos:.5f}]")
print(f"Numero de contagiados: Media={media_contagiados:.5f}, IC=[{inf_contagiados:.5f}, {sup_contagiados:.5f}]")
print(f"Numero de sanos: Media={media_sanos:.5f}, IC=[{inf_sanos:.5f}, {sup_sanos:.5f}]")
