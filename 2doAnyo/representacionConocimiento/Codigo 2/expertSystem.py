'''
 Sistema Experto para el guiado de un robot
 Esta clase contendrá el código creado por los alumnos de RyRDC para el control 
 y guiado de un robot móvil sobre un plano cartesiano pasando por un punto inicial
 y siguiendo una línea recta hasta un punto final

 Creado por: Diego Viejo
 el 26/09/2024
 Modificado por: 

'''

from segmento import *

class ExpertSystem:
    def __init__(self) -> None:
        self.objetivoAlcanzado = False
        self.segmentoObjetivo = None

    # función setObjetivo
    #   Especifica un segmento como objetivo para el recorrido del robot
    def setObjetivo(self, segmento):
        self.objetivoAlcanzado = False
        self.segmentoObjetivo = segmento


    # función tomarDecision. 
    #   Recibe una tupla de 3 valores con la pose del robot y un objeto
    #   de clase Segmento con la información del segmento a seguir
    #   
    #   Devuelve una tupla con la velocidad lineal y angular que se
    #   quiere dar al robot
    def tomarDecision(self, poseRobot):
        # código del sistema experto. A completar por la alumna o alumno

        return (3, 0.25)
    
    # función esObjetivoAlcanzado 
    #   Devuelve True cuando el punto final del objetivo ha sido alcanzado. 
    #   Es responsabilidad de la alumna o alumno cambiar el valor de la 
    #   variable objetivoAlcanzado cuando se detecte que el robot ha llegado 
    #   a su objetivo. Esto se llevará a cabo en el método tomarDecision
    #   Este método NO debería ser modificado
    def esObjetivoAlcanzado(self):
        return self.objetivoAlcanzado