import threading
import time

class Filosofo(threading.Thread):
    def __init__(self, id_filos, tenedor_izq, tenedor_der):
        threading.Thread.__init__(self)
        self.id = id_filos
        self.tenedor_izq = tenedor_izq
        self.tenedor_der = tenedor_der
        # Puedes inicializar variables adicionales si lo necesitas

    def run(self):
        # Implementa aquí el comportamiento del filósofo
        pass

if __name__ == "__main__":
    N = 5  # Número de filósofos y tenedores
    tenedores = [threading.Lock() for _ in range(N)]
    filosofos = []

    for i in range(N):
        # Asignar tenedores a cada filósofo
        filosofo = Filosofo(i, tenedores[i], tenedores[(i + 1) % N])
        filosofos.append(filosofo)

    # Iniciar los hilos de los filósofos
    for filosofo in filosofos:
        filosofo.start()

    # Esperar a que todos los filósofos terminen (opcional)
    for filosofo in filosofos:
        filosofo.join()
