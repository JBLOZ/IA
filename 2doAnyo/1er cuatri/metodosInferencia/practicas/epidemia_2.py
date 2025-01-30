import numpy as np
from scipy import stats

########################################################
#######    Constantes y Parámetros
########################################################
cont_ID = 0  # Contador de ID
dist_contagi = 0.05
temps_contagi = 15
grid_size = 0.1

########################################################
#######    Persona
########################################################
class Persona:
    def __init__(self, area=(0, 1, 0, 1), barrio=None, reduccion_movilidad=False):
        global cont_ID
        cont_ID += 1
        self.ID = cont_ID
        self.edat = np.random.normal(37, 12)
        while self.edat < 0:
            self.edat = np.random.normal(37, 12)
        self.sexe = 'Dona' if np.random.rand() < 0.6 else 'Home'
        self.estat = 'sa'  # Estados posibles: sa, infectat, contagiat, mort
        self.Vx = np.random.uniform(-0.01, 0.01)
        self.Vy = np.random.uniform(-0.01, 0.01)
        self.tcont = 0  # Tiempo de contagio
        self.barrio = barrio
        self.reduccion_movilidad = reduccion_movilidad
        self.area = area  # (xmin, xmax, ymin, ymax)
        self.Posx = np.random.uniform(self.area[0], self.area[1])
        self.Posy = np.random.uniform(self.area[2], self.area[3])

    def moverse(self):
        self.Posx += self.Vx
        self.Posy += self.Vy

        # Aplicar límites según reducción de movilidad
        if self.reduccion_movilidad and self.barrio is not None:
            xmin, xmax, ymin, ymax = self.area
            if self.Posx <= xmin or self.Posx >= xmax:
                self.Vx *= -1
                self.Posx = max(xmin, min(self.Posx, xmax))
            if self.Posy <= ymin or self.Posy >= ymax:
                self.Vy *= -1
                self.Posy = max(ymin, min(self.Posy, ymax))
        else:
            # Área total sin restricciones
            if self.Posx <= 0 or self.Posx >= 2:
                self.Vx *= -1
                self.Posx = max(0, min(self.Posx, 2))
            if self.Posy <= 0 or self.Posy >= 2:
                self.Vy *= -1
                self.Posy = max(0, min(self.Posy, 2))

########################################################
#######    Población
########################################################
class Poblacio:
    def __init__(self, name):
        self.name = name
        self.tt = 0  # Tiempo
        self.individuos = []
        self.cuadricula = {}

    def agregar_persona(self, persona):
        self.individuos.append(persona)

    def actualizar(self):
        self.cuadricula = {}
        for p in self.individuos:
            cell = (int(p.Posx // grid_size), int(p.Posy // grid_size))
            if cell not in self.cuadricula:
                self.cuadricula[cell] = []
            self.cuadricula[cell].append(p)

    def moverse(self):
        for p in self.individuos:
            p.moverse()
        self.actualizar()

    def evoluciona(self):
        self.tt += 1
        self.moverse()
        for cell in self.cuadricula.keys():
            individuos_en_celda = self.cuadricula[cell]
            for p1 in individuos_en_celda:
                if p1.estat == 'infectat':
                    vecinos = self.obtener_vecinos(cell)
                    for p2 in vecinos:
                        if p2.estat == 'sa' and p1 != p2:
                            d = dist(p1, p2)
                            if d < dist_contagi:
                                prob_cont = prob_contagio(p1)
                                if np.random.rand() < prob_cont:
                                    p2.estat = 'infectat'
                                    p2.tcont = self.tt
        # Actualizar estados
        for p in self.individuos:
            if p.estat == 'infectat' and self.tt - p.tcont > temps_contagi:
                mort_prob = prob_mortalidad(p)
                if np.random.rand() < mort_prob:
                    p.estat = 'mort'
                else:
                    p.estat = 'contagiat'

    def obtener_vecinos(self, cell):
        vecinos = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                vecino_cell = (cell[0] + dx, cell[1] + dy)
                if vecino_cell in self.cuadricula:
                    vecinos.extend(self.cuadricula[vecino_cell])
        return vecinos

    def contador_info(self):
        counts = {'sa': 0, 'infectat': 0, 'contagiat': 0, 'mort': 0}
        for p in self.individuos:
            counts[p.estat] += 1
        return counts

    def ciclo(self):
        self.tt = 0
        while any(p.estat == 'infectat' for p in self.individuos) and self.tt < 200:
            self.evoluciona()
        counts = self.contador_info()
        num_iteraciones = self.tt
        num_muertos = counts['mort']
        num_contagiados = counts['contagiat']
        num_sanos = counts['sa']
        return num_iteraciones, num_muertos, num_contagiados, num_sanos

########################################################
#######    Funciones Auxiliares
########################################################
def dist(p1, p2):
    return np.hypot(p1.Posx - p2.Posx, p1.Posy - p2.Posy)

def prob_contagio(p):
    if p.sexe == 'Dona':
        if p.edat < 30:
            return 0.07
        elif p.edat <= 60:
            return 0.10
        else:
            return 0.13
    else:
        if p.edat < 30:
            return 0.03
        elif p.edat <= 60:
            return 0.07
        else:
            return 0.11

def prob_mortalidad(p):
    if p.edat < 30:
        return 0.005
    elif p.edat <= 60:
        return 0.02
    else:
        return 0.1

def calcular_intervalo(data, confianza=0.90):
    n = len(data)
    media = np.mean(data)
    std_dev = np.std(data, ddof=1)
    se = std_dev / np.sqrt(n)
    z = stats.norm.ppf(1 - (1 - confianza) / 2)
    margen_de_error = z * se
    return media, (media - margen_de_error, media + margen_de_error)

########################################################
#######    Simulación en Área Ampliada [0,2]x[0,2]
########################################################
def simular_pandemia_area_ampliada(tamano_poblacion=1000, n_infectados_iniciales=1):
    global cont_ID
    cont_ID = 0  # Reiniciar ID
    area_total = (0, 2, 0, 2)
    poblacion = Poblacio('Área Ampliada')

    # Crear personas sanas
    for _ in range(tamano_poblacion - n_infectados_iniciales):
        persona = Persona(area=area_total)
        poblacion.agregar_persona(persona)

    # Crear personas infectadas inicialmente
    for _ in range(n_infectados_iniciales):
        persona = Persona(area=area_total)
        persona.estat = 'infectat'
        poblacion.agregar_persona(persona)

    n_iter, num_muertos, num_contagiados, num_sanos = poblacion.ciclo()
    return num_muertos

def main_simulaciones_area_ampliada(num_simulaciones=200):
    resultados_muertos = []
    for sim_num in range(num_simulaciones):
        fallecidos = simular_pandemia_area_ampliada()
        resultados_muertos.append(fallecidos)
    return resultados_muertos

########################################################
#######    Simulación con Dos Barrios
########################################################
def simular_pandemia_dos_barrios(tamano_poblacion=1000, n_infectados_iniciales=1, reduccion_movilidad=True):
    global cont_ID
    cont_ID = 0  # Reiniciar ID
    poblacion = Poblacio('Dos Barrios')

    # Definir áreas de los barrios
    area_barrio1 = (0, 1, 0, 2)
    area_barrio2 = (1, 2, 0, 2)

    # Crear personas sanas en barrio 1
    for _ in range(tamano_poblacion // 2):
        persona = Persona(area=area_barrio1, barrio=1, reduccion_movilidad=reduccion_movilidad)
        poblacion.agregar_persona(persona)

    # Crear personas sanas en barrio 2
    for _ in range(tamano_poblacion // 2):
        persona = Persona(area=area_barrio2, barrio=2, reduccion_movilidad=reduccion_movilidad)
        poblacion.agregar_persona(persona)

    # Infectar inicialmente a una persona aleatoria
    total_personas = poblacion.individuos.copy()
    np.random.shuffle(total_personas)
    infectados_iniciales = total_personas[:n_infectados_iniciales]
    for persona in infectados_iniciales:
        persona.estat = 'infectat'

    # Si no hay reducción de movilidad, las personas pueden moverse libremente
    if not reduccion_movilidad:
        for persona in poblacion.individuos:
            persona.reduccion_movilidad = False

    n_iter, num_muertos, num_contagiados, num_sanos = poblacion.ciclo()
    return num_muertos

def main_simulaciones_dos_barrios(num_simulaciones=200, reduccion_movilidad=True):
    resultados_muertos = []
    for sim_num in range(num_simulaciones):
        fallecidos = simular_pandemia_dos_barrios(reduccion_movilidad=reduccion_movilidad)
        resultados_muertos.append(fallecidos)
    return resultados_muertos

########################################################
#######    Ejecución y Análisis Estadístico
########################################################
if __name__ == "__main__":
    num_simulaciones = 200

    # Simulación en Área Ampliada
    print("\nSimulando población en área ampliada [0,2]x[0,2]...")
    resultados_muertos_area_ampliada = main_simulaciones_area_ampliada(num_simulaciones=num_simulaciones)

    # Simulación en Área Original [0,1]x[0,1]
    print("\nSimulando población en área original [0,1]x[0,1]...")
    resultados_muertos_area_original = []
    for sim_num in range(num_simulaciones):
        # Inicializar población con 999 individuos y 1 infectado
        cont_ID = 0  # Reiniciar ID
        poblacion = Poblacio('Área Original')
        for _ in range(1000 - 1):
            persona = Persona()
            poblacion.agregar_persona(persona)
        persona_infectada = Persona()
        persona_infectada.estat = 'infectat'
        poblacion.agregar_persona(persona_infectada)
        n_iter, num_muertos, num_contagiados, num_sanos = poblacion.ciclo()
        resultados_muertos_area_original.append(num_muertos)

    # Análisis Estadístico entre Área Ampliada y Área Original
    media_original, intervalo_original = calcular_intervalo(resultados_muertos_area_original, confianza=0.90)
    media_ampliada, intervalo_ampliada = calcular_intervalo(resultados_muertos_area_ampliada, confianza=0.90)

    # Test de Levene para igualdad de varianzas
    stat_levene_area, p_levene_area = stats.levene(resultados_muertos_area_original, resultados_muertos_area_ampliada)

    # Elegir el test t apropiado según igualdad de varianzas
    if p_levene_area > 0.05:
        # Asumimos varianzas iguales
        t_statistic_area, p_value_area = stats.ttest_ind(
            resultados_muertos_area_original, resultados_muertos_area_ampliada, equal_var=True
        )
    else:
        # No asumimos varianzas iguales
        t_statistic_area, p_value_area = stats.ttest_ind(
            resultados_muertos_area_original, resultados_muertos_area_ampliada, equal_var=False
        )

    print("\nComparación Área Original vs Área Ampliada:")
    print(f"Media de fallecidos en Área Original: {media_original:.2f}, Intervalo al 90%: {intervalo_original}")
    print(f"Media de fallecidos en Área Ampliada: {media_ampliada:.2f}, Intervalo al 90%: {intervalo_ampliada}")
    print(f"Test de Levene: Estadístico = {stat_levene_area:.4f}, p-value = {p_levene_area:.4f}")
    print(f"Estadístico t: {t_statistic_area:.4f}, Valor p: {p_value_area:.4f}")

    # Interpretación de resultados
    if p_value_area < 0.05:
        print("Hay una diferencia significativa en la media de fallecidos entre las dos áreas.")
    else:
        print("No hay una diferencia significativa en la media de fallecidos entre las dos áreas.")

    if p_levene_area < 0.05:
        print("Hay una diferencia significativa en la variabilidad de fallecidos entre las dos áreas.")
    else:
        print("No hay una diferencia significativa en la variabilidad de fallecidos entre las dos áreas.")

    # Simulaciones con Dos Barrios
    print("\nSimulando con reducción de movilidad entre barrios...")
    resultados_muertos_reducido = main_simulaciones_dos_barrios(num_simulaciones=num_simulaciones, reduccion_movilidad=True)

    print("\nSimulando sin reducción de movilidad entre barrios...")
    resultados_muertos_no_reducido = main_simulaciones_dos_barrios(num_simulaciones=num_simulaciones, reduccion_movilidad=False)

    # Análisis Estadístico entre reducción y no reducción de movilidad
    media_reducido, intervalo_reducido = calcular_intervalo(resultados_muertos_reducido, confianza=0.90)
    media_no_reducido, intervalo_no_reducido = calcular_intervalo(resultados_muertos_no_reducido, confianza=0.90)

    # Test de Levene para igualdad de varianzas
    stat_levene_barrios, p_levene_barrios = stats.levene(resultados_muertos_reducido, resultados_muertos_no_reducido)

    # Elegir el test t apropiado según igualdad de varianzas
    if p_levene_barrios > 0.05:
        # Asumimos varianzas iguales
        t_statistic_barrios, p_value_barrios = stats.ttest_ind(
            resultados_muertos_reducido, resultados_muertos_no_reducido, equal_var=True
        )
    else:
        # No asumimos varianzas iguales
        t_statistic_barrios, p_value_barrios = stats.ttest_ind(
            resultados_muertos_reducido, resultados_muertos_no_reducido, equal_var=False
        )

    print("\nComparación con y sin reducción de movilidad:")
    print(f"Media de fallecidos con reducción: {media_reducido:.2f}, Intervalo al 90%: {intervalo_reducido}")
    print(f"Media de fallecidos sin reducción: {media_no_reducido:.2f}, Intervalo al 90%: {intervalo_no_reducido}")
    print(f"Test de Levene: Estadístico = {stat_levene_barrios:.4f}, p-value = {p_levene_barrios:.4f}")
    print(f"Estadístico t: {t_statistic_barrios:.4f}, Valor p: {p_value_barrios:.4f}")

    # Interpretación de resultados
    if p_value_barrios < 0.05:
        print("Hay una diferencia significativa en la media de fallecidos entre los dos escenarios.")
    else:
        print("No hay una diferencia significativa en la media de fallecidos entre los dos escenarios.")

    if p_levene_barrios < 0.05:
        print("Hay una diferencia significativa en la variabilidad de fallecidos entre los dos escenarios.")
    else:
        print("No hay una diferencia significativa en la variabilidad de fallecidos entre los dos escenarios.")
