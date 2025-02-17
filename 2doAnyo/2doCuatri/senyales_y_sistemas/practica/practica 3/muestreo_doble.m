function muestreo(f01, Ts, K, fase)
    % f01: Frecuencia de la primera sinusoide continua (Hz)
    % Ts: Período de muestreo (s)
    % K: Factor para calcular f02
    % fs: Frecuencia de muestreo (Hz)   
    fs = 1/Ts;

    

    f02 = f01 + K * fs;
    

    T_max = 2 / min(f01, f02);

    t = 0:Ts/10:T_max; 


    xa1 = cos(2 * pi * f01 * t + fase);
    xa2 = cos(2 * pi * f02 * t + fase);


    nTs = 0:Ts:T_max;
    xs1 = cos(2 * pi * f01 * nTs + fase);
    xs2 = cos(2 * pi * f02 * nTs + fase);
    n = 0:length(nTs)-1;
    figure()

    subplot(2, 2, 1);
    plot(t, xa1, 'b');
    grid on;
    xlabel('Tiempo (s)', 'Fontsize', 10);
    ylabel('Amplitud', 'Fontsize', 10);
    title(['Señal continua x_{a1}(t), f01 = ', num2str(f01), ' Hz']);
    axis([0 T_max -1.5 1.5]);

    % Señal continua f02 (arriba derecha)
    subplot(2, 2, 2);
    plot(t, xa2, 'r');
    grid on;
    xlabel('Tiempo (s)', 'Fontsize', 10);
    ylabel('Amplitud', 'Fontsize', 10);
    title(['Señal continua x_{a2}(t), f02 = ', num2str(f02), ' Hz']);
    axis([0 T_max -1.5 1.5]);

    % Señal discreta f01 (abajo izquierda)
    subplot(2, 2, 3);
    stem(nTs, xs1, 'b', 'MarkerSize', 3);
    grid on;
    xlabel('Tiempo (s)', 'Fontsize', 10);
    ylabel('Amplitud', 'Fontsize', 10);
    title('Señal discreta x_{1}[n]');
    axis([0 T_max -1.5 1.5]);

    % Señal discreta f02 (abajo derecha)
    subplot(2, 2, 4);
    stem(nTs, xs2, 'r', 'MarkerSize', 3);
    grid on;
    xlabel('Tiempo (s)', 'Fontsize', 10);
    ylabel('Amplitud', 'Fontsize', 10);
    title('Señal discreta x_{2}[n]');
    axis([0 T_max -1.5 1.5]);

end
