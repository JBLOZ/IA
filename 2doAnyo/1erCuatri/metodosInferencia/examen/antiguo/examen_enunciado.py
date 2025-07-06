# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 14:17:34 2024

@author: FERRAN
"""

import math
from scipy.stats import t

def prueba_t(v1, v2, alpha=0.05):
    # tamaños de muestra, medias y desviaciones estándar
    n1 = len(v1)
    n2 = len(v2)
    media1 = sum(v1) / n1
    media2 = sum(v2) / n2
    var1 = sum((x - media1) ** 2 for x in v1) / (n1 - 1)
    var2 = sum((x - media2) ** 2 for x in v2) / (n2 - 1)
    
    # Varianza combinada
    sp2 = ((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2)
    sp = math.sqrt(sp2)
    
    # Estadístico t
    t_observado = (media1 - media2) / (sp * math.sqrt(1/n1 + 1/n2))
    
    # Grados de libertad
    gl = n1 + n2 - 2
    
    # Valor crítico teórico
    t_teorico = t.ppf(alpha, gl)  # Unilateral, cola izquierda
    
    # Resultado del test
    if t_observado < t_teorico:
        resultado = "Rechazamos H0: la media de v1 es menor que la media de v2."
    else:
        resultado = "No rechazamos H0: no hay evidencia suficiente para afirmar que la media de v1 es menor que la media de v2."
    
    return {
        "t_observado": t_observado,
        "t_teorico": t_teorico,
        "resultado": resultado
    }

# Ejemplo de uso
v1 = [19, 22, 21, 18, 20, 23, 17, 20]
v2 = [25, 27, 26, 24, 23, 28, 22, 24]

resultado = prueba_t(v1, v2)
print("Estadístico t observado:", resultado["t_observado"])
print("Valor crítico t teórico:", resultado["t_teorico"])
print("Resultado:", resultado["resultado"])
