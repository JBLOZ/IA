import math
import numpy as np

from fuzzy_expert.variable import FuzzyVariable
from fuzzy_expert.rule import FuzzyRule
from fuzzy_expert.inference import DecompositionalInference

class FuzzySystem:
    """
    Sistema experto difuso para el control de un robot que navega a través de segmentos.
    Utiliza lógica difusa para determinar la velocidad angular basada en el error angular.
    La velocidad lineal se mantiene constante en VMAX, con ajustes en segmentos triangulares.
    """

    # Definición de constantes de clase
    VMAX = 3.0  # Velocidad lineal máxima (m/s)
    VMAX_TRIANGULO = 2.9  # Velocidad lineal máxima en segmentos triangulares (m/s)
    WMAX = 1.0  # Velocidad angular máxima (rad/s)
    WMAX_TRIANGULO = 1.0  # Velocidad angular máxima en segmentos triangulares (rad/s)
    VACC = 1.0  # Aceleración lineal máxima (m/s²)
    WACC = 0.5  # Aceleración angular máxima (rad/s²)
    TOLERACION_FIN_SEGMENTO = 0.5  # Tolerancia para considerar que se alcanzó el final del segmento (m)
    TOLERANCIA_MEDIO = 3  # Tolerancia para considerar que se alcanzó el punto medio del triángulo (m)

    def __init__(self):
        """
        Inicializa el sistema experto difuso, definiendo las variables difusas y las reglas.
        """
        self.objetivoAlcanzado = False  
        self.segmentoObjetivo = None  
        self.velocidad_lineal_previa = 0.0  
        self.velocidad_angular_previa = 0.0  
        self.medioAlcanzado = False 
        self.segmento = 0  

        # Definir variables difusas
        self.variables_normales = self.definir_variables_normales()
        self.variables_triangulo = self.definir_variables_triangulo()

        # Definir reglas difusas
        self.rules = self.definir_reglas()

        # Configurar el modelo de inferencia
        self.modelo = DecompositionalInference(
            and_operator="min",
            or_operator="max",
            implication_operator="Rc",
            composition_operator="max-min",
            production_link="max",
            defuzzification_operator="cog",
        )

    
    def setObjetivo(self, segmento):
        """
        Establece un nuevo objetivo para el robot.
        """
        self.objetivoAlcanzado = False
        self.segmentoObjetivo = segmento
        self.medioAlcanzado = False  
        self.segmento += 0.5 


    def definir_variables_normales(self):
        """
        Define las variables difusas de entrada y salida para segmentos normales.
        """
        variables = {
            # Entrada: error angular
            "error_angular": FuzzyVariable(
                universe_range=(-math.pi, math.pi),
                terms={
                    "NegativoGrande": ('trimf', -math.pi, -math.pi, -math.pi/2),
                    "NegativoPequeno": ('trimf', -math.pi, -math.pi/2, 0),
                    "Cero": ('trimf', -math.pi/4, 0, math.pi/4),
                    "PositivoPequeno": ('trimf', 0, math.pi/2, math.pi),
                    "PositivoGrande": ('trimf', math.pi/2, math.pi, math.pi),
                },
            ),
            # Salida: velocidad angular
            "velocidad_angular": FuzzyVariable(
                universe_range=(-self.WMAX, self.WMAX),
                terms={
                    "FuerteIzquierda": ('trimf', -self.WMAX, -self.WMAX, -self.WMAX/2),
                    "Izquierda": ('trimf', -self.WMAX, -self.WMAX/2, 0),
                    "Recto": ('trimf', -self.WMAX/4, 0, self.WMAX/4),
                    "Derecha": ('trimf', 0, self.WMAX/2, self.WMAX),
                    "FuerteDerecha": ('trimf', self.WMAX/2, self.WMAX, self.WMAX),
                },
            ),
        }
        return variables

    def definir_variables_triangulo(self):
        """
        Define las variables difusas de entrada y salida para segmentos triangulares.
        Permite giros más bruscos al ajustar las funciones de membresía.
        """
        variables = {
            # Entrada: error angular
            "error_angular": FuzzyVariable(
                universe_range=(-math.pi, math.pi),
                terms={
                    "NegativoGrande": ('trimf', -math.pi, -math.pi, -math.pi/8),
                    "NegativoPequeno": ('trimf', -math.pi/4, -math.pi/8, 0),
                    "Cero": ('trimf', -math.pi/16, 0, math.pi/16),
                    "PositivoPequeno": ('trimf', 0, math.pi/8, math.pi/4),
                    "PositivoGrande": ('trimf', math.pi/8, math.pi, math.pi),
                },
            ),
            # Salida: velocidad angular
            "velocidad_angular": FuzzyVariable(
                universe_range=(-self.WMAX_TRIANGULO, self.WMAX_TRIANGULO),
                terms={
                    "FuerteIzquierda": ('trimf', -self.WMAX_TRIANGULO, -self.WMAX_TRIANGULO, -self.WMAX_TRIANGULO/2),
                    "Izquierda": ('trimf', -self.WMAX_TRIANGULO, -self.WMAX_TRIANGULO/2, 0),
                    "Recto": ('trimf', -self.WMAX_TRIANGULO/16, 0, self.WMAX_TRIANGULO/16),
                    "Derecha": ('trimf', 0, self.WMAX_TRIANGULO/2, self.WMAX_TRIANGULO),
                    "FuerteDerecha": ('trimf', self.WMAX_TRIANGULO/2, self.WMAX_TRIANGULO, self.WMAX_TRIANGULO),
                },
            ),
        }
        return variables

    def definir_reglas(self):
        """
        Define las reglas difusas para el sistema.
        """
        rules = [
            # Si el error angular es Cero, entonces angular es Recto
            FuzzyRule(
                premise=[
                    ("error_angular", "Cero"),
                ],
                consequence=[
                    ("velocidad_angular", "Recto"),
                ],
            ),
            # Si el error angular es PositivoPequeno, entonces angular es Derecha
            FuzzyRule(
                premise=[
                    ("error_angular", "PositivoPequeno"),
                ],
                consequence=[
                    ("velocidad_angular", "Derecha"),
                ],
            ),
            # Si el error angular es PositivoGrande, entonces angular es FuerteDerecha
            FuzzyRule(
                premise=[
                    ("error_angular", "PositivoGrande"),
                ],
                consequence=[
                    ("velocidad_angular", "FuerteDerecha"),
                ],
            ),
            # Si el error angular es NegativoPequeno, entonces angular es Izquierda
            FuzzyRule(
                premise=[
                    ("error_angular", "NegativoPequeno"),
                ],
                consequence=[
                    ("velocidad_angular", "Izquierda"),
                ],
            ),
            # Si el error angular es NegativoGrande, entonces angular es FuerteIzquierda
            FuzzyRule(
                premise=[
                    ("error_angular", "NegativoGrande"),
                ],
                consequence=[
                    ("velocidad_angular", "FuerteIzquierda"),
                ],
            ),
        ]
        return rules


    @staticmethod
    def straightToPointDistance(p1, p2, p3):
        """
        Calcula la distancia perpendicular desde un punto a una línea definida por dos puntos.
        """
        return np.linalg.norm(np.cross(p2 - p1, p1 - p3)) / np.linalg.norm(p2 - p1)



    @staticmethod
    def get_point_on_segment(k, start_point, end_point):
        """
        Calcula un punto específico en un segmento definido por dos puntos: inicio y fin
        """
        return (1 - k) * np.array(start_point) + k * np.array(end_point)

    def actualizarEstado(self, poseRobot, puntoFin):
        """
        Actualiza el estado del robot basado en la distancia al punto final del segmento.
        """
        distancia_punto_final = np.linalg.norm(puntoFin - np.array(poseRobot[0:2]))
        if distancia_punto_final <= FuzzySystem.TOLERACION_FIN_SEGMENTO:
            self.objetivoAlcanzado = True

    def calcularPuntoObjetivo(self, inicio, fin, poseRobot):
        """
        Calcula el punto objetivo para el robot basado en la posición actual y la anticipación.
        """
        # Aumentar la distancia de anticipación para empezar a girar antes
        distancia_anticipacion = self.VMAX * 2.0  # Factor de anticipación aumentado

        longitud_segmento = np.linalg.norm(fin - inicio)
        x, y = poseRobot[0], poseRobot[1]
        k_inicial = ((x - inicio[0]) * (fin[0] - inicio[0]) + (y - inicio[1]) * (fin[1] - inicio[1])) / (longitud_segmento ** 2)
        k_inicial = min(max(k_inicial, 0.0), 1.0)

        k_final = k_inicial + (distancia_anticipacion / longitud_segmento)
        k_final = min(max(k_final, 0.0), 1.0)

        target_point = self.get_point_on_segment(k_final, inicio, fin)
        return target_point

    def calcularPuntoMedioTrianguloExtendido(self, inicio, fin, medio):
        """
        Calcula el punto medio extendido del triángulo, desplazando el punto medio original
        4 unidades en la dirección perpendicular al segmento inicio-fin.
        """
        # Vector director del segmento inicio-fin
        vector_segmento = fin - inicio
        vector_segmento = vector_segmento / np.linalg.norm(vector_segmento)

        # Vector perpendicular al segmento
        vector_perpendicular = np.array([-vector_segmento[1], vector_segmento[0]])

        # Extender el punto medio 1 unidad en la dirección del vector perpendicular
        punto_medio_extendido = medio + 1 * vector_perpendicular

        return punto_medio_extendido

    def calcularControl(self, V, W):
        """
        Aplica las restricciones de aceleración y velocidad máxima a las velocidades calculadas.
        """
        # Limitar aceleración lineal
        delta_v = V - self.velocidad_lineal_previa
        delta_v = max(min(delta_v, self.VACC), -self.VACC)
        velocidad_lineal = self.velocidad_lineal_previa + delta_v
        velocidad_lineal = min(max(velocidad_lineal, 0), V)

        # Limitar aceleración angular
        delta_w = W - self.velocidad_angular_previa
        delta_w = max(min(delta_w, self.WACC), -self.WACC)
        velocidad_angular = self.velocidad_angular_previa + delta_w

        # Asegurar que la velocidad angular no exceda los límites
        velocidad_angular = max(min(velocidad_angular, self.WMAX), -self.WMAX)

        # Actualizar velocidades previas
        self.velocidad_lineal_previa = velocidad_lineal
        self.velocidad_angular_previa = velocidad_angular

        return velocidad_lineal, velocidad_angular

    def tomarDecision(self, poseRobot):
        """
        Toma una decisión sobre las velocidades de control basadas en la posición actual del robot.
        """

        fin = np.array(self.segmentoObjetivo.getFin())  
        inicio = np.array(self.segmentoObjetivo.getInicio())  

        # Cálculo de distancia al segmento
        dist = FuzzySystem.straightToPointDistance(inicio, fin, np.array(poseRobot[0:2]))
        
        # Actualizar estado del robot respecto al punto final
        self.actualizarEstado(poseRobot, fin)

        # Implementar lógica para segmentos de tipo 2 (triángulos)
        if self.segmentoObjetivo.getType() == 2 and not self.medioAlcanzado:
            medio = np.array(self.segmentoObjetivo.getMedio())  # Obtener el punto medio del triángulo

            # Calcular el punto medio extendido
            medio_extendido = self.calcularPuntoMedioTrianguloExtendido(inicio, fin, medio)
            dist_a_medio = np.linalg.norm(medio_extendido - np.array(poseRobot[:2]))

            if dist_a_medio > self.TOLERANCIA_MEDIO:
                # Dirigirse al punto medio extendido
                target_point = self.calcularPuntoObjetivo(inicio, medio_extendido, poseRobot)
            else:
                # Cambiar objetivo al punto final
                self.medioAlcanzado = True
                target_point = self.calcularPuntoObjetivo(medio_extendido, fin, poseRobot)
        else:
            # Para otros segmentos o si ya se alcanzó el punto medio, dirigirse al final
            target_point = self.calcularPuntoObjetivo(inicio, fin, poseRobot)

        # Calcular el error angular
        x, y, theta_deg = poseRobot[0], poseRobot[1], poseRobot[2]
        theta = math.radians(theta_deg)
        delta_x = target_point[0] - x
        delta_y = target_point[1] - y
        angulo_a_target = math.atan2(delta_y, delta_x)
        error_angular = angulo_a_target - theta
        error_angular = (error_angular + math.pi) % (2 * math.pi) - math.pi

        # Preparar entradas difusas
        inputs = {
            "error_angular": error_angular,
        }

        # Determinar si estamos en un segmento triangular
        if self.segmentoObjetivo.getType() == 2:
            variables = self.variables_triangulo
            V = self.VMAX_TRIANGULO


        else:
            variables = self.variables_normales
            V = self.VMAX

        # Ejecutar inferencia difusa
        resultado, cf = self.modelo(
            variables=variables,
            rules=self.rules,
            error_angular=inputs["error_angular"],
        )

        # Obtener valor de salida difuso
        W_fuzzy = resultado.get("velocidad_angular", 0)


        # Aplicar restricciones de aceleración y velocidad
        velocidad_lineal, velocidad_angular = self.calcularControl(V, W_fuzzy)

        return velocidad_lineal, velocidad_angular


    def esObjetivoAlcanzado(self):
        """
        Devuelve si se ha alcanzado el objetivo.
        """
        return self.objetivoAlcanzado

    def hayParteOptativa(self):
        """
        Indica si hay una parte optativa implementada.
        """
        return True
