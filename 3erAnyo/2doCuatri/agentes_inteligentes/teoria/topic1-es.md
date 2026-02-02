## Redes Neuronales de Grafos
### ¿Por qué GNNs?
Comencemos definiendo nuestros vectores multidimensionales $\mathbf{x}\in\mathbb{R}^d$ para $\text{Train}$ (Entrenamiento) y $\text{Test}$ (Prueba). Entonces, en nuestro entorno vectorial **habitual**, el objetivo de una Red Neuronal, por ejemplo un Perceptrón Multicapa (MLP), es aprender un **espacio latente** donde las proyecciones $\mathbf{h}\in\mathbb{R}^{d'}$ (con $d'\ll d$) de las entradas $\mathbf{x}$ minimicen una función de pérdida dada, como la entropía cruzada con respecto a $\text{Train}$. Esto se expresa normalmente de la siguiente manera:

$$
\mathbf{h} = \text{MLP}_{\Theta}(\mathbf{x}_{\text{Test}})\;,\text{donde}\;\; \Theta =\arg\min_{\Omega} \text{CE}(\mathbf{x}_{\text{Train}})\;,
$$

donde $\Omega$ es el espacio de parámetros donde "viven" las incógnitas $\Theta$ del aprendiz.

En virtud de la composición funcional, un MLP es simplemente el apilamiento de muchas funciones no lineales llamadas **capas** $\text{L}^{l}$, con $l\ge 1$. Usando recursividad, tenemos:

$$
\text{L}^{(l)}=
\begin{cases}
     \sigma^{(l)}(\mathbf{W}^{(l)}\mathbf{h}^{(l-1)} + \mathbf{b}^{(l)}) &\;\text{si}\;  l> 1 \\[2ex]
     \sigma^{(1)}(\mathbf{W}^{(1)}\mathbf{x} + \mathbf{b}^{(1)})
     &\;\text{de lo contrario}\\[2ex]
\end{cases}
$$

La definición anterior es *ambigua a propósito*. ¿Por qué?

- En primer lugar, la **incrustación (embedding)** $\mathbf{h}^{(l)}$ resultante de **la función** $\text{L}^{(l)}$ viene dada por la composición:

$$
\mathbf{h}^{(l)}=\text{L}^{(l)}\circ \text{L}^{(l-1)}\;.
$$

- Sin embargo, en lugar de usar una anotación funcional para $\text{L}^{(l-1)}$, usamos la incrustación resultante $\mathbf{h}^{(l-1)}$ de esa capa. Nótese que el caso base de la recursión es $\mathbf{h}^{(0)}=\mathbf{x}$, que corresponde a $\text{L}^{(1)}$.

Por lo tanto, si el MLP tiene $L$ capas, podemos considerarlo como la siguiente función:

$$
\text{MLP}(\mathbf{x})=\text{L}^{(L-1)}\circ \text{L}^{(L-2)}\circ\ldots\circ \text{L}^{(1)}\;.
$$

En términos de resultados, $\mathbf{h}=\mathbf{h}^{(L)}$ resulta de la siguiente cadena de procesamiento:

$$
\mathbf{h}\xleftarrow{\Theta^{(L)}} \mathbf{h}^{(L-1)}\xleftarrow{\Theta^{(L-1)}}\mathbf{h}^{(L-2)}\xleftarrow{\Theta^{(L-2)}} \ldots\xleftarrow{\Theta^{(1)}}\mathbf{h}^{(0)}\;.
$$

donde $\Theta^{(l)}=(\mathbf{W}^{(l)},\mathbf{h}^{(l)},\sigma^{(l)})$ son los parámetros (pesos, sesgos y activaciones no lineales) que caracterizan cada capa. Realmente,

$$
\Omega = \Theta^{(L)}\times \Theta^{(L-1)}\times\ldots\times \Theta^{(1)}
$$

¡es normalmente un espacio (de parámetros) enorme!

**El aprendizaje como búsqueda**. Como resultado, el aprendizaje a través de MLPs (o NNs en general) puede verse como la búsqueda de los parámetros $\Theta\in\Omega$ de una *función compuesta* $\text{MLP}_{\Theta}$ que mejor mapee las entradas $\mathbf{x}$ con las salidas $\mathbf{h}$.

#### El contexto lo es todo
Las NNs evolucionadas, como los [Transformers](https://huggingface.co/docs/transformers/en/index), el núcleo del estado del arte de los LLMs y otros agentes de IA, aprovechan el concepto de **contexto**. En resumen, las entradas $\mathbf{x}$ no aparecen aisladas sino en **flujos (streams)** (esto es válido tanto para palabras en textos como para parches en imágenes).

Por lo tanto, cuando una entrada $\mathbf{x}_k$ se ve como parte de un flujo:

$$
\ldots\;\underbrace{\mathbf{x}_{k-\frac{h}{2}}\;\mathbf\;{x}_{k-\frac{h}{2}+1}\;\ldots\;\mathbf{x}_{k-1}}_{\text{contexto izquierdo}}\mathbf{x}_k\;\underbrace{\mathbf{x}_{k+1}\;\ldots\;\mathbf{x}_{k+h-1}\mathbf{x}_{k+\frac{h}{2}}}_{\text{contexto derecho}}\;\ldots
$$

su **contexto** viene dado por las entradas anteriores (contexto izquierdo) y las posteriores (contexto derecho) en el flujo. En general, este contexto es *finito hasta los recursos de memoria* y su tamaño viene dado por $h$. Por ejemplo, para $h=4$ deberíamos tener:

$$
\ldots\;\underbrace{\mathbf{x}_{k-2}\;\mathbf\;{x}_{k-1}}_{\text{contexto izquierdo}}\mathbf{x}_k\;\underbrace{\mathbf{x}_{k+1}\;\mathbf{x}_{k+2}}_{\text{contexto derecho}}\;\ldots
$$

##### ¿Cómo consideramos el contexto durante el entrenamiento?
En los Transformers, el mecanismo impulsor es la [Autoatención (Self Attention)](https://arxiv.org/abs/1706.03762). Vamos a desglosarlo a través de un ejemplo.

Consideremos, por ejemplo, el siguiente flujo de entrada:

$$
\mathbf{H} = 
\underbrace{\text{"El}}_{\mathbf{h}_1}\;
\underbrace{\text{animal}}_{\mathbf{h}_2}\;  
\underbrace{\text{no}}_{\mathbf{h}_3}\;
\underbrace{\text{cruzó}}_{\mathbf{h}_4}\;
\underbrace{\text{la}}_{\mathbf{h}_5}\;    
\underbrace{\text{calle}}_{\mathbf{h}_6}\; 
\underbrace{\text{porque}}_{\mathbf{h}_7}\; 
\underbrace{\textbf{estaba}}_{\mathbf{h}_8}\;  
\underbrace{\text{demasiado}}_{\mathbf{h}_9}\; 
\underbrace{\text{cansado."}}_{\mathbf{h}_{10}}\; 
$$

Este flujo de entrada se considera una **matriz** $N\times d_{model}$ $\mathbf{H}$ donde cada fila es la **incrustación numérica** de un término/palabra $\mathbf{h}_1, \mathbf{h}_2, \ldots,$, codificando cada una numéricamente la semántica básica de cada palabra ("El", "animal", etc.). Todas las incrustaciones tienen dimensión $d_{model}$.

Todas las incrustaciones son aprendibles y pueden desempeñar tres roles diferentes:

- **Consulta / Query (Q)**: El vector Consulta para una palabra determina qué información está buscando de otras palabras en la secuencia. Es el "selector" o "interrogador".

- **Clave / Key (K)**: El vector Clave para una palabra determina qué tan relevante es para las consultas de otras palabras. Es contra lo que se comparan los vectores Consulta.

- **Valor / Value (V)**: El vector Valor para una palabra contiene la información que se pasará a otras palabras, ponderada por sus puntuaciones de atención. Es el contenido real que se comunica.

Al crear estos vectores separados, el mecanismo de autoatención puede aprender a **capturar diferentes aspectos del significado de la palabra y su relación con otras palabras**. La interacción entre Consultas y Claves determina los pesos de atención, que a su vez dictan cuánto contribuye cada vector Valor a la representación de salida final de una palabra. Esto permite al modelo ponderar dinámicamente la importancia de diferentes palabras en la secuencia de entrada al procesar una palabra específica.

Las claves, consultas y valores se toman de *diccionarios*. Por ejemplo, consultamos un diccionario por "estaba" y cuando la consulta coincide con una entrada clave en el diccionario, recuperamos un valor (descripción).

Entonces, dada una incrustación inicial, digamos $\mathbf{h}_{\omega}$, por ejemplo $\omega=\text{"it"}$ (en el ejemplo original en inglés), obtenemos su "sabor" como Clave, Consulta y Valor mediante proyección lineal:

$$
\mathbf{K}_{\omega}=\mathbf{W}_K\mathbf{h}_{\omega},\;\;
\mathbf{Q}_{\omega}=\mathbf{W}_Q\mathbf{h}_{\omega},\;\;\text{y}\;\;
\mathbf{V}_{\omega}=\mathbf{W}_V\mathbf{h}_{\omega}\;.
$$

donde $\mathbf{W}_K$, $\mathbf{W}_Q$ y $\mathbf{W}_V$ son **matrices aprendibles** de tamaño respectivo $d_{model}\times d_k$, $d_{model}\times d_q$ y $d_{model}\times d_v$. En realidad, estas matrices funcionan como MLPs separados.

**NOTA**: dado que *las Claves y las Consultas deberían coincidir idealmente*, normalmente se asume que $d_k=d_q$. Sin embargo, $d_v$ puede ser diferente de $d_k$ y $d_q$. Esto se hace, por ejemplo, para acomodar una semántica más rica como sucede en los diccionarios reales. También es típico hacer $d_v$ más pequeño por razones de eficiencia.
<br></br>
<span style="color:#2f6004">
**¿Cómo sabemos que "estaba" (o "it") se refiere al "animal" en este caso?**.
</span>
<br></br>
Bueno, el mecanismo básico para construir el resultado del Transformer con respecto a una consulta dada (por ejemplo, "estaba") es el siguiente:

**No normalizado**. Dada la Consulta $\mathbf{Q}_{\omega=\text{"estaba"}}$, deberíamos dar cuenta del nivel de correlación entre esta y cada una de las Claves. En matemáticas, la correlación entre dos vectores $\mathbf{u}$ y $\mathbf{v}$ se realiza normalmente a través del producto escalar $\langle \mathbf{u}, \mathbf{v}\rangle := \mathbf{u}\mathbf{v}^T$ (proyección del primero sobre el segundo):

$$
\mathbf{Q}_{\omega=\text{"estaba"}}\mathbf{K}^T_{\omega'}\;\;\text{con}\;\;\omega'\in \{\text{"El"},\text{"animal"},\ldots,\text{"cansado."}\}\;.
$$

Cada uno de los productos anteriores *resulta en un valor escalar*, digamos $S_{(\omega=\text{"estaba"},\omega')}$. Entonces, desde el punto de vista de la Consulta "estaba", tenemos una secuencia de correlaciones:

$$
S_{(\omega=\text{"estaba"},\omega'=\text{"El"})}\;,
S_{(\omega=\text{"estaba"},\omega'=\text{"animal"})}\;,\ldots,\;
S_{(\omega=\text{"estaba"},\omega'=\text{"cansado."})}\;.
$$

Dado que cada uno de estos valores puede ser positivo o negativo, transformamos la secuencia anterior en una [distribución de probabilidad](https://medium.com/@touhid3.1416/the-surprisingly-simple-math-behind-transformer-attention-mechanism-d354fbb4fef6) mediante la función softmax.

Recuerda que $\text{Softmax}(\mathbf{x}_i):=\mathbf{\exp(\mathbf{x}_i)/\sum_{i'} \exp(\mathbf{x}_{i'})}$ opera sobre un vector/secuencia $\mathbf{x}$ y el resultado está altamente sesgado hacia los valores máximos de $\mathbf{x}$, donde asigna un $1$, y los más pequeños, donde asigna un $0$. Los autores de [Attention is all You Need](https://arxiv.org/pdf/1706.03762) señalaron que, cuando el producto escalar es grande en magnitud, el softmax es empujado a regiones donde el gradiente es pequeño, dificultando así el aprendizaje. Por eso los productos escalares se escalan por $\frac{1}{\sqrt{d_k}}$.

En resumen, aplicar softmax a cada fila y apilar las filas conduce a crear la siguiente matriz $N\times N$:

$$
\mathbf{S}:=\text{Softmax}\left(\frac{\mathbf{Q}\mathbf{K}^T}{\sqrt{d_k}}\right)\;,
$$

donde $\sum_{\omega'} S_{\omega,\omega'}=1\;\forall\omega$ (cada fila suma $1$).

**Los valores**. En paralelo al cálculo de los coeficientes softmax, ya hemos proyectado la *semántica real* de cada término, que está contenida en los **valores** $\mathbf{V}_{\omega'}$ de los términos respectivos.

Entonces, la nueva incrustación de valores (por ejemplo, para $\mathbf{V}_{\omega}$) resulta de la suma ponderada:

$$
\mathbf{h}_{\omega} := \sum_{\omega'}S_{(\omega,\omega')}\mathbf{V}_{\omega'}\;.
$$

Entonces, $\mathbf{h}_{\omega}$ es una forma sencilla de expresar la **semántica contextual** de $\mathbf{V}_{\omega}$. Si $\omega=\text{"estaba"}$, entonces $\mathbf{h}_{\omega}$ combinará todos los valores proporcionalmente a cómo "estaba" **atiende** (o coincide con) cada una de las Claves.

Más compactamente, la notación:

$$
\text{Attention}(\mathbf{Q},\mathbf{K},\mathbf{V}) :=
\text{Softmax}\left(\frac{\mathbf{Q}\mathbf{K}^T}{\sqrt{d_k}}\right)\mathbf{V}\;,
$$

devuelve una matriz de atención.

Este proceso se resume en la {numref}`Attention`.

```{figure} ./images/Topic1/AttentionScheme.png
---
name: Attention
width: 600px
align: center
height: 500px
---
Contexto completo para el significado de "it" (o "estaba"). Imagen generada parcialmente por Gemini. 
```

**Sobre el aprendizaje de las Claves, Consultas y Valores de entrada**. Aquí, es importante notar que la incrustación para la palabra "animal", por ejemplo, es *única* y aprendible. Es por eso que proyectamos esta incrustación en $\mathbf{W}_K$, $\mathbf{W}_Q$ y $\mathbf{W}_V$ para obtener el "sabor" de la "misma palabra" como Clave, Consulta o Valor, cuando sea necesario.

##### Los Transformers como grafos 

Mirando $\mathbf{S}:=\text{Softmax}\left(\frac{\mathbf{K}\mathbf{Q}^T}{\sqrt{d_k}}\right)$ podemos ver a $\mathbf{S}$ como un *grafo atribuido* donde $\mathbf{S}\in\mathbb{R}^{M\times M}$ es una *matriz de adyacencia atribuida* y $\mathbf{S}_{(\omega,\omega')}\in [0,1]$ es el peso de atención correspondiente de $\mathbf{Q}_{\omega}$ con respecto a $\mathbf{K}_{\omega'}$.

Echemos ahora un vistazo global a $\mathbf{S}$ (ver {numref}`AttentionGE`):

```{figure} ./images/Topic1/AttentionGraphE.png
---
name: AttentionGE
width: 800px
align: center
height: 250px
---
La atención como un grafo atribuido. Imagen generada parcialmente por Gemini. 
```
Nótese que los nodos tienen **bucles (self-loops)** correspondientes a autoatenciones (elementos de la diagonal $\mathbf{S}_{(\omega,\omega)}$) porque resultan ser relevantes para ellos mismos. Sin embargo, no todos son igualmente relevantes.

En particular, la palabra "animal" se atiende principalmente a sí misma, mientras que "estaba" (o "it") atiende también a "animal" (obviamente) y a "cansado" (porque es una propiedad del animal). Los términos restantes tienen autoatenciones muy bajas (por debajo de $0.01$ no aparecen en la figura).

**NOTA**: Este grafo cambia dinámicamente, así como las incrustaciones y los pesos de las matrices Consulta, Clave y Valor.

**Actualización como Paso de Mensajes**. Finalmente, la actualización:

$$
\mathbf{h}_{\omega} := \sum_{\omega'}S_{(\omega,\omega')}\mathbf{V}_{\omega'}\;.
$$

puede verse como si todos los nodos $\omega'$ del grafo enviaran un mensaje $\mathbf{V}_{\omega'}$ al nodo $\omega$, donde este mensaje es modulado por $S_{(\omega,\omega')}$. ¡Como resultado, el nodo $\omega$ actualiza su estado!

En la {numref}`AttentionGE`, $\mathbf{h}_{\omega=\text{"it"}}$ se mide principalmente por el valor actual de "animal" así como por el valor existente de "it" (autoatención).

##### Enmascaramiento y secuencialidad 

A pesar de que la visualización anterior del grafo de atención es explicativa, *no se utiliza durante el pase hacia adelante real o el entrenamiento de un modelo Transformer*.

El **Enmascaramiento de Atención** (ver máscara opcional en {numref}`Attention`) se utiliza para evitar que ciertos términos/tokens atiendan a otros tokens. El tipo más común de enmascaramiento relevante para el procesamiento secuencial es el **enmascaramiento de mirada hacia adelante (look-ahead masking)** (también conocido como enmascaramiento causal), que se utiliza típicamente en el decodificador de un Transformer. En el enmascaramiento de mirada hacia adelante, las puntuaciones de atención para los tokens futuros se establecen en un valor muy bajo (efectivamente cero después de la función softmax) de modo que un token solo puede atender a los tokens que vienen antes de él en la secuencia. *Esto es esencial para tareas como la generación de lenguaje donde el modelo no debe tener acceso a información futura*.

Hemos reconstruido este grafo para atender solo a los tokens pasados en la {numref}`AttentionSeq`.

```{figure} ./images/Topic1/SequentialAttention.png
---
name: AttentionSeq
width: 600px
align: center
height: 500px
---
Atención secuencial. Imagen generada parcialmente por Gemini. 
```

Ahora, la autoatención aumenta (atender al presente, así como al pasado, pero no al futuro). En otras palabras, ¡$\mathbf{S}$ es cero por encima de la diagonal! Es decir:

$$
\mathbf{h}_{\omega} := \sum_{\omega'\le\omega}S_{(\omega,\omega')}\mathbf{V}_{\omega'}\;.
$$

Dado que estos Transformers **que imponen decodificadores** utilizan el pasado y el presente para predecir (generar) el futuro, normalmente se les llama **máquinas de siguiente token**.

Este es el entorno habitual para los LLMs (Transformers basados en lenguaje) y **limita la expresividad** del Transformer (como veremos más adelante). Sin embargo, en los Modelos de Lenguaje Visual o VLMs (Transformers de Visión o ViT), se aplica la atención libre. Ahí, los tokens son parches de imagen "secuencializados" y es lógico que un parche pueda atender a cualquier otro parche.

### El poder de la agregación
El **Paso de Mensajes** es implícito en ciertos tipos de Transformers. Este es uno de los ingredientes que hacen que los Transformers sean tan poderosos.

Como hemos visto, el Paso de Mensajes (MP) proporciona una combinación flexible de la salida de tres MLPs (Consultas, Claves y Valores) que se ejecutan en paralelo para las mismas entradas.

Sin embargo, los Transformers suelen **procesar secuencias** (NLP) o transformar objetos (ViT) en secuencias para su posterior procesamiento. Pero **¿qué pasa si los objetos a procesar no son secuencias, sino grafos o redes?**

Este último punto es importante, ya que **los grafos no son estructuras ordenadas**. De hecho, <span style="color:#2f6004">el poder expresivo de los grafos reside en el hecho de que son **invariantes a cualquier orden**</span>.

#### Nubes de Puntos e Invariancia 
Además de los Transformers, que pueden verse como grafos (grafos de atención), existe un problema donde la <span style="color:#2f6004">**invariancia ante permutaciones**</span> se vuelve clave: este problema es el **reconocimiento y la segmentación de nubes de puntos** (ver {numref}`PointCloud`). A continuación, vemos cómo las arquitecturas MLP tradicionales deben introducir operadores invariantes para resolverlo, y esto conduce a una formulación natural basada en grafos.

```{figure} ./images/Topic1/PointCloud.png
---
name: PointCloud
width: 700px
align: center
height: 350px
---
Reconocimiento y segmentación de nubes de puntos. [Crédito](https://github.com/charlesq34/pointnet). 
```

##### Invariancia ante Permutaciones
Un MLP implementa la invariancia ante permutaciones si sucede esto:

$$
\text{MLP}_{\Theta}({\cal S}) = \text{MLP}_{\Theta}(\Pi({\cal S}))\;,
$$

donde ${\cal S}=\{\mathbf{x}_1,\mathbf{x}_2,\ldots,\mathbf{x}_N\}$ es un conjunto de $N$ puntos en $\mathbb{R}^d$ (donde $d=3$ en nubes de puntos 3D) y $\Pi:\{1,2,\ldots N\}\rightarrow \{1,2,\ldots N\}$ es una función que permuta el orden de los puntos en ${\cal S}$:

$$
\Pi({\cal S})=\{\mathbf{x}_{\Pi(1)},\mathbf{x}_{\Pi(2)},\ldots,\mathbf{x}_{\Pi(N)}\}\;.
$$

Por ejemplo, en $\Pi(\{1,2,3,\ldots N\})=\{2,1,3,\ldots N\}$, $\Pi$ solo permuta los dos primeros elementos.

Obviamente, hay $N!$ permutaciones posibles y el MLP tiene que dar la misma salida. En otras palabras, si el conjunto ${\cal S_{avion}}$ debe ser clasificado como un avión, entonces $\Pi({\cal S_{avion}})$ también debe ser clasificado como un avión por el mismo MLP.

La solución se representa en la {numref}`PointNet`. La NN PointNet es un desarrollo innovador. Aparentemente es otro (enorme) MLP pero tenemos algunas observaciones:

```{figure} ./images/Topic1/PointNet.png
---
name: PointNet
width: 700px
align: center
height: 300px
---
PointNet para reconocimiento y segmentación. [Crédito](https://github.com/charlesq34/pointnet). 
```

1) **Entrada**. Es un tensor de $N\times 3$ (pila de $N$ puntos 3D $(x,y,z)$). Nótese que si tenemos modelos 3D, todos ellos se discretizan a la misma resolución ($N$ es una constante). Además, si dos modelos corresponden a la misma categoría (por ejemplo, aviones) **no están pre-alineados**, es decir, uno se ve como una permutación del otro.
2) **1er T-Net**. T-Net es una NN con dos objetivos: (1) Aprender una transformación común de $3\times 3$ (alineación) con todas las nubes de puntos de entrenamiento, y (2) aplicarla a la entrada $N\times 3$.
3) **1er MLP**. Transforma la salida $N\times 3$ de la primera T-Net en un $N\times 64$. Esto es básicamente necesario para añadir algo de contexto a los puntos $(x,y,z)$: con $64$ dimensiones totales es posible discriminar entre puntos de esquina y puntos de superficie, etc.
4) **2da T-Net**. Versión a escala de la 1ra, ahora con una nube de puntos de $N\times 64$.
5) **2do MLP**. Versión a escala del 1er MLP, pasando ahora de $64$ a $1024$ dimensiones.
6) **Max Pooling**. Esta es la <span style="color:#2f6004">**parte invariante de PointNet**</span>. Dado el tensor de tamaño $N\times 1024$ cuyas filas corresponden a características extendidas de los puntos $(x,y,z)$, ahora colapsa en un tensor único de $1\times 1024$ tomando el $\max$ en cada dimensión. Esta simple operación hace que tensores de entrada idénticos pero correspondientes a la "misma permutación" resulten en un hash de $1\times 1024$ similar.
7) Una vez que tenemos el hash global podemos alimentar a un **MLP final** o enviarlo a alimentar la red de segmentación con también un MLP final.

La solución se representa en la {numref}`PointNet++`. La NN PointNet++ mejora PointNet de la siguiente manera:

```{figure} ./images/Topic1/PointNet++.png
---
name: PointNet++
width: 700px
align: center
height: 400px
---
PointNet++. Izquierda: transformación del modelo 3D de una mesa en una nube de puntos y luego en un grafo KNN. Derecha: arquitectura PointNet enriquecida donde el agrupamiento (pooling) se realiza de acuerdo con los puntos vecinos en el grafo. [Crédito](https://arxiv.org/pdf/2311.02608) y Pytorch Geometric. 
```

1) **Grafo KNN**. La entrada a la NN no es un tensor sino un grafo donde dos puntos están vinculados si se encuentran entre los $K$ vecinos más cercanos de cada punto. Los nodos contienen las características $(x,y,z)$ de los puntos correspondientes.

2) **Convolución Discreta**. Este es el nombre de la agregación de vecindario más un MLP que permite capturar el contexto local de cada punto <span style="color:#2f6004">**de una manera invariante ante las permutaciones**</span>.

3) **Submuestreo (Downsampling)**. Esencialmente una agrupación (pooling).

#### Los grafos implementan Convoluciones Discretas 
Sea $G = (V, E)$ un grafo, donde $V = \{v_1, v_2, \ldots, v_N\}$ representa el conjunto de $N$ nodos y $E \subseteq V \times V$ representa el conjunto de aristas. Utilizamos la matriz de adyacencia $\mathbf{A} \in \{0, 1\}^{N \times N}$ para codificar la estructura del grafo, donde $\mathbf{A}_{ij} = 1$ si existe una arista entre los nodos $v_i$ y $v_j$, y $\mathbf{A}_{ij} = 0$ en caso contrario.

**Características y etiquetas de los nodos**. Cada nodo $v_i$ está asociado con un vector de características $\mathbf{x}_i \in \mathbb{R}^d$, donde $d$ es la dimensionalidad del espacio de características. Estas características se representan colectivamente como una matriz $\mathbf{X} \in \mathbb{R}^{N \times d}$, donde la fila $i$-ésima corresponde al vector de características del nodo $v_i$. Para la **clasificación de nodos supervisada**, un subconjunto de nodos $V_L \subset V$ tiene etiquetas asociadas $y_i \in \{1, 2, \ldots, C\}$, donde $C$ es el número de clases.

**Ejemplo**. En la {numref}`GraphInit`, mostramos un grafo con nodos:

$$V=\{A,B,C,D,E\}$$
y aristas:

$$
E=\{(A,B),(A,C),(B,C),(C,D),(C,E),(D,E)\}\;.
$$

En este caso, el grafo es *no dirigido*, lo que significa que si $(i,j)\in E$ entonces $(j,i)\in E$ y no necesitamos denotar ambas aristas.

```{figure} ./images/Topic1/Graph1.png
---
name: GraphInit
width: 600px
align: center
height: 500px
---
Grafo inicial con características. Imagen generada parcialmente por Gemini. 
```

**Características y etiquetas**. Nótese que mostramos las características $\mathbf{x}_i$ de cada nodo $i$ y sus *etiquetas reales (ground-truth)* $y_i$. En este ejemplo, tenemos $d=2$ características por nodo y $C=2$ clases.

Mirando las características, tenemos que los nodos $A$ y $B$ están asociados consistentemente con la clase $0$: en esta clase $\mathbf{x}_i(1)> \mathbf{x}_i(2)$ y $\mathbf{x}_i(2)\ge 0.5$. De igual manera, los nodos $C$ y $D$ están asociados consistentemente con la clase $1$: $\mathbf{x}_i(1)> \mathbf{x}_i(2)$ y $\mathbf{x}_i(1)\ge 0.5$. Sin embargo, las características del nodo $C$ lo sitúan en medio de ambas clases.

Independientemente de la división entre entrenamiento y prueba (que es irrelevante para este ejemplo), ¡<span style="color:#2f6004">**una separación lineal será difícil en este caso**</span> debido al nodo $C$! Por lo tanto, para un MLP simple obtendremos algo cercano a la decisión en {numref}`MLPInit`.

```{figure} ./images/Topic1/MLP1.png
---
name: MLPInit
width: 600px
align: center
height: 500px
---
Clasificación mediante un MLP simple. Imagen generada parcialmente por Gemini. 
```
**Los grafos proporcionan contexto local**. La razón de la falta de rendimiento anterior es bastante obvia: los MLPs tratan las características de los nodos de forma **independiente**. Sin embargo, dado que <span style="color:#2f6004">**los grafos implementan relaciones de pares entre variables**</span>, se espera que los nodos vecinos tengan propiedades similares, en particular sus etiquetas. Cuando los vecinos tienden a compartir la misma etiqueta, esto se conoce como **homofilia**.

Al **ignorar las aristas del grafo** y el contexto proporcionado por el vecindario, un MLP no logra capturar los patrones relacionales que a menudo son indicativos de la clase de un nodo en los datos estructurados en grafos.

**Agregación invariante**. Supongamos ahora que, para cualquier nodo $\mathbf{v}_i$, *agregamos las características de sus vecinos* y pasamos la agregación, en lugar de pasar directamente sus características al MLP. En otras palabras, todo lo que hacemos es alimentar al MLP con una *nueva incrustación que dé cuenta del contexto local de cada nodo*. Dicha incrustación, $\mathbf{h}_i$, se <span style="color:#2f6004">**agrega de una manera invariante con respecto al orden de los vecinos**</span>. Esto significa que solo podemos usar funciones como la SUMA (SUM), el PROMEDIO (MEAN) y el MÁXIMO (MAX) como agregadores:

$$
\mathbf{h}_i := \sum_{j\in \mathcal{N}(i)\cup \{i\}}\mathbf{x}_j,\;\; \mathbf{h}_i :=\frac{1}{|{\cal N}(i)|}\sum_{j\in \mathcal{N}(i) \bigcup \{i\}}\mathbf{x}_j,\;\;\text{o}\;
\;\mathbf{h}_i :=\max_{j\in \mathcal{N}(i)\bigcup \{i\}}\mathbf{x}_j\;, 
$$

donde $\mathcal{N}(i)$ denota a los *vecinos* del nodo $v_i$. Nótese que las características de $\mathbf{x}_i$ se incluyen en la actualización, como si hubiera un bucle para cada nodo en el grafo (como la autoatención en los Transformers).

Bajo una agregación invariante, el resultado $\mathbf{h}_i$ es el mismo independientemente del orden en el que se procesan los vecinos. Por lo tanto, los grafos tienen una codificación más flexible que las secuencias.

En la {numref}`MLPAgg`, vemos que las representaciones $\mathbf{h}_i$ de los nodos $A/B$ y $C/D$ colapsan en el mismo punto, facilitando así la decisión del MLP, y la representación de $C$ es *atraída* hacia el área de $A$ y $B$:

```{figure} ./images/Topic1/MLP2.png
---
name: MLPAgg
width: 700px
align: center
height: 500px
---
Clasificación mediante MLP simple de características agregadas. Imagen generada parcialmente por Gemini. 
```

<br></br>
<span style="color:#2f6004"> 
**Ejercicio**. Dado el ejemplo anterior. ¿Cuál es la representación después de aplicar una segunda agregación (utiliza suma como invariante y sin bucles)? Explica el resultado:
</span>
<br></br>
<span style="color:#2f6004"> 
En primer lugar, calculemos las incrustaciones para la primera agregación. Separamos la agregación (de los vecinos) y la actualización: 
<br></br>
</span>
<span style="color:#2f6004"> 
$
\begin{aligned}
&\begin{array}{cccc}
\text{Nodo} &\text{Estado} & \text{Vecinos} & \text{Agregación} & \text{Actualización} \\\hline
v_A & [1.0\;0.5] & \{B,C\} & [0.8\;0.7]+[0.2\;0.9]  & [2.0\; 2.1]\\
v_B & [0.8\;0.7] & \{A,C\} & [1.0\;0.5]+[0.2\;0.9]  & [2.0\; 2.1]\\
v_C & [0.2\;0.9] & \{A,B,D,E\} & [1.0\;0.5]+[0.8\;0.7] + [0.5\;0.1] + [0.9\;0.3]  & [3.4\;2.5]\\
v_D & [0.5\;0.1] & \{C,E\} & [0.2\;0.9] + [0.9\;0.3] & [1.6\; 1.3]\\
v_E & [0.9\;0.3] & \{C,D\} & [0.2\;0.9] + [0.5\;0.1] & [1.6\; 1.3]\\
\end{array}
\end{aligned}
$
</span>
<br></br>
<span style="color:#2f6004"> 
Nótese que después de que la primera agregación también se muestra en {numref}`MLPAgg`. Dos pares de nodos $(A,B)$ y $(D,E)$ colapsan en el mismo punto de representación, lo cual es bueno ya que son homólogos (misma clase). Sin embargo, el nodo $C$, que pertenece a la clase $1$, no colapsa aunque está más cerca de sus homólogos que de los otros nodos.
<br></br>
Ahora, suponiendo que el "Estado" no es proyectado por un MLP (o simplemente que dicha proyección es la identidad $\mathbf{I}$) reemplazamos la columna "Estado" por los resultados anteriores en "Actualización" y volvemos a calcular:
</span>
<br></br>
<span style="color:#2f6004"> 
$
\begin{aligned}
&\begin{array}{cccc}
\text{Nodo} &\text{Estado} & \text{Vecinos} & \text{Agregación} & \text{Actualización} \\\hline
v_A & [2.0\; 2.1] & \{B,C\} & [2.0\; 2.1]+[3.4\;2.5]  & [7.4\;6.7]\\
v_B & [2.0\; 2.1] & \{A,C\} & [2.0\; 2.1]+[3.4\;2.5]  & [7.4\;6.7]\\
v_C & [3.4\;2.5] & \{A,B,D,E\} & 2\cdot[2.0\; 2.1] + 2\cdot[1.6\; 1.3] & [10.6\;9.3]\\
v_D & [1.6\; 1.3] & \{C,E\} & [3.4\;2.5] + [1.6\; 1.3] & [6.6\;5.1]\\
v_E & [1.6\; 1.3] & \{C,D\} & [3.4\;2.5] + [1.6\; 1.3] & [6.6\;5.1]\\
\end{array}
\end{aligned}
$
</span>
<br></br>
<span style="color:#2f6004"> 
Como podemos ver, ¡**los colapsos homólogos aún persisten**! Y el nodo $C$ sigue estando en su categoría. Bajo estas condiciones, **un MLP en el 'Estado' hará que las características de $C$ colapsen con las de $A$ y $B$ tan pronto como $C$ sea clasificado erróneamente**.
</span>
<br></br>

### Arquitectura básica de las GNNs
En resumen, dado un grafo de entrada $G=(V,E)$ (que puede cambiar mediante [reconexión / rewiring](https://ellisalicante.org/tutorials/GraphRewiring)), cada una de las $L$ capas de una GNN tiene tres componentes:

1) **Paso de mensajes**. Cada nodo envía su estado interno (su incrustación actual) a sus vecinos (posiblemente incluyéndose a sí mismo).

2) **Agregación**. Cada nodo recibe un mensaje de sus vecinos adyacentes. Este mensaje suele estar ponderado por un **coeficiente de confianza**. Luego, todos los mensajes se agregan utilizando un operador invariante al orden (SUM, MEAN, MAX).

3) **Actualización**. El nuevo estado interno se construye tanto a partir de la agregación como de su *proyección* a través de un MLP.

Todos estos pasos se resumen en la {numref}`GNNArchitecture`, donde destacamos la última capa MLP para clasificación/regresión:

```{figure} ./images/Topic1/GNNArchitecture.png
---
name: GNNArchitecture
width: 800px
align: center
height: 700px
---
Arquitectura GNN (para el grafo del ejemplo). Imagen generada parcialmente por Gemini. 
```

De forma más formal, tenemos:

$$
\mathbf{h}_i^{(l+1)} := \text{UPDATE}^{(l)} \left( \mathbf{h}_i^{(l)}, \text{AGGREGATE}^{(l)} \left( \{ \text{MESSAGE}^{(l)}(\mathbf{h}_i^{(l)}, \mathbf{h}_j^{(l)}, \mathbf{e}_{ij}) : j \in \mathcal{N}(i)\cup \{i\} \} \right) \right)
$$

que coincide básicamente (para la SUMA) con:

$$
\mathbf{h}_i^{(l+1)} :=\sigma^{(l)}\left(\mathbf{W}^{(l)} \left(\sum_{j \in \mathcal{N}(i)\cup \{i\}}\alpha_{ij}\mathbf{h}_i^{(l)}
\right)+ b^{(l)}\right) = \text{MLP}^{(l)}_{\Theta}\left(\sum_{j \in \mathcal{N}(i)\cup \{i\}}\alpha_{ij}\mathbf{h}_i^{(l)}\right)\;,
$$

donde $\alpha_{ij}$ son *coeficientes de atención aprendibles* (ver más abajo). En resumen, <span style="color:#2f6004">**una capa GNN es un MLP de la agregación**</span>.

En forma matricial tenemos (omitiendo los coeficientes de atención y los sesgos en aras de la claridad):

$$
\mathbf{H}^{(l+1)} := \sigma^{(l)}(\mathbf{W}^{(l)}\tilde{\mathbf{A}}\mathbf{H}^{(l)})\;,
$$

donde $\tilde{\mathbf{A}}=\mathbf{A} + \mathbf{I}$ es la matriz de adyacencia con bucles (unos en la diagonal). Por lo tanto, $\mathbf{H}^{(l+1)}$ es una matriz $N\times d^{(l+1)}$, donde $d^{(l+1)}$ es la dimensión de salida del $l$-ésimo MLP. Entonces, esta matriz encapsula la *nueva* incrustación de los nodos en sus filas.

Además, la expresión $\tilde{\mathbf{A}}\mathbf{H}^{(l)}$, donde $\mathbf{H}^{(l)}$ es una matriz $N\times d^{(l)}$ (normalmente con $d^{(l)}\ge d^{(l+1)}$) compacta todas las agregaciones, ya que:

$$
(\tilde{\mathbf{A}}\mathbf{H}^{(l)})_{ij}=
\langle\tilde{\mathbf{A}}_{i:},\mathbf{H}^{(l)}_{j:}\rangle = 
\sum_{j}\tilde{\mathbf{A}}_{ij}\mathbf{H}^{(l)}_{ij}\;.
$$

Nótese que la matriz $\tilde{\mathbf{A}}$ se mantiene constante a lo largo de todas las capas (a menos que apliquemos *reconexión / rewiring*).

### Redes de Atención en Grafos (Graph Attention Networks)
La GNN vanilla (arriba) fue introducida por [Kipf & Welling](https://arxiv.org/abs/1609.02907). Más tarde, [Gilmer et al.](https://arxiv.org/abs/1704.01212) acuñaron el término Redes Neuronales de Paso de Mensajes (MPNNs) y revisaron las variantes emergentes del modelo vanilla. En particular, el modelo de Kipf-Welling tiene una interpretación espectral para modular el paso de mensajes (volveremos a este punto más adelante).

Las GNNs vanilla (también conocidas como **Redes Convolucionales de Grafos** o **GCNs**) tienen una **limitación** importante: **<span style="color:#2f6004">agregan ciegamente mensajes provenientes de todos los vecinos</span>**:
- Esto es eficaz en regímenes homofílicos donde los vecinos no solo comparten etiquetas sino que tienen vectores de características similares.
- En entornos más generales, sin embargo, las características de los vecinos pueden ser muy diferentes incluso cuando sus nodos correspondientes comparten la misma etiqueta.
- Si se mantiene esta **atención constante** (todos los mensajes nacen iguales) podemos sesgar la agregación y crear así un **espacio latente subóptimo**.

Las **Redes de Atención en Grafos** o **GATs**, por [Velickovic et al.](https://arxiv.org/pdf/1710.10903), abordan este problema calculando y aprendiendo los **coeficientes de atención** $\alpha_{ij}$ de la siguiente manera:

1) Dada una arista $(i,j)$ en el grafo, su *coeficiente de atención no normalizado* (después de la proyección de las incrustaciones de nodos $\mathbf{h}_i$ y $\mathbf{h}_j$) es:

$$
e_{ij}:=\mathbf{a}\left(\mathbf{W}\mathbf{h}_i,\mathbf{W}\mathbf{h}_i\right)\;,
$$

donde $\mathbf{a}:\mathbb{R}^d\times \mathbb{R}^d\rightarrow \mathbb{R}$ es un MLP parametrizado por $\mathbf{a}\in\mathbb{R}^{2d}$. ¿Por qué?

2. Este MLP *concatena* las entradas $\mathbf{W}\mathbf{h}_i$ y $\mathbf{W}\mathbf{h}_j$ donde la notación es:

$$
\mathbf{W}\mathbf{h}_i||\mathbf{W}\mathbf{h}_j\;,
$$

y por eso $\mathbf{a}\in\mathbb{R}^{2d}$.

3. Dada una concatenación $\mathbf{W}\mathbf{h}_i||\mathbf{W}\mathbf{h}_j$, el MLP procede de la siguiente manera:

$$
\alpha_{ij}:=\text{Softmax}(e_{ij})=\frac{\exp(e_{ij})}{\sum_{k\in {\cal N}(i)} \exp(e_{ik})}
$$

donde, en lo siguiente, ${\cal N}(i)$ es equivalente por defecto a ${\cal N}(i)\cup \{i\}$ (se incluye a sí mismo).

En más detalle, tenemos:

$$
\alpha_{ij}:=\frac{\exp\left(\text{LeakyReLU}(\mathbf{a}^T(\mathbf{W}\mathbf{h}_i||\mathbf{W}\mathbf{h}_j)\right)}{\sum_{k\in {\cal N}(i)}\exp\left(\text{LeakyReLU}(\mathbf{a}^T(\mathbf{W}\mathbf{h}_i||\mathbf{W}\mathbf{h}_k)\right)}\;,
$$

donde $\text{LeakyReLU}$ denota la [no linealidad correspondiente con pendiente negativa](https://docs.pytorch.org/docs/stable/generated/torch.nn.LeakyReLU.html).

4. Una vez que hemos calculado los $\alpha_{ij}$ (como en el Transformer), los usamos para ACTUALIZAR el estado:

$$
\mathbf{h}^{(l+1)}_i:=\sigma\left(\sum_{j\in{\cal N}(i)}\alpha_{ij}\mathbf{W}\mathbf{h}^{(l)}_j\right)\;.
$$

5. Finalmente, como en el Transformer (aunque omitido por claridad) podemos aprender diferentes tipos de atención. Esto se llama **atención de múltiples cabezas (multi-head attention)** y ahora $\mathbf{h}'_i$ es la concatenación de $K$ resultados de atención diferentes de la siguiente manera:

$$
\mathbf{h}^{(l+1)}_i:=||_{k=1}^K \sigma\left(\sum_{j\in{\cal N}(i)}\alpha_{ij}^k\mathbf{W}^k\mathbf{h}^{(l)}_j\right)\;.
$$

En otras palabras, el mismo mensaje se proyecta de una manera diferente y se modula por el conjunto específico de coeficientes para esta cabeza de atención $k$. El resultado final es la concatenación de todos los resultados parciales.

6. La concatenación funciona bien en capas GAT intermedias, pero si tenemos una capa GAT final previa al softmax, es mejor promediar las salidas producidas por cada cabeza de atención:

$$
\mathbf{h}^{(l+1)}_i:=\sigma\left(\frac{1}{K}\sum_k\sum_{j\in{\cal N}(i)}\alpha_{ij}^k\mathbf{W}^k\mathbf{h}^{(l)}_j\right)\;.
$$

Esto se resume en la {numref}`GAT`. A la izquierda, ilustramos el MLP para calcular los coeficientes de atención. Derecha: grafo hipotético con $K=3$ cabezas de atención (colores diferentes). Visualiza esto como $K$ grafos superpuestos cuya representación nodal de diferentes colores debe concatenarse (o promediarse). En esta figura, hemos preservado la notación vectorial tradicional (flechas).

```{figure} ./images/Topic1/GAT.png
---
name: GAT
width: 800px
align: center
height: 400px
---
GAT. Imagen del artículo original: [Graph Attention Networks](https://arxiv.org/pdf/1710.10903). 
```

### Homofilia frente a Heterofilia
#### El conjunto de datos Cora
Ejemplifiquemos las ventajas de las GNNs vanilla frente a las MLPs y GATs **en el régimen homofílico** con el estudio del [conjunto de datos Cora](https://graphsandnetworks.com/the-cora-dataset/). Se trata de un grafo de 2708 publicaciones científicas representadas como nodos. Los nodos se clasifican en una de las $C=7$ clases atendiendo al tipo de publicación. Las características de cada nodo son un vector 0/1 que indica la ausencia/presencia de una palabra en un diccionario de $d=1433$ palabras. Hay $5429$ enlaces (dirigidos) que indican que un artículo cita a otro artículo. En la {numref}`Cora` mostramos el componente conectado más grande de Cora utilizando aristas no dirigidas como en [PyTorch Geometric](https://pytorch-geometric.readthedocs.io/en/latest/):

```{figure} ./images/Topic1/Cora.png
---
name: Cora
width: 800px
align: center
height: 600px
---
Componente más grande del conjunto de datos Cora. Imagen generada por PyTorch Geometric. 
```

**Conoce tu conjunto de datos**. Las estadísticas básicas de Cora se encuentran en la {numref}`Cora-Stats`. Nótese que, además del número de nodos y su grado, hay algunas especificaciones para la división entre entrenamiento y prueba. En particular, en el siguiente experimento **solo se utiliza el $5\%$ de los nodos para el entrenamiento**.

```{figure} ./images/Topic1/Cora-Stats.png
---
name: Cora-Stats
width: 800px
align: center
height: 300px
---
Estadísticas del conjunto de datos Cora. Imagen generada por PyTorch Geometric. 
```

**Grado de homofilia**. Una estadística fundamental para comprender si las GNNs pueden superar a los MLPs es la fracción de nodos cuyos vecinos tienen la misma clase. Esta es la llamada **tasa de homofilia de aristas**:

$$
h = \frac{|\{(v_i, v_j) \in E : y_i = y_j\}|}{|E|}
$$

Si $h=0$, se espera que el MLP supere a las GNNs, mientras que para $h=1$ se espera lo contrario. Para Cora, tenemos que $h^{Cora}=0.81$ lo que indica que la agregación es más prometedora que la de los MLPs para la **clasificación de nodos semisupervisada**.

**Comparación de MLPs, GNNs vanilla y GATs**. Seguimos la tendencia general de usar dos capas + softmax. Recuerda que un MLP se puede ver como una **secuencia de funciones de composición de reducción a escala** que toman la dimensión de característica inicial $\text{num\_features}=1433$, mapeándola a una $\text{dimensión oculta}=16$ y finalmente a $\text{num\_classes}=7$. Esto sigue la regla de reducción casi logarítmica:
$
O(10^3)\rightarrow O(10^1)\rightarrow O(10^0)\;.
$

El fragmento de Torch se da a continuación:

```python
from torch.functional import F
from torch.nn import Linear
class MLP(torch.nn.Module):
    def __init__(self,hidden_channels = 16):
        super(MLP, self).__init__()
        # MLP de 2 capas
        self.lin1 = Linear(dataset.num_features, hidden_channels)
        self.lin2 = Linear(hidden_channels, dataset.num_classes)

    def forward(self, x, edge_index):
        # edge_index no se utiliza
        x = self.lin1(x)
        x = x.relu()
        x = F.dropout(x, p=0.5, training=self.training)
        x = self.lin2(x)
        return x.softmax(dim=1)
```

Para las capas GCN y GAT, utilizamos dos capas convolucionales + softmax. Las capas convolucionales (respectivamente $\text{GCNConv}$ y $\text{GATConv}$ son proporcionadas por Pytorch Geometric):

```python
from torch_geometric.nn import GCNConv
from torch.functional import F
'''
    En PyTorch, se define un modelo subclasificando torch.nn.Module y definiendo un método forward() que recibe datos de entrada y devuelve datos de salida.
    El método forward() puede usar otros módulos definidos en el constructor como submódulos, y puede usar operadores arbitrarios en tensores, incluyendo bucles y sentencias condicionales.
    Este enfoque es muy flexible y se puede utilizar para definir modelos de complejidad arbitraria.
'''
class GCN(torch.nn.Module):
    '''
        Argumentos de __init__:
            * hidden_channels: El número de unidades ocultas.
            * dataset.num_features: El número de características de entrada.
            * dataset.num_classes: El número de clases de salida.
        Retorna:
            * self.conv1: La primera capa GCN.
            * self.conv2: La segunda capa GCN.
    '''
    def __init__(self,hidden_channels = 16):
        super(GCN, self).__init__()
        # GCN de 2 capas
        self.conv1 = GCNConv(dataset.num_features, hidden_channels) # 16 unidades ocultas
        self.conv2 = GCNConv(hidden_channels, dataset.num_classes) # dataset.num_classes unidades de salida
    '''
        Argumentos de forward:
            * x: Las características de entrada.
            * edge_index: Los índices de las aristas.
        Retorna:
            * F.softmax(x, dim=1): La salida del modelo.
    '''
    def forward(self, x, edge_index):
        x = F.relu(self.conv1(x, edge_index)) # Activación ReLU
        x = F.dropout(x,p=0.5, training=self.training) # Dropout: el 50% de los nodos se descartan aleatoriamente durante el entrenamiento
        x = self.conv2(x, edge_index)
        return x.softmax(dim=1) # Activación Log softmax
```
y

```python
from torch_geometric.nn import GATConv
from torch.functional import F
'''
    En PyTorch, se define un modelo subclasificando torch.nn.Module y definiendo un método forward() que recibe datos de entrada y devuelve datos de salida.
    El método forward() puede usar otros módulos definidos en el constructor como submódulos, y puede usar operadores arbitrarios en tensores, incluyendo bucles y sentencias condicionales.
    Este enfoque es muy flexible y se puede utilizar para definir modelos de complejidad arbitraria.
'''
class GAT(torch.nn.Module):
    '''
        Argumentos de __init__:
            * hidden_channels: El número de unidades ocultas.
            * dataset.num_features: El número de características de entrada.
            * dataset.num_classes: El número de clases de salida.
        Retorna:
            * self.conv1: La primera capa GCN.
            * self.conv2: La segunda capa GCN.
    '''
    def __init__(self,hidden_channels = 16):
        super(GAT, self).__init__()
        # GAT de 2 capas
        self.conv1 = GATConv(dataset.num_features, hidden_channels) # 16 unidades ocultas
        self.conv2 = GATConv(hidden_channels, dataset.num_classes) # dataset.num_classes unidades de salida
    '''
        Argumentos de forward:
            * x: Las características de entrada.
            * edge_index: Los índices de las aristas.
        Retorna:
            * F.softmax(x, dim=1): La salida del modelo.
    '''
    def forward(self, x, edge_index):
        x = F.relu(self.conv1(x, edge_index)) # Activación ReLU
        x = F.dropout(x,p=0.5, training=self.training) # Dropout: el 50% de los nodos se descartan aleatoriamente durante el entrenamiento
        x = self.conv2(x, edge_index)
        return x.softmax(dim=1) # Activación Log softmax
```

Para la GAT utilizamos una única **cabeza de atención** (configurada por defecto).

**Espacios latentes**. Entrenamos los modelos anteriores con la **división de entrenamiento/prueba/validación** de $48/32/20$: $48\%$ de los nodos para entrenamiento, $32\%$ para prueba y $20\%$ para validaciones. Primero dividimos los nodos en un $80\%$ para entrenamiento y un $20\%$ para prueba. Luego dividimos los nodos de entrenamiento en un $48\%$ para entrenamiento y un $32\%$ para validación sobre el $80\%$ de los nodos.

Realizamos $10$ ejecuciones con las mismas semillas aleatorias. En la {numref}`Cora-Latent` mostramos las proyecciones [t-SNE](https://scikit-learn.org/stable/modules/generated/sklearn.manifold.TSNE.html) de los espacios latentes respectivos.

```{figure} ./images/Topic1/Cora-Latent.png
---
name: Cora-Latent
width: 800px
align: center
height: 300px
---
Cora: espacios latentes de GCN (GNN vanilla), MLP y GAT. Imagen generada por PyTorch Geometric. 
```
En la {numref}`Cora-Accuracy` mostramos las precisiones respectivas. Como se esperaba en un conjunto de datos homofílico, donde el poder de agregación es máximo, tanto GCN (GNN vanilla) como GAT superan al MLP. Aquí están las medias y las desviaciones estándar para las diez ejecuciones respectivas de cada modelo:

$$
\begin{aligned}
\text{GCN:}\; 80.55 \pm 1.18\\
\text{MLP:}\; 75.42 \pm 1.50\\
\text{GAT:}\; 79.37 \pm 1.48\\
\end{aligned}
$$

Nótese que la GCN mejora ligeramente a la GAT ya que en el entorno homofílico el valor de la atención es anulado por la agregación. En otras palabras, hacer que diferentes nodos vecinos tiendan a ser similares no tiene sentido. En este caso, la GAT tiende a inhibir dicha atención.

```{figure} ./images/Topic1/Cora-Accuracy.png
---
name: Cora-Accuracy
width: 800px
align: center
height: 300px
---
Cora: precisiones de GCN (GNN vanilla), MLP y GAT. Imagen generada por PyTorch Geometric. 
```

#### El conjunto de datos Texas
El conjunto de datos Texas se incluye en el [conjunto de datos WebKB](https://pytorch-geometric.readthedocs.io/en/latest/generated/torch_geometric.datasets.WebKB.html). El WebKB es un conjunto de datos de páginas web recopilado de departamentos de informática de varias universidades por la Universidad Carnegie Mellon. Utilizamos uno de los tres subconjuntos de datos, Cornell, Texas y Wisconsin, donde los nodos representan páginas web y las aristas son hipervínculos entre ellas. Las características de los nodos son la representación de bolsa de palabras (bag-of-words) de las páginas web. Las páginas web se clasifican manualmente en $C=5$ categorías: estudiante, proyecto, curso, personal y facultad.

La homofilia de Texas es bastante pequeña: $h^{Texas}=0.11$. Esto significa que la probabilidad de encontrar dos nodos vecinos con la misma etiqueta es de $0.11$.

```{figure} ./images/Topic1/Texas.png
---
name: Cora
width: 800px
align: center
height: 600px
---
Componente más grande del conjunto de datos Texas. Imagen generada por PyTorch Geometric. 
```

```{figure} ./images/Topic1/Texas-Stats.png
---
name: Texas-Stats
width: 800px
align: center
height: 150px
---
Estadísticas del conjunto de datos Texas. Imagen generada por PyTorch Geometric. 
```

**Resultados**. Entrenando los tres modelos bajo las mismas condiciones que antes, obtenemos los siguientes espacios latentes.

```{figure} ./images/Topic1/Texas-Latent.png
---
name: Texas-Latent
width: 800px
align: center
height: 300px
---
Texas: espacios latentes de GCN (GNN vanilla), MLP y GAT. Imagen generada por PyTorch Geometric. 
```

Estos espacios latentes son bastante ilustrativos del poder de MLP frente al aprovechamiento de la estructura del grafo como en GCN o GAT. En este régimen heterofílico, donde es muy probable que los nodos vecinos tengan etiquetas diferentes, la mejor opción es sin duda el MLP:

$$
\begin{aligned}
\text{GCN:}\; 84.05 \pm 6.22\\
\text{MLP:}\; 92.16 \pm 4.59\\
\text{GAT:}\; 81.08 \pm 7.93\\
\end{aligned}
$$

```{figure} ./images/Topic1/Texas-Accuracy.png
---
name: Texas-Accuracy
width: 800px
align: center
height: 300px
---
Texas: precisiones de GCN (GNN vanilla), MLP y GAT. Imagen generada por PyTorch Geometric. 
```

De hecho, el MLP supera a la GCN y a la GAT. Sin embargo, en términos generales, las GATs tienden a tener un rendimiento similar al del MLP. Téngase en cuenta que aquí estamos utilizando una sola cabeza de atención. Aumentar el número de cabezas mejora los resultados, pero no lo suficiente como para superar al MLP en general.

### Tema Avanzado: GNNs de Difusión-Salto (Diffusion-Jump GNNs)
Recuerde que para el caso de Cora (homofílico), tanto GCN como GAT superan al MLP, mientras que para Texas (heterofílico) sucede lo contrario. ¿Es posible diseñar una arquitectura única capaz de comportarse igual de bien en ambos casos?

Este es un tema de investigación abierto, pero en la [GNN de Difusión-Salto (DJGNN)](#Diffusion-Jump), por [Zhu et al.](https://arxiv.org/abs/2210.16075), se aborda este problema introduciendo dos nuevas capas:

1. **Capa de Difusión**. Esta es básicamente la agregación de vecindario (homofilia).
2. **Capa de Salto**. Esta es la agregación de nodos que están a una distancia $k$ (heterofilia).

Bajo este esquema, la GNN puede aprender cuándo difundir y cuándo saltar basándose en el grado de homofilia del conjunto de datos.

```{figure} ./images/Topic1/Diffusion-Jump.png
---
name: Diffusion-Jump
width: 800px
align: center
height: 500px
---
DNGNN. Imagen del artículo original: [Diffusion-Jump Graph Neural Networks](https://arxiv.org/abs/2210.16075). 
```

### Razonamiento Algorítmico Neuronal (Neural Algorithmic Reasoning)
#### Motivación
Como hemos visto, la agregación y la actualización son los mecanismos impulsores de las GNNs. Es notable el hecho de que muchos algoritmos tradicionales de grafos (como el cálculo de caminos mínimos, el orden topológico, etc.) también se basan en la agregación y actualización locales.

De hecho, la Programación Dinámica (DP) es una técnica que resuelve problemas complejos dividiéndolos en subproblemas más simples. La DP es la base de muchos algoritmos de grafos. ¿Es posible simular la DP mediante GNNs?

#### Simulación de DP mediante GNNs
Consideremos el algoritmo de [Bellman-Ford](https://en.wikipedia.org/wiki/Bellman%E2%80%93Ford_algorithm) para calcular los caminos mínimos desde un nodo fuente al resto de nodos del grafo. Sea $d_i$ el camino mínimo actual desde el nodo fuente al nodo $v_i$. La regla de actualización de Bellman-Ford es:

$$
d_i^{(l+1)} := \min \left( d_i^{(l)}, \min_{j \in \mathcal{N}(i)} (d_j^{(l)} + w_{ij}) \right)
$$

donde $w_{ij}$ es el peso de la arista entre $v_i$ y $v_j$. En otras palabras, ¡**Bellman-Ford es una GNN** donde la agregación es el MÍNIMO y el MLP es la actualización!

En general, podemos decir que un algoritmo de DP se puede alinear con una GNN si la regla de actualización de la DP puede expresarse mediante agregaciones y actualizaciones locales. Esta área se conoce como **Razonamiento Algorítmico Neuronal (NAR)**.

#### Alineación Algorítmica (Algorithmic Alignment)
Decimos que una NN está **alineada algorítmicamente** con un algoritmo si la arquitectura de la NN es capaz de simular el algoritmo con un número de pasos razonable.

Como señalaron [Xu et al.](https://arxiv.org/abs/1905.13192), las GNNs son naturalmente más potentes que los MLPs para simular algoritmos debido a su capacidad para agregar información local. De hecho, demostraron que bajo ciertas condiciones, las GNNs pueden aprender a ejecutar algoritmos con una capacidad de generalización muy alta (incluso sobre grafos de tamaños mucho mayores que los de entrenamiento).

### Neuralización Combinatoria 
#### Problema: El Máximo Clique (The Maximum Clique)
Sea $G=(V,E)$ un grafo. Un **clique (o cliqué)** $C \subseteq V$ es un subconjunto de nodos tal que cada par de nodos distintos en $C$ es adyacente (es decir, el subgrafo inducido por $C$ es completo). El **Máximo Clique (MC)** es un problema de optimización cuyo objetivo es encontrar el clique con el mayor número de nodos posible. El tamaño del MC se denota por $\omega(G)$.

Encontrar el MC es un problema **NP-difícil**. A pesar de esto, el MC es un problema fundamental en muchas aplicaciones como la bioinformática, el análisis de redes sociales y la visión artificial (donde se utiliza para el emparejamiento de grafos).

#### Algoritmo clásico: Bron-Kerbosch
Un algoritmo clásico para encontrar todos los cliques maximales en un grafo es el algoritmo de [Bron-Kerbosch (BK)](https://en.wikipedia.org/wiki/Bron%E2%80%93Kerbosch_algorithm). El algoritmo BK utiliza una técnica de ramificación y poda (branch-and-bound) para explorar el espacio de búsqueda. A pesar de su eficiencia en grafos dispersos, el tiempo de ejecución en el peor de los casos sigue siendo exponencial.

En la {numref}`BK`, mostramos el resultado de aplicar el algoritmo BK al grafo del ejemplo anterior. Nótese que el MC es $\{A,B,C\}$ y su tamaño es $\omega(G)=3$.

```{figure} ./images/Topic1/MaximalCliques.png
---
name: BK
width: 600px
align: center
height: 600px
---
Cliques maximales en el grafo del ejemplo. Imagen generada por Gemini. 
```

Nótese que nuestro grafo es "simple":
- Clique 1 (AZUL): $\{A,B,C\}$.
- Clique 2 (NARANJA): $\{C,D,E\}$.

Ambos cliques son **maximales** (no pueden ser extendidos añadiendo un nodo más), pero solo el Clique 1 y el Clique 2 son los **máximos** (tienen el mismo tamaño de 3). Para nuestro estudio, supondremos que solo nos interesa encontrar **un** MC.

#### Del Bron-Kerbosch al Razonamiento Neuronal
En principio, podríamos intentar entrenar una GNN para simular el algoritmo BK. Sin embargo, BK no es local; depende de un estado global (los conjuntos de nodos candidatos, ya visitados, etc.). ¿Es posible formular el MC como un problema local para ser resuelto por una GNN?

Como han demostrado [Cvetkovic et al.](https://arxiv.org/pdf/2301.10444.pdf), existe una alternativa más atractiva: la **Relajación de Motzkin-Strauss**.

#### Relajación de Motzkin-Strauss
En 1965, Motzkin y Strauss demostraron que el tamaño del máximo clique $\omega(G)$ de un grafo $G$ puede encontrarse mediante el siguiente problema de optimización continua:

$$
\frac{1}{\omega(G)} = 1 - \max_{\mathbf{x} \in \Delta} \mathbf{x} \mathbf{A} \mathbf{x}^T 
$$

donde $\Delta = \{\mathbf{x} \in \mathbb{R}^N : \sum_i x_i = 1, x_i \ge 0\}$ es el simplex unidad. En esta formulación, $\mathbf{A}$ es la matriz de adyacencia del grafo.

**Interpretación**. El objetivo es encontrar un vector de probabilidad $\mathbf{x}$ que maximice la forma cuadrática $f(\mathbf{x}) = \mathbf{x} \mathbf{A} \mathbf{x}^T$. El valor máximo de $f(\mathbf{x})$ es $1 - 1/\omega(G)$. Lo más importante es que el soporte de un vector óptimo $\mathbf{x}^\ast$ (el conjunto de nodos para los cuales $x_i > 0$) corresponde a un clique de $G$. Para el máximo clique, este valor es máximo.

Esta formulación es muy atractiva porque transforma un problema discreto NP-difícil en un problema de optimización continua sobre un simplex.

#### Dinámicas del Replicador (Replicator Dynamics)
Para encontrar el máximo de $f(\mathbf{x})$, podemos utilizar un sistema dinámico conocido como las **Dinámicas del Replicador (RD)**. Las RD provienen de la teoría de juegos evolutiva y su forma continua es:

$$
\dot{x}_i(t) = x_i(t) [ (\mathbf{A}\mathbf{x}(t))_i - \mathbf{x}(t)^T \mathbf{A} \mathbf{x}(t) ]
$$

Las RD tienen la propiedad fundamental de que, partiendo de cualquier punto interior del simplex $\Delta$, la trayectoria converge a un punto crítico de la forma cuadrática $f(\mathbf{x})$ sobre el simplex. En particular, si partimos del baricentro $\mathbf{x}(0) = [1/N, \ldots, 1/N]$, es probable (aunque no garantizado) que las RD converjan a un MC.

Demos un vistazo a las RDs funcionando en nuestro grafo de ejemplo ({numref}`GraphInit`).

```{figure} ./images/Topic1/RD1.png
---
name: RD1
width: 800px
align: center
height: 500px
---
Evolución de las probabilidades de los nodos durante las RDs. Imagen generada por Gemini. 
```
Observemos que:
1) Empezamos con todos los nodos con una probabilidad uniforme $x_i(0)=1/5=0.2$.
2) A través de las iteraciones, las probabilidades de los nodos $\{A,B\}$ aumentan rápidamente, mientras que las de $\{D,E\}$ disminuyen. Finalmente, la probabilidad de $C$ disminuye lentamente.
3) Alrededor de la iteración 60, las probabilidades terminan siendo: $p_A=0.33, p_B=0.33, p_C=0.33$ y $p_{D,E} \approx 0$.
4) ¡Esto significa que las RD han encontrado el MC $\{A,B,C\}$!

<br></br>
<span style="color:#2f6004"> 
Una buena forma de probar esta hipótesis es que al añadir la arista $(0,3)$ se crean 2 cliques maximales (no máximos) de tamaño 3: $C_1=\{0,3,5\}$ y $C_2=\{0,3,7\}$. La existencia de cliques maximales que están **compitiendo con el MC** complica las RDs y las hace más "abiertas" en las primeras etapas de la búsqueda.  
</span> 
<br></br>


#### Integración con GNNs
**Motivación**. En principio, las Dinámicas del Replicador son capaces de aproximar el MC (especialmente si usamos $\mathbf{A}+\frac{1}{2}\mathbf{I}$ en lugar de $\mathbf{A}$ para evitar soluciones espurias). De hecho, este es el método proporcionado por el [framework de Gurobi](https://gurobi-optimods.readthedocs.io/en/latest/index.html) para encontrar isomorfismos de grafos mediante la identificación del MC.

Sin embargo, <span style="color:#2f6004">queremos aprender de la experiencia</span> para **<span style="color:#2f6004">inicializar las Dinámicas del Replicador más cerca del óptimo en lugar de lanzarlas desde el baricentro</span>**.

**Idea principal**. Entrenemos una GNN para optimizar $f(\mathbf{x})$ (o $\hat{f}(\mathbf{x})$). Hacerlo requiere **cuatro** pasos básicos (ver {numref}`GNN-RD`): 

1) **Proporcionar características de los nodos**. Necesitamos características de nodos informativas $\mathbf{x}_i\in\mathbb{R}^d$ para inicializar las incrustaciones nodales $\mathbf{h}_i$ que forman el espacio latente. Estas características pueden ser tan simples como el grado del nodo o tan complejas como una codificación posicional tal como un conjunto de autovectores del Laplaciano. 

2) **Añadir una capa Softmax**. Después de la capa final (o $K$) de agregación de la GNN, necesitamos una capa lineal para que se pueda predecir un punto inicial del simplex $\mathbf{p}$ para todas las incrustaciones nodales finales $\mathbf{h}_i^{(K)}$. Sin embargo, para forzar que $\mathbf{p}$ sea un punto del simplex, le aplicamos un "softmax", lo que lleva a $\sum_ip_i=1$ y $p_i\ge 0\;\forall i$.

3) **Dinámicas del Replicador**. En el tiempo de entrenamiento, es posible añadir "unas pocas" (3-4) iteraciones de RD. En este sentido, utilizamos la **versión discreta de RD**: 

$$
p_i(t+1)=p_i(t)\cdot\frac{(\mathbf{A}\mathbf{p}(t))_i}{\mathbf{p}(t)^T\mathbf{A}\mathbf{p}(t)}\;.
$$

Esta expresión es claramente derivable. Sin embargo, en el tiempo de inferencia/prueba, la misma expresión se "congela" y comienza desde el $\mathbf{p}$ inicial predicho por la NN. 

```{figure} ./images/Topic1/GNN-RD.png
---
name: GNN-RD
width: 800px
align: center
height: 220px
---
Red Neuronal de Grafos con RD. Nótese que las RD son derivables (es decir, contribuyen al gradiente). Una vez congeladas, también pueden usarse en el tiempo de inferencia. Aquí, el número de iteraciones es ilimitado. 
```

4) **Decodificador RD (RD Decoder)**. En el tiempo de inferencia/prueba, una vez que la NN predice $\mathbf{p}^{\ast}$, debemos extraer qué nodos pertenecen al MC utilizando las probabilidades en $\mathbf{p}^{\ast}$. Lo hacemos de la siguiente manera: 

```{prf:algorithm} Decodificador-RD
:label: R-D-Decoder

**Entradas**: Dado un $\mathbf{p}^{\ast}$ final y un umbral $\delta\in [0.5,1)$

**Salida**: Nodos $v_i\in G$ que forman el MC. 

1. $p^{\ast}_{\sigma(1)}\ge p^{\ast}_{\sigma(2)}\ge,\ldots,\ge p^{\ast}_{\sigma(n)} = \text{Sort}(-\mathbf{p}^{\ast})$

2. ${\cal C}=\emptyset$

3. **para** $n\in \{\sigma(1),\sigma(2),\ldots,\sigma(n)\}$: 

    1. **si** $(\mathbf{p}^{\ast}_n < \epsilon)$ & $(|{\cal C}|>0)$
**entonces** **detener**

    2. **si** $\text{Can_Extend}({\cal C},n)$ 
    **entonces** ${\cal C}={\cal C}\cup \{n\}$

**return** ${\cal C}$
```

Este Decodificador-RD es realmente sencillo. Es una estrategia voraz (greedy) que comienza con los nodos de alta probabilidad y los añade al MC candidato siempre que: (a) la probabilidad sea suficientemente buena, y (b) el nodo añadido forme un clique con respecto a los nodos existentes en el clique. 


