'''
 Sistema Experto Difuso para el guiado de un robot
 Esta clase contendrá el código creado por los alumnos de RyRDC para el control 
 y guiado de un robot móvil sobre un plano cartesiano para recorrer diferentes 
 objetivos utilizando un esquema de sistema experto difuso.
 
 Para implementar el sistema experto difuso hay que instalar la librería
 https://jdvelasq.github.io/fuzzy-expert/

 Creado por: [Tu Nombre]
 el [Fecha]
 Modificado por: [Tu Nombre]

'''

import numpy as np
import math

from fuzzy_expert.variable import FuzzyVariable
from fuzzy_expert.rule import FuzzyRule
from fuzzy_expert.inference import DecompositionalInference
from fuzzy_expert.operators import defuzzificate

from segmento import *

class FuzzySystem:
    def __init__(self) -> None:
        self.objetivoAlcanzado = False
        self.segmentoObjetivo = None

        # Definir variables difusas de entrada: Error Angular (EA) y Distancia (D)
        self.EA = FuzzyVariable(
            universe_range=(-180, 180),
            terms={
                'NL': [(-180, 1.0), (-150, 1.0), (-120, 0.0)],
                'NM': [(-150, 0.0), (-90, 1.0), (-30, 0.0)],
                'NS': [(-90, 0.0), (-30, 1.0), (0, 0.0)],
                'Z':  [(-30, 0.0), (0, 1.0), (30, 0.0)],
                'PS': [(0, 0.0), (30, 1.0), (90, 0.0)],
                'PM': [(30, 0.0), (90, 1.0), (150, 0.0)],
                'PL': [(120, 0.0), (150, 1.0), (180, 1.0)],
            },
            step=1.0
        )

        self.D = FuzzyVariable(
            universe_range=(0, 10),
            terms={
                'C': [(0, 1.0), (1, 1.0), (2, 0.0)],
                'M': [(1, 0.0), (5, 1.0), (9, 0.0)],
                'F': [(8, 0.0), (9, 1.0), (10, 1.0)],
            },
            step=0.1
        )

        # Definir variables difusas de salida: Velocidad Lineal (V) y Velocidad Angular (W)
        self.V = FuzzyVariable(
            universe_range=(0, 3.0),
            terms={
                'S': [(0, 1.0), (0.75, 1.0), (1.5, 0.0)],
                'M': [(0.75, 0.0), (1.5, 1.0), (2.25, 0.0)],
                'F': [(1.5, 0.0), (2.25, 1.0), (3.0, 1.0)],
            },
            step=0.1
        )

        self.W = FuzzyVariable(
            universe_range=(-1.0, 1.0),
            terms={
                'NF': [(-1.0, 1.0), (-0.75, 1.0), (-0.5, 0.0)],
                'NS': [(-0.75, 0.0), (-0.5, 1.0), (-0.25, 0.0)],
                'Z':  [(-0.1, 0.0), (0.0, 1.0), (0.1, 0.0)],
                'PS': [(0.25, 0.0), (0.5, 1.0), (0.75, 0.0)],
                'PF': [(0.5, 0.0), (0.75, 1.0), (1.0, 1.0)],
            },
            step=0.01
        )

        # Definir reglas difusas (corregidas sin 'AND' en la consecuencia)
        self.rules = [
            FuzzyRule(
                premise=[("EA", "Z"), ("AND", "D", "F")],
                consequence=[("V", "F"), ("W", "Z")]
            ),
            FuzzyRule(
                premise=[("EA", "Z"), ("AND", "D", "M")],
                consequence=[("V", "M"), ("W", "Z")]
            ),
            FuzzyRule(
                premise=[("EA", "Z"), ("AND", "D", "C")],
                consequence=[("V", "S"), ("W", "Z")]
            ),
            FuzzyRule(
                premise=[("EA", "NL")],
                consequence=[("V", "S"), ("W", "NF")]
            ),
            FuzzyRule(
                premise=[("EA", "NM")],
                consequence=[("V", "M"), ("W", "NS")]
            ),
            FuzzyRule(
                premise=[("EA", "NS")],
                consequence=[("V", "F"), ("W", "NS")]
            ),
            FuzzyRule(
                premise=[("EA", "PS")],
                consequence=[("V", "F"), ("W", "PS")]
            ),
            FuzzyRule(
                premise=[("EA", "PM")],
                consequence=[("V", "M"), ("W", "PS")]
            ),
            FuzzyRule(
                premise=[("EA", "PL")],
                consequence=[("V", "S"), ("W", "PF")]
            ),
            # Regla por defecto que siempre se activa
            FuzzyRule(
                premise=[],
                consequence=[("V", "S"), ("W", "Z")]
            ),
        ]

        # Construcción del modelo difuso
        self.inference_system = DecompositionalInference(
            and_operator="min",
            or_operator="max",
            implication_operator="Rc",
            composition_operator="max",
            production_link="max",
            defuzzification_operator="cog"
        )

    # función setObjetivo
    #   Especifica un objetivo que debe ser recorrido por el robot
    def setObjetivo(self, obj):
        self.objetivoAlcanzado = False
        self.segmentoObjetivo = obj

    def tomarDecision(self, poseRobot):
        if self.objetivoAlcanzado:
            return (0, 0)

        inicio = np.array(self.segmentoObjetivo.getInicio())
        fin = np.array(self.segmentoObjetivo.getFin())

        # Calcular si se ha alcanzado el objetivo
        robot_pos = np.array(poseRobot[0:2])
        distancia_punto_final = np.linalg.norm(fin - robot_pos)
        if distancia_punto_final <= 0.5:
            self.objetivoAlcanzado = True
            return (0, 0)

        # Calcular el punto objetivo en el segmento
        segment_vector = fin - inicio
        segment_length = np.linalg.norm(segment_vector)
        if segment_length == 0:
            segment_length = 1e-6  # Evitar división por cero

        segment_direction = segment_vector / segment_length

        vector_to_robot = robot_pos - inicio
        t = np.dot(vector_to_robot, segment_direction) / segment_length
        t = min(max(t, 0.0), 1.0)  # Asegurar que t esté entre 0 y 1

        # Obtener el punto más cercano en el segmento
        closest_point = inicio + t * segment_vector

        # Avanzar una distancia de anticipación
        lookahead_distance = 1.0  # Ajustar según sea necesario
        target_t = t + lookahead_distance / segment_length
        target_t = min(max(target_t, 0.0), 1.0)
        target_point = inicio + target_t * segment_vector

        # Calcular EA y D
        delta_x = target_point[0] - poseRobot[0]
        delta_y = target_point[1] - poseRobot[1]

        desired_angle_rad = math.atan2(delta_y, delta_x)
        desired_angle_deg = math.degrees(desired_angle_rad)

        EA = desired_angle_deg - poseRobot[2]  # poseRobot[2] en grados
        EA = (EA + 180) % 360 - 180  # Normalizar EA a [-180, 180]

        D = np.linalg.norm(target_point - robot_pos)

        # Asegurarse de que EA y D están dentro de los rangos
        EA = max(min(EA, 180), -180)
        D = max(min(D, 10), 0)

        # Construir los hechos
        facts = {
            'EA': EA,
            'D': D
        }

        # Uso del modelo difuso para obtener V y W
        result = self.inference_system(
            variables={
                'EA': self.EA,
                'D': self.D,
                'V': self.V,
                'W': self.W
            },
            rules=self.rules,
            **facts
        )

        # Defuzzificación de las salidas
        V_crisp = defuzzificate(self.V.universe, result['V'], operator=self.inference_system.defuzzification_operator)
        W_crisp = defuzzificate(self.W.universe, result['W'], operator=self.inference_system.defuzzification_operator)

        return (V_crisp, W_crisp)
        
    # función esObjetivoAlcanzado 
    #   Devuelve True cuando el punto final del objetivo ha sido alcanzado. 
    #   Es responsabilidad de la alumna o alumno cambiar el valor de la 
    #   variable objetivoAlcanzado cuando se detecte que el robot ha llegado 
    #   a su objetivo. Esto se llevará a cabo en el método tomarDecision
    #   Este método NO debería ser modificado
    def esObjetivoAlcanzado(self):
        return self.objetivoAlcanzado
        
    # función hayParteOptativa.
    #   Deberá devolver True si la parte optativa ha sido implementada, es decir, si se consideran objetivos de tipo triángulo
    def hayParteOptativa(self):
        return False  # Modificar a True si se implementa la parte optativa
