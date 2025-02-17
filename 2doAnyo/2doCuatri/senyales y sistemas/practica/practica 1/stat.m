function [mean, stdev] = stat(x)
    % Declaración de una función
    % Esta función calcula la media y la desviación típica
    % de todos los elementos de la entrada si
    % la variable de entrada es un vector.
    % Si la variable de entrada es una matriz,
    % obtiene un vector fila con los valores medios
    % y las desviaciones típicas de cada columna.

    [m, n] = size(x);
    if m == 1
        m = n;
    end
    mean = sum(x) / m;
    stdev = sqrt(sum(x.^2) / m - mean.^2);

end