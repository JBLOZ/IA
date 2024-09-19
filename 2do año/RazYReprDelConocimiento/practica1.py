
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def calcular_velocidades(punto_A, punto_B, Rx, Py, Pq):
    # Definición de las variables difusas
    distancia = ctrl.Antecedent(np.arange(0, 101, 1), 'distancia')
    angulo = ctrl.Antecedent(np.arange(-180, 181, 1), 'angulo')
    velocidad_lineal = ctrl.Consequent(np.arange(0, 4, 0.1), 'velocidad_lineal')
    velocidad_angular = ctrl.Consequent(np.arange(-12, 12, 0.1), 'velocidad_angular')

    # Definición de las funciones de pertenencia
    distancia['cerca'] = fuzz.trimf(distancia.universe, [0, 0, 50])
    distancia['lejos'] = fuzz.trimf(distancia.universe, [0, 50, 100])

    angulo['negativo'] = fuzz.trimf(angulo.universe, [-180, -90, 0])
    angulo['cero'] = fuzz.trimf(angulo.universe, [-90, 0, 90])
    angulo['positivo'] = fuzz.trimf(angulo.universe, [0, 90, 180])

    velocidad_lineal['lenta'] = fuzz.trimf(velocidad_lineal.universe, [0, 0, 1.5])
    velocidad_lineal['media'] = fuzz.trimf(velocidad_lineal.universe, [0, 1.5, 3])
    velocidad_lineal['rapida'] = fuzz.trimf(velocidad_lineal.universe, [1.5, 3, 3])

    velocidad_angular['negativa'] = fuzz.trimf(velocidad_angular.universe, [-11, -5.5, 0])
    velocidad_angular['cero'] = fuzz.trimf(velocidad_angular.universe, [-5.5, 0, 5.5])
    velocidad_angular['positiva'] = fuzz.trimf(velocidad_angular.universe, [0, 5.5, 11])

    # Definición de las reglas difusas
    rule1 = ctrl.Rule(distancia['cerca'] & angulo['cero'], (velocidad_lineal['lenta'], velocidad_angular['cero']))
    rule2 = ctrl.Rule(distancia['cerca'] & angulo['negativo'], (velocidad_lineal['lenta'], velocidad_angular['negativa']))
    rule3 = ctrl.Rule(distancia['cerca'] & angulo['positivo'], (velocidad_lineal['lenta'], velocidad_angular['positiva']))
    rule4 = ctrl.Rule(distancia['lejos'] & angulo['cero'], (velocidad_lineal['rapida'], velocidad_angular['cero']))
    rule5 = ctrl.Rule(distancia['lejos'] & angulo['negativo'], (velocidad_lineal['media'], velocidad_angular['negativa']))
    rule6 = ctrl.Rule(distancia['lejos'] & angulo['positivo'], (velocidad_lineal['media'], velocidad_angular['positiva']))

    # Creación del sistema de control difuso
    control_velocidad = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6])
    simulador = ctrl.ControlSystemSimulation(control_velocidad)

    # Cálculo de la distancia y el ángulo entre los puntos A y B
    dx = punto_B[0] - punto_A[0]
    dy = punto_B[1] - punto_A[1]
    distancia_AB = np.sqrt(dx**2 + dy**2)
    angulo_AB = np.degrees(np.arctan2(dy, dx)) - Pq

    # Normalización del ángulo
    if angulo_AB > 180:
        angulo_AB -= 360
    elif angulo_AB < -180:
        angulo_AB += 360

    # Asignación de los valores de entrada al simulador
    simulador.input['distancia'] = distancia_AB
    simulador.input['angulo'] = angulo_AB

    # Ejecución del simulador
    simulador.compute()

    # Obtención de las velocidades calculadas
    v = simulador.output['velocidad_lineal']
    w = simulador.output['velocidad_angular']

    return v, w

# Ejemplo de uso
punto_A = (0, 0)
punto_B = (10, 10)
Rx = 0
Py = 0
Pq = 0

v, w = calcular_velocidades(punto_A, punto_B, Rx, Py, Pq)
print(f"Velocidad lineal: {v} m/s")
print(f"Velocidad angular: {w} rad/s")
