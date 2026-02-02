## Aprendizaje por Refuerzo 
### ¿Por qué RL?
Los agentes están, por definición, diseñados para **<span style="color:#2f6004">interactuar con un entorno</span>**. Necesitan tal interacción para llevar a cabo una tarea determinada. El nivel de éxito para esa tarea depende de <span style="color:#2f6004">**qué tan bien el agente aprenda** del entorno para realizar las acciones adecuadas</span>. 

Los agentes realizan el **<span style="color:#2f6004">bucle observar-reaccionar (observe-react loop)</span>**. En la {numref}`RLAgent` mostramos este bucle para el juego Breakout de Atari:

1) **Observación**. El problema (por ejemplo, jugar un juego en este caso) es codificado por el entorno (movimientos y reglas). El agente es capaz de observar el **<span style="color:#2f6004">estado del entorno</span>**. Idealmente, el estado del entorno debería contener toda la información relevante necesaria para que el agente tome decisiones. En el juego de Atari, el entorno viene dado por las configuraciones de píxeles de la pared superior y las de la bola a rebotar.  

2) **Acciones**. Dada una observación, el agente reacciona realizando una **<span style="color:#2f6004">acción</span>** legal (por ejemplo, mover la pala a la izquierda, a la derecha o no moverla, para rebotar la bola entrante correctamente). Dado que las acciones afectan al estado del entorno de una manera diferente, el agente debe seleccionar adecuadamente.  

3) **Recompensas**. ¿Cómo puede el agente beneficiarse de la experiencia de juegos anteriores? Bueno, el entorno no solo devuelve el estado, sino también la **<span style="color:#2f6004">recompensa por la acción tomada por el agente</span>**. Dicha retroalimentación es clave para aprender una estrategia determinada para ganar. En el juego de Atari, tal recompensa *(valor positivo, negativo o cero)* está relacionada con el número de ladrillos de la pared rotos por la bola.  

```{figure} ./images/Topic2/RLAgent.png
---
name: RLAgent
width: 800px
align: center
height: 400px
---
Agente de juego de Atari. Entorno y bucle observar-reaccionar. [Crédito](https://colab.research.google.com/github/tensorflow/agents/blob/master/docs/tutorials/0_intro_rl.ipynb). 
```

<span style="color:#2f6004">**Objetivo del agente**. Maximizar las recompensas acumuladas a lo largo del tiempo.</span> En otras palabras, el agente debe optimizar la función de recompensa (algo similar al agente-MC explicado en el tema anterior). Sin embargo, aquí tal maximización conduce a **aprender una política** (una guía para interactuar con el entorno).

<span style="color:#2f6004">**Política**. Mapea cada estado posible a las probabilidades de elegir diferentes acciones.</span> Esto ayuda no solo a guiar al agente a través del entorno, sino a maximizar la recompensa acumulada. 

Por lo tanto, **<span style="color:#2f6004">el agente es básicamente un algoritmo de aprendizaje</span>**. El Aprendizaje por Refuerzo es el paradigma que conduce a aprender políticas óptimas.  


### Procesos de Decisión de Markov
#### Motivación 
En "Matemática Discreta" estudiamos las Cadenas de Markov de forma abstracta. Básicamente vale la pena recordar un par de conceptos: 

1) **Transiciones de estado**. Las Cadenas de Markov están codificadas por **matrices de transición** que declaran la probabilidad $p(s'_{t+1}|s_t)$, es decir, la probabilidad de realizar una transición del estado $s$ al estado $s'$ en el tiempo $t$. Ambos estados pertenecen al "espacio de estados" ${\cal S}$.  

2) **Propiedad de Markov**. La probabilidad $p(s'_{t+1}|s_t)$ en el tiempo $t$ es "sin memoria" (memoryless), es decir, la probabilidad condicional olvida lo que sucedió antes de $t$: 

$$
p(s'_{t+1}|s_t) = p(s'_{t+1}|s_t,s_{t-1},\ldots,s_0)\;.
$$

Los Procesos de Decisión de Markov (MDPs) incorporan dos nuevos elementos a la maquinaria de Markov: 

1) **Acciones**. La definición $p(s'_{t+1}|s_t)$ es incompleta. La palabra "Decisión" en los MDPs significa que tal probabilidad puede ser diferente para cualquiera de las acciones disponibles/legales $a$ que pertenecen al "espacio de acciones" ${\cal A}$. En otras palabras, la definición correcta es 

$$
p(s'|s,a)\;\text{donde}\;\;s',s\in {\cal S}, a\in {\cal A}\;,
$$

donde omitimos los índices de tiempo por simplicidad. Como veremos pronto, $p(s'|s,a)$ implica que **cada acción tiene su propia matriz de transición**. 

2) **Recompensas**. Llegar al estado $s'$ a través de cualquier acción $a$ implica recibir una "recompensa" (numérica) $R(s,a)$ que puede ser positiva, negativa o cero. 

Para motivar los MDPs, utilizamos el **problema del perro de servicio**. Este es un ejemplo clásico. Aquí seguimos libremente el libro [The Art of Reinforcement Learning](https://link.springer.com/book/10.1007/978-1-4842-9606-6) (disponible en Springer a través de la biblioteca de la UA). 

En la {numref}`Service-dog`, ilustramos una configuración básica para el problema del perro de servicio. 

1) Nuestro objetivo es **entrenar a un perro** que se encuentra afuera para encontrar un objeto (que está en la habitación 3).

2) La topología de la configuración muestra que el perro solo puede acceder al edificio a través de la habitación 2 y luego ir a la habitación 1 o a la habitación 3 (donde está el objeto).

3) Una vez que se encuentra el objeto, el perro se queda en la habitación 3. 


```{figure} ./images/Topic2/Service-dog.png
---
name: Service-dog
width: 800px
align: center
height: 500px
---
Configuración del perro de servicio. [Crédito](https://link.springer.com/book/10.1007/978-1-4842-9606-6). 
```
Los estados son: 

$$
{\cal S}=\{\underbrace{\text{Afuera (Outside)}}_{s_0},\underbrace{\text{Habitación 1 (Room1)}}_{s_1},\underbrace{\text{Habitación 2 (Room2)}}_{s_2}, \underbrace{\text{Habitación 3 (Room3)}}_{s_3}, \underbrace{\text{Encontrado (Found)}}_{s_4}\}\;.
$$


En lugar de tener un "único" grafo que codifique las transiciones y sus probabilidades, tenemos un "grafo por acción". Consideramos las siguientes acciones: 

$$
{\cal A}=\{\underbrace{\text{IrHabitacion1 (GoRoom1)}}_{a_0},\underbrace{\text{IrHabitacion2 (GoRoom2)}}_{a_1}, \underbrace{\text{IrHabitacion3 (GoRoom3)}}_{a_2}, \underbrace{\text{IrAfuera (GoOutside)}}_{a_3}, \underbrace{\text{IrAdentro (GoInside)}}_{a_4},\underbrace{\text{Buscar (Search)}}_{a_5}\}\;.
$$

En la {numref}`Trans`, mostramos las matrices de transición para las seis acciones. Por ejemplo: 



```{figure} ./images/Topic2/Trans.png
---
name: Trans
width: 800px
align: center
height: 500px
---
Matrices de transición para las acciones del perro de servicio. Creado por Gemini. 
```

- **IrHabitacion3 (GoRoom3)**. A esta habitación solo se puede acceder desde la habitación 2. Por lo tanto, **<span style="color:#2f6004">bajo esta acción</span>** hay una probabilidad de $0.9$ de permanecer en la habitación 2 y solo $0.1$ de ir hacia la habitación 1. Sin embargo, hay una probabilidad de $0.1$ de permanecer en la habitación 2 y $0.9$ de ir a la habitación 3. Esto muestra la "intencionalidad" del agente para acercarse al objetivo. Además, cuando se aplica a cualquier otro estado, el agente permanece en ese estado con probabilidad $1.0$. 

- **IrHabitacion2 (GoRoom2)** sigue una lógica similar. Abre la posibilidad de ir a la habitación 1 o a la habitación 3, pero está sesgado hacia la habitación 3. 

- **IrHabitacion1 (GoRoom1)** está obviamente sesgado hacia el regreso a la habitación 2, ya que esto es clave para acceder a la habitación 3. Sin embargo, cuando el agente está en la habitación 3 introducimos un gran sesgo para regresar a la habitación 2.

- **IrAfuera (GoOutside)**. Esto solo se puede hacer desde la habitación 2 y lo preferimos porque el perro puede jugar afuera. 

- **IrAdentro (GoInside)**. Incentivamos al perro para que vaya a la habitación 2 porque queremos enseñarle cómo alcanzar el objetivo. 

- **Buscar (Search)**. Esta acción es realmente simple: una vez que el perro está en la habitación 3, tiene una probabilidad de $0.9$ de encontrar el objeto, alcanzando así el objetivo. 

En la {numref}`superposed-graph`, combinamos todas las matrices de transición en un único grafo. Intenta aislar el grafo de una de las "acciones". 

```{figure} ./images/Topic2/superposed-graph.png
---
name: superposed-graph
width: 800px
align: center
height: 600px
---
Grafo superpuesto considerando todas las matrices de transición. Creado por Gemini. 
```

Como puede ver, **<span style="color:#2f6004">en el RL las acciones no se refieren (en general) a predicados atómicos sino a estrategias</span>** (o "comportamientos" en la jerga de los robots autónomos).


**Con respecto a las recompensas**. Si queremos incentivar al perro a buscar el objeto en lugar de jugar indefinidamente en el jardín, podemos utilizar las siguientes "recompensas estado-acción" individuales: 
```
  Room1:
    GoRoom1: {'Room1': -1.0}
    GoRoom2: {'Room2': -1.0}
    GoRoom3: {'Room3': -1.0}
    GoOutside: {'Outside': -1.0}
    GoInside: {'Room1': -1.0}
    Search: {'Room1': -2.0}
  Room2:
    GoRoom1: {'Room1': -1.0}
    GoRoom2: {'Room2': -1.0}
    GoRoom3: {'Room3': -1.0}
    GoOutside: {'Outside': -1.0}
    GoInside: {'Room1': -1.0}
    Search: {'Room2': -2.0}
  Room3:
    GoRoom1: {'Room1': -1.0}
    GoRoom2: {'Room2': -1.0}
    GoRoom3: {'Room3': -1.0}
    GoOutside: {'Outside': -1.0}
    GoInside: {'Room1': -1.0}
    Search: {'Found': 10.0}
  Outside:
    GoRoom1: {'Room1': -1.0}
    GoRoom2: {'Room2': -1.0}
    GoRoom3: {'Room3': -1.0}
    GoOutside: {'Outside': -1.0}
    GoInside: {'Room1': -1.0}
    Search: {'Outside': -2.0}
  Found:
    GoRoom1: {'Found': 0.0}
    GoRoom2: {'Found': 0.0}
    GoRoom3: {'Found': 0.0}
    GoOutside: {'Found': 0.0}
    GoInside: {'Found': 0.0}
    Search: {'Found': 0.0}
```

La **función de recompensa** ${\cal R}$ mapea pares de estados y acciones a valores numéricos $R(s,a)$. Dado que el agente tiende a realizar acciones que maximicen las recompensas, tenemos: 

- Para la $\text{Habitación 1}$ y la $\text{Habitación 2}$, el agente es incentivado a salir de la habitación y no a buscar (recompensas $-1$ y $-2$ respectivamente).
- Para la $\text{Habitación 3}$, hay una recompensa positiva alta por buscar ($+10$ unidades). 
- Para **Afuera**, el perro es incentivado a entrar y no a buscar. 
- Para **Encontrado (Found)** hay una incentivación neutra (recompensa $0$). Esto es típico de un estado final.

#### Retorno Futuro 
Supongamos que realizamos varios **episodios**. Un episodio es una secuencia de pares estado-acción **legales** (probabilidades de transición distintas de cero en las respectivas matrices de transición de acción). En la tabla siguiente, mostramos un par de episodios de $6$ movimientos cada uno: 

$
\begin{aligned}
&\begin{array}{cccc}
\text{Episodio}  & t & \text{Par} & R_t = R(s,a)\\
\hline
1 & 0 &(\text{Outside},\text{GoOutside}) & -1\\
  & 1 &(\text{Outside},\text{GoRoom2})   & -1\\ 
  & 2 &(\text{Room2},\text{GoRoom2})     & -1\\ 
  & 3 &(\text{Room2},\text{GoRoom3})     & -1\\
  & 4 &(\text{Room3},\text{Search})      & 10\\ 
  & 5 &(\text{Found},\text{GoRoom3})     & 0 \\
\hline
2 & 0 &(\text{Outside},\text{GoRoom2})   & -1\\
  & 1 &(\text{Room2},\text{GoRoom1})     & -1\\
  & 2 &(\text{Room1},\text{GoRoom1})     & -1\\
  & 3 &(\text{Room1},\text{GoRoom1})     & -1\\
  & 4 &(\text{Room1},\text{GoRoom2})     & -1\\
  & 5 &(\text{Room2},\text{Search})      & -2\\
\end{array}
\end{aligned}
$

El **retorno** $G_t$ para un episodio se define de la siguiente manera:

$$
G_t = R_t + \gamma R_{t+1} + \gamma^2 R_{t+2} + \gamma^3 R_{t+3} + \ldots  
$$

donde $\gamma \in (0,1)$ es un "factor de descuento" solo para evitar "retornos infinitos" (añadir indefinidamente recompensas negativas). En otras palabras, el peso de un retorno dado decae con el tiempo. 

Entonces, para el episodio 1 tenemos el siguiente retorno:

$$
G_0 = R_0 + \gamma R_1 + \ldots + \gamma^5 R_5
$$

Para $\gamma=0.9$, tenemos: 

$$
G_0 = -1 + -1\cdot 0.9 -1\cdot 0.9^2 - 1\cdot 0.9^3 + 10\cdot 0.9^4 + 0 = 3.122\;.
$$

De manera similar, para el episodio 2, tenemos 

$$
G_0 = -1 - 1\cdot 0.9 - 1\cdot 0.9^2 - 1\cdot 0.9^3 - 1\cdot 0.9^4 - 2\cdot 0.9^5 = -5.276\;.
$$

Este segundo episodio devuelve una recompensa menor ya que en el "horizonte" de $6$ pasos de tiempo, el agente (1) entra en un bucle en la habitación 1 y luego realiza una búsqueda en la habitación equivocada (habitación 2). 

#### Función de Valor 
Consideremos la siguiente propiedad de $G_t$: 

$$
\begin{align}
G_t &=R_t + \gamma R_{t+1} + \gamma^2 R_{t+2} + \gamma^3 R_{t+3} + \ldots\\
    &=R_t + \gamma\cdot(R_{t+1}+ \gamma R_{t+2}+ \gamma^2 R_{t+3} + \ldots)\\
    &=R_t + \gamma\cdot G_{t+1}\;.
\end{align}
$$

En otras palabras, los retornos futuros se calculan mediante el retorno inmediato en $t$ más el descuento del retorno futuro a partir de $t+1$ en adelante.

Aunque esta recursividad es intrigante, comparar retornos futuros para decidir qué estado es más valioso para maximizar el retorno total **depende del tiempo** (la evaluación depende del $t$ elegido). <span style="color:#2f6004">Necesitamos una medida que sea **dependiente del estado** en su lugar</span>. Esta es la **<span style="color:#2f6004">función de valor (value function)</span>**.

**Función de valor** Dado un estado $s$, su función de valor $V(s)$ <span style="color:#2f6004">da cuenta de la **recompensa esperada (expected reward)** a partir de él, definida de la siguiente manera</span>:

$$
\begin{align}
V(s) &= \mathbb{E}[G_t|s_t=s]\\
     &= \mathbb{E}[R_t + \gamma G_{t+1}|s_t=s]\\
     &= \mathbb{E}[R_t + \gamma V_{t+1}(s)|s_t=s]\;.\\
\end{align}
$$

o, más precisamente 

$$
V(s) = \sum_{a\in {\cal A}}[R(s,a)+ \gamma\sum_{s'\in {\cal S}}p(s'|s,a)V(s')]\;.\\
$$

Aquí, la "esperanza (expectation)" se basa en incorporar las probabilidades $p(s'|s,a)$ y la suma sobre todas las acciones. La ecuación anterior se conoce como la **Ecuación de Bellman**. Esto indica un vínculo estrecho con la Programación Dinámica (DP).  

Por supuesto, la Ecuación de Bellman es recursiva. Si es así, ¿cómo calculamos realmente $V(s)$? Como en la DP, lo vamos a hacer de forma **iterativa**: 

1) Supongamos que $V(s)=0$ para todo $s\in{\cal S}$ inicialmente. 

2) A continuación, en la siguiente iteración, tomemos la función de valor proporcionada por la acción más exitosa: 

$$
V(s) = \max_{a}\left[R(s,a) + \gamma\sum_{s'\in {\cal S}}p(s'|s,a)V(s')\right]
$$

3) Luego, para cada nuevo $V(s)$, obtengamos el incremento $\delta$ en valor absoluto y tomemos el máximo de todos estos valores absolutos. 

4) ¡Si tal máximo está por debajo de un $\epsilon$ dado, declaremos la convergencia y detengámonos!

Este algoritmo (que no es único) se llama la **<span style="color:#2f6004">iteración de valor (value iteration)</span>**: 

```{prf:algorithm} Iteracion-de-Valor 
:label: Value-Iteration

**Entradas**: Dado $\gamma$ y la tolerancia $\epsilon$

**Salida**: $V(s),\forall s\in {\cal S}$. 

1. Inicializar: $V(s)=0,\forall s\in {\cal S}$

2. **mientras** $\neg$convergencia: 
    1. $\delta = 0$

    2. **para** $s\in {\cal S}$:

        1. $v=V(s)$

        2. $V(s) = \max_{a}\left[R(s,a) + \gamma\sum_{s'\in {\cal S}}p(s'|s,a)V(s')\right]$

        3. $\delta = \max (\delta, |v - V(s)|)$

    3. **si** $\delta <\epsilon$ **entonces** **detener**

**return** $V(s),s\in {\cal S}$
```

#### Política Óptima y Valor Óptimo
La Iteración-de-Valor no solo proporciona $V(s)$ sino $V_{\ast}(s)$ **el valor óptimo**. ¿Por qué? 

En primer lugar, nótese que la Ecuación de Bellman suma sobre todas las acciones y luego pondera los valores existentes por los estados condicionados a las probabilidades de tales acciones. Esto es algo similar a 

$$
V^{k+1}(s) = \sum_{a\in {\cal A}}[R(s,a)+ \gamma\sum_{s'\in {\cal S}}p(s'|s,a)V^{k}(s')]\;.\\
$$

donde $V^0(s)=0,\forall s\in {\cal S}$. 

Sin embargo, la Ecuación de Bellman (que está alineada con el principio de optimalidad de la DP) retiene solo el mejor valor de cada iteración, es decir, el que proviene de tomar la mejor acción: 

$$
V^{k+1}(s) = \max_{a\in {\cal A}}[R(s,a)+ \gamma\sum_{s'\in {\cal S}}p(s'|s,a)V^{k}(s')]\;.\\
$$

Nótese que en cada iteración consideramos la **mejor acción para cada estado**. Esto suena muy "determinista" aquí, pero en general <span style="color:#2f6004">cada estado $s$ tiene asociada una distribución de probabilidad **desconocida** $\pi(a|s)$ que determina la posibilidad de que se tome una acción $a$ en el estado $s$</span>. Tal mapeo es una **<span style="color:#2f6004">política (policy)</span>**. 

Nótese que

$$
\sum_{a\in {\cal A}}\pi(a|s)=1\;,\forall s\in{\cal S}\;.
$$

Realmente, la función $V(s)$ **depende fuertemente de la política seguida**. Denotamos esto reescribiendo la Ecuación de Bellman de la siguiente manera: 

$$
V_{\pi}(s) = \sum_{a\in {\cal A}}\pi(a|s)\left[R(s,a)+ \gamma\sum_{s'\in {\cal S}}p(s'|s,a)V_{\pi}(s')\right]\;,\\
$$

que devuelve el valor para $s$ **siguiendo la política** $\pi$.

**Política Óptima**. Una política $\pi$ es óptima (y la denotamos por $\pi_{\ast}(a|s)$) si satisface: 

$$
\pi_{\ast}(a|s) = 
\begin{cases}
     1 &\;\text{si}\; a =\arg\max_{a\in{\cal A}}\left[R(s,a) + \gamma\sum_{s'\in {\cal S}}p(s'|s,a)V_{\ast}(s')\right] \\[2ex]
     0
     &\;\text{de lo contrario}\\[2ex]
\end{cases}
$$

A partir de la fórmula anterior, es bastante evidente que la política óptima $\pi_{\ast}$ se deriva tan pronto como conocemos el valor óptimo $V_{\ast}$. Esto se hace en el siguiente algoritmo: 

```{prf:algorithm} Politica-Optima 
:label: Optimal-Policy 

**Entradas**: Dado el valor óptimo $V_{\ast}(s),\forall s\in{\cal S}$. 

**Salida**: $\pi_{\ast}(a|s),\forall s\in {\cal S}$. 

1. **para** $s\in {\cal S}$:

    1. $a_{\ast}=\arg\max_{a\in{\cal A}}\left[R(s,a) + \gamma\sum_{s'\in {\cal S}}p(s'|s,a)V_{\ast}(s')\right]$
        

    2. **para** $a\in {\cal A}(s)$:

        1. **si** $a=a_{\ast}$:

           **entonces** $\pi(a|s)=1$ **de lo contrario** $\pi(a|s)=0$

**return** $\pi$
```

**Aplicación al perro de servicio**. Dada la configuración anterior, los valores y políticas óptimas son los siguientes (la convergencia es rápida): 

```
Función de Valor Óptima (V*):
Estado	Valor Óptimo
0	Room1	6.955562
1	Room2	7.814274
2	Room3	9.890110
3	Outside	6.955562
4	Found	0.000000

Política Óptima (π*):
Estado	Acción Óptima
0	Room1	GoRoom3
1	Room2	GoRoom3
2	Room3	Search
3	Outside	GoInside
4	Found	GoRoom1
```

**Valores óptimos**. En primer lugar, nótese que las funciones de valor son bastante ilustrativas de lo prometedor que es alcanzar el objetivo desde cualquier estado: $6.9$ desde la habitación 1, $7.8$ desde la habitación 2 y $9.8$ desde la habitación 3. Observe que el valor para afuera ($6.9$) es igual al de la habitación 1, lo que indica que estos estados están igualmente lejos de prometer el objetivo. Finalmente, una vez que se alcanza el objetivo, el valor es $0$. 

**Política Óptima**. En la {numref}`gop`, mostramos las probabilidades que conducen a la política óptima, junto con su correspondiente mejor acción.

```{figure} ./images/Topic2/graph-optimal-policy.png
---
name: gop
width: 800px
align: center
height: 150px
---
Grafo de la política óptima para el problema del perro de servicio. Creado por Gemini. 
```

### MDPs de Monte Carlo
El Aprendizaje por Refuerzo tipo DP <span style="color:#2f6004">asume que el agente tiene acceso total a un **modelo del entorno**</span>. Tal modelo (recompensas y probabilidades de transición) se especifica mediante la Ecuación de Bellman.

Sin embargo, en entornos con un gran número de estados y/o acciones, es bastante difícil especificar todas las recompensas y las transiciones de estado. Incluso cuando esto es posible, la evaluación de la Ecuación de Bellman para cada estado consume mucho tiempo. 

**El Problema de la Cuadrícula (Grid Problem)**. Consideremos la cuadrícula 2D de $5\times 5$ en la {numref}`grid2D`. Tenemos:  

1) Un estado objetivo $(4,4)$ con una recompensa $+10$ y un estado de penalización/pozo (pit) $(2,2)$ con recompensa $-10$. 

2) El catálogo de acciones es bastante simple 

$$
{\cal A} = \{\text{Arriba (Up)},\text{Abajo (Down)},\text{Izquierda (Left)}, \text{Derecha (Right)}\}\;,
$$

donde $\text{Arriba}=(1,0)$ aumenta el índice de la fila, $\text{Abajo}=(-1,0)$ lo disminuye, $\text{Izquierda}=(0,-1)$ disminuye el índice de la columna y, finalmente, $\text{Derecha}=(0,1)$ lo aumenta. 

3) Con respecto a las recompensas por acción, aplicar cualquier acción (excepto donde el destino sea el objetivo o el pozo) tiene una recompensa de $-1$, lo que obliga al agente a consumir el menor número de acciones posible. 

```{figure} ./images/Topic2/Grid2D.png
---
name: grid2D
width: 600px
align: center
height: 550px
---
Problema Grid2D con estados final y pozo. Creado por Gemini. 
```

En esta configuración particular, acercarse a la diagonal conduce a una recompensa subóptima desde $(0,0)$. Por lo tanto, no es una buena idea usar $\text{Arriba}$ y $\text{Derecha}$ alternativamente en este caso. 

Recuerde también que resolver un problema de RL implica calcular $V_{\ast}(s)$ para todos los estados $(i,j), i,j=0,\ldots,4$. Aquí, tenemos un número cuadrático de estados y el cálculo de $V_{\ast}(s)$ mediante Iteración-de-Valor también es cuadrático (lineal por iteración con el número de estados, que es cuadrático). Esto puede no ser asumible para cuadrículas más grandes. 

#### Recompensas Futuras

**MDPs de Monte Carlo** <span style="color:#2f6004">recopilan **varios episodios** de estado-acción-estado y sus correspondientes recompensas y toman su promedio como un medio para **aprender por la experiencia**</span>. 

Cada episodio tiene la siguiente forma: 

$$
(s_0, a_0, r_1), (s_1, a_1, r_2), \ldots, (s_{T-1}, a_{T-1}, r_T)
$$

donde $T$ es el tiempo máximo del episodio, ya que el *episodio termina (o se "completa") si se alcanza el estado del pozo o el del objetivo*.  

**Recompensas futuras**: En cada episodio, las recompensas futuras se calculan *hacia atrás* de la siguiente manera: 

$$
\begin{align}
G(s_{T-1}) &= r_{T}\\
G(s_{T-2}) &= r_{T-1} + \gamma G(s_{T-1})\\
\ldots \\
G(s_{1}) &= r_{2} + \gamma G(s_{2})\\
G(s_{0}) &= r_{1} + \gamma G(s_{1})\\
\end{align}
$$

Para ahorrar tiempo de evaluación, en los <span style="color:#2f6004">**MDPs de Monte Carlo de primera visita (First-visit)**</span>, las recompensas futuras solo se evalúan la *primera vez* que se visita cada estado $s_i$, es decir, cuando se incluye en un triplete $(s_t, a_t, r_{t+1})$ del episodio. 

Si el estado $s$ aparece en $N_{s}$ episodios, su recompensa futura global es el promedio: 

$$
\bar{G}(s)=\sum_{e=1}^{N_{s}} G(s,e)/N_{s}\;,
$$ 

donde $G(s,e)$ se refiere al valor futuro de $s$ en el episodio $e$ (la primera vez que aparece, si seguimos la estrategia de primera visita).


#### Política $\epsilon-$Greedy
En cuanto a la función de valor, dado que su cálculo depende de la elección de un conjunto de acciones, suponemos que el aprendiz sigue una política dada $\pi$. 

Recuerde que $V_{\pi}$ es el valor obtenido al seguir una política $\pi$. Usando la Ecuación de Bellman, tenemos: 

$$
V_{\pi}(s) = \sum_{a\in {\cal A}}\pi(a|s)\underbrace{\left[R(s,a)+ \gamma\sum_{s'\in {\cal S}}p(s'|s,a)V_{\pi}(s')\right]}_{Q_{\pi}(s,a)}\;,\\
$$

donde $Q_{\pi}(s,a)$ es el <span style="color:#2f6004">**valor Q (Q-value) para la acción $a$ y el estado $s$**</span>. 

Sin embargo, en Monte Carlo (que es **libre de modelo / model free**) no podemos estimar $Q_{\pi}(s,a)$ usando la Ecuación de Bellman. En su lugar, **la política se puede decidir sobre la marcha**. 

En la <span style="color:#2f6004">**Política $\epsilon-$Greedy**</span> definimos la política de la siguiente manera: 

$$
\pi(a|s)=
\begin{cases}
     1 - \epsilon + \frac{\epsilon}{|{\cal A}(s)|} &\;\text{si}\; a =\arg\max_{a\in{\cal A}}Q_{\pi}(s,a) \\[2ex]
     \frac{\epsilon}{|{\cal A}(s)|}
     &\;\text{de lo contrario}\;,\\[2ex]
\end{cases}
$$

donde: 

1) $Q_{\pi}(s,a)$ son propuestos por el MDP de Markov.  

2) $\epsilon\in [0,1]$ define **la probabilidad de tomar una acción aleatoria** desde el estado $s$, donde ${\cal A}(s)$ es el conjunto de acciones legales que se pueden tomar desde este estado y $|{\cal A}(s)|$ el número de estas acciones legales. 

3) Si $\epsilon = 0$, el agente selecciona la política (hasta ahora) óptima con probabilidad $1$. 

4) Si $\epsilon = 1$, el agente selecciona o bien la política hasta ahora óptima o cualquier otra con probabilidad $\frac{1}{|{\cal A}(s)|}$. 

Definamos el Algoritmo de Política $\epsilon-$Greedy: 

```{prf:algorithm} Politica-Epsilon
:label: Epsilon-Policy 

**Entradas**: Estado actual $s$, valores Q, $Q_{\pi}(s,a)$, ${\cal A}(s)$, $\epsilon$. 

**Salida**: Acción Óptima estimada $a^{\ast}$. 

1. **si** $\text{random}(0,1)<\epsilon$ **entonces**:

   \# Exploración: Elegir una acción aleatoria: 

    1. **return** $\text{randomChoice}({\cal A}(s))$

2. **de lo contrario**: 

    \# Explotación: Elegir la acción arg-max: 

    1. $\text{max\_q} = -\infty$
    
    2. $\text{best\_actions} =\emptyset$
        

    1. **para** $a\in {\cal A}(s)$, $q\in Q_\pi(s,a)$:

        1. **si** $q>\text{max\_q}$:

           **entonces** $\text{max\_q}=q$, $\text{best\_actions}=\{a\}$

        2. **o si** $q==\text{max\_q}$: 

           **entonces** $\text{best\_actions}=\text{best\_actions}\cup \{a\}$
           

**return** $\text{randomChoice}(\text{best\_actions})$
```

Integremos ahora el algoritmo anterior con un MDP de Monte Carlo global. 

```{prf:algorithm} Politica-Epsilon-Q 
:label: Epsilon-Policy-Q 

**Entradas**: Episodios $K$, tiempos por episodio $T$

**Salida**: $Q_{\pi\ast}$ $\epsilon-$Greedy

1. **Inicializar**. $i=0$, $Q_{\pi}(s,a)=0$, $N(s,a)=0$, $G(s,a)=0$ $\forall s\in {\cal S}, a\in {\cal A}$. 

1. **para** el episodio $i$: 

    1. Seleccionar el estado inicial $s_0$

    2. $\text{history}=\emptyset$

    3. **para** $t=\{1,\ldots,T\}$

        1. $a_{t-1} = \text{Politica-Epsilon}$($s_{t-1}$, $Q_{\pi}(s_{t-1},a_{t-1})$, ${\cal A}(s_{t-1})$, $\epsilon$)

        2. Crear triplete $(s_{t-1},a_{t-1},r_t)$

        3. $\text{history} = \text{history}\cup \{(s_{t-1},a_{t-1},r_t)\}$

    4. $G=0$ 

    5. $\text{visited\_state\_actions}=\emptyset$

    6. **para** $t\in\text{reversed}(\text{history})$: 

        1. $(s_{t-1},a_{t-1},r_t) = \text{history}[t]$

        2. $G = r_t + \gamma * G$

        3. **si** $(s_{t-1},a_{t-1})\not\in \text{visited\_state\_actions}$

        4. **entonces** 
            
            1. $\text{visited\_state\_actions} = \text{visited\_state\_actions}\cup (s_{t-1},a_{t-1})$
                
            2. $G(s_{t-1},a_{t-1}) = G(s_{t-1},a_{t-1}) + G$

            3. $N(s_{t-1},a_{t-1}) = N(s_{t-1},a_{t-1}) + 1$

            4. $Q_{\pi}(s_{t-1},a_{t-1})= \frac{G(s_{t-1},a_{t-1})}{N(s_{t-1},a_{t-1})}$ 

    7. $i = i + 1$

**return** $Q_{\pi\ast}$
```

$\text{Politica-Epsilon}$ es una subrutina de $\text{Politica-Epsilon-Q}$. Realmente, para cada episodio: 

1) <ins>Seleccionamos un estado inicial</ins> $s_0$ para comenzar el episodio. Como la acción correspondiente a este estado es desconocida y tiene que ser determinada por el método $\epsilon-$Greedy, llamamos a $\text{Politica-Epsilon}$ para obtener tal acción $a_{0}$. Esto conduce a la primera recompensa $r_1$ y el primer triplete $(s_0,a_0,r_1)$ se añade al $\text{historial (history)}$ del episodio. El bucle **para** en la línea $2.3$ se ejecuta hasta que el historial de este episodio se completa y todas las acciones $\epsilon-$Greedy se incluyen en él. 

2) <ins>Evaluamos las Recompensas Futuras</ins>. Una vez que tenemos el historial del episodio, podemos calcular las recompensas futuras como se especifica en el MPD de Monte Carlo. Sin embargo, vale la pena invertir el tiempo en la secuencia ya que $G(s_t)=r_{t+1} + \gamma G(s_{t+1})$. 

3) <ins>Primera visita y actualización de $Q$</ins>. Si el par $(s_{t-1},a_{t-1})$ aparece por primera vez en el historial del episodio con tiempo invertido, es el momento de actualizar el número total de veces que aparece y la variable $G(s_{t-1},a_{t-1})$ que acumula las recompensas futuras. La variable $Q_{\pi}(s_{t-1},a_{t-1})$ resulta de una proporción obvia. Nótese que aquí **no utilizamos la Ecuación de Bellman**. 

Dados los $Q_{\pi}(s,a),\forall s\in{\cal S}, a\in{\cal A}$, almacenamos en cada $s$ el valor máximo de $Q_{\pi}(s,a)$ para cualquier acción $a$. Mostramos el resultado en la {numref}`grid2D-Q`: 

```{figure} ./images/Topic2/Grid2D-Q.png
---
name: grid2D-Q
width: 600px
align: center
height: 550px
---
Valores Q óptimos para el problema Grid2D con estados final y pozo. Creado por Gemini. 
```

Una vez que hemos "aproximado" $Q_{\pi}$, es trivial calcular $\pi(a|s)$ como en 

$$
\pi(a|s)=
\begin{cases}
     1 - \epsilon + \frac{\epsilon}{|{\cal A}(s)|} &\;\text{si}\; a =\arg\max_{a\in{\cal A}}Q_{\pi}(s,a) \\[2ex]
     \frac{\epsilon}{|{\cal A}(s)|}
     &\;\text{de lo contrario}\;.\\[2ex]
\end{cases}
$$

La política óptima con este método $\epsilon$ se muestra en la {numref}`grid2D-P`: 

```{figure} ./images/Topic2/Grid2D-P.png
---
name: grid2D-P
width: 600px
align: center
height: 550px
---
Política $\epsilon-$Greedy para el problema Grid2D con estados final y pozo. Creado por Gemini. 
```

Básicamente, el algoritmo $\text{Politica-Epsilon-Q}$ <span style="color:#2f6004">construye la política óptima de una manera voraz que **mejora una política aleatoria simple** $(\epsilon=1)$</span>. Además, <span style="color:#2f6004">el agente está **aprendiendo de su experiencia**</span> gracias al proceso de Monte Carlo donde está incrustada la estimación de la política $\epsilon-$Greedy. 

#### Exploración frente a Explotación
Nótese que en el algoritmo $\text{Politica-Epsilon-Q}$, llamamos a la subrutina $\text{Politica-Epsilon}$ para seleccionar una acción. Sin embargo, la mejor acción resultante (hasta ahora) depende de $Q_{\pi}$, que es desconocido en las primeras etapas de $\text{Politica-Epsilon-Q}$. A medida que el MDP de Monte Carlo construye $Q_{\pi}$, las acciones son cada vez más informativas. 

De hecho, para un $Q_{\pi}$ dado, la llamada a $\text{Politica-Epsilon}$ se basa en <span style="color:#2f6004">**un $\epsilon$ fijo**</span> que declara cuán "aleatoria" puede ser la elección. Sin embargo, como la acción obtenida es cada vez más informativa a medida que avanza el MDP, tiene sentido <span style="color:#2f6004">**actualizar** $\epsilon$</span> para que tenga un impacto en  

$$
\pi(a|s)=
\begin{cases}
     1 - \epsilon + \frac{\epsilon}{|{\cal A}(s)|} &\;\text{si}\; a =\arg\max_{a\in{\cal A}}Q_{\pi}(s,a) \\[2ex]
     \frac{\epsilon}{|{\cal A}(s)|}
     &\;\text{de lo contrario}\;.\\[2ex]
\end{cases}
$$

Buscamos un **equilibrio (trade-off)** entre: 

**Exploración**. Empezamos con un **alto valor** de $\epsilon$ (más aleatorio cuando hay menos conocimiento de $Q_{\pi}$).

**Explotación**. A medida que emerge $Q_{\pi}$, lo explotamos para tomar decisiones cada vez mejores (más informadas). Esto se asocia con **valores decrecientes** de $\epsilon$. 

En la {numref}`Explore` mostramos la recompensa acumulada por etapa a medida que modificamos $\epsilon$ de la siguiente manera: 

$$
\epsilon^{t+1} = \max(\epsilon_{min}, \epsilon^{t}\cdot \epsilon_{decay})
$$

donde $\epsilon_{min}=0.01$ es el $\epsilon$ mínimo (menos aleatorio) alcanzable, $\epsilon_{decay}=0.999$ es el factor de decaimiento y $\epsilon^{0}=1$. Esto nos recuerda a la **programación de la temperatura durante el recocido (annealing scheduling)**. 

```{figure} ./images/Topic2/Explore.png
---
name: Explore
width: 800px
align: center
height: 500px
---
Recompensa total acumulada para un $\epsilon$ dinámico. 
```

¿Cómo podemos analizar la figura anterior? 

1) **Exploración Inicial**. Nótese que en las <ins>etapas tempranas</ins> (0-200), la recompensa acumulada es muy aleatoria (grandes oscilaciones a lo largo del tiempo), baja e incluso negativa. El agente está probando muchas acciones aleatorias que suelen conducir a caer en estados de penalización o a elegir caminos largos para alcanzar el objetivo. Las grandes oscilaciones muestran que el agente está simplemente "probando" o "sondeando" el entorno.

2) **Transición**. En las <ins>etapas intermedias</ins> (200-700), a medida que el epsilon decae, el agente reduce su exploración y favorece acciones que, según un $Q_{\pi}$ más informado, parecen más prometedoras en términos de recompensas acumuladas. Aunque todavía hay oscilaciones, las recompensas acumuladas aumentan en promedio. Esto muestra que el agente está "descubriendo" y "reforzando" los caminos más eficientes y/o evitando estados de penalización. 

3) **Explotación**. Cerca del <ins>final del entrenamiento</ins> (700-1000), $\epsilon$ se acerca a su valor mínimo (0.01). En esta etapa, el agente explota principalmente el conocimiento que tiene, es decir, el $Q_{\pi}$. Como resultado, hay una estabilización de la recompensa acumulada en valores altos. En este caso, los picos consistentes alrededor de $+3$ (recompensa de $+10$ por alcanzar el objetivo y $-1$ por cada uno de los normalmente 7 pasos para alcanzarlo) muestran que el agente sigue una política óptima al final del entrenamiento. 

### Diferencia Temporal y SARSA 
Los MDPs de Monte Carlo son estrategias ideales libres de modelo para "entornos episódicos" (donde hay pasos bien definidos), pero <span style="color:#2f6004">**no son adecuados para el aprendizaje continuo**</span> (no hay un final natural de la tarea). 

Además, los MDPs de Monte Carlo imponen la <span style="color:#2f6004">**actualización de la función de valor al final de cada episodio**</span>.

La <span style="color:#2f6004">**Diferencia Temporal (Temporal Difference - TD)**</span> resuelve estos dos problemas actualizando incrementalmente sus valores mediante la siguiente fórmula bien conocida: 

$$
\text{Nueva\_Estimacion} = \text{Vieja\_Estimacion} + \text{Tamaño\_del\_Paso}(\text{Objetivo} - \text{Vieja\_Estimacion})\;,
$$

donde el **Objetivo (Target)** es $G_t$, lo que conduce a 

$$
V_{\pi}(S_t)\leftarrow V_{\pi}(S_t) + \alpha \left(\underbrace{r_{t+1} + \gamma\cdot V_{\pi}(S_{t+1})}_{G_t} - V_{\pi}(S_t)\right)\;,
$$

y $\alpha$ (hiperparámetro) es el tamaño del paso o "tasa de aprendizaje (learning rate)". Este parámetro reemplaza a $1/N(S_t)$ ya que en TD no contamos $N(S_t)$. 

Nótese que para la estimación de $V_{\pi}(S_t)$ necesitamos tuplas $(s,a,r',s')$, donde tanto $r'$ como $s'$ se refieren a $t+1$ (recompensa y estado después de aplicar la acción $a$). 


<span style="color:#2f6004">**Estado-Acción-Recompensa-Estado-Acción (SARSA)**</span>. SARSA es una extensión que consiste en considerar tuplas $(s,a,r',s')$ a tuplas $(s,a,r',s',a')$. 

Realmente, la regla de actualización de SARSA es 

$$
Q_{\pi}(s_t,a_t)\leftarrow Q_{\pi}(s_t,a_t) + \alpha \left(r_{t+1} + \gamma\cdot Q_{\pi}(s_{t+1},a_{t+1}) - Q_{\pi}(s_t,a_t)\right)\;,
$$

```{prf:algorithm} SARSA 
:label: SARSA

**Entradas**: Episodios $K$, tiempos por episodio $T$, tasa de aprendizaje $\alpha$, $\epsilon_{min}$, $\epsilon_{decay}$

**Salida**: $Q_{\pi\ast}$ SARSA $\epsilon-$Greedy

1. **Inicializar**. $i=0$, $Q_{\pi}(s,a)=0$, $N(s,a)=0$, $\forall s\in {\cal S}, a\in {\cal A}$, $\epsilon=1$. 

1. **para** el episodio $i$: 

    1. $\text{current\_s} = \text{Select\_Initial\_State()}$

    2. $a_{t-1} = \text{Politica-Epsilon}$($\text{current\_s}$, $Q_{\pi}$, ${\cal A}(\text{current\_s})$, $\epsilon$)

    3. **para** $t=\{1,\ldots,T\}$

        1. Crear $(s_{t-1},a_{t-1},r_t)\rightarrow s_t$

        2. $a_{t} = \text{Politica-Epsilon}$($s_{t}$, $Q_{\pi}$, ${\cal A}(s_{t})$, $\epsilon$)

        3. $\text{old\_q}=Q_{\pi}(s_{t-1},a_{t-1})$

        4. **si** $\text{done}(s_{t})$:

        5. **entonces** $\text{target\_q}=r_t$

        6. **de lo contrario** $\text{target\_q}=r_t + \gamma\cdot Q_{\pi}(s_t,a_t)$

        7. $Q_{\pi}(s_{t-1},a_{t-1}) = \text{old\_q} + \alpha\cdot(\text{target\_q} -\text{old\_q})$ 

        8. $\text{Actualizar}:$ $\text{current\_s} = s_{t}$, $a_{t-1} = a_{t}$

    4. $\epsilon = \max(\epsilon_{min}, \epsilon\cdot \epsilon_{decay})$

    5. $i = i + 1$

**return** $Q_{\pi\ast}$
```

Algunas precisiones sobre el algoritmo anterior: 

1) <ins>¿Episodios?</ins>. Aunque seguimos la estructura episódica del algoritmo de Monte Carlo, aquí los episodios solo se utilizan para encontrar un estado inicial a seguir (como una trayectoria). Nótese que justo antes del final de cada "episodio" actualizamos el $\epsilon$. Por lo tanto, el proceso puede verse como $K$ etapas o **épocas (epochs)**, cada una con $T$ pasos, de un algoritmo de aprendizaje continuo. Pero, <span style="color:#2f6004">**conceptualmente $K$ puede ser ilimitado**</span>. 

2) <ins>Tuplas</ins>. El algoritmo SARSA simplemente construye tuplas $(s,a,r,s',s')$ para actualizar $Q_{\pi}(s_{t-1},a_{t-1})$, es decir, $Q_{\pi}(s,a)$ a partir del viejo $Q_{\pi}(s,a)$ y el nuevo $Q_{\pi}(s',a')$. Por eso necesitamos dos llamadas a $\text{Politica-Epsilon}$ (una para $a_{t-1}$ y otra para $a_{t}$). Finalmente, la función $\text{done}(s_{t})$ se detiene si llegamos a un estado objetivo o a un estado de penalización. 

3) <ins>Aprendizaje Online</ins>. SARSA no necesita terminar un episodio para obtener una estimación de $Q_{\pi}$. <span style="color:#2f6004">**La actualización se realiza tan pronto como la información está disponible**</span>. Esto significa "online" y esta estrategia también es útil para problemas no episódicos (más realistas). 

En la {numref}`grid2D-SARSA` mostramos los valores máximos de $Q_{\pi\ast}$ para el algoritmo SARSA donde tenemos: $K=1000$, $T=100$, $\alpha = 0.1$, $\gamma = 0.9$, $\epsilon = 1.0$, $\epsilon_{min}=0.01$ y $\epsilon_{decay}=0.995$.

```{figure} ./images/Topic2/Grid2D-SARSA.png
---
name: grid2D-SARSA
width: 600px
align: center
height: 550px
---
Valores Q óptimos para el problema Grid2D con estados final y pozo para SARSA. Creado por Gemini. 
```

### On-Policy frente a Off-Policy
SARSA es un algoritmo <span style="color:#2f6004">**on-policy**</span> ya que: 

1) Utiliza acciones que son **realmente seleccionadas** por la política del agente (por ejemplo, $\epsilon-$greedy).

2) SARSA aprende $Q_{\pi}$ a partir de la política $\pi$ que el agente está **siguiendo realmente**, incluyendo su comportamiento de exploración.

3) Como resultado, SARSA busca la **política óptima considerando la exploración del agente**. 

Las <span style="color:#2f6004">estrategias **On-Policy** pueden conducir a **políticas muy conservadoras** en entornos peligrosos (ya que penaliza los estados de alto riesgo, incluso si el camino óptimo pasa por ellos)</span>. 

La <span style="color:#2f6004">**exploración Off-policy**</span>, sin embargo, es una estrategia donde la política de comportamiento y la política objetivo son **diferentes**. 

<span style="color:#2f6004">Los algoritmos de aprendizaje por refuerzo Off-policy suelen ser **más potentes** porque pueden utilizar la experiencia generada por una política de comportamiento diferente, que puede ser más exploratoria que la política objetivo</span>.

**Resumiendo**: On-policy es aprender de **lo que hago**, mientras que Off-policy es aprender de **lo que otros hacen**. 

### Q-Learning
Q-Learning es un algoritmo TD y es el algoritmo **Off-policy** más utilizado. <span style="color:#2f6004">Aprende la política óptima de forma **independiente** al comportamiento del agente</span>. ¿Cómo?  

En SARSA, seguimos la regla de actualización 

$$
Q_{\pi}(s_t,a_t)\leftarrow Q_{\pi}(s_t,a_t) + \alpha \left(r_{t+1} + \gamma\cdot \mathbf{Q_{\pi}(s_{t+1},a_{t+1})} - Q_{\pi}(s_t,a_t)\right)\;,
$$
Sin embargo, en Q-Learning hacemos 

$$
Q_{\pi}(s_t,a_t)\leftarrow Q_{\pi}(s_t,a_t) + \alpha \left(r_{t+1} + \gamma\cdot \mathbf{\max_{a'}Q_{\pi}(s_{t+1},a')} - Q_{\pi}(s_t,a_t)\right)\;,
$$

donde destacamos (en negrita) las diferencias: 

- **On-Policy**. SARSA es On-Policy porque la acción $a_{t+1}$ se selecciona a partir de una política $\epsilon-$greedy que es la **misma** que la utilizada para seleccionar $a_{t}$. 

- **Off-policy**. Q-Learning es Off-Policy porque la acción $a_{t+1}$ (es decir, $a'$) es la que maximiza $Q_{\pi}$ para $s_{t+1}$. En otras palabras, es **independiente** de la elección de $a_{t}$ que (normalmente) se basa en una política $\epsilon-$greedy. 

En otras palabras, <span style="color:#2f6004">Q-Learning opera sobre el mejor objetivo posible **incluso si esta acción no ha sido tomada por la política actual**</span>. 

```{prf:algorithm} Q-Learning
:label: Q-Learning

**Entradas**: Episodios $K$, tiempos por episodio $T$, tasa de aprendizaje $\alpha$, $\epsilon_{min}$, $\epsilon_{decay}$

**Salida**: $Q_{\pi\ast}$ Q-Learning $\epsilon-$Greedy

1. **Inicializar**. $i=0$, $Q_{\pi}(s,a)=0$, $N(s,a)=0$, $\forall s\in {\cal S}, a\in {\cal A}$, $\epsilon=1$. 

1. **para** el episodio $i$: 

    1. $\text{current\_s} = \text{Select\_Initial\_State()}$

    2. **para** $t=\{1,\ldots,T\}$

        1. $a_{t-1} = \text{Politica-Epsilon}$($\text{current\_s}$, $Q_{\pi}$, ${\cal A}(\text{current\_s})$, $\epsilon$)
       
        2. Crear $(\text{current\_s},a_{t-1},r_t)\rightarrow s_t$

        3. $\text{old\_q}=Q_{\pi}(s_{t-1},a_{t-1})$

        4. **si** $\text{done}(s_{t})$:

        5. **entonces** $\text{max\_q}=0.0$

        6. **de lo contrario** $\text{max\_q}= \max_{a'} Q_{\pi}(s_t,a')$

        7. $Q_{\pi}(s_{t-1},a_{t-1}) = \text{old\_q} + \alpha\cdot(r_t +\gamma\cdot\text{max\_q} -\text{old\_q})$ 

        8. $\text{Actualizar}:$ $\text{current\_s} = s_{t}$

    4. $\epsilon = \max(\epsilon_{min}, \epsilon\cdot \epsilon_{decay})$

    5. $i = i + 1$

**return** $Q_{\pi\ast}$
```

donde no hay un bucle doble y la variable $\text{max\_q}$ sustituye a $\text{target\_q}$ en SARSA, mostrando claramente que ambas proceden de políticas potencialmente diferentes. 

En la {numref}`grid2D-Q-Learning` mostramos los valores máximos de $Q_{\pi\ast}$ para el algoritmo SARSA donde tenemos: $K=1000$, $T=100$, $\alpha = 0.1$, $\gamma = 0.9$, $\epsilon = 1.0$, $\epsilon_{min}=0.01$ y $\epsilon_{decay}=0.995$.

```{figure} ./images/Topic2/Grid2D-Q-Learning.png
---
name: grid2D-Q-Learning
width: 600px
align: center
height: 550px
---
Valores Q óptimos para el problema Grid2D con estados final y pozo para Q-Learning. Creado por Gemini. 
```
En comparación con SARSA:

1) Q-Learning produce valores más altos para el Q óptimo a medida que el agente está más cerca del objetivo, y más pequeños en los estados alejados del objetivo. Como estamos maximizando la recompensa total, los estados objetivo (y/o los estados con recompensa alta) se convierten en atractores. 

2) Q-Learning da valores más altos que SARSA a los estados cercanos a los estados 'peligrosos' (de baja recompensa). Una metáfora de esto es caminar cerca de un acantilado. 

En otras palabras, <span style="color:#2f6004">**Q-Learning es más impaciente que SARSA**, lo cual es más conveniente cuando el agente tiene que evitar estados peligrosos (de baja recompensa)</span>.

**Comparación Global**. En la {numref}`Explore-Comparison` comparamos la evolución de las recompensas acumuladas para Monte Carlo, SARSA y Q-Learning. Nótese que las estrategias TD como SARSA y Q-Learning tienen <span style="color:#2f6004">**menor varianza** en el eje y con respecto a Monte Carlo</span>. Además, **convergen más rápido** que Monte Carlo. 

```{figure} ./images/Topic2/Explore-Comparison.png
---
name: Explore-Comparison
width: 800px
align: center
height: 500px
---
Recompensas totales acumuladas para un $\epsilon$ dinámico. Comparación entre Monte Carlo, SARSA y Q-Learning. 
```

### Deep Q-Learning
#### La Imagen General (The Big Picture) 
Sustituyamos la ecuación clásica de Q-Learning

$$
Q_{\pi}(s_t,a_t)\leftarrow Q_{\pi}(s_t,a_t) + \alpha \left(r_{t+1} + \gamma\cdot \max_{a'}Q_{\pi}(s_{t+1},a') - Q_{\pi}(s_t,a_t)\right)\;,
$$

encontrando una Red Neuronal (parametrizada por $\Theta$) que minimice 

$$
J(\Theta) = \mathbb{E}_{(s,a,r,s')}\left[\left(r + \gamma\cdot \max_{a'}\hat{Q}_{\pi}(s',a';\Theta) - \hat{Q}_{\pi}(s,a;\Theta)\right)^2\right]\;,
$$

donde $\hat{Q}$ son la versión parametrizada de $Q$ según $\Theta$. En otras palabras, <span style="color:#2f6004">Deep Q-Learning se basa en encontrar **actualizaciones de Q-Learning óptimas** de acuerdo con **minimizar la diferencia entre la política actual y la objetivo**</span>. 

**¿Cómo alimentamos la NN?**. En lugar de alimentar la NN a través de pares $(s,a)$, parece más conveniente usar $s$ como entrada y colocar los $\hat{Q}_{\pi}(s,a_i;\Theta)$ en la capa de salida. De esta manera, aprendemos a ajustar $\Theta$ para minimizar $J(\Theta)$ reduciendo las disparidades entre lo que la NN espera de un $\Theta$ dado y lo que realmente debe satisfacer. Resumimos este mapeo de E/S en la {numref}`DQN-Feed`. 

Obviamente, los valores de referencia son proporcionados por algo parecido a una política $\epsilon-$greedy. 

```{figure} ./images/Topic2/DQN-Feed.png
---
name: DQN-Feed
width: 500px
align: center
height: 200px
---
Alimentación de una NN en Deep Q-Learning. Adaptado de [The Art of Reinforcement Learning](https://link.springer.com/book/10.1007/978-1-4842-9606-6). 
```


#### Entradas basadas en imágenes 
Las NN son efectivas cuando se trata de espacios de entrada de alta dimensión, como las imágenes. Aunque este no es el caso de los problemas típicos de RL (perro de servicio, grid2D, taxi, cart pole) donde tomamos muestras de **baja dimensión** como $(s,a,r,s')$ o $(s,a,r,s',a')$. 

Sin embargo, en problemas de RL más realistas, como los **juegos de Atari** (mostrados en la introducción a este tema), se tiene un entorno o representación de estado complejo. Por ejemplo, en la {numref}`RLAgent` una imagen captura la posición de la pala, la posición de la bola y la ubicación de los ladrillos superiores (supervivientes) para **Atari Breakout**. 

En este sentido, <span style="color:#2f6004">una **instantánea (snapshot)** (imagen) es una buena descripción del estado $s$</span>. Sin embargo, hay algunos **pre-procesamientos** que hacer: 

1) <ins>Escala de grises</ins>. En muchos juegos, como Atari Breakout, la información de color no es relevante y puede descartarse. 

2) <ins>Cambio de forma (Reshape)</ins>. Si queremos aprovechar la potencia de las **Redes Convolucionales** (CNNs), es conveniente transformar las imágenes rectangulares (originales) en cuadradas. 

#### Asegurar la propiedad de Markov
Recuerde que una de las precondiciones clave para el RL (visto como un MDP) es que la cadena implícita de estados sucesivos debe satisfacer la Condición de Markov: $p(s'_{t+1}|s_t) = p(s'_{t+1}|s_t,s_{t-1},\ldots,s_0)$. Con ese fin, las instantáneas consecutivas tienen que estar **decorrelacionadas** (muestras i.i.d.), lo cual no es cierto si la pala golpea una bola y tomamos cuatro imágenes consecutivas de la trayectoria de la bola: *la última posición de la bola depende fuertemente de las otras tres*. 

<span style="color:#2f6004">La forma estándar de decorrelacionar imágenes consecutivas es **dividir el flujo de imágenes en bloques de $k$ fotogramas (frames)** (digamos $k=4$) y **considerar cada bloque como un estado**</span>. 

Obviamente, el valor ideal de $k$ depende de la frecuencia de vídeo, pero el resultado es que la entrada de la CNN será un tensor de tamaño $W\times H\times k$ donde $W=H$. Normalmente $W=84$ y $k=4$ por el Atari Breakout. 

En la {numref}`DQN-Stacked`, mostramos $k=4$ fotogramas formando un estado. Nótese que los tres primeros no tienen la propiedad de Markov, la cual es habilitada por el cuarto (cambio de trayectoria).

```{figure} ./images/Topic2/DQN-Stacked.png
---
name: DQN-Stacked
width: 800px
align: center
height: 250px
---
Fotogramas apilados formando un "estado visual". Generado por Gemini.
``` 

#### Arquitectura de la CNN 
Como resultado, la CNN mapea $k$ fotogramas consecutivos del juego (codificando $s$) a $n$ acciones. En Atari Breakout $n=4$ ya que tenemos las siguientes acciones: 

$$
{\cal A}=\{0:\text{No Operación},1:\text{Mover Pala Derecha}, 2:\text{Fuego}, 3:\text{Mover Pala Izquierda}\}\;.
$$

Por lo tanto, la arquitectura de la CNN (denominada **DQN**) es bastante directa (varias Convoluciones 2D de filtros crecientes (cada una seguida de una ReLU), un aplanamiento seguido de algunas redes totalmente conectadas o Perceptrones y una capa final con $n=4$ características que codifican los valores Q para los estados de entrada): 

```
DQN(
  (conv1): Conv2d(4, 32, kernel_size=(8, 8), stride=(4, 4))
  (conv2): Conv2d(32, 64, kernel_size=(4, 4), stride=(2, 2))
  (conv3): Conv2d(64, 64, kernel_size=(3, 3), stride=(1, 1))
  (fc1): Linear(in_features=3136, out_features=512, bias=True)
  (fc2): Linear(in_features=512, out_features=4, bias=True)
)
```

cuyo grafo computacional en Pytorch está en la {numref}`dqn_target_architecture`

```{figure} ./images/Topic2/dqn_target_architecture.png
---
name: dqn_target_architecture
width: 500px
align: center
height: 700px
---
Arquitectura CNN para el juego Atari Breakout. Generado por Gemini.
``` 

Nótese que las primeras $4$ características en la primera $\text{Conv2d}$ corresponden a los $k=4$ fotogramas y las últimas $4$ características ($\text{out\_features}$) en $\text{fc2}$ corresponden a $n=4$ acciones. 

#### Repetición de Experiencia (Experience Replay) 
Este es otro elemento de Deep Q-Learning.<span style="color:#2f6004">La **repetición de experiencia (experience replay)** consiste en recopilar un búfer de $N$ tuplas $(s,a,r,s',\text{done})$ y luego tomar un **mini-lote (mini-batch)** de muestras aleatorias de él.</span> 

La motivación de esta técnica es la siguiente. Alimentar la red $\Theta$ con cadenas de tuplas $(s,a,r,s',\text{done})$ conduce a un uso pobre de los datos y a un aprendizaje lento. Recuerde que el Descenso de Gradiente Estocástico (SGD) opera sobre grupos de pares E/S para obtener una dirección de gradiente media. La Repetición de Experiencia **está alineada con el SGD**, además de que produce una fuente adicional de **decorrelación**. 

```{figure} ./images/Topic2/Replay.jpg
---
name: Replay
width: 500px
align: center
height: 250px
---
Papel de la repetición de experiencia en Deep Q-Learning. [Crédito](https://www.sciencedirect.com/science/article/pii/S2092678220300418). 
``` 

Nótese que, como los datos del mini-lote pueden provenir de estados tomados hace tiempo, 
la repetición de experiencia NO ESTÁ ALINEADA con los métodos **On-policy** como SARSA. 

#### Red de Política frente a Red de Objetivo 
La DQN 'vanilla' tiene una única red para predecir $\hat{Q}_{\pi}$ y luego actualizar 

$$
J(\Theta) = \mathbb{E}_{(s,a,r,s')}\left[\left(r + \gamma\cdot \max_{a'}\hat{Q}_{\pi}(s',a';\Theta) - \hat{Q}_{\pi}(s,a;\Theta)\right)^2\right]\;,
$$

donde $\Theta$ denota los parámetros de la llamada **red de política (policy network)**. Sin embargo, <span style="color:#2f6004">DQN también mantiene otra red, conocida como **red de objetivo (target network)**, que es estructuralmente idéntica a la red de política</span>. 

Por lo tanto, tenemos 

$$
J(\Theta) = \mathbb{E}_{(s,a,r,s')}\left[\left(r + \gamma\cdot \max_{a'}\hat{Q}_{\pi}(s',a';\Theta^{-}) - \hat{Q}_{\pi}(s,a;\Theta)\right)^2\right]\;,
$$

donde $\Theta^{-}$ son los pesos de la red de objetivo. <span style="color:#2f6004">Estos pesos son **inicialmente aleatorios** y se copian de $\Theta$ cada $C$ número de actualizaciones</span>. 

¿Por qué? Veamos: 

1) <ins>Secuencia de optimizaciones</ins>. Formalmente, utilizar la red de objetivo como una "versión antigua" de la red de política conduce a una secuencia de problemas de optimización (uno por etapa donde dicha versión antigua se **mantiene constante**). 

2) <ins>Estabilidad</ins>. Esta modificación hace que el algoritmo sea más estable en comparación con el Q-learning online estándar, donde una actualización que aumenta $Q_{\pi}(s,a)$ a menudo también aumenta $Q_{\pi}(s',a')$ para todas las acciones y, por tanto, también aumenta el objetivo, lo que posiblemente dé lugar a oscilaciones o divergencias de la política. Nótese que la red de objetivo se mantiene **temporalmente constante**. 

#### Modelo General 
Teniendo en cuenta todas las consideraciones anteriores, el algoritmo DQN procede de la siguiente manera. Aquí, utilizamos la versión introducida en el artículo de Nature [Human-level control through deep reinforcement learning](https://www.nature.com/articles/nature14236): 

```{prf:algorithm} DQN
:label: DQN

**Entradas**: Episodios $K$, tiempos por episodio $T$, factor de descuento $\gamma$, $\epsilon_{min}$, $\epsilon_{decay}$

**Salida**: $Q_{\pi\ast}$ Deep Q-Learning $\epsilon-$Greedy

1. **Inicializar**. Búfer de repetición ${\cal D}$ con capacidad $N$, función de valor-acción $Q$ con pesos aleatorios $\Theta$, función de valor-acción $\hat{Q}$ con pesos $\Theta^{-}=\Theta$
. 

1. **para** el episodio $i$: 

    1. Inicializar la secuencia $s_1=\{\mathbf{x}_1\}$ y la secuencia pre-procesada $\phi_1=\phi(s_1)$

    2. **para** $t=\{1,\ldots,T\}$

        1. Con probabilidad $\epsilon$, seleccionar una acción aleatoria $a_t$

        2. De lo contrario, seleccionar $a_t = \arg\max_{a}Q(\phi(s_t),a;\Theta)$

        3. Ejecutar $a_t$ en el emulador y observar la recompensa $r_{t+1}$ y la imagen $\mathbf{x}_{t+1}$

        4. Establecer $s_{t+1}=(s_t,a_t,\mathbf{x}_{t+1})$ y pre-procesar $\phi(s_{t+1})$

        5. Almacenar la transición $(\phi_t,a_t,r_{t+1},\phi_{t+1})$ en ${\cal D}$

        6. Muestrear un mini-lote aleatorio de transiciones $(\phi_j,a_j,r_{j+1},\phi_{j+1})$ de ${\cal D}$

        6. Establecer $y_j = \begin{cases}
                            r_{j+1} &\;\text{si el episodio termina en el paso}\; j+1 \\[2ex]
                            r_{j+1} + \gamma\cdot\max_{a'}\hat{Q}(\phi_{j+1},a';\Theta^{-})
                            &\;\text{de lo contrario}\;.\\[2ex]
                        \end{cases}$

        7. Realizar el paso de descenso de gradiente sobre $\left(y_j-Q(\phi_j,a_j\;\Theta)\right)^2$ **con respecto a los parámetros** $\Theta$

        8. Cada $C$ pasos, resetear $\hat{Q}=Q$ (transferir parámetros $\Theta^{-}\leftarrow \Theta$) 

    4. $\epsilon = \max(\epsilon_{min}, \epsilon\cdot \epsilon_{decay})$

    5. $i = i + 1$

**return** $Q_{\pi\ast}$
```

Para monitorizar el rendimiento del entrenamiento de DQN, registramos la media móvil (media de los $50$ episodios anteriores), como mostramos en la {numref}`DQN-Training`


```{figure} ./images/Topic2/DQN-Training.png
---
name: DQN-Training
width: 800px
align: center
height: 400px
---
Papel de la repetición de experiencia en Deep Q-Learning. Generado por Gemini. 
```

Nótese que la media móvil del agente aumenta, a veces disminuye, pero en promedio mejora con el tiempo. Las grandes oscilaciones muestran que todavía hay margen de mejora. 

[//]:https://lilianweng.github.io/posts/2018-02-19-rl-overview/


