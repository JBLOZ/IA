# Problemas NP-Completos

## Problemas e intratabilidad
No todos los problemas informáticos son iguales. <span style="color:#f88146">Algunos problemas son **más difíciles** que otros</span>. La dificultad de un problema forma parte de su descripción. Siguiendo el libro *Computadoras e Intratabilidad* de Garey y Johnson, para describir correctamente un problema necesitamos:
- Una descripción general de todos sus <span style="color:#f88146">parámetros</span>, y
- Una <span style="color:#f88146">declaración</span> de qué propiedades debe satisfacer la respuesta o solución.

Una <span style="color:#f88146">instancia de un problema</span> se obtiene especificando valores particulares para todos
Los parámetros del problema.

**Gráficos**. Dado que casi todos los problemas combinatorios pueden mapearse a un grafo $G=(V,E)$, los *parámetros* del problema suelen ser el *número de nodos* $n=|V|$ y la *declaración* es la *propiedad deseada* que satisfacen los nodos, caminos, ciclos y subgrafos de $G$ en la solución. <span style="color:#f88146">¡Es el cumplimiento de esta propiedad lo que los hace **tratables** o **intratables**!</span>

## El problema del SAT
**Satisfacción**. Considere el siguiente problema, que (aparentemente) no está relacionado con grafos: *Dada una fórmula bien formada (fbf) en lógica de primer orden, determine si es satisfacible*.  
- Tenemos un conjunto de $n$ variables booleanas $X=\{x_1,x_2,\ldots,x_n\}$, donde $x_i\in\{0,1\}\;\forall i$.
- En la función de fórmula matemática, podemos tener variables $x_i$ y sus negaciones $\neg x_i$.
- La wff está en Forma Normal Conjuntiva (CNF), es decir, una colección de disyunciones $\lor$ unidas por $\land$ conectores.

Por ejemplo, la wff

$$
(x_1\lor x_2\lor \neg x_3)\land (\neg x_1\lor x_3\lor x_4)\land (x_2\lor x_3\lor \neg x_4)
$$

Está en CNF: tiene tres cláusulas con tres literales cada una. Por lo tanto, determinar si es <span style="color:#f88146">satisfacible</span> significa determinar si existe una asignación booleana para las variables para que la función de función completa (fbf) sea verdadera (evaluada a $1$).
- Dado que la wff está en CNF, **todas** las cláusulas deben evaluarse como $1$.
- Dentro de cada cláusula, **al menos un** literal debe evaluarse como $1$.

Un algoritmo de **fuerza bruta** debería evaluar todas las $2^n$ asignaciones booleanas posibles $\{0,1\}$ para las $n$ variables. ¿Hay alguna forma de resolver el supuesto
¿<span style="color:#f88146">Problema SAT</span> en *tiempo polinomial* (no exponencial)? ¡Desafortunadamente, solo si cada cláusula tiene menos de $3$ literales!

**SAT2**. En el problema SAT2, todas las cláusulas tienen dos literales. Considere, por ejemplo, la función de función de trabajo (fbf)

$$
(x_1\lo x_5)\land
(x_2\lo x_3)\l
(x_1\lo x_6)\land
(x_4\lo x_4)\land
(\neg x_6\lor \neg x_3)\land
(\neg x_2\lor x_3)\land
(\neg x_4\lor x_2)\;.
$$

donde todas las cláusulas tienen dos literales y $x_4\equiv(x_4\lor x_4)$, de modo que las cláusulas con un literal terminan teniendo dos. Entonces,
- Mapeamos las variables lógicas en $X$ a $2n$ nodos en $V$: un nodo para la variable no negada $x_i$ y otro para $\neg x_i$.
- Explotando aquí las equivalencias $(\neg a\lor b)\equiv (a\Rightarrow b)\equiv (\neg b\Rightarrow \neg a)$, tenemos dos aristas por cláusula, excepto aquellas con $(x_i\lor x_i)$ donde tenemos sólo una arista.

Esto da como resultado el dígrafo (grafo dirigido) $G=(V,E)$ como el que aparece en {numref}`SAT2`:

```{figura} ./images/Topic1/SAT2-Photoroom.png
---
nombre: SAT2
ancho: 600px
alinear: centro
altura: 500px
---
Una instancia de SAT2 para $n=5$ variables.
```
Luego, el problema SAT2 se **reformula de la siguiente manera** [(Aspvall, Plass y Tarjan, 1979)](https://www.sciencedirect.com/sdfe/pdf/download/eid/1-s2.0-0020019079900024/first-page-pdf):

*Dado un CNF-dígrafo $G=(V,E)$, el CNF codificado por él es satisfacible si y solo si no hay un componente fuertemente conectado $C_k$ donde $x_i\in C_k$ y $\neg x_i\in C_k$*.

En primer lugar, dos nodos $i,j\en V$ están <span style="color:#f88146">fuertemente conectados</span> si existe un camino dirigido $\Gamma_{ij}$ que los conecta. Por ejemplo, en {numref}`SAT2`, $i=x_2$ y $j=x_1$ están fuertemente conectados, ya que tenemos $\Gamma_{ij}=\{i=x_2\rightarrow x_3\rightarrow \neg x_6\rightarrow x_1=j\}
$. En realidad, todos los nodos en naranja oscuro pertenecen al mismo **componente fuertemente conectado** $C_8=\{x_1,x_2,x_3,
x_4,\neg x_6\}$. En resumen, podemos visitar todos los nodos en $C_8$ comenzando desde cualquiera de ellos.

Además, el componente conexo $C_8$ no incluye simultáneamente un $x_i$ y su negación $\neg x_i$. Si esto también ocurre en los demás componentes fuertemente conexos, entonces la función de fórmula estructural (fbf) es satisfacible. De hecho, esto es así, ya que los demás componentes del grafo anterior son

$$
C_1=\{\neg x_1\}, C_2=\{\neg x_2\}, C_3=\{\neg x_3\}, C_4=\{\neg x_4\}, C_5=\{x_5\}, C_6=\{x_6\}, C_7=\{\neg x_5\}
$$

Todas son *atómicas* y no existe la posibilidad de que contengan tanto una variable como su negación. Por lo tanto, la función de fórmula funcional (fbf) anterior es satisfacible. ¿Por qué? Básicamente porque, a partir de cualquier nodo, es imposible alcanzar una contradicción, es decir, tener $x_i$ y $\neg x_i$ en la misma componente. Esto es tan simple que no necesitamos realizar la demostración bidireccional (condición necesaria y suficiente).

¿Es SAT2 polinomial? Bueno, la pregunta ahora se reduce a determinar si los componentes fuertemente conectados de un dígrafo pueden encontrarse en tiempo polinomial. De hecho, cada componente puede encontrarse lanzando rutas y anotando su retorno, si ocurre, o declarando un componente atómico en caso contrario. Esta es la estrategia del [Algoritmo de Tarjan](https://en.wikipedia.org/wiki/Tarjan%27s_strongly_connected_components_algorithm), que toma $O(|V| + |E|)$.
Aquí utilizamos la [notación Big-O](https://web.mit.edu/16.070/www/lecture/big_o.pdfdonde)

$$
f(n):=O(g(n))\;\text{significa}\;\existe c: |f(n)
|\le c \cdot |g(n)|\; \forall n\ge 0.
$$

Por lo tanto, **SAT2 es polinomial** y, por lo tanto, **no es intratable**. Esto se expresa diciendo <span style="color:#f88146">$\text{SAT2}\not\in\text{NP}$</span>.

## El problema de la camarilla
Aunque podríamos reducir SAT2 a un problema polinómico (encontrar componentes fuertemente conexos), esto no ocurre con el *problema general de satisfacibilidad*, donde las cláusulas tienen *cualquier* $n>2$ número de literales. [Cook y Levin](https://en.wikipedia.org/wiki/Cook%E2%80%93Levin_theorem) lo demostraron en un teorema descrito en el segundo capítulo de Garey & Johnson. El teorema es atractivo y se basa en máquinas de Turing para demostrar que la función funcional nuclear (CNF) que resuelve el problema SAT puede tener un número exponencial de términos. Sin embargo, esta demostración queda fuera del alcance de este tema.

Sin embargo, aquí nos interesa demostrar *por qué* SAT es intratable (decimos <span style="color:#f88146">$\text{SAT}\in\text{NP}$</span>) *reduciendo otros problemas a él*. El primero de estos problemas es el <span style="color:#f88146">problema de la camarilla</span>.

### De SAT3 a Clique
La conexión entre SAT y Clique se establece transformando primero un problema SAT en un problema SAT3 donde todas las cláusulas tienen 3 literales. Esto se hace de la siguiente manera:

Dada una cláusula $(x_1\lor x_2\lor\ldots\lor x_m)$, la transformamos en $m-2$ cláusulas con $3$ literales:

$$
(x_1\lo x_2\lo \alfa_2)\lo (\neg \alfa_2\lo x_3\lo \alfa_3)\lo (\neg \alfa_3\lo x_4\lo \alfa_4)\lo \ldots\lo (\neg \alfa_{m-2}\lo x_{m-1}\lo x_m)\;,
$$

Donde $\alpha_2,\ldots,\alpha_{n-2}$ son *variables nuevas* que no modifican la satisfacibilidad de la cláusula original. ¿Por qué? Nótese que si $\alpha_i$ aparece en una subcláusula $i-1$, su negación $\neg\alpha_i$ aparece en la subcláusula $i$. Por lo tanto, esta variable no interfiere en la satisfacibilidad de la cláusula.

Ahora, si originalmente tenemos $c$ cláusulas, cada una con $n\ge m>3$ literales, entonces tenemos $O(m\cdot c)$ cláusulas que son lineales en el número de términos.

**Cliques máximos**. El propósito de la transformación anterior es construir un grafo $G=(V,E)$ donde tenemos $3\cdot c$ nodos ($3$ nodos por cláusula, porque cada cláusula tiene $3$ literales). El grafo $G$ no es dirigido y existe una arista $(i,j)\in E$ si:
- $i$ y $j$ pertenecen a cláusulas diferentes: $c(i)\neq c(j)$.
- $l_i$ y $l_j$, los literales respectivos, no inducen una contradicción: $l_i\neq \neg l_j$.


Por ejemplo, en {numref}`SAT2-clique` mostramos los nodos para la wff

$$
(x_1\lor x_2\lor \neg x_3)\land (\neg x_1\lor x_3\lor x_4)\land (x_2\lor x_3\lor \neg x_4)
$$

que no necesita ninguna transformación ya que todas las cláusulas tienen $3$ literales todavía. El
Los nodos correspondientes a la misma cláusula tienen el mismo color. Nótese que el literal $x_3$ lleva a
$2$ nodos diferentes (cláusulas naranja y amarilla) y aparece negado en la cláusula roja. En general, <span style="color:#f88146">la función de fórmula formal (fbf) es satisfacible si y solo si existe un grupo de $c=3$ nodos mutuamente interconectados</span>, como $\neg x_3$, $x_4$ y $x_2$. Dicho grupo de nodos forma un subgrafo completo $K_c$ o una <span style="color:#f88146">camarilla</span> cuyo *orden* es $c$.

En realidad, todas las camarillas de orden $c$ conducen a una interpretación válida de la función de fórmula estructural (fbf): $\neg x_3=1$, $x_4=1$ y $x_2=1$, es decir, $x_3=0$, $x_4=1$ y $x_2=1$, lo que hace que la fbf anterior sea verdadera. ¿Puedes encontrar otras camarillas (grupos de $c$ nodos completamente interconectados) en el grafo? Por supuesto que sí. Por ejemplo: $\neg x_3$, $\neg x_1$ y $\neg x_4$ conducen a $x_3=0$, $x_1=0$ y $x_4=0$, lo que también hace que la fbf sea verdadera.


```{figura} ./images/Topic1/SAT2-clique-Photoroom.png
---
nombre: SAT2-clique
ancho: 600px
alinear: centro
altura: 500px
---
Encontrar camarillas máximas en SAT3 para cláusulas $c=3$.
```

**Cliques no máximos**. Dado el grafo anterior $G=(V,E)$, su construcción garantiza que <span style="color:#f88146">el tamaño máximo de cualquiera de sus cliques sea $c$</span>, y esto ocurre, al menos para un clique, solo cuando la función de función forzada (fbf) codificada por el grafo es satisfacible. Por ejemplo, es bien sabido que una fbf no es satisfacible *si y solo si (si y solo si) la fbf es una contradicción*.

La contradicción más básica en CNF es

$$
x\land \neg x\;.
$$

Sin embargo, esto no está en formato SAT3. Para ello, procedemos de la siguiente manera:

$$
x \equiv (x\lor \alfa_1\lor \alfa_2)\land (x\lor \alfa_1\lor \neg\alfa_2)\land (x\lor \neg\alfa_1\lor \alfa_2)\land (x\lor \neg\alfa_1\lor\neg\alfa_2)
$$

y

$$
\neg x \equiv (\neg x\lor \beta_1\lor \beta_2)\land (\neg x\lor \beta_1\lor \neg\beta_2)\land (\neg x\lor \beta_1\lor \neg\beta_2)\land (\neg x\lor \neg\beta_1\lor\neg\beta_2)\;,
$$

es decir, cada cláusula atómica se reemplaza por la conjunción de $4$ cláusulas y esta conjunción es satisfacible solo si la cláusula atómica es satisfacible.

Bien, ahora solo tenemos que construir el grafo $G=(V,E)$ con $c=8$ cláusulas con $3$ nodos cada una ($24$ nodos en total). La nueva fórmula equivalente a $x\land\neg x$ será satisfacible si encontramos cualquier clique de tamaño $8$ en este grafo. ¿Realmente necesitamos construir el grafo para verificar este punto? En otras palabras, ¿podemos tener un subgrafo completo $K_8$ dentro del grafo de $24$ nodos si:
- Las variables en la misma cláusula no se pueden conectar.
- ¿Ninguna variable puede ser conectada con su negación?

Para construir una camarilla de tamaño $c=8$, necesitamos $8$ literales donde no podamos incluir tanto un literal como su negación. Una opción es obtener el conjunto $C=\{x^1,x^2,x^3,x^4,\alpha^1_1,\alpha^3_2,\beta^1_1,\beta^3_2\}$, donde los superíndices hacen referencia al número de la cláusula.
- Está claro que podemos formar una $4-$clique con los $x$s.
- No hay problema en ampliarlo a una camarilla $6$ incluyendo las $\beta$s.
- Podemos ir más allá y formar una $7$-camarilla incluyendo $\alpha^3_2$.

Sin embargo, para extender la $7$-clique, necesitamos incluir $\alpha^1_1$ (no hay otra posibilidad). Pero esto no es posible, ya que $\alpha^1_1$ y $x^1$ (aún incluidos) pertenecen a la misma cláusula y no hay arista entre ellos. Por lo tanto, la función de fórmula formal (fbf) no es satisfacible.

<span style="color:#f88146"> **Una lección importante de esta demostración** es que las camarillas son subconjuntos completamente conexos. Si se pueden crear, significa que sus miembros forman una clase de equivalencia.</span>

Además, agregar cláusulas solo conduce a complicar las cosas ya que el orden necesario para la satisfacibilidad se hace mayor.
<br></br>
<span style="color:#d94f0b">
**Ejercicio**. Consideremos ahora la siguiente cláusula: $x\lor \neg x$
lo cual es una tautología, es decir, es *totalmente satisfacible* (todas las asignaciones conducen a Verdadero).
<br></br>
En este caso, el problema SAT3 equivalente tiene dos cláusulas, es decir, $c=2$ (ver Garey & Johnson, página $48$):
<br></br>
</span>
<span style="color:#d94f0b">
$
(x\lor \neg x)\equiv (x\lor \neg x\lor \alpha_1)\land (x\lor \neg x\lor \neg\alpha_1)
$
</span>
<br></br>
<span style="color:#d94f0b">
Construya el gráfico asociado y determine la camarilla máxima.
</spah>
<br></br>
<span style="color:#d94f0b">
Respuesta: $G=(V,E)$ tendrá $V=\{x^1,\neg x^1,\alpha_1, x^2,\neg x^2,\neg\alpha_1\}$, es decir, $n=6$ nodos.
Los bordes (no dirigidos) son
</span>
<br></br>
<span style="color:#d94f0b">
$
\begin{align}
E &=\{(x^1,x^2),(x^1,\neg x^2),(x^1,\neg\alpha_1)\}\cup \{(\neg x^1,x^2),(\neg x^1,\neg x^2),(\neg x^1,\neg\alpha_1)\} \cup \{(\alpha_1,x^2),(\alpha_1,\neg x^2)\}\\
\fin{alinear}
$
</span>
<br></br>
<span style="color:#d94f0b">
Todos los subconjuntos máximos posibles de $V$ tienen tamaño $3$: $\{x^1,x^2,\alpha_1\}$, $(x^1,\neg x^2,\alpha_1)$, etc. Sin embargo, es imposible formar un grupo de tamaño $3$. ¿Por qué? Porque en todos estos subconjuntos debemos incluir dos literales de la misma cláusula o dos literales contradictorios, lo cual no coincide con el conjunto de aristas $E$. Como resultado, los grupos más grandes tienen tamaño $c=2$ (de hecho, cada arista en un grafo no dirigido es un grupo de $2$) y la fórmula es satisfacible como se esperaba (véase {numref}`SAT2-clique-ex`).
</span>

```{figura} ./images/Topic1/SAT2-clique-ex-Photoroom.png
---
nombre: SAT2-clique-ex
ancho: 500px
alinear: centro
altura: 400px
---
Encontrar camarillas máximas triviales en SAT3 para cláusulas $c=2$.
```

### De Clique a SAT3
Hasta ahora, sabemos que SAT3 siempre puede reducirse a un problema Clique equivalente (máximo). Como sabemos que <span style="color:#f88146">$\text{SAT3}\in\text{NP}$</span>, entonces <span style="color:#f88146">$\text{Clique}\in\text{NP}$</span>. De hecho, esto es todo lo que tenemos que hacer para demostrar si un problema <span style="color:#f88146">$\Pi\in \text{NP}$</span>:

1) Seleccione un problema conocido <span style="color:#f88146">$\Pi'\in\text{NP}$</span>.
2) Reduce <span style="color:#f88146">$\Pi$</span> a <span style="color:#f88146">$\Pi'$</span>.
3) Pruebe si la reducción es polinomial.


En la sección anterior, trabajamos en la parte *si* de la reducción, es decir, un SAT3 puede formularse como un problema de clique. Ahora, trabajamos en la parte *si**: cualquier problema de clique puede mapearse a un SAT3 equivalente. ¡Comencemos!

En Garey y Johnson, el problema de la camarilla se **formula de la siguiente manera** (página $47$):

*Dado un grafo (no dirigido) $G=(V,E)$ y un entero positivo $J\le|V|$, ¿el grafo contiene un
camarilla de tamaño $J$ o más, es decir un subconjunto $V'\subseteq V$ tal que $|V'|\ge J$
¿Y cada dos nodos en $V'$ están unidos por una arista en $E$*?

Obviamente, el concepto de clique solo tiene sentido en grafos no dirigidos. A continuación, en Garey & Johnson, la formulación de este problema resulta de reducir SAT3 a Cobertura de Vértices (VC), otro problema de NP, y luego este a clique. Aquí, pasamos directamente de SAT3 a clique de la siguiente manera:

[//]: https://www.youtube.com/watch?v=5PJDPIjIpYA

1) Dada una constante entera $c>0$, supongamos que $G=(V,E)$ tiene $|V|=3c$ y una camarilla de tamaño $J\ge c$. Como tenemos $3c$ nodos, denotamos cada grupo $C_r$ de $3$ nodos como $C_r=\{l_1^r,l_2^r, l^3_r\}$. Sin pérdida de generalidad (wlog), podemos suponer que $(l^{r}_i,l^{r}_j)\not\in E\;\forall i,j$.

2) Entonces, si existe una $J$-clique $V'$ *solo un nodo por grupo*, $C_r$ con $r=1\ldots c$ puede estar en ella, ya que necesitamos una conexión completa del rango $J$ y los nodos dentro de un grupo no están conectados. Si denotamos este nodo como $v_i^r\in V'$, establecemos $l_i^r=1$, lo que indica que el literal asociado con este nodo es Verdadero.

3) En realidad, $c$ denota el número de cláusulas. Pero recuerda que $J\le c$.

4) Si $J=c$ entonces, como hay un literal Verdadero por cláusula, entonces la función funcional definida asociada con el y de todas las cláusulas es satisfacible.

5) Si $J<c$, entonces, tener una $J$-clique significa que solo $J$ cláusulas pueden ser *simultáneamente* verdaderas. Esto es todo lo que podemos garantizar, por lo que la función de función formal asociada al grafo, sea cual sea, no es satisfacible.

Tenga en cuenta que el tamaño del grupo máximo es crucial para la satisfacibilidad. Cuantas más cláusulas tengamos, mayor será el grupo.

Además, la camarilla $J$ puede no ser única si existe. Todas las camarillas $J$ que encuentre corresponden a una forma de satisfacer la función de fórmula formal (lo que en lógica se denomina *interpretación*).

## Problemas relacionados con las camarillas
### Reconociendo problemas de NP

El problema de la camarilla es un problema NP paradigmático. Su **naturaleza es no polinómica** porque, <span style="color:#f88146">en el peor de los casos, nos vemos obligados a enumerar todos los subconjuntos de $V\subseteq 'V$</span>. Recuerde que si $n=|V|$ hay $O(2^n)$ subconjuntos para verificar si forman una camarilla o no.

Esto ilumina nuestra interpretación de SAT3: satisfacer una wff en CNF (todas las wff se pueden transformar a esta forma) significa encontrar un subconjunto de literales (al menos uno por cláusula) que sean simultáneamente Verdaderos.

Este <span style="color:#f88146">**sabor de subconjunto**</span> es común a muchos problemas de NP. Repasemos tres de ellos, estrechamente relacionados con el problema de Clique.

### Conjuntos independientes
Un <span style="color:#f88146">conjunto independiente</span> en un grafo G=(V,E) es un subconjunto $V'\subseteq V$ tal que para todos los pares $i,j$ en $V'$ la arista $(i,j)\no\está en V'$, es decir,*los nodos de $V'$ no son mutuamente adyacentes*.

El problema del conjunto independiente es:

*Dado un grafo (no dirigido) $G=(V,E)$ y un entero positivo $J\le|V|$, ¿el grafo contiene un conjunto independiente que tiene $|V'|\ge J$*?

Este problema se reduce automáticamente al problema de la camarilla al definir el *gráfico complementario* $\bar{G}=(V,\bar{E})$ de $G$ con $\bar{E}=\{(i,j)\in E\times E, (i,j)\not\in E\}$:

*Un conjunto independiente $V'\subset V$ de $G$ es una clique en $\bar{G}$*. En realidad, un conjunto independiente se denomina <span style="color:#f88146">anticlique</span>. En el ejercicio SAT3 anterior, ilustrado en {numref}`SAT2-clique-ex`, los conjuntos independientes crean cliques entre los literales de la misma cláusula y enlaces entre literales contradictorios de cláusulas diferentes. Véase {numref}`SAT3-independent-ex`

```{figura} ./images/Topic1/SAT3-independent-ex-Photoroom.png
---
nombre: SAT3-independent-ex
ancho: 500px
alinear: centro
altura: 400px
---
Conjunto independiente máximo para un SAT3 trivial.
```

Aplicados a SAT3, los conjuntos independientes máximos informan grupos de literales provenientes de la misma cláusula. El enlace de literales negados es binario, ya que cualquier otro enlace está permitido en SAT3.

Sin embargo, los conjuntos independientes son muy interesantes *per se*. Son clave para caracterizar el <span style="color:#f88146">problema de coloración de grafos</span>. Este problema consiste en *asignar el máximo número de colores diferentes a vértices no adyacentes*. Véase el siguiente artículo en [Wikipedia](https://en.wikipedia.org/wiki/Graph_coloring).

 
Véase {numref}`Color-ex`, donde coloreamos el grafo SAT3 en {numref}`SAT2-clique-ex`. Esta coloración se obtiene al encontrar los conjuntos independientes en {numref}`SAT3-independent-ex` y luego vincular solo los nodos con diferentes colores.

```{figura} ./images/Topic1/Color-ex-Photoroom.png
---
nombre: Color-ex
ancho: 500px
alinear: centro
altura: 400px
---
Colorear un SAT3 trivial.
```

El problema de la coloración $k-$ (decidir si un grafo acepta $k$ colores) es NP, excepto para $k\in\{0,1,2\}$. Las aplicaciones de este problema en la Inteligencia Artificial (IA) incluyen el <span style="color:#f88146">Sudoku</span>, donde los colores son los dígitos del $1 al $9$ (véase {numref}`Sudoku`).

```{figura} ./images/Topic1/Sudoku-Photoroom.png
---
nombre: Sudoku
ancho: 500px
alinear: centro
altura: 400px
---
Una solución para el juego Sudoku $3\times 3$ [Fuente](https://networkx.org/nx-guides/content/generators/sudoku.html).
```

Nótese que en un Sudoku de orden $n=3$ tenemos:
- $n=3\times 3$ colores.
- $n^2\times n^2 = n^4 = 81$ nodos dispuestos en una cuadrícula.  
- $n$ filas de tamaño $n$ en las que cada color aparece exactamente una vez.
- $n$ columnas de tamaño $n$ en las que cada color aparece exactamente una vez.
- $n\times n$ *subcuadrículas* donde cada color debe aparecer exactamente una vez.

Dos vértices distintos serán adyacentes *símplemente
Las celdas correspondientes de la cuadrícula están en la misma fila, columna o subcuadrícula*. Esto es importante, ya que algunas aristas están ocultas en {numref}`Sudoku`.

Por lo tanto, si etiquetamos los vértices como $(i,j)$ con $1\le i,j\le n^2$, hay una arista entre $(i,j)$ y $(i',j')$ si

$$
(i=i'\lor j=j')\lor (\lceil i/n\rceil = \lceil i'/n\rceil \land \lceil j/n\rceil = \lceil j'/n\rceil)\;,
$$

Donde $\lceil x \rceil$ denota la operación *ceil*, es decir, el entero más grande al que se redondea $x$. Por ejemplo, $\lceil 1/2 \rceil = \lceil 3/4 \rceil = 1$. En realidad, esta segunda parte de la fórmula determina si $(i,i)$ y $(i',j')$ pertenecen a la misma subcuadrícula.

La fórmula anterior asegura que cada fila, columna y subcuadrícula tenga una camarilla de tamaño $n^2$, es decir, tenemos $3n^2$ subgrafos completos $K_{n^2}$.

En otras palabras, dos nodos pertenecen a la misma camarilla si están en la misma fila, en la misma columna o en la misma subcuadrícula.

¿Significa esto que todos los conjuntos independientes máximos encontrados son soluciones válidas del juego Sudoku?

Exploremos esta pregunta en el siguiente ejercicio.
<br></br>
<span style="color:#d94f0b">
**Ejercicio**. Algunas preguntas sobre el Sudoku 2x2 ({numref}`Sudoku-4`): **a)** Caracterice el problema: número de colores, nodos, grado de los nodos, aristas y camarillas. **b)** Caracterice el grafo complementario y **c)** Asignar la solución de coloración a la búsqueda de conjuntos independientes mediante las camarillas máximas del grafo complementario ({numref}`Sudoku-4c`). ¿Son todos los conjuntos independientes máximos encontrados soluciones válidas del Sudoku?
</span>
```{figura} ./images/Topic1/Sudoku-4-ex-Photoroom.png
---
nombre: Sudoku-4
ancho: 400px
alinear: centro
altura: 300px
---
Una solución para el juego Sudoku $2\times 2$, es decir, con $4$ colores.
```
```{figura} ./images/Topic1/Sudoku-4c-ex-Photoroom.png
---
nombre: Sudoku-4c
ancho: 400px
alinear: centro
altura: 300px
---
Gráfico complementario del Sudoku $2\times 2$.
```
<br></br>
<span style="color:#d94f0b">
Respuesta:\
**a)** El Sudoku de 2x2 corresponde a 4 colores, del 1 al 4 (p. ej., naranja, rojo, verde y azul). Esto significa que $V=\{(i,j),1\le i,j\le 4\}$ (véanse las etiquetas de los nodos en las coordenadas (columna,fila) utilizadas por NetworkX en {numref}`Sudoku-4`). Por lo tanto, tenemos 16 nodos dispuestos en una cuadrícula de 4x4.
<br></br>
Hay un grupo por fila, columna y subcuadrícula. Algunos de estos grupos (los correspondientes a filas y columnas) no son visibles en {numref}`Sudoku-4`, pero debes considerarlos. Por ejemplo, los nodos $(1,4),(2,4),(3,4)$ y $(4,4)$ forman un grupo. También lo forman los nodos $(1,4),(1,2),(1,3)$ y $(1,4)$. Los $4$ grupos en las subcuadrículas son obvios: uno de ellos es $\{(1,4),(2,4),(1,3),(2,3)\}$. En resumen, como $n=2$, tenemos $3n^2=12$ grupos, todos de tamaño $4$.
<br></br>
Número de aristas: Hay una arista entre $(i,j)$ y $(i',j')$ cuando $
(i=i'\lor j=j')$ o $(\lceil i/2\rceil = \lceil i'/2\rceil \lceil j/2\rceil = \lceil j'/2\rceil)$.
Sin embargo, en lugar de contar las aristas manualmente, es mejor calcular el grado de cada nodo. Consideremos, por ejemplo, el vértice superior izquierdo $(1,4)$. Participa en $3$ grupos** (fila, columna y subcuadrícula), cada uno con $3$ nodos diferentes. Por lo tanto, su grado es $d=(3n + 1)(n - 1)=3\cdot 2 + 1=7$. ¿Por qué? Si un nodo participa en $3$ grupos de $n^2-1$ nodos, tenemos $3(n^2-1)$. Sin embargo, observe que algunas aristas en su fila y columna correspondientes se comparten con la subcuadrícula. De hecho, al descontarlas, las aristas en la subcuadrícula se convierten en $(n-1)^2=n^2 + 1 - 2n$ en lugar de $n^2 - 1$. Entonces, contamos las aristas de este grupo por separado:
</span>
<span style="color:#d94f0b">
$
2(n^2-1) + (n-1)^2 = 2n^2 - 2 + n^2 + 1 - 2n = 3n^2 - 2n - 1 = (3n + 1)(n-1).
$
</span>
<br></br>
<span style="color:#d94f0b">
**b)** El grafo complementario tiene los mismos nodos que el original, y las aristas son las que no están en el original (y no son bucles). Ahora, conectamos los nodos que no están en la misma fila, columna ni subcuadrícula. ¿Cuántos grupos tenemos aquí y cuál es su tamaño? Consultar {numref}`Sudoku-4c` resulta útil. Consideremos de nuevo el nodo $(1,4)$. Está conectado con $8$ nodos:
</span>
<span style="color:#d94f0b">
$4$ de ellos corresponden a la subcuadrícula y no comparten ninguna fila o columna con ella.
Los otros $4$ provienen de las $2$ subcuadrículas que comparten fila o columna.
</span>
<br></br>
<span style="color:#d94f0b">
Tenemos $n^2$ subcuadrículas: $1$ comparte fila y columna con un nodo dado, $(n-1)^2$ no comparten ni fila ni columna con ese nodo. Entonces
$n^2 - (n-1)^2 - 1=n^2 - [n^2+1-2n] - 1 = 2n -2$ comparten una fila o columna con ese vértice.
</span>
<br></br>
<span style="color:#d94f0b">
 Como cada subcuadrícula tiene $n^2$ nodos, un nodo dado en el gráfico complementario está vinculado con $[(n^2-n)\cdot (2n -2)]=4$ nodos relacionados con las subcuadrículas que comparten algunos elementos y con $[n^2\cdot (n-1)^2]=4$ nodos relacionados con las subcuadrículas que no comparten ninguno.
</span>
<br></br>
<span style="color:#d94f0b">
**c)** En este ejemplo, un nodo puede tener $8$ vecinos en el grafo complementario, pero tenga en cuenta que el propósito del Sudoku es obtener $n^2$ conjuntos independientes de tamaño $n^2$ cada uno. Al observar de nuevo el grafo complementario en {numref}`Sudoku-4c`, todos los nodos del mismo color pertenecen a los mismos grupos. Sin embargo, hay aristas adicionales que forman grupos con nodos de diferentes colores. En realidad, tenemos $n^4$ grupos en $n^2$ nodos cada uno en el grafo complementario. ¿Por qué?
<br></br>
Tenga en cuenta que al vincular un nodo con otras subcuadrículas, *solo un nodo de esta subcuadrícula puede tener el mismo color, por lo que los demás tienen colores diferentes*. Por lo tanto, **solo la mitad de los grupos en el gráfico de complementos son conjuntos independientes compatibles con las soluciones del Sudoku**. ¡Simplemente filtre los grupos cuyos colores no sean iguales!
</span>

### Cubiertas de vértices
Una <span style="color:#f88146">cubierta de vértices</span> $V'\subseteq V$ en $G=(V,E)$ es un subconjunto de nodos tal que $(i,j)\in E\Leftrightarrow (i\in V'\lor j\in V')$. Entonces, tenemos el siguiente problema NP:

*Dado un grafo $G=(V,E)$ y un entero positivo $J\le|V|$, ¿el grafo contiene un
cubierta de vértice de tamaño $J$ o menor, es decir, un subconjunto $V'\subseteq V$ tal que $|V'|\ge J$
y para cada arista $(i,j)\in E$, al menos uno de $i$ y $j$ pertenece a $V'$*?

Es obvio que ahora la *cobertura trivial* es $V$. Por lo tanto, generalmente nos interesan las <span style="color:#f88146">coberturas mínimas</span>, ya que una cobertura mínima *captura la esencia o el núcleo del grafo*. En este sentido, el problema de la cobertura de vértices es en cierto modo complementario al conjunto independiente y al clique. Más precisamente:

*Un grafo $G=(V,E)$ tiene una cubierta de vértices de tamaño $J$ si y solo si el grafo complementario $\bar{G}=(V,\bar{E})$ es una camarilla de tamaño $|V|-J$* que es equivalente a

*Un gráfico $G=(V,E)$ tiene una cubierta de vértices de tamaño $J$ si y solo si tiene un conjunto independiente de tamaño $|V|-J$*.

Véase, por ejemplo, el ejemplo en {numref}`Cover`. Los nodos naranjas son una cubierta de vértices de tamaño $J=3$. Los nodos amarillos están conectados al menos a un nodo de la cubierta y forman una camarilla en el grafo complementario.

```{figura} ./images/Topic1/Cover-Photoroom.png
---
nombre: Portada
ancho: 400px
alinear: centro
altura: 300px
---
Cobertura mínima de un gráfico (en naranja) y conjunto independiente (en amarillo).
```

Tenga en cuenta que el problema de cobertura divide el grafo en los nodos del núcleo y los restantes, que forman un conjunto independiente. Tenga en cuenta también que $J=3$ es el tamaño mínimo de cobertura para este grafo, pero puede no ser único (véase, por ejemplo, $\{2,3,4\}$, donde el conjunto independiente sería $\{1,5,6\}$).

Dada la relación anterior entre las cubiertas de vértices y los conjuntos independientes, su tamaño caracteriza la <span style="color:#f88146">colorabilidad de un grafo</span> (cuántos colores diferentes podemos asignar). En {numref}`Cover-color` mostramos que el número mínimo de colores, o número cromático $\alpha(G)$, para el grafo $G$ anterior es $3$. Sin embargo, es bien sabido que *si el tamaño de la cubierta es $J=k$, entonces el grafo admite $k+1$ colores (es $k+1$ coloreable)*. Demostrar esto es simple: se asigna un color *diferente* a cada uno de los $k$ nodos de la cubierta y luego se asigna el *mismo* color a los nodos del conjunto independiente. En el ejemplo anterior, podríamos asignar ($1=\text{rojo}$,$3=\text{verde}$,$4=\text{azul}$) y $\text{naranja}$ a $2$, $5$ y $6$ (es decir, $4$ colores). Esto se hace en {numref}`Maxcolor`.

```{figura} ./images/Topic1/Cover-color-Photoroom.png
---
nombre: Color de la cubierta
ancho: 400px
alinear: centro
altura: 300px
---
Coloración mínima de un gráfico.
```

```{figura} ./images/Topic1/Colorability-Photoroom.png
---
nombre: Maxcolor
ancho: 400px
alinear: centro
altura: 300px
---
Coloración máxima de un gráfico.
```

### Reducción de SAT3
Encontrar conjuntos independientes (IS) y cubrevértices (VC) es equivalente debido a su relación con el problema de la clique. Sin embargo, esto no garantiza que <span style="color:#f88146">$\text{IS}\in \text{NP}$</span> y <span style="color:#f88146">$\text{VC}\in \text{NP}$</span>. Para demostrarlo, debemos demostrar que cualquiera de ellos está en NP. Siguiendo a Garey y Johnson, demostramos que **VC puede reducirse a SAT3**.

La prueba consta de **dos pasos**:
1) <span style="color:#f88146">Crear un grafo</span> $G=(V,E)$ que codifique el SAT3 desde una perspectiva de cobertura de vértices. Este grafo debe crearse en tiempo polinomial.
2) <span style="color:#f88146">Demuestre</span> que existe una cubierta de vértice de tamaño $J\le |V|$ (cubierta mínima) en $G$ si y solo si las cláusulas codificadas en ella son satisfacibles.

<span style="color:#f88146">**Crear un grafo**</span>. Dadas $m$ cláusulas $C_1,\ldots,C_m$ y $n$ variables $x_1,\ldots,x_n$, la construcción del grafo $G=(V,E)$ consiste en:
- Una camarilla de 3 nodos por cláusula $C_i$ que vincula sus literales.
- Una camarilla de 2 nodos (dipolo) $D_i$ por variable $x_i$ donde tenemos $x_i$ y su negación $\neg x_i$.

Luego procedemos a agregar aristas adicionales entre las cláusulas-camaras y los dipolos uniendo los literales homónimos como mostramos {numref}`CoverSAT1` donde tenemos solo $m=2$ cláusulas y $n=3$ variables:

$$
(x_1\lo\neg x_2\lo\neg x_3)\l(\neg x_1\lo\neg x_2\lo\neg x_3)
$$

y hemos coloreado literales compatibles en los dipolos y camarillas con el mismo color.

```{figura} ./images/Topic1/Cover-SAT1-Photoroom.png
---
nombre: CoverSAT1
ancho: 500px
alinear: centro
altura: 400px
---
SAT3 como cobertura de vértice. Ejemplo de construcción.
```

La "magia" de esta construcción se basa en asignar un valor de verdad $1$ a *algunos de los vértices* incluidos en una cubierta de vértices de $G$ y $0$ en caso contrario.

Recuerde que una cobertura $V'\subseteq V$ es *un subconjunto de $V$ donde todas las aristas $E$ de $G$ son alcanzables (cubiertas) desde los vértices de $V'$*. Entonces
Tenemos 3 aristas por clique de cláusula, 2 aristas por dipolo y no más de 3 millones de aristas entre cliques y dipolos. Por lo tanto, el grafo se crea en tiempo polinomial.
- Para cubrir $G$ necesitamos tomar **al menos** dos nodos por clique de cláusula y también **al menos** un nodo por dipolo.

Por ejemplo,
- Para cubrir la primera cláusula, si ponemos solo el nodo superior $\neg x_3$ en la cubierta, el borde entre los otros dos no queda cubierto, y de manera similar para la segunda cláusula con $x_2$.
- Una vez que sabemos que necesitamos dos nodos para cubrir $3$ aristas en una 3-clique, es obvio que solo necesitamos un nodo para cubrir un dipolo.
- Los nodos en los dipolos $D_i$ cubren, además de los bordes de sus contrapartes, los bordes de las camarillas de cláusula o los bordes entre los nodos en el dipolo y las camarillas de cláusula.
- Por tanto una posible cobertura sería:

$$
V' = \underbrace{\{x_1,\neg x_2\}}_{C_1}\cup \underbrace{\{\neg x_1,\neg x_3\}}_{C_2}\cup\underbrace{\{\neg x_1\}}_{D_1}
\cup\underbrace{\{x_2\}}_{D_2}
\cup\underbrace{\{\neg x_3\}}_{D_3}\;.
$$

Nótese que al asignar valores verdaderos $1$ a los nodos de la cobertura $V'$ provenientes de los dipolos, es decir, $\neg x_1=1$, $x2=1$ y $\neg x_3=1$, se satisfacen todas las cláusulas. Por lo tanto, la *interpretación lógica* $x_3=x_1=0,x_2=1$ hace que la CNF sea satisfacible. Codificamos esto coloreando en naranja los nodos pertenecientes a $V'$ en {numref}`CoverSAT2`.

**Coberturas de vértices y conjuntos independientes**. Recuerde que decir que $V'\subseteq V$ es una cobertura de tamaño $J\le |V|$ equivale a decir que $V - V'$ es un conjunto independiente. En {numref}`CoverSAT2`, los nodos del conjunto independiente correspondiente a $V'$ están coloreados en amarillo. Nótese que el tamaño del conjunto independiente es $|V|-J=5$, mientras que el tamaño de la cobertura es $J=2m + n = 7$. Más adelante demostraremos que este es el tamaño necesario para que la FNC sea satisfacible. Sin embargo, en este punto, encontrar un conjunto independiente de tamaño $|V|-(2m + n)$ es una buena manera de encontrar coberturas que hagan que la FNC sea satisfacible. Si solo podemos encontrar conjuntos independientes más pequeños, la FNC no es satisfacible.   

```{figura} ./images/Topic1/Cover-SAT2-Photoroom.png
---
nombre: CoverSAT2
ancho: 500px
alinear: centro
altura: 400px
---
Los nodos amarillos no pertenecen a la cubierta.
```
<br></br>
<span style="color:#d94f0b">
**Ejercicio**. Dado el SAT3 en {numref}`CoverSAT1`, identifique las coberturas donde **NO** se cumplen las dos cláusulas. Compárelas con la cobertura satisfacible en {numref}`CoverSAT2`.
<br></br>
Respuesta. Tenemos $2^{n=3}$ asignaciones de verdad. Cuando $(\neg x_3 = 1) \equiv (x_3=0)$, la CNF se satisface, y esto ocurre $2^2$ veces (en negrita en la tabla a continuación). De lo contrario, la CNF se satisface cuando $x_1=x_2=1$ o $x_1=x_2=0$.
<br></br>
Mirando la tabla de verdad anterior
</span>
<span style="color:#d94f0b">
<br></br>
$
\begin{alineado}
&\begin{array}{ccc|c|c|}
\hline \hline x_1 y x_2 ​​y x_3 y (x_1\lor\neg x_2\lor\neg x_3) y (\neg x_1\lor x_2\lor\neg x_3) y \text{CNF} \\
\hline
0 y 0 y \mathbf{0} y 1 y 1 y 1 \\
0 y 0 y 1 y 1 y 1 y 1 \\
0 y 1 y \mathbf{0} y 1 y 1 y 1 \\
0 y 1 y 1 y 0 y 1 y 0 \\
1 y 0 y \mathbf{0} y 1 y 1 y 1 \\
1 y 0 y 1 y 1 y 1 y 0 \\
1 y 1 y \mathbf{0} y 1 y 1 y 1 \\
1 y 1 y 1 y 1 y 1 y 1 \\
\hline
\fin{matriz}
\end{alineado}
$
</span>
<br></br>
<span style="color:#d94f0b">
Sólo un par de interpretaciones son *contramodelo*.
<br></br>
**Primer caso:** $x_1=0,x_2=1,x_3=1$. Esto significa que los nodos de la cobertura en los dipolos deben ser: $\neg x_1$, $x_2$ y $x_3$. Los literales restantes deben estar en el conjunto independiente. Esto nos obliga a colocar el literal $\neg x_3$ en $C_1$ en la cobertura; es decir, ampliamos la cobertura y reducimos el conjunto independiente. El tamaño de la cobertura ahora es $2m + n + 1$ (véase {numref}`CoverSAT3`) y la fórmula no es satisfactible.
<br></br>
</span>
```{figura} ./images/Topic1/Cover-SAT3-Photoroom.png
---
nombre: CoverSAT3
ancho: 500px
alinear: centro
altura: 400px
---
Cobertura no satisfacible. Los nodos amarillos no pertenecen a la cobertura.
```
<br></br>
<span style="color:#d94f0b">
**Segundo caso:** $x_1=1,x_2=0,x_3=1$. Esto significa que los nodos de la cubierta en los dipolos deben ser: $x_1$, $\neg x_2$ y $x_3$. Los literales restantes deben estar en el conjunto independiente. Esto nos obliga a colocar los literales $\neg x_3$ en $C_1$ y $x_2$ en $C_2$ en la cubierta. Como resultado, debemos eliminar el literal $\neg x_2$ de la cubierta y colocarlo en el conjunto independiente. El tamaño de la cubierta es nuevamente $2m + n + 1$ (véase {numref}`CoverSAT4`) y la fórmula no es satisfacible.
<br></br>
</span>
```{figura} ./images/Topic1/Cover-SAT4-Photoroom.png
---
nombre: CoverSAT4
ancho: 500px
alinear: centro
altura: 400px
---
Cobertura no satisfacible. Los nodos amarillos no pertenecen a la cobertura.
```
<br></br>
<span style="color:#f88146">**Demuestre la equivalencia:
<br></br>
$\text{Cover}\Rightarrow \text{SAT3}$**</span>. Supongamos que $G=(V,E)$ tiene una cobertura $V'\subseteq V$ de orden $J=2m + n$. Esto significa que $V'$ tiene un vértice por dipolo (tenemos $n$ dipolos) y dos vértices por cláusula (tenemos $m$ cláusulas). Compruébelo observando los nodos naranjas de {numref}`CoverSAT2`. En realidad, los nodos amarillos de cada dipolo codifican los valores de verdad *no seleccionados* para una asignación SAT (seleccionamos los valores de verdad del nodo naranja del dipolo: $\neg x_1=1$,$x_2=1$,$\neg x_3=1$).
<br></br>
<span style="color:#f88146">**$\text{SAT3}\Rightarrow\text{Cover}$**</span>. Supongamos ahora que el problema SAT3, codificado por $G=(V,E)$, es satisfacible. Como resultado, *al menos* un literal de cada cláusula $C_i$ es verdadero. Recuerde que cada cláusula $C_i$ está codificada por una 3-clique. Por construcción, sabemos que $G=(V,E)$ tendrá una cobertura $V'\subseteq V$ de tamaño $J=2m + n$. Esto significa que dos nodos por 3-clique (cláusula) cubren todas las aristas de la clique. Sin embargo, también cubren las aristas entre las 3-cliques y los dipolos. Exactamente una arista por cláusula cubrirá una arista con una asignación de verdad, ya que no podemos cubrir ambos nodos del dipolo. Entonces, si la CNF es satisfacible, tendrá una cobertura de tamaño $J=2m + n$.



## Ciclo hamiltoniano
El siguiente problema es un problema NP clásico en IA:

*Dado un grafo $G=(V,E)$, ¿es $G$ un ciclo hamiltoniano, es decir una ordenación $<v_1,v_2,\ldots,v_n>$ de los vértices de $G$ donde $n=|V|$ tal que $(v_n,v_1)\in E$ y $(v_{i},v_{i+1})\in E$, $\forall i,1\le i<n$*?

Este es el conocido problema del ciclo hamiltoniano (HC): debemos encontrar un ciclo o recorrido que visite *todos* los nodos *una vez*. El problema es NP porque, en lugar de buscar subconjuntos (<span style="color:#f88146">**sabor de subconjunto**</span>), buscamos *todos los ordenamientos de un conjunto* $<v_1,v_2,\ldots,v_n>$. Dada una permutación $\pi:V\rightarrow V$, la solución tiene la forma $<v_{\pi(1)},v_{\pi(2)},\ldots,v_{\pi(n)}>$. Recuerde que hay $n!$ ordenamientos posibles y buscar si alguno de ellos es un ciclo hamiltoniano no es polinomial en absoluto.

Sin embargo, demostrar que <span style="color:#f88146">$\text{HC}\in \text{NP}$</span> merece una reducción a cualquiera de los problemas NP. Tanto los Conjuntos Independientes (IS) como la Cobertura de Vértices (VC) son NP, es decir, <span style="color:#f88146">$\text{IS}\in \text{NP}$</span> y <span style="color:#f88146">$\text{VC}\in\text{NP}$</span>, ya que pueden reducirse al problema Clique, que es NP.

Sin embargo, la reducción de HC al problema de Clique es bastante compleja y difícil de entender. Incluso en el texto de Garey y Johnson, reducen HC al VC. Aquí, utilizamos un enfoque más simple y, a la vez, más intuitivo: <span style="color:#f88146">¡reducimos HC al problema SAT3!</span>

Recuerde que una reducción es una condición necesaria y suficiente, es decir, un si y solo si. Diseñemos una construcción donde la solución del HC esté codificada en un grafo.

Comenzamos mapeando la <span style="color:#f88146">Camino Hamiltoniano</span> (HP), en cambio, a SAT3:

*Dado un grafo $G=(V,E)$, ¿es $G$ un camino hamiltoniano, es decir una ordenación $<v_1,v_2,\ldots,v_n>$ de los vértices de $G$ donde $n=|V|$ tal que $(v_{i},v_{i+1})\in E$, $\forall i,1\le i<n$*?


```{figura} ./images/Topic1/Hamiltonian-gadget-removebg-preview.png
---
nombre: HPtoSAT3
ancho: 700px
alinear: centro
altura: 600px
---
Mapeo dígrafo de HP a SAT3. Los nodos amarillos codifican las variables (más una variable adicional).
```

El núcleo de la construcción, que se muestra en {numref}`HPtoSAT3`, se denomina <span style="color:#f88146">**dispositivo variable**</span> donde:

1. Para cada vértice $v_i\in V$ de $G$, tenemos un par de variables: $x_i$ y $x_{i+1}$. En realidad, tenemos $n+1$ variables donde $n=|V|$. Estas variables se muestran en amarillo.

2. Es un **dígrafo** (grafo dirigido), que comienza en el vértice superior $x_1$ y desciende hasta el vértice inferior $x_{n+1}$. Por lo tanto, en la figura, tenemos $n=3$ variables en el SAT3 (aún por mapear) y $x_4$ es una variable adicional.

3. Nótese que, al descender de $x_1$ a $x_4$, podemos seguir el camino **izquierdo** (en azul) y el camino **derecho** (en rojo). En cada $x_i$ podemos cambiar de color (de azul a rojo o de rojo a azul). Como resultado, <span style="color:#f88146">**podríamos tener $2^n$ caminos diferentes de $x_1$ a $x_4$**</span>.

4. Debajo de cada $x_i$, $i=1,2,\ldots,n$ tenemos un **gráfico de caminos** bidireccional con nodos $x_i$\_$p_1$ a $x_i$\_$p_{3\cdot c}$ donde $c$ es el **número de cláusulas**: $c=3$ en este caso.

5. Estos grafos de trayectoria permiten continuar de izquierda a derecha, de derecha a izquierda o cambiar de sentido para alcanzar el siguiente **nivel** $x_{i+1}$. Sin embargo, *si queremos visitar todos los nodos $x_1$ a $x_4$ que pasan por los grafos de trayectoria <span style="color:#f88146">**una vez**</span>, debemos <span style="color:#f88146">**elegir uno de los sentidos**</span> en cada grafo de trayectoria*.

6. Asociamos un <span style="color:#f88146">**valor de verdad**</span> a cada ruta. En la figura, las rutas "Verdaderas" tienen todas sus aristas en "azul" y las "Falsas" en "rojas". Las aristas negras se interpretan como "azules" (Verdaderas) si van de izquierda a derecha y como "rojas" (Falsas) en caso contrario. Este **truco de construcción** es clave para forzar una ruta hamiltoniana de $x_1$ a $x_4$ que recorra todos los nodos del grafo construido.

7. Sin embargo, aún debemos <span style="color:#f88146">**coincidir con una ruta hamiltoniana "Verdadera"** con una solución SAT, si la hay</span>. De lo contrario, la ruta hamiltoniana será falsa.

8. Para ello, usamos $c$ **modos adicionales** $c_i$ (uno por cláusula). ¿Cómo los usamos?

Bueno, en {numref}`HPtoSAT3` asumimos la siguiente CNF:

$$
\underbrace{(x_1\lor x_2\lor \neg x_3)}_{c_1}\land \underbrace{(x_1\lor x_2\lor x_3)}_{c_2}\land \underbrace{(x_1\lor x_2\lor \neg x_3)}_{c_3}
$$

Procedemos de la siguiente manera:

1. Como $x_1$ es "positivo" (Verdadero) en $c_1$, debemos convertir $x_1\rightarrow x_1\_p_1$, luego ir a $c_1$ usando una **cláusula de borde verde** y luego regresar a esta ruta a través de $c_1\rightarrow x_1\_p_2$. De esta manera, podemos avanzar hacia la derecha a través de $x_1\_p_3$.

2. A continuación, estamos en $x_1\_p_4$ (el primero de un grupo de $3$ nodos que codifican la función de la variable $x_1$ en la cláusula $c_2$). Nótese que, como $x_1$ también es positivo en $c_2$, vamos a $c_2$ y regresamos como antes, y luego regresamos a $x_1\_p_5$. A continuación, repetimos la misma codificación para la función de $x_1$ en $c_3$.

3. En este punto, aún no hemos visitado $c_1$, $c_2$ y $c_3$ porque $x_1$ es positivo en todos ellos. <span style="color:#f88146">**Aún sabemos que la CNF es safistificable**, pero aún tenemos que progresar para visitar todos los nodos del dígrafo una vez (camino hamiltoniano)</span>. ¿Podemos hacerlo?

4. Por supuesto. Como $x_1$ es "Verdadero" en todas las cláusulas, solo necesitamos descender por $x_2$ y proceder de izquierda a derecha desde $x_2\_p_1,\ldots,x_2\_p_9$ sin visitar ningún nodo de la cláusula. Luego descender por $x_3$ y repetir el proceso hasta llegar a $x_4$, donde hemos completado la siguiente ruta hamiltoniana:

$$
\begin{align}
x_1, y x_1\_p_1, \mathbf{c_1}, x_1\_p_2, x_1\_p_3,x_1\_p_4, \mathbf{c_2}, x_1\_p_5, x_1\_p_6, x_1\_p_7, \mathbf{c_3}, x_1\_p_8, x_1\_p_9\\
x_2, y x_2\_p1,\ldots,x_2\_p_9\\
x_3, y x_3\_p1,\ldots,x_3\_p_9\\
x_4. & \\
\fin{alinear}
$$

5. Dado que $x_2$ es 'Verdadero' en todas las cláusulas, podemos proceder de manera similar, lo que conduce al siguiente camino

$$
\begin{align}
x_1, y x_1\_p1,\ldots,x_1\_p_9\\
x_2, y x_2\_p_1, \mathbf{c_1}, x_2\_p_2, x_2\_p_3,x_2\_p_4, \mathbf{c_2}, x_2\_p_5, x_2\_p_6, x_2\_p_7, \mathbf{c_3}, x_2\_p_8, x_2\_p_9\\
x_3, y x_3\_p1,\ldots,x_3\_p_9\\
x_4. & \\
\fin{alinear}
$$

6. Sin embargo, $x_3$ es negativo tanto en $c_1$ como en $c_3$, y positivo en $c_2$. Esto *implica que $x_3$ contribuye a que la CNF sea insatisfactoria*. En otras palabras, <span style="color:#f88146">esperar para visitar los nodos de la cláusula hasta el nivel $3$ **no conduce a un camino hamiltoniano**, ya que allí debemos ir tanto de derecha a izquierda como de izquierda a derecha</span>. Los nodos de la cláusula deben visitarse antes del nivel $3$.

Por lo tanto, la construcción anterior muestra que HP es reducible a SAT3, es decir: *hay un HP en el gráfico anterior solo si la CNF es satisfacible*.

Extender este resultado al **Ciclo Hamiltoniano** (HC) es sencillo: simplemente crea un vínculo hacia atrás entre $x_4$ y $x_1$.
<br></br>
<span style="color:#d94f0b">
**Ejercicio**. Dado el SAT3 $(x_1\lor x_2\lor \neg x_3 )\l y (\neg x_1\lor\neg x_2\lor x_3)$, que es claramente insatisfactorio (una variable y su negación están presentes en todas las cláusulas), planteamos lo siguiente: **a)** Construir la construcción HC y **b)** Demostrar que no tiene ciclos hamiltonianos.
</span>
<br></br>
<span style="color:#d94f0b">
Respuesta. Mostramos tres construcciones HC en {numref}`HPtoSAT3Ex`. Nótese que tenemos $3\cdot 2 = 6$ nodos por grafo de trayectorias, ya que hay $c=2$ cláusulas.
<br></br>
```{figura} ./images/Topic1/Hamiltonian-gadget-Excercise-removebg-preview.png
---
nombre: HPtoSAT3Ex
ancho: 700px
alinear: centro
altura: 600px
---
Mapeo dígrafo de HP a SAT3. Los nodos amarillos codifican las variables (más una variable adicional).
```
<br></br>
</span>
<span style="color:#d94f0b">
Obsérvese que los dos primeros grafos de trayectorias llegan primero a $c_1$ de izquierda a derecha, lo que indica que $x_1$ y $x_2$ deben ser "Verdaderos", respectivamente, pero acceden en orden inverso a $c_2$, donde deben ser "Falsos". Con el tercer grafo de trayectorias, se obtiene lo contrario, ya que $x_3$ debe ser falso en $c_1$ y verdadero en $c_2$. Por lo tanto, es imposible dibujar un ciclo hamiltoniano en el grafo de {numref}`HPtoSAT3Ex`.
</span>



<!--
Las cubiertas de vértices tienen dos aplicaciones principales en IA:
- En primer lugar, dada su relación con conjuntos independientes, su tamaño caracteriza la <span style="color:#f88146">colorabilidad de un gráfico</span> (cuántos colores diferentes podemos asignar).
- En segundo lugar, su significado central los hace útiles para demostrar la completitud NP de otros problemas, como el hallazgo del <span style="color:#f88146">ciclo hamiltoniano</span> (un ciclo que visita todos los nodos del gráfico una vez) si existe.

**k-Colorabilidad**. En {numref}`Cover-color` mostramos que el número mínimo de colores, o número cromático $\alpha(G)$, para el grafo $G$ anterior es $3$. Sin embargo, es bien sabido que *si el tamaño de la cubierta es $J=k$, entonces el grafo admite $k+1$ colores (es $k+1$ coloreable)*. Demostrar esto es simple: asigne un color *diferente* a cada uno de los $k$ nodos en la cubierta y luego asigne el *mismo* color a los nodos en el conjunto independiente. En el ejemplo anterior, podríamos asignar ($1=\text{rojo}$,$3=\text{verde}$,$4=\text{azul}$) y $\text{naranja}$ a $2$, $5$ y $6$ (es decir, $4$ colores).

```{figura} ./images/Topic1/Cover-color-Photoroom.png
---
nombre: Color de la cubierta
ancho: 400px
alinear: centro
altura: 300px
---
Coloración mínima de un gráfico.
```

**Ciclos hamiltonianos**. Para determinar si un grafo tiene un ciclo hamiltoniano, se formula de la siguiente manera:

*Dado un grafo $G=(V,E)$, ¿es $G$ un ciclo hamiltoniano, es decir una ordenación $<v_1,v_2,\ldots,v_n>$ de los vértices de $G$ donde $n=|V|$ tal que $(v_n,v_1)\in E$ y $(v_{i},v_{i+1})\in E$, $\forall i,1\le i<n$*?

 En este caso, el <span style="color:#f88146">**sabor de subconjunto**</span> no es tan obvio. Detectar ciclos hamiltonianos en $G=(V,E)$ requiere explorar todas las permutaciones $P(n)$, donde $n=|V|$, y determinar si alguna de ellas implementa un ciclo que visite todos los vértices exactamente una vez.
-->




<!--
**Un problema sencillo**. Por ejemplo, dado un grafo dirigido $G=(V,E)$ (un **dígrafo**), considere su matriz de adyacencia $\mathbf{A}\in\{0,1\}^{n\times n}$
donde $n=|V|$ es el número de nodos. Un problema simple que involucra $\mathbf{A}$ es *calcular de cuántas maneras se puede acceder a un nodo desde otro en dos saltos*. Luego
- Dado que el problema involucra nodos, el gráfico se puede parametrizar mediante $n$.
La matriz de adyacencia nos indica cómo llegar a un nodo $i$ desde otro $j$ *en un salto*. En resumen, si $\mathbf{A}_{ij}=1$, entonces $j$ es accesible desde $j$ *en un salto*.

Sean $\mathbf{a}_{i:}$ y $\mathbf{a}_{:j}$, respectivamente, la fila del nodo $i$ y la columna del nodo $j$ en $\mathbf{A}$. Los $1$ en $\mathbf{a}_{i:}$ son los nodos vecinos de $i$. De forma similar, los $1$ en $\mathbf{a}_{:j}$ son los nodos vecinos de $j$. Entonces, *$j$ es accesible desde $i$ en dos saltos* si tienen (al menos) un vecino común $k$, llamado **pivote**, de modo que $\mathbf{A}_{ik}=1$ y $\mathbf{A}_{kj}=1$. Por lo tanto, $\mathbf{a}_{ik}=\mathbf{a}_{kj}=1$ (hay un $1$ en la posición $k$) tanto en $\mathbf{a}_{i:}$ como en $\mathbf{a}_{:j}$. Por lo tanto, el número de maneras de llegar a $j$ desde $i$ es

$$
\left<\mathbf{a}_{i:},\mathbf{a}_{j:}\right>:=\sum_k \mathbf{a}_{ik}\mathbf{a}_{kj}\;,
$$

Donde $\left<,\right>$ es el producto escalar. Esto se puede calcular en $O(n)$ (tiempo lineal). Aquí, utilizamos la notación Big-O.

$$
f(n):=O(g(n))\;\text{significa}\;\existe c: |f(n)
|\le c \cdot |g(n)|\; \forall n\ge 0.
$$

Si queremos calcular la accesibilidad de dos saltos entre cualquier par de nodos, debemos calcular $n^2$ productos escalares por par $(i,j)\in V\times V$. Ahora la complejidad es $O(n^3)$ (cúbica). En esencia, lo que hacemos es calcular $\mathbf{A}^2$. La complejidad en el peor caso de la multiplicación de matrices es en realidad $O(n^3)$, aunque puede realizarse en $O(n^{2.371552})$ desde el año pasado. Consulta las complejidades de las operaciones matriciales en [Wikipedia](https://en.wikipedia.org/wiki/Computational_complexity_of_matrix_multiplication).

[//]: https://cs.stackexchange.com/questions/1147/complexity-of-computing-matrix-powers

¿Qué sucedería si ahora se nos pidiera **calcular accesibilidades de $k$ saltos** con $k > 2$? Por supuesto, esto se puede hacer calculando $\mathbf{A}^k$, que requiere $O(n^3\cdot\log k)$. Sin embargo, calcular los autovalores (almacenados en la matriz diagonal $\Lambda$) y sus autovectores (almacenados en la matriz $\Phi$) requiere $O(n^3)$. Entonces, el *teorema espectral* conduce a $\mathbf{A}^k=\Phi\Lambda^k\Phi^T$. Dado que calcular $\Lambda^k$ (la potencia de una matriz diagonal) requiere $O(n\log k)$, tenemos una complejidad total de $O(n^3 + n\log k)$.

**Problemas insolubles**. Un vértice $j$ es accesible desde $i$ en $k$ saltos si $\mathbf{A}^{k}_{ij}=1$. Por lo tanto, existe un *camino* $\Gamma=\{i=i_{1},i_{2},\ldots,i_k=j\}$ de longitud $k$ entre $i$ y $j$. En realidad, si $i=j$, tenemos un *circuito* o *ciclo* de longitud $k$ sobre $i$. Sin embargo, dicho circuito/ciclo no tiene ningún significado especial más allá de su longitud. En la vida real, sin embargo, nos interesa encontrar circuitos con propiedades especiales, es decir, *que cubran todos los nodos de una vez*. Esto es extremadamente útil para diseñar rondas para robots, planificar torneos justos y secuenciar ADN, entre otras aplicaciones. Buscamos entonces un ciclo <span style="color:#f88146">hamiltoniano</span>. Sin embargo, responder a la pregunta "¿existe algún ciclo hamiltoniano?" es un problema insoluble. ¿Por qué? Algunas consideraciones:
Los ciclos hamiltonianos, si existen, tienen una longitud $n+1$. Por lo tanto, podríamos investigar la diagonal de $\mathbf{A}^{n+1}$ y comprobar los elementos $\mathbf{A}^{n+1}_{ii}\neq 0$. Si todos son cero, ¡tenemos suerte! Sin embargo, este no es el caso en muchos <span style="color:#f88146">casos</span> del problema: **todos** son distintos de cero (por ejemplo, si el grafo no es dirigido y completo).
Para cada $\mathbf{A}^{n+1}_{ii}\neq 0$, debemos investigar todos los caminos $\Gamma=\{i=i_{1},i_{2},\ldots,i_k=j\}$ de longitud $n$ que comienzan en $i$ y terminan en cada $j$ donde $\mathbf{A}_{ji}=1$. Si alguno de ellos *visita todos los nodos una vez*, se proporciona la respuesta. Si ninguno lo hace, también se proporciona la respuesta.
- Matemáticamente, *visitar todos los nodos una vez* significa que $\Gamma = \text{sort}(V)$, es decir, $\Gamma$ se da reordenando $V$ de una manera particular a determinar.


Para llegar a los nodos *en dos saltos* se requiere calcular $\mathbf{A}^2 = \mathbf{A}\mathbf{A}$, es decir, se requiere un producto matricial. ¿Qué tan difícil es...?  
-->