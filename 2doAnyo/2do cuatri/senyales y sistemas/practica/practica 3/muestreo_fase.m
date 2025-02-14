function muestreo_fase(f0, Ts,fase)
    % f0: Frecuencia de la sinusoide continua (en Hz)
    % Ts: Período de muestreo (en segundos)

    T0 = 1 / f0; % Período de la señal continua

    % Señal continua
    t = 0:2*T0/10000:2*T0;
    xa = cos(2 * pi * f0 * t + fase);

    figure;
    subplot(2, 1, 1);
    plot(t, xa);
    grid on;
    xlabel('Tiempo (s)', 'Fontsize', 8);
    ylabel('Amplitud', 'Fontsize', 8);
    title('Señal continua x_{a}(t)');
    axis([0 2*T0 -1.5 1.5]);

    % Señal discreta
    nTs = 0:Ts:2*T0;
    xs = cos(2 * pi * f0 * nTs + fase);
    n = 0:length(nTs)-1;

    subplot(2, 1, 2);
    stem(n, xs);
    grid on;
    xlabel('Índice de muestreo, n', 'Fontsize', 8);
    ylabel('Amplitud', 'Fontsize', 8);
    title('Señal discreta x[n]');
    axis([0 2*T0/Ts -1.5 1.5]);
end
