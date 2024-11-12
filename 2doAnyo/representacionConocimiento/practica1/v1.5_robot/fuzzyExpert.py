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
    """
    Sistema Experto Difuso para el control de un robot móvil que sigue segmentos en un plano cartesiano.
    """

    VMAX = 3.0  # Velocidad lineal máxima (m/s)
    WMAX = 1.0  # Velocidad angular máxima (rad/s)
    VACC = 1.0  # Aceleración lineal máxima (m/s²)
    WACC = 0.5  # Aceleración angular máxima (rad/s²)
    TOLERANCIA_OBJETIVO = 0.5  # Tolerancia para considerar el objetivo alcanzado (m)

    def __init__(self) -> None:
        self.objetivoAlcanzado = False
        self.segmentoObjetivo = None
        self.segmento = 0
        self.medioAlcanzado = False
        self.velocidad_lineal_previa = 0.0
        self.velocidad_angular_previa = 0.0

    def setObjetivo(self, obj):
        """
        Establece un nuevo objetivo que debe ser recorrido por el robot.
        """
        self.objetivoAlcanzado = False
        self.segmentoObjetivo = obj
        self.segmento += 0.5
        self.medioAlcanzado = False  # Reiniciar para el nuevo segmento

    @staticmethod
    def straightToPointDistance(p1, p2, p3):
        """
        Calcula la distancia perpendicular desde un punto a una línea definida por dos puntos.
        """
        p1 = np.array(p1)
        p2 = np.array(p2)
        p3 = np.array(p3)
        return np.linalg.norm(np.cross(p2 - p1, p1 - p3)) / np.linalg.norm(p2 - p1)

    def get_point_ahead_on_line(self, start_point, end_point, current_pos, lookahead_distance):
        """
        Calcula un punto adelantado en la línea, a una distancia específica desde el punto más cercano al robot.
        """
        # Vector de dirección de la línea
        line_vec = end_point - start_point
        line_vec_normalized = line_vec / np.linalg.norm(line_vec)

        # Proyección del robot en la línea
        robot_vec = current_pos - start_point
        proj_length = np.dot(robot_vec, line_vec_normalized)
        proj_point = start_point + proj_length * line_vec_normalized

        # Punto adelantado en la línea
        target_point = proj_point + lookahead_distance * line_vec_normalized

        # Asegurar que el punto adelantado no exceda el segmento
        total_length = np.linalg.norm(end_point - start_point)
        target_length = np.dot(target_point - start_point, line_vec_normalized)
        if target_length > total_length:
            target_point = end_point
        elif target_length < 0:
            target_point = start_point

        return target_point

    def tomarDecision(self, poseRobot):
        """
        Toma una decisión sobre las velocidades lineal y angular del robot
        utilizando el modelo de inferencia difusa basado en la posición actual
        y el objetivo a alcanzar.

        Maneja segmentos lineales y triangulares.
        """
        if self.segmentoObjetivo is None:
            return (0, 0)

        # Pose del robot
        x, y, theta_deg = poseRobot[0:3]
        theta = math.radians(theta_deg)  # Convertir a radianes

        # Puntos de inicio y fin del segmento objetivo
        inicio = np.array(self.segmentoObjetivo.getInicio())
        fin = np.array(self.segmentoObjetivo.getFin())
        current_pos = np.array([x, y])

        # Calcular la distancia al punto final del segmento
        dx_fin = fin[0] - x
        dy_fin = fin[1] - y
        distancia_objetivo = math.hypot(dx_fin, dy_fin)  # Distancia euclidiana

        # Actualizar objetivoAlcanzado si se ha llegado al punto final
        if distancia_objetivo <= self.TOLERANCIA_OBJETIVO:
            self.objetivoAlcanzado = True
            return (0, 0)

        # Determinar si estamos en un segmento triangular o lineal
        if self.segmentoObjetivo.getType() == 2:
            # Segmento triangular
            medio = np.array(self.segmentoObjetivo.getMedio())

            if not self.medioAlcanzado:
                # Dirigirse al punto medio
                target_point = medio
                # Verificar si hemos alcanzado el punto medio
                dx_medio = medio[0] - x
                dy_medio = medio[1] - y
                distancia_medio = math.hypot(dx_medio, dy_medio)
                if distancia_medio <= self.TOLERANCIA_OBJETIVO:
                    self.medioAlcanzado = True
            else:
                # Después de pasar por el medio, dirigirse al fin
                target_point = fin
        else:
            # Segmento lineal
            # Calcular el punto adelantado en la línea
            lookahead_distance = 5.0  # Distancia de anticipación
            target_point = self.get_point_ahead_on_line(inicio, fin, current_pos, lookahead_distance)

        # Calcular el ángulo hacia el punto objetivo
        dx_target = target_point[0] - x
        dy_target = target_point[1] - y
        angulo_a_target = math.atan2(dy_target, dx_target)
        # Calcular diferencia angular entre orientación actual y ángulo al objetivo
        error_angular = angulo_a_target - theta
        # Normalizar el ángulo al rango [-pi, pi]
        error_angular = (error_angular + math.pi) % (2 * math.pi) - math.pi
        # Convertir error angular a grados
        error_angular_deg = math.degrees(error_angular)

        # Preparar entradas para el sistema de inferencia difusa
        # Usaremos solo la orientación para ajustar la velocidad angular
        orientacion_input = max(-180, min(error_angular_deg, 180))

        # Definimos las variables difusas y reglas
        orientacion_var = FuzzyVariable(
            universe_range=(-180, 180),
            terms={
                'DesalineadoIzquierda': ('zmf', -90, -5),
                'Alineado': ('trimf', -5, 0, 5),
                'DesalineadoDerecha': ('smf', 5, 90)
            }
        )

        velocidad_angular_var = FuzzyVariable(
            universe_range=(-self.WMAX, self.WMAX),
            terms={
                'GiroIzquierda': ('trimf', -self.WMAX, -self.WMAX/2, 0),
                'SinGiro': ('trimf', -0.1, 0, 0.1),
                'GiroDerecha': ('trimf', 0, self.WMAX/2, self.WMAX)
            }
        )

        rules = [
            # Regla 1: Si está desalineado a la izquierda, gira a la izquierda
            FuzzyRule(
                premise=[
                    ('orientacion', 'DesalineadoIzquierda')
                ],
                consequence=[
                    ('velocidad_angular', 'GiroIzquierda')
                ]
            ),
            # Regla 2: Si está desalineado a la derecha, gira a la derecha
            FuzzyRule(
                premise=[
                    ('orientacion', 'DesalineadoDerecha')
                ],
                consequence=[
                    ('velocidad_angular', 'GiroDerecha')
                ]
            ),
            # Regla 3: Si está alineado, no gira
            FuzzyRule(
                premise=[
                    ('orientacion', 'Alineado')
                ],
                consequence=[
                    ('velocidad_angular', 'SinGiro')
                ]
            )
        ]

        model = DecompositionalInference(
            and_operator='min',
            or_operator='max',
            implication_operator='Rc',
            composition_operator='max-min',
            production_link='max',
            defuzzification_operator='cog'
        )

        # Ejecutar el modelo de inferencia difusa
        output, _ = model(
            variables={
                'orientacion': orientacion_var,
                'velocidad_angular': velocidad_angular_var
            },
            rules=rules,
            orientacion=orientacion_input
        )

        # Obtener los valores defuzzificados de las salidas
        velocidad_angular_deseada = output.get('velocidad_angular', 0)

        # Limitar las velocidades dentro de los rangos permitidos
        velocidad_lineal_deseada = self.VMAX  # Siempre a velocidad máxima
        velocidad_angular_deseada = max(-self.WMAX, min(velocidad_angular_deseada, self.WMAX))

        # Aplicar aceleraciones máximas
        delta_v = velocidad_lineal_deseada - self.velocidad_lineal_previa
        delta_v = max(min(delta_v, self.VACC), -self.VACC)

        delta_w = velocidad_angular_deseada - self.velocidad_angular_previa
        delta_w = max(min(delta_w, self.WACC), -self.WACC)

        # Actualizar velocidades
        velocidad_lineal = self.velocidad_lineal_previa + delta_v
        velocidad_angular = self.velocidad_angular_previa + delta_w

        # Almacenar velocidades previas para el siguiente ciclo
        self.velocidad_lineal_previa = velocidad_lineal
        self.velocidad_angular_previa = velocidad_angular

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
        return True
