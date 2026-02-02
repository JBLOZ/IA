# Aprendizaje por Refuerzo

## Sesión Práctica 2: Aprendizaje por Refuerzo Basado en el Valor

### Introducción

En esta sesión práctica, profundizaremos en el campo del **Aprendizaje por Refuerzo (RL)**, un subcampo del Aprendizaje Automático donde un **agente** aprende a tomar decisiones interactuando con un **entorno**. A diferencia del aprendizaje supervisado, donde el modelo aprende de un conjunto de datos fijo de ejemplos etiquetados, un agente de RL descubre qué acciones producen las mayores recompensas mediante ensayo y error.

El objetivo del agente es aprender una **política** óptima $\pi$ —un mapeo de estados a acciones— que maximice la **recompensa** acumulativa descontada (retorno) a lo largo del tiempo.

### Planteamiento del Problema: El Entorno Taxi-v3

Nos centraremos en el entorno **Taxi-v3**, un problema clásico disponible en la biblioteca [Gymnasium](https://gymnasium.farama.org/environments/toy_text/taxi/) (un fork mantenido de OpenAI Gym).

En este escenario, un taxista debe navegar por una cuadrícula de $5 \times 5$ para recoger a un pasajero en una de cuatro ubicaciones designadas (Rojo, Verde, Amarillo y Azul) y dejarlo en un destino específico. El desafío consiste en aprender el camino más corto evitando maniobras ilegales y minimizando el tiempo.

```{figure} ./images/Practice2/taxi_problem.png
---
name: TaxiRL
height: 600px
width: 590px
align: center
---
Problema de Aprendizaje por Refuerzo Taxi-v3. Imagen generada parcialmente por Gemini.
```

### Formulación del Proceso de Decisión de Markov

Para resolver este problema utilizando RL, primero debemos formalizarlo como un **Proceso de Decisión de Markov (MDP)**. Un MDP se define por la tupla $(S, A, P, R)$:

**Espacio de Estados ($S$)**

El espacio de estados contiene toda la información necesaria para determinar la situación actual del entorno. En Taxi-v3, hay **500 estados discretos**. Un estado se define por la combinación de:

- La posición actual del taxi ($5 \times 5 = 25$ ubicaciones posibles).
- La ubicación del pasajero (4 puntos designados o dentro del taxi: $4 + 1 = 5$ posibilidades).
- La ubicación del destino (4 puntos designados).

Matemáticamente, un estado $s \in S$ se puede representar como:

$$
s = f(\text{fila\_taxi}, \text{col\_taxi}, \text{idx\_pasajero}, \text{idx\_destino})
$$

**Espacio de Acciones ($A$)**

El agente puede realizar una de **6 acciones discretas** en cada paso de tiempo:

- $a = 0$: Moverse al Sur
- $a = 1$: Moverse al Norte
- $a = 2$: Moverse al Este
- $a = 3$: Moverse al Oeste
- $a = 4$: Recoger pasajero
- $a = 5$: Dejar pasajero

**Función de Recompensa ($R$)**

La función de recompensa $R(s, a)$ define el objetivo de la tarea proporcionando retroalimentación numérica:

- **-1** por cada paso para fomentar el camino más corto.
- **+20** por dejar al pasajero con éxito.
- **-10** por acciones ilegales de "recoger" o "dejar".

**Función de Transición ($P$)**

La función de transición $P(s^{\prime} | s, a)$ especifica la probabilidad de moverse al estado $s^{\prime}$ después de realizar la acción $a$ en el estado $s$. Para esta sesión práctica, la dinámica es **determinista** ($P = 1.0$ para el movimiento previsto) en este entorno, siempre que no haya paredes. Si el taxi choca contra una pared, permanece en su estado actual.

### Bucle de Interacción Agente-Entorno

El bucle fundamental de RL involucra al agente observando un estado, eligiendo una acción y recibiendo retroalimentación. Este proceso se puede resumir en el siguiente pseudocódigo:

```{prf:algorithm} Bucle Básico de Interacción de RL
:label: RL-Loop

**Entradas**: Entorno $Env$, Política $\pi$
 
**Estado inicial**: $s_0 \leftarrow Env.reset()$

**Mientras** el episodio no haya terminado:
1. Seleccionar la acción $a_t$ basándose en la política $\pi(s_t)$.    
2. Ejecutar $a_t$ en $Env$.    
3. Observar la recompensa $r_t$ y el nuevo estado $s_{t + 1}$.    
4. (Opcional) Actualizar $\pi$ basándose en $(s_t, a_t, r_t, s_{t + 1})$.    
5. $s_t \leftarrow s_{t + 1}$.
```

### Política ($\pi$)

Para ilustrar la importancia del aprendizaje, podemos comparar los siguientes comportamientos:

**Agente no entrenado**

El siguiente GIF muestra a un agente seleccionando acciones al azar sin ningún entrenamiento previo. Esto se conoce a menudo como un enfoque de "fuerza bruta", donde el agente deambula sin rumbo por el entorno.

```{figure} ./images/Practice2/random_policy.gif
---
name: RandomWalk
align: center
---
Agente Taxi-v3 seleccionando acciones al azar sin ningún entrenamiento previo.
```

**Agente entrenado**

En contraste, este GIF muestra a un agente después de una fase de entrenamiento utilizando Aprendizaje por Refuerzo. El taxi ahora sigue el camino correcto para recoger al pasajero y entregarlo en el destino de manera eficiente.

```{figure} ./images/Practice2/learned_policy.gif
---
name: RLBehavior
align: center
---
Agente Taxi-v3 después de una fase de entrenamiento utilizando Aprendizaje por Refuerzo.
```

## Ejercicio 1: Caminata Aleatoria

### Objetivos

El objetivo de este primer ejercicio es familiarizarse con la API de **Gymnasium** y la dinámica del entorno **Taxi-v3**. Implementarás un bucle de interacción básico donde el agente toma decisiones sin ningún proceso de aprendizaje, basándose puramente en la selección aleatoria (un enfoque de "fuerza bruta"). Esto servirá como línea base para evaluar la necesidad y efectividad de los algoritmos de Aprendizaje por Refuerzo.

### Descripción de la Tarea

Debes implementar un script de Python que ejecute el bucle de interacción entre el agente y el entorno durante **100 episodios consecutivos**. Dado que este es un enfoque sin aprendizaje, estos episodios constituyen la **fase de evaluación** de una política aleatoria.

Para cada episodio, el agente debe:

1.  Reiniciar el entorno a un estado inicial aleatorio.
2.  Seleccionar acciones al azar del espacio de acciones $A$ usando `env.action_space.sample()`.
3.  Ejecutar la acción y transicionar al siguiente estado hasta que el episodio termine (pasajero entregado) o se alcance el límite máximo de 200 pasos de tiempo.

### Métricas de Rendimiento

Para cuantificar la (in)eficiencia de la política aleatoria, debes recopilar las siguientes tres métricas para cada uno de los 100 episodios:

- **Recompensa Acumulada**: La suma de todas las recompensas obtenidas por el agente desde el inicio hasta el final del episodio.
- **Pasos de tiempo por Episodio**: El número total de pasos dados antes de que concluya el episodio.
- **Número de Penalizaciones**: El recuento de veces que el agente recibe una recompensa de **-10** (específicamente por acciones ilegales de "recoger" o "dejar").

Después de completar los 100 episodios, utiliza la biblioteca **Matplotlib** para generar gráficos que muestren la progresión de estas métricas. Debes mostrar los valores para cada episodio y calcular la **media** y la **desviación estándar** para facilitar tu análisis.

### Análisis y Visualización

En tu informe, debes proporcionar un análisis detallado de los resultados. Discute por qué una política puramente aleatoria no logra resolver el problema de Taxi-v3 de manera efectiva, haciendo referencia al alto número de pasos de tiempo y penalizaciones observados.

Para ilustrar tus hallazgos, debes generar un **GIF** de un episodio representativo de tu evaluación. Para ayudarte con esto, utiliza la siguiente función auxiliar para convertir los fotogramas RGB capturados durante el renderizado en un GIF serializado:

```{code-block} python
import moviepy as mp
from IPython.display import Image

def save_gif(frames, filename, fps = 10):
    """
    Crea y serializa un GIF a partir de una lista de fotogramas RGB.

    Argumentos:
        frames (list): Lista de arrays de NumPy que representan fotogramas RGB.
        filename (str): Nombre del archivo a guardar.
        fps (int): Los fotogramas por segundo de la animación.
    """
    clip = mp.ImageSequenceClip(frames, fps = fps)
    clip.write_gif(filename, fps = fps) 
```

```{note}
Para usar esta función, debes asegurarte de estar renderizando el entorno en modo `rgb_array` y almacenando los fotogramas resultantes en una lista durante el bucle del episodio.
```

### Tarea Opcional: Enmascaramiento de Acciones (Action Masking)

Para obtener créditos extra, repite el proceso de evaluación pero incorpora el uso de una **Máscara de Acciones**. El entorno Taxi-v3 de Gymnasium proporciona una máscara que identifica qué acciones son legales en el estado actual (por ejemplo, evitando que el agente elija "recoger" si el pasajero no está presente).

Implementa el bucle aleatorio nuevamente, pero esta vez solo muestreando de las acciones válidas proporcionadas por la máscara. Compara estos resultados con el enfoque aleatorio "ciego" anterior y discute el impacto en las métricas de rendimiento recopiladas.

### Configuración del Entorno

Para comenzar la implementación, asegúrate de tener instaladas las bibliotecas necesarias en tu entorno de Python. Puedes instalarlas usando los siguientes comandos:

```{code-block} bash
pip install "gymnasium[toy-text]" numpy matplotlib moviepy    
```

## Ejercicio 2: SARSA

### Introducción a SARSA

En el ejercicio anterior, observamos las limitaciones de una política aleatoria. Para mejorar el rendimiento del agente, ahora implementaremos **SARSA** (State-Action-Reward-State-Action), un algoritmo fundamental de Aprendizaje por Refuerzo on-policy (basado en la política seguida).

A diferencia del enfoque de "fuerza bruta", SARSA permite al agente aprender una **Función de Valor**, específicamente una tabla $Q$, que estima la calidad de realizar una acción particular en un estado determinado. Como método **on-policy**, SARSA actualiza sus estimaciones basándose en las acciones reales tomadas por la política actual $\pi$, siguiendo la tupla $(s_t, a_t, r_{t + 1}, s_{t + 1}, a_{t + 1})$.

### La Regla de Actualización de SARSA

El núcleo del algoritmo es la actualización de los **valores $Q$**. Para cada transición, el agente actualiza su conocimiento según la siguiente expresión matemática:

$$
Q(s_t, a_t) \leftarrow Q(s_t, a_t) + \alpha [r_{t + 1} + \gamma Q(s_{t + 1}, a_{t + 1}) - Q(s_t, a_t)]
$$

Donde los componentes se definen de la siguiente manera:

- $Q(s_t, a_t)$: La estimación actual del valor de la acción $a_t$ en el estado $s_t$.
- $\alpha$ (**Tasa de Aprendizaje**): Determina en qué medida la información recién adquirida anula la información antigua ($0 < \alpha \leq 1$).
- $r_{t + 1}$: La recompensa inmediata recibida después de ejecutar la acción $a_t$.
- $\gamma$ (**Factor de Descuento**): Cuantifica la importancia de las recompensas futuras ($0 \leq \gamma \leq 1$). Un valor cercano a 1 enfatiza el éxito a largo plazo.
- $Q(s_{t + 1}, a_{t + 1})$: El valor estimado de la acción $a_{t + 1}$ realmente elegida en el siguiente estado $s_{t + 1}$ según la política actual.
- $[r_{t + 1} + \gamma Q(s_{t + 1}, a_{t + 1}) - Q(s_t, a_t)]$: Este término se conoce como el **Error TD** (Error de Diferencia Temporal).

### Exploración vs. Explotación

Un desafío crítico en RL es el equilibrio entre la **exploración** (probar nuevas acciones) y la **explotación** (utilizar la información conocida). Para abordar esto, debes implementar una **estrategia $\epsilon$-greedy** para seleccionar acciones:

- Con probabilidad $\epsilon$ (**Tasa de Exploración**), el agente selecciona una acción al azar.
- Con probabilidad $1 - \epsilon$, el agente selecciona la acción con el valor $Q$ más alto para el estado actual.

### Tareas de Implementación

Debes implementar las siguientes dos fases distintas:

**Fase A: Entrenamiento**

Implementa el bucle de entrenamiento SARSA para el entorno **Taxi-v3**. Durante esta fase, el agente poblará y actualizará la tabla $Q$. Eres responsable de:

1.  Inicializar una tabla $Q$ de tamaño $500 \times 6$.
2.  Establecer valores apropiados para los hiperparámetros ($\alpha$, $\gamma$ y $\epsilon$).
3.  Ejecutar el bucle de entrenamiento durante un número suficiente de episodios hasta que la política converja.
4.  Generar gráficos de Matplotlib para la **Recompensa Acumulada**, los **Pasos de tiempo** y las **Penalizaciones**.
5.  Calcular la **media** y la **desviación estándar** para las tres métricas.

**Fase B: Evaluación**

Una vez que el entrenamiento se haya completado, evalúa la política aprendida durante **100 episodios**. En esta fase, el agente debe actuar de manera codiciosa (greedy) (utilizando la tabla $Q$ aprendida para elegir la mejor acción) para demostrar la efectividad del entrenamiento.

### Análisis y Visualización

Utilizando los datos recopilados durante los 100 episodios de evaluación, proporciona lo siguiente:

- **Gráficos de Rendimiento**: Genera gráficos de Matplotlib para la **Recompensa Acumulada**, los **Pasos de tiempo** y las **Penalizaciones**.
- **Demostración Visual**: Crea un **GIF** que muestre al agente navegando con éxito por el entorno y entregando al pasajero.
- **Discusión**: Analiza los resultados y discute la elección de tus hiperparámetros. Debes justificar por qué tus valores específicos para $\alpha$, $\gamma$ y $\epsilon$ produjeron una política efectiva y cómo influyeron en el proceso de aprendizaje.

Compara estos resultados con el agente aleatorio del Ejercicio 1. ¿Cómo cambia el "comportamiento" del taxi gracias a la "inteligencia" proporcionada por SARSA?

## Ejercicio 3: Q-Learning

### Introducción a Q-Learning

Basándonos en el ejercicio anterior, ahora implementaremos **Q-Learning**. Mientras que SARSA es un método on-policy, Q-Learning es un algoritmo **off-policy** (independiente de la política) muy popular. La diferencia fundamental reside en cómo el agente desarrolla sus estimaciones de valor: mientras que SARSA utiliza la acción realmente seleccionada por la política actual para el siguiente estado, Q-Learning actualiza sus estimaciones utilizando el **valor máximo posible** del siguiente estado, independientemente de la acción que se tome realmente.

### La Regla de Actualización de Q-Learning

El agente aprende un mapeo de estados a acciones óptimas actualizando iterativamente la **tabla $Q$**. La formulación matemática para la regla de actualización en Q-Learning es la siguiente:

$$
Q(s_t, a_t) \leftarrow Q(s_t, a_t) + \alpha [r_{t + 1} + \gamma \max_{a} Q(s_{t + 1}, a) - Q(s_t, a_t)]
$$

En esta ecuación:

- $Q(s_t, a_t)$: El valor actual para el par estado-acción.
- $\alpha$ (**Tasa de Aprendizaje**): Controla la magnitud de la actualización ($0 < \alpha \leq 1$).
- $r_{t + 1}$: La recompensa obtenida después de realizar la acción $a_t$.
- $\gamma$ (**Factor de Descuento**): Determina el peso de las recompensas futuras ($0 \leq \gamma \leq 1$).
- $\max_{a} Q(s_{t + 1}, a)$: El valor máximo estimado para el siguiente estado $s_{t + 1}$ sobre todas las acciones posibles $a$. Este término representa el "optimismo" del agente sobre el futuro, independientemente de su política de exploración.
- $[r_{t + 1} + \gamma \max_{a} Q(s_{t + 1}, a) - Q(s_t, a_t)]$: Este término se conoce como el **Error TD** (Error de Diferencia Temporal).

### Tareas de Implementación

Debes implementar el bucle de interacción para el entorno **Taxi-v3** utilizando los mismos tres hiperparámetros que en el Ejercicio 2:

1.  $\alpha$.
2.  $\gamma$.
3.  $\epsilon$ (**Tasa de Exploración**) para la **estrategia $\epsilon$-greedy** utilizada durante el entrenamiento.

**Fase A: Entrenamiento**

Desarrolla el bucle de entrenamiento para poblar la tabla $Q$ a lo largo de varios miles de episodios. Durante esta fase, el agente debe equilibrar la exploración y la explotación utilizando el enfoque $\epsilon$-greedy.

**Fase B: Evaluación**

Después del entrenamiento, ejecuta la fase de evaluación durante **100 episodios consecutivos**. En esta fase, el agente debe actuar de forma puramente **codiciosa (greedy)** seleccionando la acción con el valor $Q$ más alto para cada estado.

### Análisis y Visualización

Para ambas fases, debes registrar y graficar las mismas tres métricas:

- **Recompensa Acumulada** por episodio.
- **Pasos de tiempo** por episodio.
- **Penalizaciones** (recogidas/entregas ilegales) por episodio.

Además, para la fase de evaluación, crea un **GIF** de un episodio exitoso para visualizar la política aprendida.

**Discusión Comparativa**

Una parte crítica de este ejercicio es el **análisis comparativo** entre las soluciones de SARSA (on-policy) y Q-Learning (off-policy). Debes:

- Comparar la velocidad de convergencia y la estabilidad final de las políticas.
- Analizar el impacto de los hiperparámetros en ambos algoritmos.
- Discutir las posibles diferencias de comportamiento entre un agente que aprende basándose en su camino real (**SARSA**) versus un agente que aprende basándose en el máximo teórico (**Q-Learning**).

## Ejercicio 4: Deep Q-Network

### Aprendizaje por Refuerzo Profundo (Deep RL)

En los ejercicios anteriores, resolvimos con éxito el entorno **Taxi-v3** utilizando una tabla $Q$. Sin embargo, los métodos tabulares se vuelven computacionalmente inviables a medida que el espacio de estados crece. En este último ejercicio, pasaremos al **Aprendizaje por Refuerzo Profundo (DRL)** reemplazando la tabla $Q$ estática con una **Red Neuronal**.

Para implementar esto, utilizaremos [PyTorch](https://pytorch.org), un marco líder de Aprendizaje Automático de código abierto que proporciona las herramientas necesarias para construir y entrenar arquitecturas neuronales complejas. Podemos instalar este marco de Deep Learning usando:

```{code-block} bash
pip install torch    
```

### La Arquitectura de la Q-Network

A diferencia de la tabla $Q$, la Red Neuronal tomará el estado actual como entrada y devolverá los valores $Q$ estimados para todas las acciones posibles. A continuación se muestra la implementación en Python para nuestro **agente DQN**:

```{code-block} python
import torch
import torch.nn as nn

class DQN(nn.Module):
    
    def __init__(self, n_states, n_actions):
        super(DQN, self).__init__()
        # Capa de incrustación (Embedding) para manejar estados discretos
        self.embedding_layer = nn.Embedding(n_states, 10)
        # Capas totalmente conectadas (fully connected)
        self.fc_layer1 = nn.Linear(10, 50)
        self.fc_layer2 = nn.Linear(50, 50)
        # Capa de salida
        self.fc_layer3 = nn.Linear(50, n_actions)

    def forward(self, x):
        # x es el estado de entrada
        x = self.embedding_layer(x)
        x = torch.relu(self.fc_layer1(x))
        x = torch.relu(self.fc_layer2(x))
        return self.fc_layer3(x)
```

**Explicación de las Capas**

- **Capa de Incrustación (Embedding Layer)**: Dado que nuestro estado es un único entero discreto (0-499), esta capa lo mapea a un vector denso de tamaño 10, lo que permite a la red aprender relaciones significativas entre los estados.
- **Capas Totalmente Conectadas (Fully Connected Layers)**: Estas capas ocultas (con 50 neuronas cada una) realizan transformaciones no lineales utilizando la función de activación ReLU para extraer características de la representación del estado.
- **Capa de Salida (Output Layer)**: Esta capa final mapea la información procesada a las 6 acciones posibles, representando el valor $Q$ para cada acción en el estado dado.

### El Algoritmo DQN con Experience Replay

Para estabilizar el entrenamiento de las redes neuronales en RL, implementarás una versión sofisticada de DQN que incluye **Experience Replay** (Repetición de Experiencia) y una **Red de Destino** (Target Network), como se describe en el siguiente pseudocódigo:

```{prf:algorithm} Fase de Entrenamiento de DQN con Experience Replay y Target Network  
:label: DQN-Loop

**Entradas**: Frecuencia de actualización de la Red de Destino $C$

**Inicializar**: Memoria de Repetición $D$, Red de Política $Q_{\theta}$, Red de Destino $Q_{\theta^-}$

**Para** cada episodio:

1. Reiniciar el entorno al estado $s$.

2. **Mientras** el episodio no haya terminado:

    1.  Seleccionar la acción $a_t$ usando una estrategia $\epsilon$-greedy basada en $Q_{\theta}(s_t)$.
    2.  Ejecutar $a_t$ y observar la recompensa $r_t$ y el siguiente estado $s_{t + 1}$.
    3.  Almacenar la transición $(s_t, a_t, r_t, s_{t + 1})$ en $D$.
    4.  Muestrear un mini-lote aleatorio de $D$.
    5.  Calcular el Objetivo TD para el mini-lote usando $Q_{\theta^-}$.
    6.  Actualizar $Q_{\theta}$ minimizando la pérdida calculada.
    7.  Actualizar la Red de Destino: cada $C$ pasos, establecer $\theta^- \leftarrow \theta$.
    8.  $s_t \leftarrow s_{t + 1}$.
```

### Tareas de Implementación

Debes completar dos fases:

**Fase A: Entrenamiento**

Implementa el bucle anterior. Además de los hiperparámetros estándar (**$\alpha$**, **$\gamma$**, **$\epsilon$**), debes ajustar el **Tamaño del Lote (Batch Size)**, el **Tamaño de la Memoria de Repetición** y la **Frecuencia de Actualización de la Red de Destino**.

**Fase B: Evaluación**

Prueba tu red entrenada durante **100 episodios** utilizando una política codiciosa (greedy).

### Análisis y Visualización

- Pérdida y Optimizador: Debes seleccionar una **Función de Pérdida** y un **Optimizador** adecuados de la biblioteca PyTorch para entrenar la Q-Network.

- Informe Comparativo: Compara tus **resultados de DQN** con los agentes SARSA y Q-Learning de los ejercicios anteriores. Discute por qué el enfoque profundo podría ser más estable o complejo de ajustar.

- Visualizaciones: Proporciona **gráficos de rendimiento** y un **GIF** de una entrega exitosa del taxi.

### Tarea Opcional: Decaimiento de Parámetros

Para obtener puntos extra, implementa una estrategia de decaimiento para la **tasa de aprendizaje** ($\alpha$), el **factor de descuento** ($\gamma$) o la **tasa de exploración** ($\epsilon$). Justifica cómo la disminución de estos valores con el tiempo mejora la estabilidad y el rendimiento de tu agente.
