'''
 Sistema Experto Difuso para el guiado de un robot
 Esta clase contendrá el código creado por los alumnos de RyRDC para el control 
 y guiado de un robot móvil sobre un plano cartesiano para recorrer diferentes 
 objetivos utilizando un esquema de sistema experto difuso.
 
 Para implementar el sistema experto difuso hay que instalar la librería
 https://jdvelasq.github.io/fuzzy-expert/

 Creado por: Diego Viejo
 el 24/10/2024
 Modificado por: Diego Viejo. 

'''
import numpy as np
import math

from fuzzy_expert.variable import FuzzyVariable
from fuzzy_expert.rule import FuzzyRule
from fuzzy_expert.inference import DecompositionalInference

from segmento import *

class FuzzySystem:
    def __init__(self) -> None:
        self.objetivoAlcanzado = False
        self.segmentoObjetivo = None

        # Definición de variables difusas de entrada:

        # Variable 'distancia' representa la distancia al punto final del segmento
        # Universo de discurso: de 0 a 100 metros
        # Términos difusos:
        # - 'Cerca': distancia corta al objetivo
        # - 'Medio': distancia intermedia al objetivo
        # - 'Lejos': distancia larga al objetivo
        self.distancia = FuzzyVariable(
            universe_range=(0, 100),
            terms={
                'Cerca': ('zmf', 0, 20),
                'Medio': ('trimf', 15, 50, 85),
                'Lejos': ('smf', 50, 100)
            }
        )

        # Variable 'orientacion' representa el error angular hacia el objetivo
        # Universo de discurso: de -180 a 180 grados
        # Términos difusos:
        # - 'MuyDesalineadoIzquierda': gran desviación hacia la izquierda
        # - 'DesalineadoIzquierda': desviación moderada hacia la izquierda
        # - 'Alineado': orientación correcta hacia el objetivo
        # - 'DesalineadoDerecha': desviación moderada hacia la derecha
        # - 'MuyDesalineadoDerecha': gran desviación hacia la derecha
        self.orientacion = FuzzyVariable(
            universe_range=(-180, 180),
            terms={
                'MuyDesalineadoIzquierda': ('zmf', -180, -90),
                'DesalineadoIzquierda': ('trimf', -135, -45, 0),
                'Alineado': ('trimf', -10, 0, 10),
                'DesalineadoDerecha': ('trimf', 0, 45, 135),
                'MuyDesalineadoDerecha': ('smf', 90, 180)
            }
        )

        # Variable 'desviacion' representa la distancia perpendicular a la línea del segmento
        # Universo de discurso: de 0 a 10 metros
        # Términos difusos:
        # - 'EnLinea': robot está sobre la línea
        # - 'PocoDesviado': robot ligeramente desviado de la línea
        # - 'MuyDesviado': robot muy desviado de la línea
        self.desviacion = FuzzyVariable(
            universe_range=(0, 10),
            terms={
                'EnLinea': ('zmf', 0, 1),
                'PocoDesviado': ('trimf', 0.5, 2, 3.5),
                'MuyDesviado': ('smf', 3, 10)
            }
        )

        # Definición de variables difusas de salida:

        # Variable 'velocidad_lineal' representa la velocidad lineal del robot
        # Universo de discurso: de 0 a 3 m/s
        # Términos difusos:
        # - 'Lento': velocidad baja
        # - 'Normal': velocidad intermedia
        # - 'Rapido': velocidad alta
        self.velocidad_lineal = FuzzyVariable(
            universe_range=(0, 3),
            terms={
                'Lento': ('trimf', 0, 0, 1),
                'Normal': ('trimf', 0.5, 1.5, 2.5),
                'Rapido': ('trimf', 2, 3, 3)
            }
        )

        # Variable 'velocidad_angular' representa la velocidad angular del robot
        # Universo de discurso: de -1 a 1 rad/s
        # Términos difusos:
        # - 'GiroFuerteIzquierda': giro pronunciado a la izquierda
        # - 'GiroLeveIzquierda': giro suave a la izquierda
        # - 'SinGiro': sin giro
        # - 'GiroLeveDerecha': giro suave a la derecha
        # - 'GiroFuerteDerecha': giro pronunciado a la derecha
        self.velocidad_angular = FuzzyVariable(
            universe_range=(-1, 1),
            terms={
                'GiroFuerteIzquierda': ('trimf', -1, -1, -0.5),
                'GiroLeveIzquierda': ('trimf', -0.75, -0.25, 0),
                'SinGiro': ('trimf', -0.1, 0, 0.1),
                'GiroLeveDerecha': ('trimf', 0, 0.25, 0.75),
                'GiroFuerteDerecha': ('trimf', 0.5, 1, 1)
            }
        )

        # Definición de reglas difusas usando FuzzyRule
        # Las reglas determinan la velocidad lineal y angular en función de la distancia, orientación y desviación

        self.rules = [
            # Regla 1: Si distancia es Lejos y desviación es EnLinea y orientación es Alineado, entonces velocidad_lineal es Rapido y velocidad_angular es SinGiro
            FuzzyRule(
                premise=[
                    ('distancia', 'Lejos'),
                    ('AND', 'desviacion', 'EnLinea'),
                    ('AND', 'orientacion', 'Alineado')
                ],
                consequence=[
                    ('velocidad_lineal', 'Rapido'),
                    ('velocidad_angular', 'SinGiro')
                ]
            ),
            # Regla 2: Si desviación es MuyDesviado, entonces velocidad_lineal es Lento y velocidad_angular es GiroFuerte (izquierda o derecha según orientación)
            FuzzyRule(
                premise=[
                    ('desviacion', 'MuyDesviado'),
                    ('AND', 'orientacion', 'MuyDesalineadoIzquierda')
                ],
                consequence=[
                    ('velocidad_lineal', 'Lento'),
                    ('velocidad_angular', 'GiroFuerteIzquierda')
                ]
            ),
            FuzzyRule(
                premise=[
                    ('desviacion', 'MuyDesviado'),
                    ('AND', 'orientacion', 'MuyDesalineadoDerecha')
                ],
                consequence=[
                    ('velocidad_lineal', 'Lento'),
                    ('velocidad_angular', 'GiroFuerteDerecha')
                ]
            ),
            # Regla 3: Si desviación es PocoDesviado y orientación es Desalineado, entonces velocidad_lineal es Normal y velocidad_angular es GiroLeve
            FuzzyRule(
                premise=[
                    ('desviacion', 'PocoDesviado'),
                    ('AND', 'orientacion', 'DesalineadoIzquierda')
                ],
                consequence=[
                    ('velocidad_lineal', 'Normal'),
                    ('velocidad_angular', 'GiroLeveIzquierda')
                ]
            ),
            FuzzyRule(
                premise=[
                    ('desviacion', 'PocoDesviado'),
                    ('AND', 'orientacion', 'DesalineadoDerecha')
                ],
                consequence=[
                    ('velocidad_lineal', 'Normal'),
                    ('velocidad_angular', 'GiroLeveDerecha')
                ]
            ),
            # Regla 4: Si desviación es EnLinea y orientación es Alineado, entonces velocidad_lineal es Rapido y velocidad_angular es SinGiro
            FuzzyRule(
                premise=[
                    ('desviacion', 'EnLinea'),
                    ('AND', 'orientacion', 'Alineado')
                ],
                consequence=[
                    ('velocidad_lineal', 'Rapido'),
                    ('velocidad_angular', 'SinGiro')
                ]
            ),
            # Regla 5: Si desviación es EnLinea y orientación es Desalineado, entonces velocidad_lineal es Normal y velocidad_angular es GiroLeve
            FuzzyRule(
                premise=[
                    ('desviacion', 'EnLinea'),
                    ('AND', 'orientacion', 'DesalineadoIzquierda')
                ],
                consequence=[
                    ('velocidad_lineal', 'Normal'),
                    ('velocidad_angular', 'GiroLeveIzquierda')
                ]
            ),
            FuzzyRule(
                premise=[
                    ('desviacion', 'EnLinea'),
                    ('AND', 'orientacion', 'DesalineadoDerecha')
                ],
                consequence=[
                    ('velocidad_lineal', 'Normal'),
                    ('velocidad_angular', 'GiroLeveDerecha')
                ]
            ),
            # Regla 6: Si distancia es Cerca, entonces velocidad_lineal es Lento
            FuzzyRule(
                premise=[
                    ('distancia', 'Cerca')
                ],
                consequence=[
                    ('velocidad_lineal', 'Lento')
                ]
            ),
            # Regla 7: Si desviación es MuyDesviado, entonces velocidad_angular es GiroFuerte
            FuzzyRule(
                premise=[
                    ('desviacion', 'MuyDesviado'),
                    ('AND', 'orientacion', 'DesalineadoIzquierda')
                ],
                consequence=[
                    ('velocidad_angular', 'GiroFuerteIzquierda')
                ]
            ),
            FuzzyRule(
                premise=[
                    ('desviacion', 'MuyDesviado'),
                    ('AND', 'orientacion', 'DesalineadoDerecha')
                ],
                consequence=[
                    ('velocidad_angular', 'GiroFuerteDerecha')
                ]
            ),
            # Se pueden agregar más reglas según sea necesario
        ]

        # Configuración del sistema de inferencia difusa usando DecompositionalInference
        # Se especifican los operadores: min para AND, max para OR, y 'cog' para defuzzificación
        self.model = DecompositionalInference(
            and_operator='min',
            or_operator='max',
            implication_operator='Rc',  # Operador de implicación estándar (Mamdani)
            composition_operator='max-min',
            production_link='max',
            defuzzification_operator='cog'  # Centro de gravedad
        )

    @staticmethod
    def straightToPointDistance(p1, p2, p3):
        """
        Calcula la distancia perpendicular desde un punto a una línea definida por dos puntos.

        Parámetros:
            p1: np.array, Coordenadas del primer punto que define el segmento
            p2: np.array, Coordenadas del segundo punto que define el segmento
            p3: np.array, Coordenadas del punto (robot) desde el cual se calcula la distancia perpendicular a la línea

        Retorna:
            float: La distancia perpendicular desde el punto `p3` a la línea definida por `p1` y `p2`
        """
        return np.linalg.norm(np.cross(p2 - p1, p1 - p3)) / np.linalg.norm(p2 - p1)

    def setObjetivo(self, obj):
        """
        Establece un nuevo objetivo que debe ser recorrido por el robot.
        """
        self.objetivoAlcanzado = False
        self.segmentoObjetivo = obj

    def tomarDecision(self, poseRobot):
        """
        Toma una decisión sobre las velocidades lineal y angular del robot
        utilizando el modelo de inferencia difusa basado en la posición actual,
        la orientación, la desviación y el objetivo a alcanzar.
        """
        if self.segmentoObjetivo is None:
            return (0, 0)

        x, y, theta_deg = poseRobot[0:3]
        theta = math.radians(theta_deg)  # Convertir a radianes

        # Obtener el punto inicial y final del segmento objetivo
        inicio = np.array(self.segmentoObjetivo.getInicio())
        fin = np.array(self.segmentoObjetivo.getFin())

        # Calcular la distancia al punto final del segmento
        dx = fin[0] - x
        dy = fin[1] - y
        distancia = math.hypot(dx, dy)  # Distancia euclidiana

        # Actualizar objetivoAlcanzado si se ha llegado al punto final
        if distancia <= 0.5:  # Tolerancia definida en el enunciado
            self.objetivoAlcanzado = True

        # Calcular el ángulo hacia el punto final del segmento
        angulo_a_target = math.atan2(dy, dx)
        # Calcular diferencia angular entre orientación actual y ángulo al objetivo
        error_angular = angulo_a_target - theta
        # Normalizar el ángulo al rango [-pi, pi]
        error_angular = (error_angular + math.pi) % (2 * math.pi) - math.pi
        # Convertir error angular a grados
        error_angular_deg = math.degrees(error_angular)

        # Calcular la desviación (distancia perpendicular a la línea del segmento)
        desviacion = self.straightToPointDistance(inicio, fin, np.array([x, y]))

        # Preparar entradas para el sistema de inferencia difusa
        # Asegurar que las entradas están dentro del rango de las variables difusas
        distancia_input = max(0, min(distancia, 100))
        orientacion_input = max(-180, min(error_angular_deg, 180))
        desviacion_input = max(0, min(desviacion, 10))

        # Ejecutar el modelo de inferencia difusa
        output, _ = self.model(
            variables={
                'distancia': self.distancia,
                'orientacion': self.orientacion,
                'desviacion': self.desviacion,
                'velocidad_lineal': self.velocidad_lineal,
                'velocidad_angular': self.velocidad_angular
            },
            rules=self.rules,
            distancia=distancia_input,
            orientacion=orientacion_input,
            desviacion=desviacion_input
        )

        # Obtener los valores defuzzificados de las salidas
        velocidad_lineal = output.get('velocidad_lineal', 0)
        velocidad_angular = output.get('velocidad_angular', 0)

        # Limitar las velocidades dentro de los rangos permitidos
        VMAX = 3.0  # Velocidad lineal máxima
        WMAX = 1.0  # Velocidad angular máxima

        velocidad_lineal = max(0, min(velocidad_lineal, VMAX))
        velocidad_angular = max(-WMAX, min(velocidad_angular, WMAX))

        return (velocidad_lineal, velocidad_angular)

    def esObjetivoAlcanzado(self):
        """
        Devuelve True si el robot ha alcanzado el objetivo.
        """
        return self.objetivoAlcanzado

    def hayParteOptativa(self):
        """
        Indica si se ha implementado la parte optativa (objetivos tipo triángulo).
        """
        return False  # Cambiar a True si se implementa la parte optativa
