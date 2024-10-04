import math

class ExpertSystem:
    
    def __init__(self):
        pass
    
    def tomarDecision(self, pose, segmentoObjetivo):
        # Datos del robot
        x_robot, y_robot, theta_robot = pose['x'], pose['y'], pose['theta']

        # Datos del segmento objetivo
        x_inicial, y_inicial = segmentoObjetivo.inicio['x'], segmentoObjetivo.inicio['y']
        x_final, y_final = segmentoObjetivo.fin['x'], segmentoObjetivo.fin['y']

        # Calcular el vector dirección del segmento
        dir_segmento_x = x_final - x_inicial
        dir_segmento_y = y_final - y_inicial

        # Calcular el vector desde el robot al punto inicial del segmento
        vector_inicial_x = x_inicial - x_robot
        vector_inicial_y = y_inicial - y_robot

        # Calcular la distancia al punto inicial
        distancia_inicial = (vector_inicial_x**2 + vector_inicial_y**2)**0.5

        # Calcular el ángulo al punto inicial
        angulo_deseado = math.atan2(vector_inicial_y, vector_inicial_x)
        error_angular = angulo_deseado - theta_robot

        # Ajuste de la velocidad angular
        K_angular = 1.0  # Constante de proporcionalidad
        velocidad_angular = K_angular * error_angular

        # Limitar la velocidad angular a los máximos permitidos
        velocidad_angular = max(-1, min(velocidad_angular, 1))

        # Ajuste de la velocidad lineal
        K_lineal = 0.5  # Constante de proporcionalidad
        velocidad_lineal = K_lineal * distancia_inicial

        # Limitar la velocidad lineal a los máximos permitidos
        velocidad_lineal = max(0, min(velocidad_lineal, 3))

        # Cuando el robot está cerca del punto final, marcar como alcanzado
        if distancia_inicial < 0.1:  # Tolerancia para estar cerca del objetivo
            objetivoAlcanzado = True
            velocidad_lineal = 0
            velocidad_angular = 0

        return velocidad_lineal, velocidad_angular

    def hayParteOptativa(self):
        # Por defecto, no implementamos la parte optativa
        return False

