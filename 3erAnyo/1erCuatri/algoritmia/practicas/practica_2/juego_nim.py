def is_winning_position(n, max_take=3):
    """
    Función recursiva para determinar si la posición n es ganadora para el jugador actual,
    asumiendo que ambos juegan óptimamente. En Nim de un solo montón, el que toma el último gana.
    """
    if n == 0:
        return False  # El jugador actual pierde si no hay objetos.
    # El jugador actual puede ganar si existe un movimiento que deje al oponente en una posición perdedora.
    for k in range(1, min(max_take, n) + 1):
        if not is_winning_position(n - k, max_take):
            return True
    # Si todos los movimientos dejan al oponente en posición ganadora, entonces pierde.
    return False

print(is_winning_position(14))