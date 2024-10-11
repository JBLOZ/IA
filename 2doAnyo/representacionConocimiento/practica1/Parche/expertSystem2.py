import math
import numpy as np
import datetime
import os

class ExpertSystem:
    """
    Sistema experto para el control de un robot que navega a través de segmentos.
    Calcula velocidades de control, puntúa la trayectoria y registra logs de desempeño.
    """

    # Definición de constantes de clase
    VMAX = 3.0  # Velocidad lineal máxima (m/s)
    WMAX = 1.0  # Velocidad angular máxima (rad/s)
    VACC = 1.0  # Aceleración lineal máxima (m/s²)
    WACC = 0.5  # Aceleración angular máxima (rad/s²)
    ANTICIPACION_TIEMPO = 1.3  # Segundos de anticipación para el punto objetivo
    TOLERACION_FIN_SEGMENTO = 0.5  # Tolerancia para considerar que se alcanzó el final del segmento (m)
    DIST_MIN_SCORE = 0.01  # Distancia mínima para puntuación máxima (m)

    LOG_FILE_NAME = "logs_objetivo_alcanzado.csv"  # Nombre del archivo de log

    def __init__(self):
        """
        Inicializa los atributos del sistema experto.

        Atributos:
            objetivoAlcanzado (bool): Indica si se ha alcanzado el objetivo.
            segmentoObjetivo (Segmento): Segmento de la trayectoria actual.
            estado (int): Estado actual del robot (1: en movimiento, 2: objetivo alcanzado).
            velocidad_lineal_previa (float): Velocidad lineal previa del robot (m/s).
            velocidad_angular_previa (float): Velocidad angular previa del robot (rad/s).
            primerSegmento (bool): Indica si es el primer segmento.
            posiciones (list): Lista para almacenar las posiciones recientes del robot.
            tinicio (datetime): Tiempo de inicio del segmento actual.
        """
        self.objetivoAlcanzado = False  # Indica si se alcanzó el objetivo
        self.segmentoObjetivo = None  # Segmento de la trayectoria actual
        self.estado = 1  # Estado actual del robot
        self.velocidad_lineal_previa = 0.0  # Velocidad lineal previa
        self.velocidad_angular_previa = 0.0  # Velocidad angular previa
        self.primerSegmento = True  # Indica si es el primer segmento

        # Inicializa el sistema de puntuación
        self.posiciones = []  # Lista para almacenar las posiciones

        # Inicializa el tiempo de inicio
        self.tinicio = None  # Tiempo de inicio del segmento

        # Crear el archivo de log si no existe y escribir el encabezado
        if not os.path.exists(self.LOG_FILE_NAME):
            try:
                with open(self.LOG_FILE_NAME, 'w') as file:
                    file.write("timestamp,puntuacion_del_segmento,puntuacion_bruta,tiempo_segundo\n")
            except Exception as e:
                print(f"Error al crear el archivo de log: {e}")

    def setObjetivo(self, segmento):
        """
        Establece un nuevo objetivo para el robot.

        Args:
            segmento (Segmento): Objeto que representa el segmento objetivo con métodos getInicio() y getFin().
        """
        self.objetivoAlcanzado = False
        self.segmentoObjetivo = segmento
        self.estado = 1
        self.posiciones.clear()  # Limpia las posiciones anteriores al cambiar de objetivo
        self.tinicio = datetime.datetime.now()  # Establece el tiempo de inicio del nuevo segmento

    @staticmethod
    def straightToPointDistance(p1, p2, p3):
        """
        Calcula la distancia perpendicular de un punto a una línea definida por dos puntos.

        Args:
            p1 (np.array): Punto inicial de la línea.
            p2 (np.array): Punto final de la línea.
            p3 (np.array): Punto desde el cual se calcula la distancia.

        Returns:
            float: Distancia perpendicular desde p3 a la línea p1-p2.
        """
        return np.linalg.norm(np.cross(p2 - p1, p1 - p3)) / np.linalg.norm(p2 - p1)

    @staticmethod
    def get_point_on_segment(k, start_point, end_point):
        """
        Calcula un punto en el segmento definido por start_point y end_point.

        Args:
            k (float): Parámetro que determina la posición en el segmento (0 <= k <= 1).
            start_point (tuple): Punto inicial del segmento.
            end_point (tuple): Punto final del segmento.

        Returns:
            np.array: Coordenadas del punto en el segmento correspondiente a k.
        """
        return (1 - k) * np.array(start_point) + k * np.array(end_point)

    @staticmethod
    def getSegmentScore(segmento, posiciones, tiempo):
        """
        Calcula la puntuación del segmento basado en las posiciones recientes del robot.
        Retorna una tupla con la puntuación normalizada, la puntuación bruta y el tiempo.

        Args:
            segmento (Segmento): Segmento objetivo.
            posiciones (list): Lista de posiciones recientes del robot.
            tiempo (float): Intervalo de tiempo considerado para la puntuación (s).

        Returns:
            tuple: (puntuacion_normalizada, puntuacion_bruta, tiempo).
        """
        inicio = np.array(segmento.getInicio())
        fin = np.array(segmento.getFin())
        score = 0
        for pos in posiciones:
            dist = np.abs(ExpertSystem.straightToPointDistance(inicio, fin, np.array(pos[0:2])))
            if dist < 3:
                if dist < ExpertSystem.DIST_MIN_SCORE:
                    score += 100
                else:
                    score += 1 / dist
        puntuacion_normalizada = score / (tiempo ** 3) if tiempo != 0 else 0
        puntuacion_bruta = score
        return (puntuacion_normalizada, puntuacion_bruta, tiempo)

    def actualizarEstado(self, distancia_punto_final, toleracionFinSegmento):
        """
        Actualiza el estado del robot basado en la distancia al punto final del segmento.

        Args:
            distancia_punto_final (float): Distancia actual al punto final del segmento (m).
            toleracionFinSegmento (float): Tolerancia para considerar que se alcanzó el final del segmento (m).
        """
        if distancia_punto_final <= toleracionFinSegmento:
            self.estado = 2

        if self.estado == 2:
            # Si se alcanza el punto final del segmento, se alcanza el objetivo
            self.objetivoAlcanzado = True

    def calcularPuntoObjetivo(self, inicio, fin, poseRobot):
        """
        Calcula el punto objetivo adelantado basado en la posición actual del robot.

        Este método implementa la lógica de **anticipación** para determinar un punto
        en el segmento objetivo al cual el robot debe dirigirse. La anticipación permite
        que el robot comience a corregir su trayectoria antes de llegar al punto objetivo,
        mejorando la eficiencia y precisión del movimiento.

        **Fórmulas y Razonamiento:**

        1. **Velocidad Promedio:**
           - Calcula la velocidad promedio entre la velocidad lineal previa y la velocidad máxima.
           - `velocidad_promedio = (velocidad_lineal_previa + VMAX) / 2`

        2. **Distancia de Anticipación:**
           - Determina cuánto adelantarse en el segmento objetivo basado en la velocidad promedio y el tiempo de anticipación.
           - `distancia_anticipacion = velocidad_promedio * ANTICIPACION_TIEMPO`

        3. **Longitud del Segmento:**
           - Calcula la longitud total del segmento objetivo.
           - `longitud_segmento = ||fin - inicio||`

        4. **Proyección de la Posición Actual:**
           - Calcula `k_inicial`, que es la proyección de la posición actual del robot sobre el segmento objetivo.
           - `k_inicial = ((x - inicio_x) * (fin_x - inicio_x) + (y - inicio_y) * (fin_y - inicio_y)) / (longitud_segmento ** 2)`
           - Se asegura que `k_inicial` esté en el rango [0, 1].

        5. **Punto Objetivo Adelantado:**
           - Calcula `k_final` sumando la proporción de anticipación sobre la longitud del segmento.
           - `k_final = k_inicial + (distancia_anticipacion / longitud_segmento)`
           - Se asegura que `k_final` esté en el rango [0, 1].
           - Finalmente, se obtiene el punto objetivo adelantado en el segmento usando `get_point_on_segment`.

        Args:
            inicio (np.array): Punto inicial del segmento objetivo (m).
            fin (np.array): Punto final del segmento objetivo (m).
            poseRobot (tuple): Tupla (x, y, theta) que representa la posición y orientación del robot.

        Returns:
            np.array: Coordenadas del punto objetivo adelantado en el segmento (m).
        """
        # Parámetros para anticipación
        velocidad_promedio = (self.velocidad_lineal_previa + self.VMAX) / 2
        distancia_anticipacion = velocidad_promedio * self.ANTICIPACION_TIEMPO

        # Cálculo de la distancia total del segmento
        longitud_segmento = np.linalg.norm(fin - inicio)

        # Cálculo de k_closest (proyección de la posición actual sobre el segmento)
        x, y = poseRobot[0], poseRobot[1]
        k_inicial = ((x - inicio[0]) * (fin[0] - inicio[0]) + (y - inicio[1]) * (fin[1] - inicio[1])) / (longitud_segmento ** 2)

        k_inicial = min(max(k_inicial, 0.0), 1.0)  # Asegurar que k_inicial esté entre 0 y 1

        # Cálculo de k_lookahead (posición adelantada en el segmento)
        k_final = k_inicial + (distancia_anticipacion / longitud_segmento) 
        k_final = min(max(k_final, 0.0), 1.0)  # Asegurar que k_final esté entre 0 y 1

        # Obtener el punto objetivo adelantado
        target_point = self.get_point_on_segment(k_final, inicio, fin)

        return target_point

    def calcularControl(self, target_point, poseRobot):
        """
        Calcula las velocidades lineal y angular necesarias para dirigir el robot hacia el punto objetivo.

        Este método implementa un **control proporcional** para ajustar la orientación del robot
        hacia el punto objetivo adelantado. La velocidad lineal se mantiene constante en VMAX,
        mientras que la velocidad angular se ajusta para minimizar el error angular.

        **Fórmulas y Razonamiento:**

        1. **Cálculo del Error Angular:**
           - Determina la diferencia entre el ángulo actual del robot y el ángulo hacia el punto objetivo.
           - `error_angular = angulo_a_target - theta`
           - Se normaliza el ángulo de error para que esté en el rango [-π, π].

        2. **Velocidad Angular Deseada:**
           - Se aplica una ganancia proporcional `k_w` y una función de activación `tanh` para suavizar la respuesta.
           - `velocidad_angular_deseada = WMAX * tanh(k_w * error_angular)`

        3. **Velocidades Deseadas:**
           - La velocidad lineal deseada se mantiene constante en VMAX para asegurar movimiento constante.
           - `velocidad_lineal_deseada = VMAX`

        4. **Limitación de Velocidades:**
           - Se asegura que la velocidad angular deseada no exceda WMAX.
           - `velocidad_angular_deseada = clamp(velocidad_angular_deseada, -WMAX, WMAX)`

        5. **Control de Velocidad (PID Simplificado):**
           - Se calculan las variaciones de velocidad lineal y angular basadas en la aceleración máxima permitida.
           - `delta_v = velocidad_lineal_deseada - velocidad_lineal_previa`
           - `delta_w = velocidad_angular_deseada - velocidad_angular_previa`
           - Se limita `delta_v` y `delta_w` a `VACC` y `WACC` respectivamente.

        6. **Actualización de Velocidades:**
           - Se actualizan las velocidades lineal y angular previas con las variaciones calculadas.
           - Se asegura que la velocidad lineal no exceda `VMAX`.

        Args:
            target_point (np.array): Punto objetivo adelantado hacia el cual se dirige el robot (m).
            poseRobot (tuple): Tupla (x, y, theta) que representa la posición y orientación del robot.

        Returns:
            tuple: (velocidad_lineal, velocidad_angular) en (m/s, rad/s).
        """
        x, y, theta_deg = poseRobot
        theta = math.radians(theta_deg)

        # Diferencias en posición
        delta_x = target_point[0] - x
        delta_y = target_point[1] - y

        # Ángulo hacia el punto objetivo
        angulo_a_target = math.atan2(delta_y, delta_x)
        error_angular = angulo_a_target - theta
        error_angular = (error_angular + math.pi) % (2 * math.pi) - math.pi  # Normalización del ángulo

        # Ganancias de control
        k_w = 2.0  # Ganancia proporcional para la velocidad angular

        # Velocidades deseadas
        velocidad_angular_deseada = self.WMAX * math.tanh(k_w * error_angular)
        velocidad_lineal_deseada = self.VMAX  # Mantener la velocidad máxima siempre

        # Limitación de velocidades máximas para angular
        velocidad_angular_deseada = max(min(velocidad_angular_deseada, self.WMAX), -self.WMAX)

        # Cálculo de las variaciones de velocidad
        delta_v = velocidad_lineal_deseada - self.velocidad_lineal_previa
        delta_v = max(min(delta_v, self.VACC), -self.VACC)

        delta_w = velocidad_angular_deseada - self.velocidad_angular_previa
        delta_w = max(min(delta_w, self.WACC), -self.WACC)

        # Actualización de velocidades
        velocidad_lineal = self.velocidad_lineal_previa + delta_v
        velocidad_angular = self.velocidad_angular_previa + delta_w

        # Asegurar que la velocidad lineal no exceda VMAX
        velocidad_lineal = min(velocidad_lineal, self.VMAX)

        # Almacenamiento de velocidades anteriores para el siguiente ciclo
        self.velocidad_lineal_previa = velocidad_lineal
        self.velocidad_angular_previa = velocidad_angular

        return velocidad_lineal, velocidad_angular

    def tomarDecision(self, poseRobot):
        """
        Toma una decisión basada en la posición actual del robot y el objetivo establecido.
        Devuelve las velocidades lineal y angular calculadas.

        Este método coordina las funciones de cálculo de punto objetivo, control y puntuación.
        Determina si el robot ha alcanzado el objetivo y actualiza el estado en consecuencia.

        **Proceso Interno:**

        1. **Cálculo de Distancias:**
           - Calcula la distancia perpendicular al segmento objetivo.
           - Calcula la distancia al punto final del segmento.

        2. **Actualización del Estado:**
           - Si la distancia al punto final está dentro de la tolerancia, se marca el objetivo como alcanzado.

        3. **Almacenamiento de Posiciones:**
           - Registra la posición actual para el cálculo de la puntuación.

        4. **Verificación de Objetivo Alcanzado:**
           - Si el objetivo ha sido alcanzado, calcula la puntuación del segmento, guarda los logs y detiene el robot.

        5. **Cálculo del Punto Objetivo Adelantado:**
           - Determina el punto al cual el robot debe dirigirse anticipadamente.

        6. **Cálculo de Velocidades de Control:**
           - Obtiene las velocidades lineal y angular necesarias para dirigir el robot hacia el punto objetivo.

        7. **Cálculo y Registro de Puntuación en Tiempo Real:**
           - Calcula la puntuación basada en las posiciones recientes y el tiempo transcurrido.
           - Imprime la puntuación en la consola para monitoreo en tiempo real.

        Args:
            poseRobot (tuple): Tupla (x, y, theta) que representa la posición y orientación del robot.

        Returns:
            tuple: (velocidad_lineal, velocidad_angular) en (m/s, rad/s).
        """
        # Obtener puntos inicial y final del segmento objetivo
        inicio = np.array(self.segmentoObjetivo.getInicio())  # Punto inicial del segmento
        fin = np.array(self.segmentoObjetivo.getFin())  # Punto final del segmento

        # Cálculo de la distancia al segmento (distancia perpendicular)
        dist = self.straightToPointDistance(inicio, fin, np.array(poseRobot[0:2]))

        # Cálculo de la distancia al punto final del segmento
        distancia_punto_final = np.linalg.norm(fin - np.array(poseRobot[0:2]))

        # Actualización del estado del robot basado en la distancia al punto final
        self.actualizarEstado(distancia_punto_final, self.TOLERACION_FIN_SEGMENTO)

        # Almacenar la posición actual para la puntuación
        self.posiciones.append(poseRobot)

        if self.objetivoAlcanzado:
            print("Objetivo alcanzado.")
            # Calcular la puntuación del segmento con el tiempo real transcurrido
            if self.tinicio is not None:
                tiempo_transcurrido = (datetime.datetime.now() - self.tinicio).total_seconds()
            else:
                tiempo_transcurrido = 0
            segmentScore = self.getSegmentScore(self.segmentoObjetivo, self.posiciones, tiempo_transcurrido)
            # Guardar los logs en un archivo
            self.guardarLogsEnArchivo(segmentScore)
            # Resetear posiciones para el siguiente segmento
            self.posiciones.clear()
            return 0.0, 0.0  # Detener el robot al alcanzar el objetivo

        # Calcular el punto objetivo adelantado
        target_point = self.calcularPuntoObjetivo(inicio, fin, poseRobot)

        # Calcular las velocidades de control
        velocidad_lineal, velocidad_angular = self.calcularControl(target_point, poseRobot)

        # Calcular la puntuación en tiempo real
        # Se utiliza el tiempo transcurrido desde el inicio del segmento
        if self.tinicio is not None:
            tiempo_transcurrido = (datetime.datetime.now() - self.tinicio).total_seconds()
        else:
            tiempo_transcurrido = 0

        # Calcular la puntuación actual
        puntuacion_normalizada, puntuacion_bruta, tiempo_calculado = self.getSegmentScore(
            self.segmentoObjetivo, self.posiciones, tiempo_transcurrido
        )

        # Imprimir la puntuación en tiempo real
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(
            f"[{timestamp}] Distancia al segmento: {dist:.4f} m, "
            f"Velocidad Lineal: {velocidad_lineal:.4f} m/s, "
            f"Velocidad Angular: {velocidad_angular:.4f} rad/s, "
            f"Puntuación del segmento: {puntuacion_normalizada:.4f} en {tiempo_transcurrido:.4f} segundos"
        )

        return velocidad_lineal, velocidad_angular

    def guardarLogsEnArchivo(self, segmentScore):
        """
        Guarda los logs acumulados en un archivo cuando se alcanza el objetivo.

        Esta función añade una nueva línea al archivo CSV de logs con la información
        del segmento completado, incluyendo timestamp, puntuación normalizada,
        puntuación bruta y tiempo transcurrido.

        Args:
            segmentScore (tuple): Tuple (puntuacion_normalizada, puntuacion_bruta, tiempo).
        """
        # Crear una entrada de log
        log = {
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "puntuacion_del_segmento": segmentScore[0],
            "puntuacion_bruta": segmentScore[1],
            "tiempo_segundo": segmentScore[2]
        }

        # Escribir los logs en formato CSV
        try:
            with open(self.LOG_FILE_NAME, 'a') as file:
                # Escribir la entrada de log
                line = (
                    f"{log['timestamp']},"
                    f"{log['puntuacion_del_segmento']:.4f},"
                    f"{log['puntuacion_bruta']:.4f},"
                    f"{log['tiempo_segundo']:.4f}\n"
                )
                file.write(line)

            # Imprimir de la misma manera que el launcher
            print(f"Puntuación del segmento: {segmentScore[0]:.4f}. "
                  f"Puntuación bruta del segmento: {segmentScore[1]:.4f} "
                  f"en {segmentScore[2]:.4f} segundos")
            print(f"Logs guardados en el archivo: {self.LOG_FILE_NAME}")
        except Exception as e:
            print(f"Error al guardar los logs: {e}")

    def esObjetivoAlcanzado(self):
        """
        Devuelve si se ha alcanzado el objetivo.

        Returns:
            bool: True si el objetivo ha sido alcanzado, False en caso contrario.
        """
        return self.objetivoAlcanzado

    def hayParteOptativa(self):
        """
        Indica si hay una parte optativa (en este caso siempre es False).

        Returns:
            bool: False.
        """
        return False
