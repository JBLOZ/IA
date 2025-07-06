# Universitat d'Alacant
## Universidad de Alicante
### Métodos de Inferencia (GAT)
### Examen 14/1/2025

[cite_start]**1.- (1 Punto)** Sabemos que el 55% de la población utiliza Tik Tuk, el 30% feisbuk y el 20% ambos. [cite: 1] [cite_start]Si elegimos una persona al azar: [cite: 2]
[cite_start]a) Sabiendo que utiliza TikTuk, ¿Cuál es la probabilidad de que también utilice feisbuk? [cite: 2]
[cite_start]b) Si utiliza feisbuk, ¿Cuál es la probabilidad de que no utilice Tik Tuk? [cite: 3]
[cite_start]c) ¿Cuál es la probabilidad de que no utilice ninguna de estas dos redes sociales? [cite: 4]

[cite_start]**Solución** [cite: 5]

[cite_start]Consideramos [cite: 5]
* [cite_start]El suceso A: La persona utiliza Tik Tuk. [cite: 5]
* [cite_start]El suceso B: La persona utiliza Feisbuk. [cite: 5]

[cite_start]Con esta reinterpretación, tendríamos que: [cite: 6]
[cite_start]$P(A) = 0.55$, $P(B) = 0.30$, $P(A \cap B) = 0.20$ [cite: 6]

[cite_start]a) Nos están preguntando la siguiente probabilidad condicional: [cite: 6]
[cite_start]$P(B|A) = \frac{P(A \cap B)}{P(A)}$ [cite: 6]
[cite_start]Sustituyendo los valores: [cite: 6]
[cite_start]$P(B|A) = \frac{0.20}{0.55} \approx 0.364$ [cite: 6]
[cite_start]Por lo tanto, la probabilidad es aproximadamente 36.4%. [cite: 6]

[cite_start]b) Si utiliza Feisbuk, ¿cuál es la probabilidad de que no utilice TikTuk? [cite: 7]
[cite_start]La probabilidad de que no utilice Tik Tuk dado que utiliza Feisbuk es: [cite: 8]
[cite_start]$P(A'|B) = 1 - P(A|B)$ [cite: 8]
[cite_start]Primero calculamos $P(A|B)$: [cite: 8]
[cite_start]$P(A|B) = \frac{P(A \cap B)}{P(B)} = \frac{0.20}{0.30} \approx 0.667$ [cite: 8]
[cite_start]Entonces: [cite: 8]
[cite_start]$P(A'|B) = 1 - 0.667 = 0.333$ [cite: 8]
[cite_start]Por lo tanto, la probabilidad es aproximadamente 33.3%. [cite: 8]

[cite_start]c) Primero calculamos la probabilidad de que una persona utilice al menos una de las dos redes sociales: [cite: 9]
[cite_start]$P(A \cup B) = P(A) + P(B) - P(A \cap B)$ [cite: 9]
[cite_start]Sustituyendo los valores: [cite: 9]
[cite_start]$P(A \cup B) = 0.55 + 0.30 - 0.20 = 0.65$ [cite: 9]
[cite_start]Por lo tanto, la probabilidad de que no utilice ninguna de estas redes sociales es el complementario: [cite: 9]
[cite_start]$P((A \cup B)') = 1 - P(A \cup B) = 1 - 0.65 = 0.35$ [cite: 9]
[cite_start]Así que la probabilidad es 35%. [cite: 9]

---

[cite_start]**2.- (1,5 Puntos)** Considera $X \sim N(3, \sigma=5)$, $Y \sim N(4, \sigma^2=6)$, $W \sim F_{4,5}$. [cite: 10] [cite_start]Calcula: [cite: 11]
[cite_start]a) Los percentiles 25, 50 y 75 de X. [cite: 11]
[cite_start]b) Los percentiles 20, 30, 60 y 80 de $X+Y$. [cite: 11]
[cite_start]c) El percentil 10 de W. [cite: 11]
[cite_start]d) Un intervalo de confianza al 80% para W. [cite: 11]

**Solución**

a) Percentiles 25, 50 y 75 de X:
[cite_start]Para calcular el percentil 50, $P_{50}$, solo cabe tener presente las propiedades de simetría de la normal. [cite: 11] [cite_start]Así, tenemos que $P_{50}=3$. [cite: 12] [cite_start]Por otro lado y también basándonos en la simetría, solo habría que calcular un percentil ya que el otro se deduciría con facilidad a partir del anterior. [cite: 12] [cite_start]Por ejemplo el Percentil 75: [cite: 13]
[cite_start]Observa que $\frac{X-3}{5} = Z$ entendiendo por Z una normal estándard $N(0,1)$ que tenemos tabulada. [cite: 13] [cite_start]Así que calculamos el percentil 75 de Z, que venimos representando como $Z_{0.25} \approx 0.674$. [cite: 14]

[cite_start]Los valores de $z_p$ son: [cite: 16]
[cite_start]$z_{0.25} = 0.674$ [cite: 16]
[cite_start]$z_{0.50} = 0$ [cite: 16]
[cite_start]$z_{0.75} = -0.674$ [cite: 16]

[cite_start]Cálculos: [cite: 16]
[cite_start]$P_{25} = 3 + (-0.674) \cdot 5 = 3 - 3.37 = -0.37$ [cite: 16]
[cite_start]$P_{50} = 3 + (0) \cdot 5 = 3$ [cite: 16]
[cite_start]$P_{75} = 3 + (0.674) \cdot 5 = 3 + 3.37 = 6.37$ [cite: 16]

b) Percentiles 20, 30, 60 y 80 de $X+Y$:
[cite_start]Sabemos que $X+Y \sim N(\mu_{X+Y}, \sigma_{X+Y}^2) \sim N(7, \sqrt{31})$. [cite: 16] [cite_start]Observa que: [cite: 17]
[cite_start]$\sigma_{X+Y}^2 = \sigma_X^2 + \sigma_Y^2 = 5^2 + 6 = 25 + 6 = 31$, $\sigma_{X+Y} = \sqrt{31} \approx 5.57$ [cite: 17]

[cite_start]Repetimos el razonamiento anterior, después de haber calculado los respectivos percentiles de la $N(0,1)$: [cite: 17]
[cite_start]$z_{0.20} = 0.841$, $z_{0.70} = 0.524$, $z_{0.40} = 0.253$, $z_{0.80} = -0.841$ [cite: 18]

[cite_start]Percentiles de $X+Y$: [cite: 18]
[cite_start]$P_{20} = 7 + (-0.841) \cdot 5.57 \approx 7 - 4.68 = 2.32$ [cite: 18]
[cite_start]$P_{30} = 7 + (-0.524) \cdot 5.57 \approx 7 - 2.92 = 4.08$ [cite: 18]
[cite_start]$P_{60} = 7 + (0.253) \cdot 5.57 \approx 7 + 1.41 = 8.41$ [cite: 18]
[cite_start]$P_{80} = 7 + (0.841) \cdot 5.57 \approx 7 + 4.68 = 11.68$ [cite: 18]

c) Percentil 10 de $W \sim F_{4,5}$
[cite_start]El percentil 10 se define como el valor w tal que: [cite: 18]
[cite_start]$P(W \le w) = 0.10$ [cite: 18]
[cite_start]Usando tablas o software estadístico, obtenemos: [cite: 18]
[cite_start]$F_{0.10,4,5} = \frac{1}{F_{0.9,5,4)}} \approx \frac{1}{4.05} \approx 0.2469$ [cite: 18]
[cite_start]Por lo tanto: [cite: 18]
[cite_start]$P_{10} \approx 0.2469$ [cite: 18]

d) Intervalo de confianza al 80% para $W \sim F_{4,5}$:
[cite_start]Un intervalo de confianza al 80% para W está definido por los valores $w_1$ y $w_2$ tales que: [cite: 18]
[cite_start]$P(w_1 \le W \le w_2) = 0.80$ [cite: 18]
[cite_start]Esto implica: [cite: 18]
[cite_start]$P(W \le w_1) = 0.10$ y $P(W \le w_2) = 0.90$ [cite: 18]
[cite_start]Usando tablas o software estadístico, obtenemos: [cite: 18]
[cite_start]$F_{0.10,4.5} \approx 0.2469$, $F_{0.90,4.5} \approx 3.52$ [cite: 18]
[cite_start]Por lo tanto, el intervalo de confianza al 80% es: [cite: 18]
[cite_start][0.25, 3.52] [cite: 18]

---

[cite_start]**3.- (1.5 Puntos)** X se distribuye normalmente con media 200. Se sabe que la probabilidad de que X sea superior a 250 es 0,2. [cite: 24] [cite_start]Calcular: [cite: 25]
[cite_start]a) ¿Cuál es la probabilidad de que X sea inferior a 150? [cite: 25]
[cite_start]b) ¿Cuál es la varianza de X? [cite: 25]
[cite_start]c) ¿Cuál es la probabilidad de que $X > 300$? [cite: 26]
[cite_start]d) ¿Cuántos valores de X, independientes, deben observarse para tener una probabilidad mayor que 0,5 de que al menos el mayor de ellos sea superior a 300? [cite: 26]

[cite_start]**Solución** [cite: 27]

a) Para este cálculo, primero debemos calcular la varianza. [cite_start]Así adelantaremos ya la respuesta al apartado siguiente. [cite: 27] [cite_start]Usamos el dato $P(X > 250) = 0.2$. [cite: 28] [cite_start]Sabemos que: [cite: 28]
[cite_start]$P(X>250) = P(Z > \frac{250-200}{\sigma}) = 0.2$ [cite: 28]
[cite_start]Esto implica: [cite: 28]
[cite_start]$P(Z > \frac{50}{\sigma}) = 0.2$ [cite: 28]
[cite_start]De las tablas o software, sabemos que: [cite: 28]
[cite_start]$P(Z > 0.8416) = 0.2$ [cite: 28]
[cite_start]Por lo tanto: [cite: 28]
[cite_start]$\frac{50}{\sigma} = 0.8416 \Rightarrow \sigma = \frac{50}{0.8416} \approx 59.39$ [cite: 28]
[cite_start]Ahora calculamos $P(X < 150)$: [cite: 28]
[cite_start]$P(X<150) = P(Z < \frac{150-200}{\sigma}) = P(Z < \frac{-50}{59.39})$ [cite: 28]
[cite_start]$P(X<150) = P(Z < -0.8416)$ [cite: 28]
[cite_start]De las tablas, $P(Z < -0.8416) \approx 0.2$. [cite: 28] [cite_start]Por lo tanto: [cite: 28]
[cite_start]$P(X < 150) \approx 0.2$ [cite: 28]
[cite_start]Nota: Podríamos haber llegado a la misma conclusión simplemente aplicando simetría de la normal, puesto que la media es 200 y se está planteando la probabilidad en un valor simétrico al valor donde se conoce ya la probabilidad. [cite: 28]

[cite_start]b) La varianza de X es: $Var(X) = \sigma^2 = 59.39^2 \approx 3536.26$ [cite: 32]

[cite_start]c) $P(X > 300) = P(Z > \frac{300-200}{\sigma}) = P(Z > \frac{100}{59.39}) = P(Z > 1.683)$ [cite: 32]
[cite_start]De las tablas, $P(Z > 1.683) \approx 1 - 0.954 \approx 0.046 \rightarrow P(X > 300) \approx 0.046$ [cite: 32]

[cite_start]d) La probabilidad de que al menos uno de los n valores sea superior a 300 es: [cite: 35]
$P(\text{al menos uno superior a 300}) = 1 - P(X \le 300)^n$
[cite_start]$P(X \le 300) = 1 - P(X > 300) = 1 - 0.046 = 0.954$ [cite: 35]
[cite_start]Queremos que: [cite: 35]
[cite_start]$1 - (0.954)^n > 0.5 \rightarrow (0.954)^n < 0.5$ [cite: 35]
[cite_start]Tomamos logaritmos: [cite: 36]
[cite_start]$n \cdot \ln(0.954) < \ln(0.5) \rightarrow n > \frac{\ln(0.5)}{\ln(0.954)} \approx \frac{-0.6931}{-0.0469} \approx 14.77$ [cite: 36]
[cite_start]Por lo tanto, se necesitan al menos $n=15$ observaciones de X. [cite: 36]

---
[cite_start]**4.- (2 Puntos)** En el tiempo de respuesta, medido en segundos, a determinado tipo de preguntas de dos tipos de redes neuronales artificiales (RNA), A y B, se han registrado los siguientes datos: [cite: 37]

| | n | $\bar{x}$ | $s^2$ |
| :--- | :-: | :---: | :---: |
| **RNA A** | 15 | 16.2 | 23.7 |
| **RNA B** | 11 | 14.9 | 26.4 |
[cite_start][cite: 38]

[cite_start]a) ¿Muestran los datos que hay evidencia de diferencias en el tiempo de respuesta de cada una? [cite: 39] [cite_start]Si debes realizar uno o varios contrastes, utiliza el p-valor en alguno de ellos. [cite: 40]

[cite_start]**Solución** [cite: 41]

1.  [cite_start]**Primero contrastamos si las varianzas son iguales para poder determinar el siguiente contraste** [cite: 41]
    [cite_start]Para comparar las varianzas de dos poblaciones, se realiza una prueba F, donde la hipótesis nula establece que las varianzas son iguales: [cite: 41]
    [cite_start]$H_0: \sigma_A^2 = \sigma_B^2$ [cite: 41]
    [cite_start]$H_1: \sigma_A^2 \ne \sigma_B^2$ [cite: 41]

    [cite_start]El estadístico de prueba es: $F = \frac{s_A^2}{s_B^2}$ [cite: 41]
    [cite_start]Sustituyendo los valores: $F = \frac{23.7}{26.4} \approx 0.8978$ [cite: 41]
    [cite_start]Los grados de libertad son: $df_A = n_A - 1 = 15 - 1 = 14$ y $df_B = n_B - 1 = 11 - 1 = 10$. [cite: 41]

    [cite_start]Para un nivel de significación $\alpha = 0.05$, consultamos los valores críticos de F(14,10) en tablas: [cite: 41]
    [cite_start]$F_{\alpha/2, 14, 10} \approx 3.55$ [cite: 41]
    [cite_start]$F_{1-\alpha/2, 14, 10} = \frac{1}{F_{\alpha/2, 10, 14}} \approx \frac{1}{3.15} \approx 0.318$ [cite: 41]

    [cite_start]El valor calculado F se encuentra entre los valores críticos, [0.318, 3.55]. [cite: 41]
    [cite_start]Conclusión: No se rechaza $H_0$. [cite: 41] [cite_start]Las varianzas pueden considerarse iguales a un nivel de significación $\alpha=0.05$. [cite: 42]

2.  [cite_start]**Contrastar si hay diferencias en los tiempos de soporte (su media)** [cite: 42]
    [cite_start]Ya que no se rechazó la igualdad de varianzas, realizamos una prueba t de Student para muestras independientes asumiendo que las varianzas son iguales. [cite: 42] [cite_start]Las hipótesis son: [cite: 43]
    * [cite_start]$H_0: \mu_A = \mu_B$ (las medias son iguales). [cite: 43]
    * [cite_start]$H_a: \mu_A \ne \mu_B$ (las medias son diferentes). [cite: 43]

    [cite_start]El estadístico de prueba es: $t = \frac{|\bar{x}_A - \bar{x}_B|}{s_p \sqrt{\frac{1}{n_A} + \frac{1}{n_B}}}$ [cite: 43]
    [cite_start]donde $s_p^2$ es la varianza agrupada (pooled variance), calculada como: $s_p^2 = \frac{(n_A - 1)s_A^2 + (n_B - 1)s_B^2}{n_A + n_B - 2}$ [cite: 44]

    [cite_start]Sustituyendo los valores: [cite: 45]
    [cite_start]$s_p^2 = \frac{14 \cdot 23.7 + 10 \cdot 26.4}{24} = \frac{331.8 + 264}{24} = \frac{595.8}{24} \approx 24.825 \rightarrow s_p = \sqrt{24.825} \approx 4.982$ [cite: 45]
    [cite_start]$t = \frac{16.2 - 14.9}{4.982 \cdot \sqrt{\frac{1}{15} + \frac{1}{11}}} \approx 0.657$ [cite: 45]
    [cite_start]Los grados de libertad son $df = n_1 + n_2 - 2 = 15 + 11 - 2 = 24$. [cite: 45]
    [cite_start]Para $t = 0.657$ con $df=24$, el p-valor es superior a 0.25, por lo que es mayor a 0.05, por lo tanto no hay evidencia para rechazar la hipótesis. [cite: 45]

    **Conclusión:** No se rechaza $H_0$. [cite_start]No hay evidencia significativa para afirmar que existen diferencias en los tiempos de soporte entre las dos versiones del juego. [cite: 48]

---

[cite_start]**5.- (2 Puntos)** En un experimento se han registrado los minutos transcurridos (t) y el nivel de bilirrubina (Y) en los testers de un nuevo videojuego: [cite: 49]

| t | 3 | 3,5 | 4 | 2.5 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 15 | 14 |
| :--- | :-: | :-: | :-: | :---: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| **Y** | 18 | 14 | 11,8 | 21,5 | 7,87 | 6,36 | 5,07 | 3,72 | 3,33 | 2,86 | 2,46 | 2,34 | 2,03 | 1,69 | 1,98 |
[cite_start][cite: 50]

[cite_start]Se ha obtenido que $\bar{t}=8.2$, $\bar{y}=7.002$, $\Sigma t_i Y_i=539.6$, $\Sigma t_i^2=1253.5$. [cite: 51]
[cite_start]¿Crees que hay relación lineal entre ambas variables? [cite: 51] [cite_start]Suponiendo que la respuesta fuera que sí, al cabo de 20 minutos, ¿cuál sería el nivel de bilirrubina? [cite: 52] [cite_start]Razona todas las respuestas. [cite: 53]

**Solución**
[cite_start]Bajo la suposición de que si existe relación lineal, debemos ajustar un modelo de regresión lineal simple para las variables t (tiempo en minutos) e Y (nivel de bilirrubina): [cite: 54]
[cite_start]$Y = a + bt$ [cite: 55]
[cite_start]Las fórmulas para calcular b y a son: [cite: 55]
[cite_start]$b = \frac{\Sigma t_i Y_i - n \bar{t} \bar{y}}{\Sigma t_i^2 - n \bar{t}^2}$ [cite: 55]
[cite_start]$a = \bar{y} - b \bar{t}$ [cite: 55]

[cite_start]Datos conocidos: [cite: 55]
* [cite_start]Media de t: $\bar{t}=8.2$ [cite: 51]
* [cite_start]Media de Y: $\bar{y}=7.002$ [cite: 51]
* [cite_start]Suma de productos: $\Sigma t_i Y_i = 539.6$ [cite: 51]
* [cite_start]Suma de cuadrados: $\Sigma t_i^2 = 1253.5$ [cite: 51]
* [cite_start]Número de observaciones: $n=15$ [cite: 55]

[cite_start]Pendiente b: [cite: 55]
[cite_start]$b = \frac{539.6 - 15(8.2)(7.002)}{1253.5 - 15(8.2)^2} \approx \frac{-321.646}{244.9} \approx -1.313$ [cite: 55]

[cite_start]Ordenada en el origen a: [cite: 55]
[cite_start]$a = \bar{y} - b\bar{t} = 7.002 - (-1.313)(8.2) = 17.772$ [cite: 55]

[cite_start]Ecuación de la recta: [cite: 55]
[cite_start]$Y = 17.77 - 1.31t$ [cite: 55]

[cite_start]Predicción para t=20: [cite: 55]
[cite_start]$Y(20) = 17.77 - 1.31(20) = -8.50$ [cite: 55]

**Relación lineal**
[cite_start]Para determinar si hay una relación lineal, se calcula el coeficiente de correlación (r) y el coeficiente de determinación ($R^2$). [cite: 56]
[cite_start]Aprovechando cálculos previos: [cite: 58]
[cite_start]$r = \frac{\Sigma(t_i - \bar{t})(Y_i - \bar{Y})}{\sqrt{\Sigma(t_i - \bar{t})^2 \cdot \Sigma(Y_i - \bar{Y})^2}} = \frac{-321.646}{\sqrt{244.9} S_Y}$ [cite: 58]
[cite_start]El valor de $R^2$ es 0,739117516, el cual está suficientemente alejado de 1 como para no tener mucha confianza en la linealidad de la relación. [cite: 58]

[cite_start]**Conclusión** [cite: 59]
* [cite_start]La pendiente $b=-1.31$ indica que, en promedio, el nivel de bilirrubina disminuye en 1.31 unidades por cada minuto adicional. [cite: 59]
* [cite_start]La predicción para $t=20$ es $Y=-8.50$. [cite: 60] [cite_start]Sin embargo, dado que el nivel de bilirrubina no puede ser negativo, el modelo lineal no es adecuado para extrapolar más allá del intervalo observado ($2.5 \le t \le 15$). [cite: 60]

---

[cite_start]**6.- (2 Puntos)** El nuevo Chat de la UA (Aitana) ha registrado los siguientes usuarios (medidos en centenares) durante 10 semanas: [cite: 61]

| Día | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | w10 | $\bar{X_i}$ | $S_i$ |
| :--- | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :---: | :---: |
| **Lunes** | 26 | 37 | 22 | 55 | 23 | 38 | 46 | 25 | 25 | 23 | 32.2 | 11.36 |
| **Martes** | 35 | 20 | 28 | 12 | 17 | 17 | 57 | 42 | 25 | 63 | 31.5 | 17.46 |
| **Miércoles**| 25 | 40 | 63 | 18 | 62 | 30 | 38 | 23 | 37 | 26 | 36.1 | 15.63 |
| **Jueves** | 51 | 20 | 30 | 13 | 42 | 28 | 17 | 73 | 25 | 22 | 31.9 | 18.16 |
| **Viernes** | 30 | 62 | 40 | 15 | 26 | 37 | 52 | 12 | 16 | 25 | 31.4 | 16.41 |
[cite_start][cite: 62]

[cite_start]¿Crees que podemos afirmar que todos los días de la semana hay la misma afluencia de usuarios? [cite: 63] [cite_start](Suponer normalidad, independencia y homogeneidad de varianzas) [cite: 64]

[cite_start]**Solución** [cite: 65]

**Hipótesis a contrastar**
* [cite_start]$H_0$: Las medias de número de usuarios registrados son iguales para todos los días de la semana. [cite: 65]
* [cite_start]$H_a$: No todos los días se registra una misma media de usuarios. [cite: 65]

**Metodología**
[cite_start]Para realizar el contraste, utilizamos un análisis de varianza (ANOVA) de una vía. [cite: 65] [cite_start]El estadístico F se calcula como: [cite: 65]
[cite_start]$F = \frac{MSB}{MSW} = \frac{\frac{SSB}{k-1}}{\frac{SSW}{n-k}}$ [cite: 65]
[cite_start]donde k es el número de grupos (días), n es el número total de observaciones, SSB es la suma de cuadrados entre los grupos y SSW es la suma de cuadrados dentro de los grupos. [cite: 65]

**Resultados**
[cite_start]Dando por buenos los cálculos aportados en el enunciado: [cite: 65]
* [cite_start]Estadístico $F \approx 0.1521$ [cite: 65]
* [cite_start]p-valor $p = 0.9611$ [cite: 65]

**Conclusión**
[cite_start]Dado que el valor $p=0.9611$ es mucho mayor que el nivel de significación típico ($\alpha=0.05$), no se puede rechazar la hipótesis nula ($H_0$). [cite: 65]
[cite_start]Alternativamente, se rechaza $H_0$ si $0.1521 > F_{0.05;4,45}=2.5787$. [cite: 65] [cite_start]Por esta vía tampoco rechazamos $H_0$. [cite: 68]
[cite_start]Por lo tanto, no hay evidencia suficiente para afirmar que las medias de afluencia de usuarios son diferentes entre los días de la semana. [cite: 68] [cite_start]Esto implica que la afluencia diaria puede considerarse similar en promedio. [cite: 69]