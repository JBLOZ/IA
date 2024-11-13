def fontanero_diligente(tiempos):
    # Ordenar las reparaciones por tiempo creciente
    secuencia_optima = sorted(tiempos)
    
    tiempos_espera = []
    espera_acumulada = 0
    E_total = 0
    
    for t in secuencia_optima:
        espera_acumulada += t
        tiempos_espera.append(espera_acumulada)
        E_total += espera_acumulada
    
    tiempo_medio_espera = E_total / len(tiempos)
    
    print("Secuencia óptima de reparaciones:", secuencia_optima)
    print("Tiempos de espera individuales:", tiempos_espera)
    print("Tiempo total de espera (E):", E_total)
    print("Tiempo medio de espera:", tiempo_medio_espera)
    
    return secuencia_optima, E_total

# Ejemplo de uso
tiempos_reparacion = [2, 5, 1]
print(fontanero_diligente(tiempos_reparacion))
