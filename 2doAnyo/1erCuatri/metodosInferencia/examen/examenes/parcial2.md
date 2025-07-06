# Universitat d'Alacant
## Universidad de Alicante

### Examen 17/12/2024

[cite_start]**1.-** Se ha detectado que los ciberataques que sufre la UA llegan de cuatro continentes (A,B,C y D). [cite: 1] [cite_start]Se sospecha que la proporción de ataques es 3:1:1:1 respectivamente. [cite: 2] [cite_start]Se han recogido los siguientes intentos de ataque informático en un mes: A: 325: B:110: C: 101: D: 99. ¿Hay motivos para refutar la sospecha? [cite: 3] [cite_start]¿Por qué? [cite: 4]

**Solución**

Se plantea la siguiente hipótesis:
* [cite_start]$H_0$: Las proporciones de ciberataques son 3:1:1:1. [cite: 4]
* [cite_start]$H_1$: Las proporciones de ciberataques no son 3:1:1:1. [cite: 5]

**Cálculo de frecuencias esperadas**
El total de ataques observados es:
Total = $325 + 110 + 101 + 99 = 635$
Bajo la hipótesis nula, las proporciones esperadas son $\frac{3}{6}, \frac{1}{6}, \frac{1}{6}, \frac{1}{6}$. Por lo tanto, las frecuencias esperadas se calculan como:
$E_i = Proporción_i \times Total$

| Continente | Frecuencia Observada $O_i$ | Frecuencia Esperada $E_i$ |
| :--- | :--- | :--- |
| **A** | 325 | $\frac{3}{6} \times 635 = 317.5$ |
| **B** | 110 | $\frac{1}{6} \times 635 = 105.83$ |
| **C** | 101 | $\frac{1}{6} \times 635 = 105.83$ |
| **D** | 99 | $\frac{1}{6} \times 635 = 105.83$ |
[cite_start][cite: 6]

[cite_start]**Estadística de prueba $\chi^2$** [cite: 7]
La estadística de prueba $\chi^2$ se define como:
$\chi^2 = \sum_{i=1}^{k} \frac{(O_i - E_i)^2}{E_i}$
Sustituyendo los valores observados y esperados:
$\chi^2 = \frac{(325-317.5)^2}{317.5} + \frac{(110-105.83)^2}{105.83} + \frac{(101-105.83)^2}{105.83} + \frac{(99-105.83)^2}{105.83}$
Realizando los cálculos, obtenemos:
$\chi^2 = 1.00$

**Grados de libertad**
El número de grados de libertad es:
$df = k - 1 = 4 - 1 = 3$

**Valor p**
El valor p asociado a la estadística $\chi^2 = 1.00$ con 3 grados de libertad se calcula como:
$p = P(\chi^2 > 1.00) \approx 0.8013$

[cite_start]Por todo lo expuesto, concluimos que dado que el p-valor ($p \approx 0.8013$) es mucho mayor que el nivel de significación típico ($\alpha = 0.05$), no podemos rechazar la hipótesis nula $H_0$. [cite: 8] [cite_start]Es decir, no hay evidencia suficiente para refutar la sospecha de que las proporciones de ciberataques siguen la distribución 3:1:1:1. [cite: 9]

---

[cite_start]**2.** Con el comando `random.normalvariate(5,3)` de la librería random de Python, hemos generado 20 valores de una normal con el siguiente resultado: [cite: 10]
7.71, 4.23, 7.84, 1.61, 7.42, 6.3, 8.66, 1.81, 11.28, 3.98, 4.32, 5.13, 4.67, 3.68, 6.02, 2.72, 5.82, 5.15, 6.11, 4.61
[cite_start]¿Tenemos razones para pensar que el comando funciona mal? [cite: 10] [cite_start]¿Por qué? [cite: 11]
[cite_start]Nota: $\bar{X}=5.4535$, $S=2.3$ [cite: 11]

**Solución**

**Hipótesis**
* [cite_start]$H_0$: Los datos siguen la distribución $N(5, 3^2)$. [cite: 11]
* [cite_start]$H_1$: Los datos no siguen la distribución $N(5, 3^2)$. [cite: 12]

**Definición de intervalos**
[cite_start]Al tener una muestra de tamaño 20, sería conveniente definir intervalos donde tuviéramos al menos, 5 valores esperados, por tanto, probabilidad 0.25. [cite: 12] [cite_start]Se requiere calcular 4 intervalos disjuntos para una variable aleatoria normal con media $\mu=5$ y varianza $\sigma^2=9$ (desviación estándar $\sigma=3$), tales que la probabilidad de que la variable esté dentro de cada intervalo sea 0.25. [cite: 13]

**Método**
Primero calculamos los valores de una distribución estándar $N(0,1)$ y los adaptamos a la escala de $N(5,9)$ usando:
$x = \mu + \sigma z$
Donde z son los valores críticos obtenidos.

**Resultados**
Los valores z para dividir la N(0,1) en 4 intervalos de igual probabilidad (cuartiles) son:
$z_{0.25} = -0.675$, $z_{0.5} = 0$, $z_{0.75} = 0.675$
Adaptando a la escala $N(5,3^2)$, los límites de los intervalos son:
* Límite 1: $5 + 3 \times (-0.675) = 2.975 \approx 2.98$
* Límite 2: $5 + 3 \times 0 = 5.00$
* Límite 3: $5 + 3 \times (0.675) = 7.025 \approx 7.02$

Los intervalos y las frecuencias son:

| Intervalo | Frecuencia Observada $(O_i)$ | Frecuencia Esperada $(E_i)$ |
| :--- | :--- | :--- |
| $(-\infty, 2.98)$ | 3 | 5 |
| $(2.98, 5.00)$ | 6 | 5 |
| $(5.00, 7.02)$ | 6 | 5 |
| $(7.02, \infty)$ | 5 | 5 |
[cite_start][cite: 14]

[cite_start]El estadístico chi-cuadrado se calcula como: [cite: 15]
$\chi^2 = \sum \frac{(O_i - E_i)^2}{E_i}$
Sustituyendo los valores:
[cite_start]$\chi^2 = \frac{(3-5)^2}{5} + \frac{(6-5)^2}{5} + \frac{(6-5)^2}{5} + \frac{(5-5)^2}{5} = 1.2$ [cite: 15]

**Decisión**
* [cite_start]**Grados de libertad (gl):** $gl = (\text{número de intervalos}) - 1 - (\text{número de parámetros estimados}) = 4 - 1 - 0 = 3$ [cite: 16]
* [cite_start]**Valor crítico** $\chi^2_{critico}$ para $\alpha=0.05$ y $gl=3$: $\chi^2_{critico} \approx 7.81473$ [cite: 17]
* [cite_start]**P-Valor**: $p = 0.753$ [cite: 16]

[cite_start]Como $\chi^2 = 1.2 \le \chi^2_{critico} \approx 7.81473$ o equivalentemente $p = 0.753 > 0.05$, no rechazamos la hipótesis nula ($H_0$). [cite: 17]
[cite_start]No hay evidencia suficiente al nivel de significación del 5% para rechazar que los datos provienen de una distribución normal $N(5, 3^2)$. [cite: 17]

---

[cite_start]**3.-** Bajo la suposición de que los datos anteriores sí sean de la distribución normal, [cite: 18]
[cite_start]a) Da un intervalo de confianza al 95% de la media de la distribución. [cite: 18, 19]
[cite_start]b) ¿Podemos pensar que la media es superior a 5? [cite: 19]
[cite_start]c) ¿Podemos pensar que la varianza no es 5.3? [cite: 19]

[cite_start]**Solución** [cite: 20]

[cite_start]**a) Intervalo de confianza al 95%.** [cite: 20]
Dado que asumimos que los datos provienen de una distribución normal, el intervalo de confianza para la media $\mu$ al 95% se calcula con la fórmula:
[cite_start]$IC = \bar{x} \pm t_{\alpha/2, n-1} \cdot \frac{s}{\sqrt{n}}$ [cite: 20]
donde:
* [cite_start]$\bar{x} = 5.45$ Media muestral. [cite: 20]
* [cite_start]$s = 2.36$ Desviación estándar muestral. [cite: 21]
* [cite_start]$n = 20$ Tamaño de la muestra. [cite: 21]
* [cite_start]$t_{0.025, 19} = 2.093$ Cuantil para un nivel de confianza del 95% y 19 grados de libertad. [cite: 21]

El margen de error es:
[cite_start]$ME = t_{0.025, 19} \cdot \frac{s}{\sqrt{n}} = 2.093 \cdot \frac{2.36}{\sqrt{20}} \approx 1.1$ [cite: 22]
Por lo tanto, el intervalo de confianza es:
[cite_start]$I_{95\%} = [5.45 - 1.1, 5.45 + 1.1] = [4.35, 6.56]$ [cite: 22]

**b) ¿Podemos pensar que la media es superior a 5?**
Planteamos un contraste de hipótesis:
* [cite_start]Hipótesis nula ($H_0$): $\mu \le 5$ (La media es menor o igual a 5). [cite: 22]
* [cite_start]Hipótesis alternativa ($H_1$): $\mu > 5$ (La media es mayor a 5). [cite: 23]
* [cite_start]**Nivel de significación**: 5% ($\alpha = 0.05$). [cite: 24]
* [cite_start]**Estadístico de prueba**: $t = \frac{\bar{x} - \mu_0}{s / \sqrt{n}}$ [cite: 25]
    [cite_start]Sustituyendo los valores: $t = \frac{5.45 - 5}{2.36 / \sqrt{20}} \approx 0.86$ [cite: 25]
* [cite_start]**Región de rechazo**: El valor crítico para una cola derecha con $\alpha = 0.05$ y $n-1 = 19$ grados de libertad es: $t_{critico} = t_{0.95, 19} = 1.73$. [cite: 25]

**Decisión**
* [cite_start]Como $t = 0.86 \le t_{critico} = 1.73$, no rechazamos $H_0$. [cite: 25]
* [cite_start]El valor p asociado al estadístico $t=0.86$ es: $p = 0.200$. [cite: 26]
* [cite_start]Dado que $p > 0.05$, tampoco rechazamos $H_0$. [cite: 26]

**Conclusión**
[cite_start]No hay evidencia suficiente al nivel de significación del 5% para afirmar que la media de los datos es superior a 5. [cite: 26]

**c) ¿Podemos pensar que la varianza no es 5.3?**
Se plantea el contraste:
* [cite_start]Hipótesis nula ($H_0$): $\sigma^2 = 5.3$ (La varianza poblacional es igual a 5.3). [cite: 26]
* [cite_start]Hipótesis alternativa ($H_1$): $\sigma^2 \ne 5.3$ (La varianza poblacional es diferente de 5.3). [cite: 27]
* [cite_start]**Estadístico de prueba**: $\chi^2 = \frac{(n-1) \cdot s^2}{\sigma_0^2}$ [cite: 29]
    [cite_start]donde: $n=20$, $s^2 = 2.36^2 = 5.57$, $\sigma_0^2 = 5.3$. [cite: 28, 29]
    [cite_start]Sustituyendo los valores: $\chi^2 = \frac{(20-1) \cdot 5.57}{5.3} \approx 19.93$ [cite: 29]
* [cite_start]**Región de rechazo**: El contraste es bilateral con $\alpha=0.05$. [cite: 29] [cite_start]Los valores críticos se obtienen de la distribución chi-cuadrado con $n-1=19$ grados de libertad: [cite: 30]
    * [cite_start]$\chi^2_{\alpha/2, 19} = \chi^2_{0.025, 19} = 8.91$ [cite: 30]
    * [cite_start]$\chi^2_{1-\alpha/2, 19} = \chi^2_{0.975, 19} = 32.85$ [cite: 30]
    [cite_start]La región de rechazo es: $\chi^2 < 8.91$ o $\chi^2 > 32.85$. [cite: 30]

**Decisión**
[cite_start]Dado que $8.91 \le \chi^2 = 19.93 \le 32.85$, no rechazamos la hipótesis nula ($H_0$). [cite: 30, 31] [cite_start]Adicionalmente, el p-valor es $p = 0.798 > 0.05$. [cite: 30]

**Conclusión**
[cite_start]No hay evidencia suficiente al nivel de significancia del 5% para rechazar que la varianza poblacional sea igual a 5.3. [cite: 31] [cite_start]Por lo tanto, podemos aceptar que $\sigma^2 = 5.3$. [cite: 32]

---
[cite_start]**4.-** En un experimento sobre dos muestras de betatesters se les hace jugar hasta que no puedan aguantar más a dos versiones distintas del juego para medirles el umbral de soporte. [cite: 32] [cite_start]Los datos obtenidos (en tiempo de aguante) están en la siguiente tabla: [cite: 33]

| | Versión 1 | Versión 2 |
| :--- | :--- | :--- |
| **n** | 14 | 10 |
| **$\bar{x}$** | 16.2 | 14.9 |
| **$s^2$** | 12.7 | 26.4 |
[cite_start][cite: 34]

[cite_start]a) ¿Muestran los datos que hay evidencia de que hay diferencias en el tiempo que se soporta el juego? [cite: 35]
[cite_start]b) Si debes realizar uno o varios contrastes, utiliza el p-valor en alguno de ellos. [cite: 36]

[cite_start]**Solución** [cite: 37]

**1. [cite_start]Contrastar si las varianzas son iguales** [cite: 37]
[cite_start]Para comparar las varianzas de dos poblaciones, se realiza una prueba F, donde la hipótesis nula establece que las varianzas son iguales: [cite: 37]
[cite_start]$H_0: \sigma_1^2 = \sigma_2^2$ vs $H_1: \sigma_1^2 \ne \sigma_2^2$ [cite: 37]
El estadístico de prueba es: $F = \frac{s_{mayor}^2}{s_{menor}^2} = \frac{26.4}{12.7} \approx 2.079$
[cite_start]Los grados de libertad son $df_1=10-1=9$ (para la varianza mayor) y $df_2=14-1=13$ (para la varianza menor). [cite: 37]
[cite_start]Para un nivel de significación $\alpha=0.05$, consultamos los valores críticos de F(9,13) en tablas: [cite: 37]
* [cite_start]$F_{superior} = F_{\alpha/2, 9, 13} = 3.68$ [cite: 37]
* [cite_start]$F_{inferior} = F_{1-\alpha/2, 9, 13} = \frac{1}{F_{\alpha/2, 13, 9}} \approx \frac{1}{3.33} \approx 0.30$ [cite: 37]
[cite_start]El valor calculado $F=2.079$ se encuentra entre los valores críticos, lo que indica que el p-valor es mayor a 0.05. [cite: 37]
**Conclusión:** No se rechaza $H_0$. [cite_start]Las varianzas pueden considerarse iguales. [cite: 38]

**2. [cite_start]Contrastar si hay diferencias en los tiempos de soporte** [cite: 38]
[cite_start]Ya que no se rechazó la igualdad de varianzas, realizamos una prueba t de Student para muestras independientes con varianzas iguales. [cite: 39]
* [cite_start]**Hipótesis:** $H_0: \mu_1 = \mu_2$ vs $H_1: \mu_1 \ne \mu_2$. [cite: 40]
* [cite_start]**Estadístico de prueba:** $t = \frac{\bar{x}_1 - \bar{x}_2}{s_p \sqrt{\frac{1}{n_1} + \frac{1}{n_2}}}$ [cite: 40]
* [cite_start]**Varianza combinada ($s_p^2$):** $s_p^2 = \frac{(n_1-1)s_1^2 + (n_2-1)s_2^2}{n_1+n_2-2}$ [cite: 40]
    [cite_start]Sustituyendo los valores: $s_p^2 = \frac{(14-1)(12.7) + (10-1)(26.4)}{14+10-2} = \frac{165.1 + 237.6}{22} \approx 18.28$. [cite: 40]
    [cite_start]$s_p = \sqrt{18.28} \approx 4.28$ [cite: 40]
* [cite_start]**Cálculo del estadístico t:** $t = \frac{16.2 - 14.9}{4.28 \sqrt{\frac{1}{14} + \frac{1}{10}}} = \frac{1.3}{4.28 \cdot 0.446} \approx \frac{1.3}{1.91} \approx 0.681$ [cite: 40]
* [cite_start]**Grados de libertad:** $df = n_1 + n_2 - 2 = 14 + 10 - 2 = 22$. [cite: 40]
* [cite_start]**Decisión:** Para $t=0.681$ con $df=22$, el p-valor es mayor a 0.05. [cite: 40]

**Conclusión:** No se rechaza $H_0$. [cite_start]No hay evidencia significativa para afirmar que existen diferencias en los tiempos de soporte entre las dos versiones del juego. [cite: 41]

**3. [cite_start]Uso del p-valor** [cite: 42]
* [cite_start]En el contraste de varianzas, el p-valor fue mayor a 0.05, por lo que no se rechazó la igualdad de varianzas. [cite: 42]
* [cite_start]En el contraste de medias, el p-valor también fue mayor a 0.05, indicando que no hay evidencia suficiente para rechazar la igualdad de medias. [cite: 43]

**Resumen:**
* [cite_start]Las varianzas pueden considerarse iguales. [cite: 44]
* [cite_start]No hay evidencia significativa para afirmar que hay diferencias en los tiempos de soporte entre las dos versiones del juego. [cite: 44]

---
[cite_start]**5.** A la hora de plantear la resolución de problemas a un LLM, se han detectado los siguientes porcentajes de errores en función de si se planteaba a GPT4, Gemini, Claude v1, Cohere, Copilot: [cite: 45, 46]

| | GPT4 | Gemini | Claude | Cohere | Copilot |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Datos** | 24 | 33 | 24 | 50 | 32 |
| | 37 | 20 | 40 | 20 | 62 |
| | 22 | 28 | 63 | 30 | 40 |
| | 55 | 12 | 18 | 13 | 15 |
| | 23 | 17 | 62 | 42 | 26 |
| | 38 | 17 | 30 | 28 | 37 |
| | 46 | 57 | 38 | 17 | 52 |
| | 25 | 42 | 23 | 73 | 12 |
| | 25 | 25 | 37 | 25 | 16 |
| | 23 | 63 | 26 | 22 | 25 |
| **$\bar{X_i}$** | 31.27 | 31.73 | 35.09 | 33.73 | 31.55 |
| **$S_i$** | 11.01 | 16.56 | 14.86 | 17.42 | 15.55 |
[cite_start][cite: 47]

[cite_start]La media global es $\bar{X}=32.67$ y la varianza global es $S=14.744$. [cite: 48] [cite_start]Hemos comprobado también que las varianzas son homogéneas. [cite: 48] [cite_start]¿Podemos afirmar si hay diferencias entre los modelos planteados? [cite: 49] [cite_start]¿Por qué? [cite: 49]

[cite_start]**Solución** [cite: 50]
* **Hipótesis nula ($H_0$):** $\mu_{GPT4}=\mu_{Gemini}=\mu_{Claude}=\mu_{Cohere}=\mu_{Copilot}$. [cite_start]No hay diferencias en las medias de los modelos. [cite: 50]
* [cite_start]**Hipótesis alternativa ($H_1$):** Al menos una de las medias es diferente. [cite: 50]

**Cálculo del estadístico F**
* [cite_start]**Suma de cuadrados entre grupos ($SS_B$):** $SS_B = n \sum_{i=1}^{k} (\bar{X_i} - \bar{X})^2 \approx 10 \cdot [(31.27-32.67)^2 + (31.73-32.67)^2 + (35.09-32.67)^2 + (33.73-32.67)^2 + (31.55-32.67)^2] \approx 110.78$ [cite: 50]
* [cite_start]**Suma de cuadrados dentro de los grupos ($SS_W$):** $SS_W = \sum_{i=1}^{k} (n_i - 1) \cdot S_i^2 = 9 \cdot [(11.01)^2 + (16.56)^2 + (14.86)^2 + (17.42)^2 + (15.55)^2] = 10453.79$ [cite: 50]
* [cite_start]**Grados de libertad:** $df_B = k - 1 = 4$, $df_W = N - k = 50 - 5 = 45$. [cite: 50]
* **Media cuadrática:**
    * [cite_start]$MS_B = \frac{SS_B}{df_B} = \frac{110.78}{4} = 27.70$ [cite: 50]
    * [cite_start]$MS_W = \frac{SS_W}{df_W} = \frac{10453.79}{45} = 232.31$ [cite: 50]
* [cite_start]**Estadístico F:** $F = \frac{MS_B}{MS_W} = \frac{27.70}{232.31} = 0.12$ [cite: 50]

**Valores críticos y p-valor**
* [cite_start]**Valor crítico ($F_{critico}$):** $F_{critico} = F_{0.95, 4, 45} = 2.58$. [cite: 51]
* [cite_start]**p-valor:** $p = 0.975$. [cite: 51]

**Decisión**
[cite_start]Como $F = 0.12 \le F_{critico} = 2.58$ y $p = 0.975 > 0.05$, no rechazamos la hipótesis nula ($H_0$), por lo que NO hay evidencia suficiente al nivel de significancia del 5% para afirmar que existen diferencias significativas entre los modelos en términos de porcentaje de error. [cite: 51] [cite_start]Esto indicaría que los modelos presentan un comportamiento similar en este aspecto. [cite: 52]

[cite_start]*2 Puntos por ejercicio.* [cite: 52]