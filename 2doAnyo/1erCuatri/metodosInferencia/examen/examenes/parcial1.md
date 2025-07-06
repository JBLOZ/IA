# Universitat d'Alacant
## Universidad de Alicante

### Examen 29/10/2024 A 

**1.-** Una potente empresa tiene en el mercado 3 redes sociales, TicTac, InstaKilo y TúyYo. En el Consejo de Administración de cada una, se ha planteado un debate ético sobre la conveniencia de adoptar medidas beligerantes en la lucha contra el cambio climático frente a la posición negacionista. En TicTac, la votación ha sido: 9 Beligerantes y 10 Negacionistas. En InstaKilo, 16 Beligerante y 17 Negacionistas y en Túy Yo empate a 18. Por tanto la empresa, escuchadas las posiciones de las tres redes (2 negacionistas y 1 empate) optaría por la posición negacionista. Si embargo, en una maniobra de última hora, se decide repetir la votación después de transferir por sorteo un miembro del consejo de administración de TicTac a InstaKilo y posteriormente una persona de InstaKilo a Túy Yo (también por sorteo). ¿Cuál es la probabilidad de que TúyYo tenga mayoría beligerante? ¿Cuál es la probabilidad de que si descubrimos al azar un miembro de Tú y Yo, éste sea de posición beligerante? Por otro lado, si sabemos que finalmente ha salido mayoría beligerante en Túy Yo, cuál es la probabilidad respectiva en cada caso de que TicTac sea beligerante, negacionista o neutral? 

**Solución** 

**Traslados de miembros y Primera cuestión** Se realizarán dos traslados:
1. Un miembro de TicTac se traslada a InstaKilo. Las probabilidades son: 
   P(Beligerante transferido) = $\frac{9}{19}$
   P(Negacionista transferido) = $\frac{10}{19}$

2. Un miembro de InstaKilo se traslada a TúyYo. Las probabilidades dependerán del primer traslado: 
   - Si se transfiere un beligerante de TicTac:
     P(Beligerante transferido a TúyYo) = $\frac{17}{34}$ P(Negacionista transferido a TúyYo) = $1 - \frac{17}{34}$
   - Si se transfiere un negacionista de TicTac:
     P(Beligerante transferido a TúyYo) = $\frac{16}{34}$ P(Negacionista transferido a TúyYo) = $1 - \frac{16}{34}$

Por tanto, la probabilidad de que tengamos mayoría beligerante en el tercer consejo es:
$\frac{9}{19} \cdot \frac{17}{34} + \frac{10}{19} \cdot \frac{16}{34} = \frac{313}{646} \approx 0.4845201238390093$

**Segunda cuestión** La probabilidad es similar a la anterior, solo que podría haber salido mayoría negacionista en lugar de beligerante. P(Mayoría negacionista en TúyYo) = $1 - 313/646$ Por tanto la probabilidad de elegir un miembro de Tuy Yo y que sea beligerante es: 

P (Mayoría negacionista en Yúy Yo) y P (Salga miembro beligerante) ó
P (Mayoría negacionista en Yúy Yo) y P (Salga miembro beligerante)

$P = \frac{11941}{23902} \approx 0.4995816249686219$

**Tercera cuestión**
Aplicando el teorema de bayes tenemos:
La probabilidad de que Tic Tac se haya quedado neutral es que la primera transferencia haya sido de un negacionista: 
$\frac{\frac{10}{19}\cdot\frac{16}{34}}{\frac{9}{19}\cdot\frac{17}{34}+\frac{10}{19}\cdot\frac{16}{34}}=\frac{160}{313}\approx0.5111821086261981$

La probabilidad de que TicTac siga negacionista es que la primera transferencia haya sido de un beligerante:
$\frac{\frac{9}{19}\cdot\frac{17}{34}}{\frac{9}{19}\cdot\frac{17}{34}+\frac{10}{19}\cdot\frac{16}{34}}=\frac{153}{313}\approx0.488178913738019$

Observa que la probabilidad de que pase a ser Beligerante es cero, ya que no hay posibilidad con un solo traslado de cambiar la mayoría.

---

**2.-** El peso que se asigna a la entrada de tipo A de una determinada red neuronal sigue una distribución normal $N(49.1,0.5)$. En las entradas de tipo B, una $N(56.1,0.8)$ Calcula:
a) Probabilidad de que la suma de los pesos de 20 entradas de tipo A no supere el umbral de 983.0. 
b) ¿Cuál es el peso acumulado de las entradas de una red neuronal con 11 entradas de tipo A y 11 entradas de tipo B que está por debajo del percentil 69? 
c) Si tenemos dos redes neuronales de las anteriores, Red1 y Red2, ¿Cuál es la probabilidad de que el peso acumulado de las entradas en la primera sea, al menos, una unidad mayor que el de la segunda? Y, ¿la probabilidad de que tengan el mismo peso acumulado? 

**Solución**

a) Si consideramos la v.a. $X$ = Peso acumulado en 20 entradas de tipo A, tenemos que: 
$X \sim N(982.0, 1.0\sqrt{5})$
Por tanto, $P(X < 983.0) \approx 0.9873263406612658$

b) Si consideramos la v.a. $Y$ = peso acumulado en la red neuronal especificada tendríamos que $Y \sim N(1157.2, 3.128897569432403))$. Por tanto nos están preguntando por el valor y tal que $P(Y < y) = \frac{69}{100}$ por lo que tendríamos $y = 472.0386744280353$ 

c) Si consideramos dos v.a. de las planteadas en el primer apartado, $X_1$, $X_2$, nos estarían preguntando por: 
$P(X_1 \ge X_2 + 1) = P(X_1 - X_2 \ge 1)$
Como $X_1 - X_2 \sim N(0, \sqrt{2} \cdot 3.128897569432403)$ tendríamos que:
$P(X_1 - X_2 \ge 1) \approx 0.3233507736521497$
Respecto a la probabilidad de que el peso acumulado sea el mismo, habría que tener en cuenta que $X_1 - X_2$ es una v.a. continua, por lo que dicha probabilidad es NULA. 

---

**3.-** Dada la f.d.p de la v.a. X 
$f(x) = \begin{cases} k(49-x^2) & si \quad |x| \le 7 \\ 0 & si \quad |x| > 7 \end{cases}$ 
Determina el valor de k, calcula $E[X]$ y $Var[X]$

**Solución**

**1. Calcular k**
Sabemos que la integral total de la función de densidad debe ser igual a 1:
$\int_{-7}^{7} k(49-x^2) dx = 1$
Resolvemos la integral y planteamos que:
$k \int_{-7}^{7} (49-x^2) dx = 1$
Por lo tanto, como:
$\int_{-7}^{7} (49-x^2) dx = \frac{1372}{3}$
Sustituyendo en la ecuación para k:
$k \cdot \frac{1372}{3} = 1 \Rightarrow k = \frac{3}{1372}$

**2. Calcular E(X)**
La esperanza matemática $E(X)$ está dada por:
$E(X) = \int_{-\infty}^{\infty} xf(x) dx = k \cdot \int_{-7}^{7} x(49-x^2) dx = 0$

**3. Calcular Var(X)**
La varianza está dada por:
$Var(X) = E(X^2) - [E(X)]^2$
Ya sabemos que $E(X)=0$, así que necesitamos calcular $E(X^2)$:
$E(X^2) = \int_{-\infty}^{\infty} x^2 f(x) dx = k \cdot \int_{-7}^{7} x^2(49-x^2) dx$
Desarrollamos la integral: 
$E(X^2) = k \cdot \frac{67228}{15}$
Por lo tanto:
$Var(X) = E(X^2) - (E[X])^2 = \frac{3}{1372} \cdot \frac{67228}{15} = \frac{49}{5} = 9.8$

**Resumen**
- $k = \frac{3}{1372} \approx 0.002186588921282799$
- $E(X) = 0$
- $Var(X) = \frac{49}{5} = 9.8$ 

---

**4.-** En la construcción de un Data Center se necesitan miles de minicomponentes. Para el proveedor A, se está diseñando un plan de control de calidad de forma que tomando un lote de n unidades, se rechace si se observa alguna minicomponente defectuosa. Determina n para que, si el lote tiene un 8 por mil (o más) de unidades defectuosas, la probabilidad de aceptarlo sea menor del 1%. El proveedor B, sirve lotes de 17 minicomponentes y sabemos que son defectuosos un 6 por mil de los minicomponentes. Si en este caso seguimos la regla de rechazar el lote si salen más de 3 minicomponentes defectuosos, y hoy nos ha enviado 17 lotes ¿Cuál es la probabilidad de rechazar hoy 1 lotes? Mañana llegarán 159 lotes, ¿Cuál será la probabilidad de rechazar 2 lotes como máximo? 

**Solución** 

**a) Diseño control de calidad**
Sea $p = 0.008$ la probabilidad de que una minicomponente sea defectuosa (8 por mil). La probabilidad de que una minicomponente no sea defectuosa es $1-p = 0.992$. 
Para una muestra de tamaño n, la probabilidad de aceptar el lote, es decir, la probabilidad de que ninguna de las n unidades seleccionadas sea defectuosa, está dada por:
P(aceptar el lote) = $(1-p)^n = 0.992^n$
Queremos que esta probabilidad sea menor que el 0.01, es decir: 
$0.992^n < 0.01$ 
Tomamos logaritmos en ambos lados de la desigualdad:
$n \cdot ln(0.992) < ln(0.01)$
Sabemos que $ln(0.992)$ es negativo, por lo tanto despejamos n:
$n > \frac{ln(0.01)}{ln(0.992)} \rightarrow n > 573.3406056990289$
Por lo tanto, el primer entero mayor viene dado por $n = 574$.

**b) Probabilidad de rechazar los 17 lotes que nos ha enviado hoy**
Si consideramos $X$ = N. de minicomponentes en un lote del proveedor B, claramente
$X \sim B(17, 0.006)$
Por tanto, la probabilidad de que un lote sea rechazado es:
$P(X > 3) = 1 - P(X \le 3) = 3.707746519254762e-6$
Solo quedaría ahora considerar la variable aleatoria $Y$ = N. de lotes rechazados hoy del proveedor B, que también cumple que $Y \sim B(17, 3.707746519254762e-6)$ y calcular
$P(Y = 1) \approx 6.302795164279538e-5$

**c) Probabilidad de rechazar como mucho 2 lotes de los 159 que nos envía mañana.** 
En esta ocasión tenemos que la variable $Y_2$ = N. de lotes rechazados mañana del proveedor B es: $Y_2 \sim B(159, 3.707746519254762e-6)$ y debemos calcular:
$P(Y_2 \le 2) = 0.999999999665078$

---

**5.-** Sabiendo que el número de averías en un día en el servidor A sigue una distribución Poisson $X \sim Poi(8)$ y análogamente en el servidor B, $Y \sim Poi(4)$ y que son independientes, calcula: a) la probabilidad de que A tenga 5 averías en un día sabiendo que entre ambos han tenido 7. b) Que A no tenga averías en una semana c) Que B tenga menos de 10 averías en una semana. 

**Solución** 

a) Aplicando el teorema de Bayes, tenemos que: 
$P(X=5 | X+Y=7) = \frac{P(X=5 \cap X+Y=7)}{P(X+Y=7)} = \frac{P(X=5) \cdot P(Y=2)}{P(X+Y=7)}$
La suma de dos variables Poisson independientes sigue otra distribución Poisson, con parámetro igual a la suma de los parámetros:
$X+Y \sim Poi(8+4) = Poi(12)$
$P(X=5) = \frac{e^{-8} \cdot 8^5}{5!}$, $P(Y=2) = \frac{e^{-4} \cdot 4^2}{2!}$, $P(X+Y=7) = \frac{e^{-12} \cdot 12^7}{7!}$
Sustituyendo en la fórmula de Bayes, tendremos que:
$P(X=5|X+Y=7) = \frac{(\frac{e^{-8} \cdot 8^5}{5!}) \cdot (\frac{e^{-4} \cdot 4^2}{2!})}{\frac{e^{-12} \cdot 12^7}{7!}} = \frac{\frac{8^5 \cdot 4^2}{5! \cdot 2!}}{\frac{12^7}{7!}}$
...simplificando:
$\frac{8^5 \cdot 4^2 \cdot 7!}{5! \cdot 2! \cdot 12^7} \approx 0.2102$

b) Si consideramos $X_7$ como el número de averías en una semana, sabemos que $X_7 \sim Poi(56)$. Y se nos pregunta por: 
$P(X_7 = 0) = \frac{56^0}{0!} \cdot e^{-56} = e^{-56} \approx 4.780892883885469e-25 \approx 0$ 

c) Si consideramos $Y_7$ el número de averías en una semana, sabemos que $Y_7 \sim Poi(28)$. La probabilidad es $P(Y_7 \le 9) = \sum_{i=0}^{9} \frac{28^i}{i!} \cdot e^{-28}$. Recuerda que para valores de n suficientemente grandes, podríamos aproximar una variable Poisson por una normal: $Poi(\lambda) \approx N(\lambda, \sqrt{\lambda})$ Por tanto, podríamos también afirmar que:
$P(Y_7 \le 9) \approx P(\frac{Y_7 - 28}{\sqrt{28}} \le \frac{9-28}{\sqrt{28}}) = P(Z \le -3.5906) \approx 0.0001653389807201311$

*2 Puntos por ejercicio.*

---
### Examen 29/10/2024 B 

**1.** Una potente empresa tiene en el mercado 3 redes sociales, TicTac, InstaKilo y TúyYo. En el Consejo de Administración de cada una, se ha planteado un debate ético sobre la conveniencia de adoptar medidas beligerantes en la lucha contra el cambio climático frente a la posición negacionista. En TicTac, la votación ha sido: 8 Beligerantes y 9 Negacionistas. En InstaKilo, 15 Beligerante y 16 Negacionistas y en TúyYo empate a 6. Por tanto la empresa, escuchadas las posiciones de las tres redes (2 negacionistas y 1 empate) optaría por la posición negacionista. Si embargo, en una maniobra de última hora, se decide repetir la votación después de transferir por sorteo un miembro del consejo de administración de TicTac a InstaKilo y posteriormente una persona de InstaKilo a TúyYo (también por sorteo). ¿Cuál es la probabilidad de que TúyYo tenga mayoría beligerante? ¿Cuál es la probabilidad de que si descubrimos al azar un miembro de Tú y Yo, éste sea de posición beligerante? Por otro lado, si sabemos que finalmente ha salido mayoría beligerante en TúyYo, cuál es la probabilidad respectiva en cada caso de que TicTac sea beligerante, negacionista o neutral? 

**Solución** 

**Traslados de miembros y Primera cuestión** Se realizarán dos traslados:
1. Un miembro de TicTac se traslada a InstaKilo. Las probabilidades son: 
   P(Beligerante transferido) = $\frac{8}{17}$, P(Negacionista transferido) = $\frac{9}{17}$

2. Un miembro de InstaKilo se traslada a TúyYo. Las probabilidades dependerán del primer traslado: 
   - Si se transfiere un beligerante de TicTac:
     P(Beligerante transferido a TúyYo) = $\frac{16}{32}$, P(Negacionista transferido a TúyYo) = $1 - \frac{16}{32}$
   - Si se transfiere un negacionista de TicTac:
     P(Beligerante transferido a TúyYo) = $\frac{15}{32}$, P(Negacionista transferido a TúyYo) = $1 - \frac{15}{32}$

Por tanto, la probabilidad de que tengamos mayoría beligerante en el tercer consejo es:
$\frac{8}{17} \cdot \frac{16}{32} + \frac{9}{17} \cdot \frac{15}{32} = \frac{263}{544} \approx 0.4834558823529412$

**Segunda cuestión** La probabilidad es similar a la anterior, solo que podría haber salido mayoría negacionista en lugar de beligerante. P(Mayoría negacionista en TúyYo) = $1 - 263/544$ Por tanto la probabilidad de elegir un miembro de Tuy Yo y que sea beligerante es:
P (Mayoría negacionista en Yúy Yo) y P (Salga miembro beligerante) ó 
P (Mayoría negacionista en Yúy Yo) y P (Salga miembro beligerante)
$P = \frac{3527}{7072} \approx 0.4987273755656109$ 

**Tercera cuestión**
Aplicando el teorema de bayes tenemos: 
La probabilidad de que TicTac se haya quedado neutral es que la primera transferencia haya sido de un negacionista:
$\frac{\frac{9}{17} \cdot \frac{15}{32}}{\frac{8}{17} \cdot \frac{16}{32} + \frac{9}{17} \cdot \frac{15}{32}} = \frac{135}{263} \approx 0.5133079847908745$

La probabilidad de que TicTac siga negacionista es que la primera transferencia haya sido de un beligerante:
$\frac{\frac{8}{17} \cdot \frac{16}{32}}{\frac{8}{17} \cdot \frac{16}{32} + \frac{9}{17} \cdot \frac{15}{32}} = \frac{128}{263} \approx 0.4866920152091255$

Observa que la probabilidad de que pase a ser Beligerante es cero, ya que no hay posibilidad con un solo traslado de cambiar la mayoría.

---

**2.** El peso que se asigna a la entrada de tipo A de una determinada red neuronal sigue una distribución normal $N(40.3, 1.5)$ En las entradas de tipo B, una $N(47.5, 1.3)$ Calcula: 
a) Probabilidad de que la suma de los pesos de 16 entradas de tipo A no supere el umbral de 647.8. 
b) ¿Cuál es el peso acumulado de las entradas de una red neuronal con 12 entradas de tipo A y 5 entradas de tipo B que está por debajo del percentil 59? 
c) Si tenemos dos redes neuronales de las anteriores, Red1 y Red2, ¿Cuál es la probabilidad de que el peso acumulado de las entradas en la primera sea, al menos, una unidad mayor que el de la segunda? Y, ¿la probabilidad de que tengan el mismo peso acumulado? 

**Solución**

a) Si consideramos la v.a. $X$ = Peso acumulado en 16 entradas de tipo A, tenemos que: 
$X \sim N(644.8, 6.0)$
Por tanto, $P(X < 647.8) \approx 0.9873263406612658$

b) Si consideramos la v.a. $Y$ = peso acumulado en la red neuronal especificada tendríamos que $Y \sim N(721.1, 5.953990258641679))$. Por tanto nos están preguntando por el valor y tal que $P(Y < y) = \frac{59}{100}$, por lo que tendríamos $y = 472.0386744280353$ 

c) Si consideramos dos v.a. de las planteadas en el primer apartado, $X_1$, $X_2$, nos estarían preguntando por: 
$P(X_1 \ge X_2 + 1) = P(X_1 - X_2 \ge 1)$
Como $X_1 - X_2 \sim N(0, \sqrt{2} \cdot 5.953990258641679)$ tendríamos que:
$P(X_1 - X_2 \ge 1) \approx 0.3233507736521497$
Respecto a la probabilidad de que el peso acumulado sea el mismo, habría que tener en cuenta que $X_1 - X_2$ es una v.a. continua, por lo que dicha probabilidad es NULA. 

---
**3.** Dada la f.d.p de la v.a. X 
$f(x) = \begin{cases} k(9-x^2) & si \quad |x| \le 3 \\ 0 & si \quad |x| > 3 \end{cases}$ 
Determina el valor de k, calcula $E[X]$ y $Var[X]$

**Solución**

**1. Calcular k**
Sabemos que la integral total de la función de densidad debe ser igual a 1:
$\int_{-3}^{3} k(9-x^2) dx = 1$
Resolvemos la integral y planteamos que:
$k \int_{-3}^{3} (9-x^2) dx = 1$
Por lo tanto, como:
$\int_{-3}^{3} (9-x^2) dx = 36$
Sustituyendo en la ecuación para k:
$k \cdot 36 = 1 \Rightarrow k = \frac{1}{36}$

**2. Calcular E(X)**
La esperanza matemática $E(X)$ está dada por:
$E(X) = \int_{-\infty}^{\infty} xf(x) dx = k \cdot \int_{-3}^{3} x(9-x^2) dx = 0$

**3. Calcular Var(X)**
La varianza está dada por:
$Var(X) = E(X^2) - [E(X)]^2$
Ya sabemos que $E(X)=0$, así que necesitamos calcular $E(X^2)$:
$E(X^2) = \int_{-\infty}^{\infty} x^2 f(x) dx = k \cdot \int_{-3}^{3} x^2(9-x^2) dx$ 
Desarrollamos la integral:
$E(X^2) = k \cdot \frac{324}{5}$
Por lo tanto:
$Var(X) = E(X^2) - (E[X])^2 = \frac{1}{36} \cdot \frac{324}{5} = \frac{9}{5} = 1.8$

**Resumen**
- $k = \frac{1}{36} \approx 0.027777777777777777778$
- $E(X) = 0$
- $Var(X) = \frac{9}{5} = 1.8$ 

---
**4.** En la construcción de un Data Center se necesitan miles de minicomponentes. Para el proveedor A, se está diseñando un plan de control de calidad de forma que tomando un lote de n unidades, se rechace si se observa alguna minicomponente defectuosa. Determina n para que, si el lote tiene un 8 por mil (o más) de unidades defectuosas, la probabilidad de aceptarlo sea menor del 4%. El proveedor B, sirve lotes de 12 minicomponentes y sabemos que son defectuosos un 5 por mil de los minicomponentes. Si en este caso seguimos la regla de rechazar el lote si salen más de 3 minicomponentes defectuosos, y hoy nos ha enviado 12 lotes ¿Cuál es la probabilidad de rechazar hoy 1 lotes? Mañana llegarán 136 lotes, ¿Cuál será la probabilidad de rechazar 4 lotes como máximo? 

**Solución** 

**a) Diseño control de calidad**
Sea $p = 0.008$ la probabilidad de que una minicomponente sea defectuosa (8 por mil). La probabilidad de que una minicomponente no sea defectuosa es $1-p = 0.992$. 
Para una muestra de tamaño n, la probabilidad de aceptar el lote, es decir, la probabilidad de que ninguna de las n unidades seleccionadas sea defectuosa, está dada por: 
P(aceptar el lote) = $(1-p)^n = 0.992^n$ 
Queremos que esta probabilidad sea menor que el 0.04, es decir:
$0.992^n < 0.04$
Tomamos logaritmos en ambos lados de la desigualdad:
$n \cdot ln(0.992) < ln(0.04)$
Sabemos que $ln(0.992)$ es negativo, por lo tanto despejamos n:
$n > \frac{ln(0.04)}{ln(0.992)} \rightarrow n > 400.7478856514658$
Por lo tanto, el primer entero mayor viene dado por $n = 401$.

**b) Probabilidad de rechazar los 12 lotes que nos ha enviado hoy**
Si consideramos $X$ = N. de minicomponentes en un lote del proveedor B, claramente
$X \sim B(12, 0.005)$
Por tanto, la probabilidad de que un lote sea rechazado es:
$P(X > 3) = 1 - P(X \le 3) = 2.281311667018393e-6$
Solo quedaría ahora considerar la variable aleatoria $Y$ = N. de lotes rechazados hoy del proveedor B, que también cumple que $Y \sim B(12, 2.281311667018393e-6)$ y calcular 
$P(Y = 1) \approx 2.737505303351101e-5$

**c) Probabilidad de rechazar como mucho 4 lotes de los 136 que nos envía mañana.**
En esta ocasión tenemos que la variable $Y_2$ = N. de lotes rechazados mañana del proveedor B es: $Y_2 \sim B(136, 2.281311667018393e-6)$ y debemos calcular: 
$P(Y_2 \le 4) = 1.0$ 

---
**5.** Sabiendo que el número de averías en un día en el servidor A sigue una distribución Poisson $X \sim Poi(6)$ y análogamente en el servidor B, $Y \sim Poi(3)$ y que son independientes, calcula: a) la probabilidad de que A tenga 6 averías en un día sabiendo que entre ambos han tenido 11. b) Que A no tenga averías en una semana c) Que B tenga menos de 11 averías en una semana.

**Solución** 

a) La probabilidad solicitada es: $P = 9856/59049$ b) Si consideramos $X_7$ como el número de averías en una semana, sabemos que $X_7 \sim Poi(42)$. Y se nos pregunta por: 
$P(X_7 = 0) = \frac{42^0}{0!} \cdot e^{-42} = e^{-42} \approx 5.74952226429356e-19$ 

c) La probabilidad es $P(Y_7 < 10) = Q(11, 21)$

*2 Puntos por ejercicio.*

---
### Examen 29/10/2024 C 

**1.** Una potente empresa tiene en el mercado 3 redes sociales, TicTac, InstaKilo y TúyYo. En el Consejo de Administración de cada una, se ha planteado un debate ético sobre la conveniencia de adoptar medidas beligerantes en la lucha contra el cambio climático frente a la posición negacionista. En TicTac, la votación ha sido: 14 Beligerantes y 15 Negacionistas. En InstaKilo, 8 Beligerante y 9 Negacionistas y en TúyYo empate a 13. Por tanto la empresa, escuchadas las posiciones de las tres redes (2 negacionistas y 1 empate) optaría por la posición negacionista. Si embargo, en una maniobra de última hora, se decide repetir la votación después de transferir por sorteo un miembro del consejo de administración de TicTac a InstaKilo y posteriormente una persona de InstaKilo a Túy Yo (también por sorteo). ¿Cuál es la probabilidad de que Túy Yo tenga mayoría beligerante? ¿Cuál es la probabilidad de que si descubrimos al azar un miembro de Tú y Yo, éste sea de posición beligerante? Por otro lado, si sabemos que finalmente ha salido mayoría beligerante en Túy Yo, cuál es la probabilidad respectiva en cada caso de que Tic Tac sea beligerante, negacionista o neutral? 

**Solución** 

**Traslados de miembros y Primera cuestión** Se realizarán dos traslados:
1. Un miembro de TicTac se traslada a InstaKilo. Las probabilidades son: 
   P(Beligerante transferido) = $\frac{14}{29}$
   P(Negacionista transferido) = $\frac{15}{29}$

2. Un miembro de InstaKilo se traslada a TúyYo. Las probabilidades dependerán del primer traslado: 
   - Si se transfiere un beligerante de TicTac:
     P(Beligerante transferido a TúyYo) = $\frac{9}{18}$ P(Negacionista transferido a TúyYo) = $1-\frac{9}{18}$
   - Si se transfiere un negacionista de TicTac:
     P(Beligerante transferido a TúyYo) = $\frac{8}{18}$ P(Negacionista transferido a TúyYo) = $1 - \frac{8}{18}$

Por tanto, la probabilidad de que tengamos mayoría beligerante en el tercer consejo es:
$\frac{14}{29} \cdot \frac{9}{18} + \frac{15}{29} \cdot \frac{8}{18} = \frac{41}{87} \approx 0.4712643678160919$

**Segunda cuestión** La probabilidad es similar a la anterior, solo que podría haber salido mayoría negacionista en lugar de beligerante. P(Mayoría negacionista en TúyYo) = $1-41/87$ Por tanto la probabilidad de elegir un miembro de Tuy Yo y que sea beligerante es: 
P (Mayoría negacionista en Yúy Yo) y P (Salga miembro beligerante) ó
P (Mayoría negacionista en Yúy Yo) y P (Salga miembro beligerante)
$P = \frac{1172}{2349} \approx 0.4989357173265219$

**Tercera cuestión**
Aplicando el teorema de bayes tenemos: 
La probabilidad de que TicTac se haya quedado neutral es que la primera transferencia haya sido de un negacionista:
$\frac{\frac{15}{29}\cdot\frac{8}{18}}{\frac{14}{29}\cdot\frac{9}{18}+\frac{15}{29}\cdot\frac{8}{18}} = \frac{20}{41} \approx 0.487804878048780487805$

La probabilidad de que TicTac siga negacionista es que la primera transferencia haya sido de un beligerante:
$\frac{\frac{14}{29}\cdot\frac{9}{18}}{\frac{14}{29}\cdot\frac{9}{18}+\frac{15}{29}\cdot\frac{8}{18}} = \frac{21}{41} \approx 0.51219512195$

Observa que la probabilidad de que pase a ser Beligerante es cero, ya que no hay posibilidad con un solo traslado de cambiar la mayoría.

---
**2.** El peso que se asigna a la entrada de tipo A de una determinada red neuronal sigue una distribución normal $N(46.0, 0.6)$ En las entradas de tipo B, una $N(62.8, 0.7)$. Calcula: 
a) Probabilidad de que la suma de los pesos de 17 entradas de tipo A no supere el umbral de 778.0. 
b) ¿Cuál es el peso acumulado de las entradas de una red neuronal con 15 entradas de tipo A y 13 entradas de tipo B que está por debajo del percentil 62? 
c) Si tenemos dos redes neuronales de las anteriores, Red1 y Red2, ¿Cuál es la probabilidad de que el peso acumulado de las entradas en la primera sea, al menos, una unidad mayor que el de la segunda? Y, ¿la probabilidad de que tengan el mismo peso acumulado? 

**Solución**

a) Si consideramos la v.a. $X$ = Peso acumulado en 17 entradas de tipo A, tenemos que: 
$X \sim N(782.0, 0.6\sqrt{17})$
Por tanto, $P(X < 778.0) \approx 0.9873263406612658$

b) Si consideramos la v.a. $Y$ = peso acumulado en la red neuronal especificada tendríamos que YN(1506.4, 3.430743359681689)). Por tanto nos están preguntando por el valor y tal que $P(Y < y) = \frac{31}{50}$, por lo que tendríamos $y = 472.0386744280353$ 

c) Si consideramos dos v.a. de las planteadas en el primer apartado, $X_1$, $X_2$, nos estarían preguntando por: 
$P(X_1 \ge X_2 + 1) = P(X_1 - X_2 \ge 1)$
Como $X_1 - X_2 \sim N(0, \sqrt{2} \cdot 3.430743359681689)$ tendríamos que:
$P(X_1 - X_2 \ge 1) \approx 0.3233507736521497$
Respecto a la probabilidad de que el peso acumulado sea el mismo, habría que tener en cuenta que $X_1 - X_2$ es una v.a. continua, por lo que dicha probabilidad es NULA. 

---
**3.** Dada la f.d.p de la v.a. X 
$f(x) = \begin{cases} k(36-x^2) & si \quad |x| \le 6 \\ 0 & si \quad |x| > 6 \end{cases}$ 
Determina el valor de k, calcula $E[X]$ y $Var[X]$

**Solución**

**1. Calcular k**
Sabemos que la integral total de la función de densidad debe ser igual a 1:
$\int_{-6}^{6} k(36-x^2) dx = 1$
Resolvemos la integral y planteamos que:
$k \int_{-6}^{6} (36-x^2) dx = 1$
Por lo tanto, como:
$\int_{-6}^{6} (36-x^2) dx = 288$
Sustituyendo en la ecuación para k:
$k \cdot 288 = 1 \Rightarrow k = \frac{1}{288}$

**2. Calcular E(X)**
La esperanza matemática $E(X)$ está dada por:
$E(X) = \int_{-\infty}^{\infty} xf(x) dx = k \cdot \int_{-6}^{6} x(36-x^2) dx = 0$

**3. Calcular Var(X)**
La varianza está dada por:
$Var(X) = E(X^2) - [E(X)]^2$
Ya sabemos que $E(X)=0$, así que necesitamos calcular $E(X^2)$:
$E(X^2) = \int_{-\infty}^{\infty} x^2f(x) dx = k \cdot \int_{-6}^{6} x^2(36-x^2) dx$ 
Desarrollamos la integral:
$E(X^2) = k \cdot \frac{10368}{5}$
Por lo tanto:
$Var(X) = E(X^2) - (E[X])^2 = \frac{1}{288} \cdot \frac{10368}{5} = \frac{36}{5} = 7.2$

**Resumen**
- $k = \frac{1}{288} \approx 0.0034722222222222222222$
- $E(X) = 0$
- $Var(X) = \frac{36}{5} = 7.2$ 

---
**4.** En la construcción de un Data Center se necesitan miles de minicomponentes. Para el proveedor A, se está diseñando un plan de control de calidad de forma que tomando un lote de n unidades, se rechace si se observa alguna minicomponente defectuosa. Determina n para que, si el lote tiene un 3 por mil (o más) de unidades defectuosas, la probabilidad de aceptarlo sea menor del 2%. El proveedor B, sirve lotes de 14 minicomponentes y sabemos que son defectuosos un 2 por mil de los minicomponentes. Si en este caso seguimos la regla de rechazar el lote si salen más de 2 minicomponentes defectuosos, y hoy nos ha enviado 14 lotes ¿Cuál es la probabilidad de rechazar hoy 1 lotes? Mañana llegarán 200 lotes, ¿Cuál será la probabilidad de rechazar 5 lotes como máximo? 

**Solución** 

**a) Diseño control de calidad**
Sea $p = 0.003$ la probabilidad de que una minicomponente sea defectuosa (3 por mil). La probabilidad de que una minicomponente no sea defectuosa es $1-p = 0.997$. 
Para una muestra de tamaño n, la probabilidad de aceptar el lote, es decir, la probabilidad de que ninguna de las n unidades seleccionadas sea defectuosa, está dada por: 
P(aceptar el lote) = $(1-p)^n = 0.997^n$ 
Queremos que esta probabilidad sea menor que el 0.02, es decir:
$0.997^n < 0.02$
Tomamos logaritmos en ambos lados de la desigualdad:
$n \cdot ln(0.997) < ln(0.02)$
Sabemos que $ln(0.997)$ es negativo, por lo tanto despejamos n:
$n > \frac{ln(0.02)}{ln(0.997)} \rightarrow n > 1302.05067749778$
Por lo tanto, el primer entero mayor viene dado por $n = 1303$.

**b) Probabilidad de rechazar los 14 lotes que nos ha enviado hoy**
Si consideramos $X$ = N. de minicomponentes en un lote del proveedor B, claramente
$X \sim B(14, 0.002)$
Por tanto, la probabilidad de que un lote sea rechazado es:
$P(X > 2) = 1 - P(X \le 2) = 7.568167307847595e-6$
Solo quedaría ahora considerar la variable aleatoria $Y$ = N. de lotes rechazados hoy del proveedor B, que también cumple que $Y \sim B(14, 7.568167307847595e-6)$ y calcular 
$P(Y=1) \approx 1.05943918340752e-4$

**c) Probabilidad de rechazar como mucho 5 lotes de los 200 que nos envía mañana.**
En esta ocasión tenemos que la variable $Y_2$ = N. de lotes rechazados mañana del proveedor B es: $Y_2 \sim B(200, 7.568167307847595e-6)$ y debemos calcular: 
$P(Y_2 \le 5) = 1.0$ 

---
**5.** Sabiendo que el número de averías en un día en el servidor A sigue una distribución Poisson $X \sim Poi(8)$ y análogamente en el servidor B, $Y \sim Poi(4)$ y que son independientes, calcula: a) la probabilidad de que A tenga 3 averías en un día sabiendo que entre ambos han tenido 4. b) Que A no tenga averías en una semana c) Que B tenga menos de 12 averías en una semana.

**Solución** 

a) La probabilidad solicitada es: $P = 32/81$ b) Si consideramos $X_7$ como el número de averías en una semana, sabemos que $X_7 \sim Poi(56)$. Y se nos pregunta por: 
$P(X_7 = 0) = \frac{56^0}{0!} \cdot e^{-56} = e^{-56} \approx 4.780892883885469e-25$ 
c) La probabilidad es $P(Y_7 < 11) = Q(12, 28)$

*2 Puntos por ejercicio.*

---
### Examen 29/10/2024 D 

**1.** Una potente empresa tiene en el mercado 3 redes sociales, TicTac, InstaKilo y TúyYo. En el Consejo de Administración de cada una, se ha planteado un debate ético sobre la conveniencia de adoptar medidas beligerantes en la lucha contra el cambio climático frente a la posición negacionista. En TicTac, la votación ha sido: 9 Beligerantes y 10 Negacionistas. En InstaKilo, 14 Beligerante y 15 Negacionistas y en TúyYo empate a 13. Por tanto la empresa, escuchadas las posiciones de las tres redes (2 negacionistas y 1 empate) optaría por la posición negacionista. Si embargo, en una maniobra de última hora, se decide repetir la votación después de transferir por sorteo un miembro del consejo de administración de TicTac a InstaKilo y posteriormente una persona de InstaKilo a Túy Yo (también por sorteo). ¿Cuál es la probabilidad de que Túy Yo tenga mayoría beligerante? ¿Cuál es la probabilidad de que si descubrimos al azar un miembro de Tú y Yo, éste sea de posición beligerante? Por otro lado, si sabemos que finalmente ha salido mayoría beligerante en Túy Yo, cuál es la probabilidad respectiva en cada caso de que Tic Tac sea beligerante, negacionista o neutral? 

**Solución** 

**Traslados de miembros y Primera cuestión** Se realizarán dos traslados:
1. Un miembro de TicTac se traslada a InstaKilo. Las probabilidades son: 
   P(Beligerante transferido) = $\frac{9}{19}$ P(Negacionista transferido) = $\frac{10}{19}$
2. Un miembro de InstaKilo se traslada a TúyYo. Las probabilidades dependerán del primer traslado: 
   - Si se transfiere un beligerante de TicTac:
     P(Beligerante transferido a TúyYo) = $\frac{15}{30}$, P(Negacionista transferido a TúyYo) = $1-\frac{15}{30}$
   - Si se transfiere un negacionista de TicTac:
     P(Beligerante transferido a TúyYo) = $\frac{14}{30}$, P(Negacionista transferido a TúyYo) = $1 - \frac{14}{30}$

Por tanto, la probabilidad de que tengamos mayoría beligerante en el tercer consejo es:
$\frac{9}{19} \cdot \frac{15}{30} + \frac{10}{19} \cdot \frac{14}{30} = \frac{55}{114} \approx 0.4824561403508772$

**Segunda cuestión** La probabilidad es similar a la anterior, solo que podría haber salido mayoría negacionista en lugar de beligerante. P(Mayoría negacionista en TúyYo) = $1-55/114$ Por tanto la probabilidad de elegir un miembro de Tuy Yo y que sea beligerante es: 
P (Mayoría negacionista en Yúy Yo) y P (Salga miembro beligerante) ó
P (Mayoría negacionista en Yúy Yo) y P (Salga miembro beligerante)
$P = \frac{1537}{3078} \approx 0.4993502274204029$ 

**Tercera cuestión**
Aplicando el teorema de bayes tenemos: 
La probabilidad de que TicTac se haya quedado neutral es que la primera transferencia haya sido de un negacionista:
$\frac{\frac{10}{19} \cdot \frac{14}{30}}{\frac{9}{19} \cdot \frac{15}{30} + \frac{10}{19} \cdot \frac{14}{30}} = \frac{28}{55} \approx 0.50909090909$

La probabilidad de que TicTac siga negacionista es que la primera transferencia haya sido de un beligerante:
$\frac{\frac{9}{19} \cdot \frac{15}{30}}{\frac{9}{19} \cdot \frac{15}{30} + \frac{10}{19} \cdot \frac{14}{30}} = \frac{27}{55} \approx 0.490909090909$

Observa que la probabilidad de que pase a ser Beligerante es cero, ya que no hay posibilidad con un solo traslado de cambiar la mayoría.

---
**2.** El peso que se asigna a la entrada de tipo A de una determinada red neuronal sigue una distribución normal $N(45.2, 1.3)$ En las entradas de tipo B, una $N(61.4, 1.1)$. Calcula: 
a) Probabilidad de que la suma de los pesos de 15 entradas de tipo A no supere el umbral de 697.0. 
b) ¿Cuál es el peso acumulado de las entradas de una red neuronal con 15 entradas de tipo A y 7 entradas de tipo B que está por debajo del percentil 45? 
c) Si tenemos dos redes neuronales de las anteriores, Red1 y Red2, ¿Cuál es la probabilidad de que el peso acumulado de las entradas en la primera sea, al menos, una unidad mayor que el de la segunda? Y, ¿la probabilidad de que tengan el mismo peso acumulado? 

**Solución**

a) Si consideramos la v.a. $X$ = Peso acumulado en 15 entradas de tipo A, tenemos que: 
$X \sim N(678.0, 1.3\sqrt{15})$
Por tanto, $P(X < 697.0) \approx 0.9873263406612658$

b) Si consideramos la v.a. $Y$ = peso acumulado en la red neuronal especificada tendríamos que YN(1107.8, 5.815496539419485)). Por tanto nos están preguntando por el valor y tal que $P(Y < y) = \frac{9}{20}$, por lo que tendríamos $y = 472.0386744280353$ 

c) Si consideramos dos v.a. de las planteadas en el primer apartado, $X_1$, $X_2$, nos estarían preguntando por: 
$P(X_1 \ge X_2 + 1) = P(X_1 - X_2 \ge 1)$
Como $X_1 - X_2 \sim N(0, \sqrt{2} \cdot 5.815496539419485)$ tendríamos que:
$P(X_1 - X_2 \ge 1) \approx 0.3233507736521497$
Respecto a la probabilidad de que el peso acumulado sea el mismo, habría que tener en cuenta que $X_1 - X_2$ es una v.a. continua, por lo que dicha probabilidad es NULA. 

---
**3.** Dada la f.d.p de la v.a. X 
$f(x) = \begin{cases} k(64-x^2) & si \quad |x| \le 8 \\ 0 & si \quad |x| > 8 \end{cases}$ 
Determina el valor de k, calcula $E[X]$ y $Var[X]$

**Solución**

**1. Calcular k**
Sabemos que la integral total de la función de densidad debe ser igual a 1:
$\int_{-8}^{8} k(64-x^2) dx = 1$
Resolvemos la integral y planteamos que:
$k \int_{-8}^{8} (64-x^2) dx = 1$
Por lo tanto, como:
$\int_{-8}^{8} (64-x^2) dx = \frac{2048}{3}$
Sustituyendo en la ecuación para k:
$k \cdot \frac{2048}{3} = 1 \Rightarrow k = \frac{3}{2048}$

**2. Calcular E(X)**
La esperanza matemática $E(X)$ está dada por:
$E(X) = \int_{-\infty}^{\infty} xf(x) dx = k \cdot \int_{-8}^{8} x(64-x^2) dx = 0$

**3. Calcular Var(X)**
La varianza está dada por:
$Var(X) = E(X^2) - [E(X)]^2$
Ya sabemos que $E(X)=0$, así que necesitamos calcular $E(X^2)$:
$E(X^2) = \int_{-\infty}^{\infty} x^2f(x) dx = k \cdot \int_{-8}^{8} x^2(64-x^2) dx$ 
Desarrollamos la integral:
$E(X^2) = k \cdot \frac{131072}{15}$
Por lo tanto:
$Var(X) = E(X^2) - (E[X])^2 = \frac{3}{2048} \cdot \frac{131072}{15} = \frac{64}{5} = 12.8$

**Resumen**
- $k = \frac{3}{2048} \approx 0.00146484375$
- $E(X) = 0$
- $Var(X) = \frac{64}{5} = 12.8$ 

---
**4.** En la construcción de un Data Center se necesitan miles de minicomponentes. Para el proveedor A, se está diseñando un plan de control de calidad de forma que tomando un lote de n unidades, se rechace si se observa alguna minicomponente defectuosa. Determina n para que, si el lote tiene un 9 por mil (o más) de unidades defectuosas, la probabilidad de aceptarlo sea menor del 3%. El proveedor B, sirve lotes de 10 minicomponentes y sabemos que son defectuosos un 5 por mil de los minicomponentes. Si en este caso seguimos la regla de rechazar el lote si salen más de 3 minicomponentes defectuosos, y hoy nos ha enviado 10 lotes ¿Cuál es la probabilidad de rechazar hoy 2 lotes? Mañana llegarán 140 lotes, ¿Cuál será la probabilidad de rechazar 5 lotes como máximo? 

**Solución** 

**a) Diseño control de calidad**
Sea $p = 0.009$ la probabilidad de que una minicomponente sea defectuosa (9 por mil). La probabilidad de que una minicomponente no sea defectuosa es $1-p = 0.991$. 
Para una muestra de tamaño n, la probabilidad de aceptar el lote, es decir, la probabilidad de que ninguna de las n unidades seleccionadas sea defectuosa, está dada por: 
P(aceptar el lote) = $(1-p)^n = 0.991^n$ 
Queremos que esta probabilidad sea menor que el 0.03, es decir:
$0.991^n < 0.03$
Tomamos logaritmos en ambos lados de la desigualdad:
$n \cdot ln(0.991) < ln(0.03)$
Sabemos que $ln(0.991)$ es negativo, por lo tanto despejamos n:
$n > \frac{ln(0.03)}{ln(0.991)} \rightarrow n > 387.8616233770566$
Por lo tanto, el primer entero mayor viene dado por $n = 388$.

**b) Probabilidad de rechazar los 10 lotes que nos ha enviado hoy**
Si consideramos $X$ = N. de minicomponentes en un lote del proveedor B, claramente
$X \sim B(10, 0.005)$
Por tanto, la probabilidad de que un lote sea rechazado es:
$P(X > 3) = 1 - P(X \le 3) = 2.281311667018393e-6$
Solo quedaría ahora considerar la variable aleatoria $Y$ = N. de lotes rechazados hoy del proveedor B, que también cumple que $Y \sim B(10, 2.281311667018393e-6)$ y calcular 
$P(Y = 2) \approx 2.341929573124558e-10$

**c) Probabilidad de rechazar como mucho 5 lotes de los 140 que nos envía mañana.**
En esta ocasión tenemos que la variable $Y_2$ = N. de lotes rechazados mañana del proveedor B es: $Y_2 \sim B(140, 2.281311667018393e-6)$ y debemos calcular: 
$P(Y_2 \le 5) = 1.0$ 

---
**5.** Sabiendo que el número de averías en un día en el servidor A sigue una distribución Poisson $X \sim Poi(6)$ y análogamente en el servidor B, Y~ Poi(3) y que son independientes, calcula: a) la probabilidad de que A tenga 6 averías en un día sabiendo que entre ambos han tenido 8. b) Que A no tenga averías en una semana c) Que B tenga menos de 11 averías en una semana.

**Solución** 

a) La probabilidad solicitada es: $P=1792/6561$ b) Si consideramos $X_7$ como el número de averías en una semana, sabemos que $X_7 \sim Poi(42)$. Y se nos pregunta por: 
$P(X_7 = 0) = \frac{42^0}{0!} \cdot e^{-42} \approx 5.74952226429356e-19$ 
c) La probabilidad es $P(Y_7 < 10) = Q(11, 21)$

*2 Puntos por ejercicio.*