def hay_jugada_ganadora(N, M):
    """
    Determina si el jugador que está a punto de mover tiene una jugada ganadora.

    :param N: Número total de fichas restantes.
    :param M: Máximo de fichas que se pueden retirar en un turno.
    :return: Booleano indicando si hay una jugada ganadora para el jugador actual.
    """
    return N % (M + 1) != 0

def determinar_mejor_jugada(N, M):
    """
    Calcula la mejor cantidad de fichas a retirar para forzar una posición perdedora al oponente.

    :param N: Número total de fichas restantes.
    :param M: Máximo de fichas que se pueden retirar en un turno.
    :return: Número de fichas a retirar.
    """
    jugada = N % (M + 1)
    if jugada == 0:
        # No hay jugada ganadora; elige retirar 1 ficha como movimiento predeterminado
        return 1
    else:
        return jugada

def jugar_nim(mostrar_optima=False):
    """
    Permite jugar al Nim entre dos jugadores humanos.

    :param mostrar_optima: Booleano que indica si se debe mostrar información sobre posiciones óptimas.
    """
    print("\n=== Juego del Nim ===")
    try:
        N = int(input("Ingrese el número total de fichas (N): "))
        M = int(input("Ingrese el máximo de fichas que se pueden retirar en un turno (M): "))
    except ValueError:
        print("Por favor, ingrese números enteros válidos para N y M.")
        return

    if N <= 0 or M <= 0:
        print("N y M deben ser mayores que 0.")
        return

    print(f"\nHay {N} fichas en el tablero.")
    print(f"Cada jugador puede retirar entre 1 y {M} fichas por turno.\n")

    jugador_actual = 1  # Comienza el Jugador 1

    # Determinar si el Jugador 1 tiene una jugada ganadora al inicio
    if mostrar_optima:
        jugador1_ganador = hay_jugada_ganadora(N, M)
        if jugador1_ganador:
            print("El Jugador 1 está en una posición ganadora.")
            mejor_jugada = determinar_mejor_jugada(N, M)
            print(f"Mejor jugada para el Jugador 1: Retirar {mejor_jugada} ficha(s).\n")
        else:
            print("El Jugador 1 está en una posición perdedora (si el Jugador 2 juega óptimamente).\n")

    while N > 0:
        print(f"Fichas restantes: {N}")
        try:
            retiro = int(input(f"Jugador {jugador_actual}, ¿cuántas fichas desea retirar? (1-{min(M, N)}): "))
        except ValueError:
            print("Entrada inválida. Por favor, ingrese un número entero.\n")
            continue

        if retiro < 1 or retiro > min(M, N):
            print(f"Movimiento inválido. Debe retirar entre 1 y {min(M, N)} fichas.\n")
            continue

        N -= retiro
        print(f"Jugador {jugador_actual} retiró {retiro} ficha(s).\n")

        if N == 0:
            print(f"¡Jugador {jugador_actual} ha retirado la última ficha y gana!\n")
            break

        # Cambiar al siguiente jugador
        jugador_actual = 2 if jugador_actual == 1 else 1

        # Si mostrar_optima está activado, informar la posición óptima después del movimiento
        if mostrar_optima:
            jugador_ganador = hay_jugada_ganadora(N, M)
            if jugador_ganador:
                print(f"Jugador {jugador_actual} está en una posición ganadora.\n")
                mejor_jugada = determinar_mejor_jugada(N, M)
                print(f"Mejor jugada para el Jugador {jugador_actual}: Retirar {mejor_jugada} ficha(s).\n")
            else:
                print(f"Jugador {jugador_actual} está en una posición perdedora (si el oponente juega óptimamente).\n")

def main():
    """
    Función principal para iniciar el juego y configurar opciones.
    """
    print("=== Bienvenido al Juego del Nim ===")

    # Configuración de N y M
    while True:
        try:
            N = int(input("Ingrese el número total de fichas (N): "))
            M = int(input("Ingrese el máximo de fichas que se pueden retirar en un turno (M): "))
            if N <= 0 or M <= 0:
                print("N y M deben ser mayores que 0. Inténtalo de nuevo.\n")
                continue
            break
        except ValueError:
            print("Entrada inválida. Por favor, ingrese números enteros.\n")

    # Preguntar si desea mostrar posiciones óptimas
    while True:
        respuesta = input("\n¿Desea mostrar las posiciones óptimas durante el juego? (s/n): ").strip().lower()
        if respuesta in ['s', 'n']:
            mostrar_optima = respuesta == 's'
            break
        else:
            print("Respuesta inválida. Por favor, ingrese 's' para sí o 'n' para no.\n")

    # Mostrar análisis inicial si se desea
    if mostrar_optima:
        jugador1_ganador = hay_jugada_ganadora(N, M)
        if jugador1_ganador:
            print("\nEl Jugador 1 está en una posición ganadora.")
            mejor_jugada = determinar_mejor_jugada(N, M)
            print(f"Mejor jugada para el Jugador 1: Retirar {mejor_jugada} ficha(s).\n")
        else:
            print("\nEl Jugador 1 está en una posición perdedora (si el Jugador 2 juega óptimamente).\n")

    # Preguntar si desea comenzar a jugar
    while True:
        jugar = input("¿Desea comenzar una partida del Nim? (s/n): ").strip().lower()
        if jugar == 's':
            jugar_nim(mostrar_optima)
            break
        elif jugar == 'n':
            print("Fin del programa. ¡Hasta luego!")
            break
        else:
            print("Respuesta inválida. Por favor, ingrese 's' para sí o 'n' para no.\n")

if __name__ == "__main__":
    main()
