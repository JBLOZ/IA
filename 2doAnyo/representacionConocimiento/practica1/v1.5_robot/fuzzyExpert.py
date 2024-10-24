import numpy as np
import math

from fuzzy_expert.variable import FuzzyVariable
from fuzzy_expert.rule import FuzzyRule
from fuzzy_expert.inference import DecompositionalInference

from segmento import *

class FuzzySystem:
    def __init__(self):
        self.objetivoAlcanzado = False
        self.segmentoObjetivo = None
        self.velocidad_lineal_previa = 0.0
        self.velocidad_angular_previa = 0.0

        # Constantes
        self.VMAX = 3.0  # Velocidad lineal máxima (m/s)
        self.WMAX = 1.0  # Velocidad angular máxima (rad/s)
        self.TOLERACION_FIN_SEGMENTO = 0.5  # Tolerancia para considerar que se alcanzó el objetivo (m)

        # Definir variables y reglas difusas
        self.definir_variables_difusas()
        self.definir_reglas_difusas()

        # Crear el sistema de inferencia
        self.sistema_inferencia = DecompositionalInference(self.reglas_difusas)

    def definir_variables_difusas(self):
        # Variable de entrada: error angular [-π, π]
        self.error_angular = FuzzyVariable({
            'Negativo_Grande': lambda x: 1 if x <= -math.pi/2 else 0,
            'Negativo_Pequeño': lambda x: (-x) / (math.pi/2) if -math.pi/2 <= x < 0 else 0,
            'Cero': lambda x: 1 - abs(x) / (math.pi/4) if -math.pi/4 <= x <= math.pi/4 else 0,
            'Positivo_Pequeño': lambda x: x / (math.pi/2) if 0 < x <= math.pi/2 else 0,
            'Positivo_Grande': lambda x: 1 if x >= math.pi/2 else 0,
        })

        # Variable de salida: velocidad angular [-WMAX, WMAX]
        self.velocidad_angular_var = FuzzyVariable({
            'Negativa_Alta': lambda x: 1 if x <= -self.WMAX/2 else 0,
            'Negativa_Baja': lambda x: (-x) / (self.WMAX/2) if -self.WMAX/2 <= x < 0 else 0,
            'Cero': lambda x: 1 - abs(x) / (self.WMAX/4) if -self.WMAX/4 <= x <= self.WMAX/4 else 0,
            'Positiva_Baja': lambda x: x / (self.WMAX/2) if 0 < x <= self.WMAX/2 else 0,
            'Positiva_Alta': lambda x: 1 if x >= self.WMAX/2 else 0,
        })

        # Variable de salida: velocidad lineal [0, VMAX]
        self.velocidad_lineal_var = FuzzyVariable({
            'Lento': lambda x: 1 - x / (self.VMAX/2) if x <= self.VMAX/2 else 0,
            'Rápido': lambda x: (x - self.VMAX/2) / (self.VMAX/2) if x >= self.VMAX/2 else 0,
        })

    def definir_reglas_difusas(self):
        self.reglas_difusas = [
            FuzzyRule(
                antecedent=self.error_angular['Negativo_Grande'],
                consequent={
                    self.velocidad_angular_var: 'Negativa_Alta',
                    self.velocidad_lineal_var: 'Lento'
                }
            ),
            FuzzyRule(
                antecedent=self.error_angular['Negativo_Pequeño'],
                consequent={
                    self.velocidad_angular_var: 'Negativa_Baja',
                    self.velocidad_lineal_var: 'Lento'
                }
            ),
            FuzzyRule(
                antecedent=self.error_angular['Cero'],
                consequent={
                    self.velocidad_angular_var: 'Cero',
                    self.velocidad_lineal_var: 'Rápido'
                }
            ),
            FuzzyRule(
                antecedent=self.error_angular['Positivo_Pequeño'],
                consequent={
                    self.velocidad_angular_var: 'Positiva_Baja',
                    self.velocidad_lineal_var: 'Lento'
                }
            ),
            FuzzyRule(
                antecedent=self.error_angular['Positivo_Grande'],
                consequent={
                    self.velocidad_angular_var: 'Positiva_Alta',
                    self.velocidad_lineal_var: 'Lento'
                }
            )
        ]

    def setObjetivo(self, obj):
        self.objetivoAlcanzado = False
        self.segmentoObjetivo = obj

    def esObjetivoAlcanzado(self):
        return self.objetivoAlcanzado

    def hayParteOptativa(self):
        return False  # Cambiar a True si implementas la parte optativa

    def tomarDecision(self, poseRobot):
        x, y, theta_deg = poseRobot[0], poseRobot[1], poseRobot[2]
        theta = math.radians(theta_deg)

        fin = np.array(self.segmentoObjetivo.getFin())

        # Verificar si se ha alcanzado el objetivo
        distancia_punto_final = np.linalg.norm(fin - np.array([x, y]))
        if distancia_punto_final <= self.TOLERACION_FIN_SEGMENTO:
            self.objetivoAlcanzado = True
            return (0, 0)

        # Calcular el error angular
        delta_x = fin[0] - x
        delta_y = fin[1] - y

        angulo_deseado = math.atan2(delta_y, delta_x)
        error_angular = angulo_deseado - theta
        error_angular = (error_angular + math.pi) % (2 * math.pi) - math.pi  # Normalizar a [-π, π]

        # Realizar inferencia difusa
        entradas = {'error_angular': error_angular}
        resultados = self.sistema_inferencia.infer(entradas)

        # Desdifusificar las salidas
        velocidad_angular = self.velocidad_angular_var.defuzzify(resultados[self.velocidad_angular_var])
        velocidad_lineal = self.velocidad_lineal_var.defuzzify(resultados[self.velocidad_lineal_var])

        # Limitar las salidas a los máximos permitidos
        velocidad_lineal = min(max(velocidad_lineal, 0), self.VMAX)
        velocidad_angular = min(max(velocidad_angular, -self.WMAX), self.WMAX)

        # Retornar las velocidades calculadas
        return (velocidad_lineal, velocidad_angular)
