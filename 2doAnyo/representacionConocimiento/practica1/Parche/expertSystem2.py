import numpy as np
import math

class ExpertSystem:
    def __init__(self):
        self.objetivoAlcanzado = False
        self.segmentoObjetivo = None
        self.trayectoria_calculada = False
        self.trajectory = []
        self.current_step = 0
        self.initial_pose = None
        self.VMAX = 3.0    # Velocidad lineal máxima (m/s)
        self.WMAX = 1.0    # Velocidad angular máxima (rad/s)
        self.VACC = 1.0    # Aceleración lineal máxima (m/s²)
        self.WACC = 0.5    # Aceleración angular máxima (rad/s²)
        self.FPS = 60
        self.TIME_STEP = 1 / self.FPS  # Tiempo entre frames

    def setObjetivo(self, segmento):
        self.objetivoAlcanzado = False
        self.segmentoObjetivo = segmento
        self.trayectoria_calculada = False
        self.trajectory = []
        self.current_step = 0
        self.initial_pose = None  # Se establecerá en tomarDecision()

    def tomarDecision(self, poseRobot):
        if not self.trayectoria_calculada:
            # Capturar la posición inicial del robot
            self.initial_pose = poseRobot
            # Calcular la trayectoria óptima
            self.calculate_trajectory()
            self.trayectoria_calculada = True

        # Si hemos alcanzado el final de la trayectoria
        if self.current_step >= len(self.trajectory):
            self.objetivoAlcanzado = True
            return (0.0, 0.0)

        # Obtener las velocidades para el paso actual
        velocidades = self.trajectory[self.current_step]
        self.current_step += 1

        return velocidades

    def calculate_trajectory(self):
        # Extract positions
        x0, y0, theta0 = self.initial_pose
        x1, y1 = self.segmentoObjetivo.getInicio()
        x2, y2 = self.segmentoObjetivo.getFin()

        # Convert theta to radians
        theta_rad = math.radians(theta0)

        # Initialize variables
        trajectory = []

        # Waypoints: from current position to start point, then to end point
        waypoints = [(x1, y1), (x2, y2)]

        for target_x, target_y in waypoints:
            # Calculate distance and angle to target
            dx = target_x - x0
            dy = target_y - y0
            distance = np.hypot(dx, dy)
            angle_to_target = math.atan2(dy, dx)

            # Calculate angle difference
            delta_theta = angle_to_target - theta_rad
            delta_theta = (delta_theta + math.pi) % (2 * math.pi) - math.pi  # Normalize

            # Time to rotate
            time_rotate = abs(delta_theta) / self.WACC
            num_frames_rotate = int(time_rotate / self.TIME_STEP) + 1

            # Angular velocity
            angular_velocity = np.sign(delta_theta) * min(self.WMAX, abs(delta_theta) / time_rotate)

            # Add rotation commands
            for _ in range(num_frames_rotate):
                trajectory.append((0.0, angular_velocity))

            # Update orientation
            theta_rad += delta_theta

            # Time to move forward
            # Calculate time to accelerate to VMAX
            time_accel = self.VMAX / self.VACC
            distance_accel = 0.5 * self.VACC * time_accel**2

            if distance_accel * 2 >= distance:
                # Cannot reach VMAX
                time_accel = math.sqrt(distance / self.VACC)
                max_velocity = self.VACC * time_accel
                time_const = 0
            else:
                # Can reach VMAX
                max_velocity = self.VMAX
                distance_const = distance - 2 * distance_accel
                time_const = distance_const / max_velocity

            num_frames_accel = int(time_accel / self.TIME_STEP)
            num_frames_const = int(time_const / self.TIME_STEP)
            num_frames_decel = num_frames_accel  # Symmetric

            # Accelerate
            for i in range(num_frames_accel):
                v = self.VACC * self.TIME_STEP * (i + 1)
                trajectory.append((v, 0.0))

            # Constant speed
            for _ in range(num_frames_const):
                trajectory.append((max_velocity, 0.0))

            # Decelerate
            for i in range(num_frames_decel):
                v = max_velocity - self.VACC * self.TIME_STEP * (i + 1)
                trajectory.append((v, 0.0))

            # Update position
            x0, y0 = target_x, target_y

        # Store the trajectory
        self.trajectory = trajectory

    def esObjetivoAlcanzado(self):
        return self.objetivoAlcanzado

    def hayParteOptativa(self):
        return False
