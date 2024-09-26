import math
import time

# Función para calcular la distancia de un punto a una línea
def distancia_a_linea(x, y, A, B):
    # Fórmula de la distancia entre un punto y una línea
    return abs((B[1] - A[1]) * x - (B[0] - A[0]) * y + B[0] * A[1] - B[1] * A[0]) / math.sqrt((B[1] - A[1])**2 + (B[0] - A[0])**2)

# Función para calcular la distancia entre el robot y un punto
def distancia_entre_puntos(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

# Función para calcular la velocidad angular y lineal
def calcular_velocidades(robot_pos, robot_rot, A, B, tiempo, puntuacion):
    # Posición y rotación actuales del robot
    x, y = robot_pos
    theta = robot_rot

    # Constantes de velocidad máxima
    max_vel_lineal = 3  # m/s
    max_vel_angular = 11  # rad/s

    # Tiempo en segundos (cada llamada es cada 10 ms)
    delta_t = 0.01

    # Cálculo de la distancia del robot a la línea A-B
    dist_linea = distancia_a_linea(x, y, A, B)

    # Reducción de la puntuación
    if dist_linea == 0:
        factor_puntuacion = 0.5  # Si está en la línea, reduce puntos más lento
    else:
        factor_puntuacion = 1

    # La puntuación disminuye con el tiempo
    puntuacion -= 1000 * delta_t * factor_puntuacion
    puntuacion = max(0, puntuacion)  # No puede ser negativa

    # Calcular la orientación hacia el punto B
    delta_x = B[0] - x
    delta_y = B[1] - y
    angulo_deseado = math.atan2(delta_y, delta_x)

    # Diferencia de ángulo entre la orientación del robot y el objetivo
    error_rotacion = angulo_deseado - theta

    # Ajustar velocidad angular para corregir la orientación
    vel_angular = min(max_vel_angular, max(-max_vel_angular, error_rotacion))

    # Si la orientación es adecuada, moverse hacia adelante
    if abs(error_rotacion) < 0.1:  # Umbral para permitir movimiento lineal
        vel_lineal = max_vel_lineal
    else:
        vel_lineal = 0  # Si no está bien orientado, detener el movimiento

    return vel_lineal, vel_angular, puntuacion

# Función principal que se ejecuta cada 10 ms
def sistema_experto():
    # Inicialización
    robot_pos = [20, 35]  # Posición inicial (puede ser aleatoria)
    robot_rot = 45  # Orientación inicial (puede ser aleatoria)
    A = [0, 0]  # Punto A
    B = [-10, 0]  # Punto B (10 metros en el eje X)

    puntuacion = 100000
    tiempo = 0
    umbral_distancia = 0.1  # Distancia mínima para considerar que ha llegado a B

    while puntuacion > 0:
        # Llamar a la función que calcula las velocidades
        vel_lineal, vel_angular, puntuacion = calcular_velocidades(robot_pos, robot_rot, A, B, tiempo, puntuacion)

        # Simular un pequeño avance (esto debería ser modelado mejor con física)
        robot_pos[0] += vel_lineal * 0.01  # Actualización de la posición en 10ms
        robot_rot += vel_angular * 0.01    # Actualización de la orientación en 10ms

        # Incrementar el tiempo
        tiempo += 0.01

        # Mostrar el estado actual
        print(f"Tiempo: {tiempo:.2f} s, Posición: {robot_pos}, Rotación: {robot_rot:.2f}, Vel Lineal: {vel_lineal:.2f}, Vel Angular: {vel_angular:.2f}, Puntuación: {puntuacion:.2f}")

        # Comprobar si el robot ha alcanzado el punto B
        dist_a_B = distancia_entre_puntos(robot_pos[0], robot_pos[1], B[0], B[1])
        if dist_a_B < umbral_distancia:
            print(f"¡El robot ha alcanzado el punto B en {tiempo:.2f} segundos con una puntuación de {puntuacion:.2f}!")
            break

        # Esperar 10 ms
        time.sleep(0.01)

# Ejecutar el sistema experto
sistema_experto()
