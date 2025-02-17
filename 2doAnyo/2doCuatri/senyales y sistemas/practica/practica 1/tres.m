% Problema "3n+1" clásico de teoría de números

while 1
    n = input('Introduzca un número positivo (para valores negativos finaliza): ');
    if n <= 0
        break;
    end
    while n > 1
        if rem(n, 2) == 0
            n = n / 2;
        else
            n = 3 * n + 1;
        end
        disp(n) % Muestra por pantalla la evolución de n
    end
end