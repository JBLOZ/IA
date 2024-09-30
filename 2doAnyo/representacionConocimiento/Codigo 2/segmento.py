'''
 ' Clase segmento
 ' Representa un segmento, con un comienzo y un final, en el plano XY
 ' Puede pintarse en un objeto screen de pygame.  Esto puede cambiar en versiones posteriores
 ' No puede ser modificado por los alumnos
'''


class segmento:
    def __init__(self):
        self.pInicio = (0, 0)
        self.pFin = (0, 0)

    def setInicio(self, inicio):
        self.pInicio = inicio
    
    def setFin(self, fin):
        self.pFin = fin

    # Obtiene el punto de inicio del segmento
    def getInicio(self):
        return self.pInicio
    
    # Obtiene el punto final del segmento
    def getFin(self):
        return self.pFin
