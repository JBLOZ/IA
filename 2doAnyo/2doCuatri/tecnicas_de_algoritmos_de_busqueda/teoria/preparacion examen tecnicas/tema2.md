# Recocido simulado y determinista

## Subgrafo común máximo

**Motivación**. Los compuestos químicos presentan patrones estructurales comunes a los compuestos de la misma familia. Uno de estos patrones es la estructura circular (hexagonal) formada por átomos de carbono (C) unidos por enlaces simples o dobles (véase {numref}`Aspirina`-Izquierda y Centro), donde los vértices no marcados representan átomos de C. En este ejemplo, la presencia del anillo hexagonal en la popular [Aspirina](https://pubchem.ncbi.nlm.nih.gov/compound/Aspirin) ({numref}`Aspirina`-Derecha) es bien conocida.

El desarrollo de técnicas de coincidencia de patrones de IA para la detección de subestructuras ha impulsado el campo de la bioinformática. Hoy en día, el análisis de conjuntos de datos de proteínas en constante crecimiento, como el Banco de Datos de Proteínas [PDB](https://www.wwpdb.org/) o de compuestos químicos como [PubChem](https://pubchem.ncbi.nlm.nih.gov/), es fundamental en la IA.

```{figura} ./images/Topic2/MCS-Aspirina-Photoroom.png
---
nombre: Aspirina
ancho: 800px
alinear: centro
altura: 300px
---
Estructura de la aspirina.
```

**MCS**. Comparar subestructuras no es un problema sencillo. Mientras que comparar subcadenas es polinomial, comparar subestructuras es un problema de NP bien conocido llamado <span style="color:#f88146">Máximo Común Subgrafo</span> o MCS:

*Dados dos gráficos $G_1=(V_1,E_1)$ y $G_2=(V_2,E_2)$, ¿cuál es el gráfico $H=(V,E)$ que es *común* a $G_1$ y $G_2$ con el número máximo de nodos*?

Aquí, *común* significa lo siguiente: $V = V\subseteq V_1$ y $E\subseteq E_1$ y existe una aplicación inyectiva (uno a uno) $f:V\rightarrow V_2$ tal que $(i,j)\in E$ si y solo si $(f(i),f(j))\in E_2$.

Esta <span style="color:#f88146">**sabor de subconjunto**</span> aclara el hecho de que <span style="color:#f88146">$\text{MCS}\in \text{NP}$</span>. En realidad, MCS no solo busca un subconjunto común, sino *el subconjunto con el número máximo de nodos*.

Esto queda bastante claro en el siguiente problema de *Breaking Bad*: <span style="color:#f88146">¿Cuál es la coincidencia estructural entre el éxtasis y la anfetamina?</span>.
- Según PubChem, la [éctasica](https://pubchem.ncbi.nlm.nih.gov/compound/3_4-Methylendioxymethamphetamine) se deriva de la [anfetamina](https://pubchem.ncbi.nlm.nih.gov/compound/Amphetamine).
- Mirando el Centro de Drogas {numref} (Éctasy)
proviene de eliminar un átomo de hidrógeno de la anfetamina ({numref}`Drogas`-Derecha), agregando un carbono y un ciclo pentagonal oxígeno-carbono.
- El MCS está en {numref}`Drogas`-Izquierda.

```{figura} ./images/Topic2/Drogas-Photoroom.png
---
nombre: Drogas
ancho: 800px
alinear: centro
altura: 200px
---
Subestructura común máxima (izquierda) de dos fármacos de diseño (centro y derecha).
```

Todas las figuras han sido generadas por el [RDKit: software quimioinformático de código abierto](https://www.rdkit.org/).


## Correspondencia de gráficos
Para resolver MCS mediante una aproximación polinomial es necesario *encontrar la función inyectiva* $f$ entre los vértices $V$ del grafo pequeño $X=(V,E)$ y los $V'$ del grafo más grande $Y=(V',E')$ en tiempo polinomial.

### Asignaciones y emparejamientos

**Asignación de nodos**. Considere los grafos (no dirigidos):

$$
\begin{alineado}
&\begin{matriz}{cll}
\text{Gráfico} y \text{Nodos} y \text{Aristas}\\
X y V=\{a,b,c\} y E=\{(a,b),(b,c)\}\\
Y & V'=\{1,2,3,4,5\} & E=\{(1,2),(1,3),(1,4),(3,4)\}\\
\fin{matriz}
\end{alineado}
$$

Como $n=|V'|=5$ y $r=|V|=3$, tenemos $P(n,r)=n\cdot (n-1)\cdot (nr + 1)$ **r-permutaciones**, es decir, funciones biunívocas $f$ o <span style="color:#f88146">**asignaciones de nodos**</span> que pueden ser soluciones potenciales al problema de MCS. En este caso, tenemos $P(5,3)=5\cdot 4\cdot 3=60$ asignaciones diferentes. Entonces, ¿<span style="color:#f88146">qué asignaciones proporcionan el MCS entre $X$ e $Y$</span>?

Para los grafos $X$ e $Y$ el tamaño del MCS es $2$, ya que $X$ tiene sólo dos aristas y si es un subgrafo de $Y$ (como realmente lo es), el tamaño del MCS tiene $|V|=3$ nodos y |E|=2$ aristas.

Sin embargo, esto depende de la calidad de la función inyectiva $f$. Para la de {numref}`Matching`, tenemos:

$$
f(a)=1,\; f(b)=2\;\text{y}\; f(c)=3\;.
$$

Como podemos ver, $(a,b)\in E$ y $(1=f(a),2=f(b))\in E'$. Sin embargo, para la otra arista $(b,c)\in E$ tenemos que $(2=f(b),3=f(c))\not\in E'$: Como resultado, $X$ e $Y$ <span style="color:#f88146">**solo tienen una arista común para $f$**</span> (en magenta).


```{figura} ./images/Topic2/Matching1-Photoroom.png
---
nombre: Coincidencia
ancho: 600px
alinear: centro
altura: 400px
---
Subestructura común no máxima.
```

Consideremos ahora la tarea:

$$
f(a)=1,\; f(b)=4\;\text{y}\; f(c)=5\;.
$$

Lo cual de hecho conduce a un MCS:

```{figura} ./images/Topic2/Matching2-Photoroom.png
---
nombre: Matching2
ancho: 600px
alinear: centro
altura: 400px
---
Una subestructura común máxima.
```

Sin embargo, esta asignación MCS **no es única**. En realidad, tenemos ${5 \choose 3}=10$ subgrafos de $Y$ donde podemos *incrustar* $X$, pero solo $8$ de ellos conducen a asignaciones MCS. En la tabla anterior, codificamos cada función inyectiva MCS $f_i$ como una lista de <span style="color:#f88146"> **emparejamientos por pares** $(v\in V, f_i(v)\in V')$</span>:

$$
\begin{alineado}
&\begin{matriz}{cl}
\text{Inyección} y \text{Asignación MCS} \\
f_1 y [(a, 1), \mathbf{(b, 4)}, (c, 5)]\\
f_2 y [(a, 2), \mathbf{(b, 1)}, (c, 3)]\\
f_3 y [(a, 2), \mathbf{(b, 1)}, (c, 4)]\\
f_4 y [(a, 3), \mathbf{(b, 1)}, (c, 2)]\\
f_5 y [(a, 3), \mathbf{(b, 1)}, (c, 4)]\\
f_6 y [(a, 4), \mathbf{(b, 1)}, (c, 2)]\\
f_7 y [(a, 4), \mathbf{(b, 1)}, (c, 3)]\\
f_8 y [(a, 5), \mathbf{(b, 4)}, (c, 1)]\\
\fin{matriz}
\end{alineado}
$$

**Vértices notables**. En la tabla anterior, observe que las asignaciones MCS suelen contener emparejamientos entre nodos con grados altos (vértices notables) en ambos grafos, es decir, $\mathbf{b}$ y $\mathbf{1}$ o $\mathbf{4}$ (en negrita). Estos emparejamientos son $\mathbf{(b,1)}$ y $\mathbf{(b,4)}$.

En el siguiente ejercicio enfatizamos el vínculo entre los subgrafos de $Y$ y las asignaciones de MCS, que es un concepto fundamental en este tema.
<br></br>
<span style="color:#d94f0b">
**Ejercicio**. Identifica los ${5 \choose 3}=10$ subgrafos de tamaño $3$ en $Y$ (indicando nodos y aristas) y:\
**a)** Detecta los que corresponden a una incrustación completa de $X$ en $Y$.**b)** Identifica estos subgrafos en las $8$ asignaciones MCS de la tabla anterior.
<br></br>
**NOTA**. Expresar siempre las aristas en **orden lexicográfico**, es decir, $(i,j)$ si $i<j$.
<br></br>
Respuesta. **a)** Los subgrafos son las $10$ combinaciones de los $5$ nodos $V'=\{1,2,3,4,5\}$ en grupos de $3$ nodos (porque $|V|=3$). Sin embargo, solo los subgrafos conexos pueden dar lugar a una incrustación completa de $X$ en $Y$:
</span>
<br></br>
<span style="color:#d94f0b">
$
\begin{alineado}
&\begin{matriz}{cclc}
\text{Subgrafo} & \text{Nodos} & \text{Aristas} & \text{¿Está conectado?}\\
s_1 & V_1'=(1, 2, 3) & E_1'=\{(1,2),(1,3)\} & \checkmark \\
s_2 & V_2'=(1, 2, 4) & E_2'=\{(1,2),(1,3)\} & \checkmark \\
s_3 & V_3'=(1, 2, 5) & E_3'=\{(1,2)\}&\\
s_4 & V_4'=(1, 3, 4) & E_4'=\{(1,3),(1,4)\}& \marca de verificación\\
s_5 & V_5'=(1, 3, 5) & E_5'=\{(1,3)\}&\\
s_6 & V_6'=(1, 4, 5) & E_6'=\{(1,4),(1,5)\}& \marca de verificación\\
s_7 y V_7'=(2, 3, 4) y E_7'=\conjunto vacío &\\
s_8 y V_8'=(2, 3, 5) y E_8'=\conjunto vacío &\\
s_9 & V_9'=(2, 4, 5) & E_9'=\{(4,5)\} &\\
s_{10} & V_{10}'=(3, 4, 5) & E_{10}'=\{(4,5)\} &\\
\fin{matriz}
\end{alineado}
$
</span>
<br></br>
<span style="color:#d94f0b">
**b)** Tenemos que solo los subgrafos $s_1$, $s_2$, $s_4$ y $s_6$ pueden acomodar el grafo completo $X$. En teoría de grafos, decimos que estos subgrafos son **isomorfos** a $Y$. Nótese que cada uno de estos subgrafos conduce a $2$ asignaciones de MCS en la tabla de inyección anterior:
</span>
<br></br>
<span style="color:#d94f0b">
$
\begin{alineado}
V_1'&=(1,2,3)\rightarrow f_2=[(a,2),(b,1),(c,3)],\; f_4=[(a,3),(b,1),(c,2)]\\
V_2'&=(1,2,4)\rightarrow f_3=[(a,2),(b,1),(c,4)],\; f_6=[(a,4),(b,1),(c,2)]\\
V_4'&=(1,3,4)\rightarrow f_5=[(a,3),(b,1),(c,4)],\; f_7=[(a,4),(b,1),(c,3)]\\
V_6'&=(1,4,5)\rightarrow f_1=[(a,1),(b,4),(c,5)],\; f_5=[(a,5),(b,4),(c,1)]\\
\end{alineado}
$
</span>
<br></br>

### Regla del rectángulo: Función de costo
Hasta ahora, la resolución de MCS gira en torno a la idea de <span style="color:#f88146">**maximizar el número de emparejamientos por pares**</span> entre los gráficos $X$ e $Y$.

Para un humano, es bastante claro adoptar una *estrategia codiciosa*:
1. Identifica vértices notables en $V$ y $V'$.
2. Para cada par coincidente entre nodos notables:
  - Ampliar los pares coincidentes a los vecinos.
  - Incrementa el número de rectables según corresponda.

Las máquinas requieren una especificación más precisa. Sin embargo, maximizar el número de rectángulos se logra con el siguiente procedimiento:

*Dados $a\in V$ y $i\in V'$, aparece un rectángulo si:*
 1. *Emparejamos $a$ y $i$*
 2. *Emparejamos $b$ y $j$, que son vecinos respectivos de $a$ e $i$: $b\in {\cal N}_a$ y $j\in {\cal N}_i$.*

 En otras palabras, se forma un rectángulo cuando emparejamos dos nodos y sus vecinos respectivos también. Precisamente por eso preferimos emparejamientos por pares entre vértices notables: porque es más probable que produzcan más rectángulos.

 Este razonamiento conduce a la <span style="color:#f88146">**variante de segundo orden**</span> de MCS, también conocida como <span style="color:#f88146">**Coincidencia de Gráficos**</span> dentro de la comunidad de Reconocimiento de Patrones. De hecho, al plantear el problema en términos matriciales, tenemos:
 - Las matrices de adyacencia $\mathbf{X}\in\{0,1\}^{m\times m}$ y $\mathbf{Y}\in\{0,1\}^{n\times n}$ de los grafos $X$ e $Y$.
 - La <span style="color:#f88146">**matriz coincidente**</span> desconocida $\mathbf{M}\in\{0,1\}^{n\times m}$, donde $\mathbf{M}_{ia}=1$ significa que $i\in V$ coincide con $a\in V'$.

Por lo tanto, existe un rectángulo si *sus cuatro lados existen*, es decir, si

$$
\existe a,b\en V, \existe i,j\en V':\; \mathbf{M}_{ai}\mathbf{M}_{bj}\mathbf{X}_{ab}\mathbf{Y}_{ij}>0\;,
$$

donde $\mathbf{X}_{ab}$ y $\mathbf{Y}_{ij}$ codifican las respectivas reglas vecinas (lados del rectángulo) como mostramos en {numref}`Rectangle`.


```{figura} ./images/Topic2/Rectangle-Photoroom.png
---
nombre: Rectángulo
ancho: 600px
alinear: centro
altura: 400px
---
La regla del rectángulo en la correspondencia de gráficos.
```

**Función de Costo Cuadrático**. Una función que cuenta el número de rectángulos dados por una matriz coincidente $\mathbf{M}$ es simplemente:

$$
F(\mathbf{M}) = \frac{1}{2}\sum_{a\in V}\sum_{i\in V'}\sum_{b\in V}\sum_{j\in V'}\mathbf{M}_{ai}\mathbf{M}_{bj}\mathbf{X}_{ab}\mathbf{Y}_{ij}\;,
$$

donde el factor $1/2$ elimina los rectángulos contados dos veces (ver la explicación a continuación).

Consideremos, por ejemplo, los grafos $X$ e $Y$ de la sección anterior (véase {numref}`Matching`). Contemos el número de rectángulos para un emparejamiento particular utilizando la formulación matricial y la función anterior.

En primer lugar, tenemos las matrices de adyacencia

$$
\begin{align}
\mathbf{X} =
\begin{array}{l}
a\\
b\\
do\\
\fin{matriz}
\begin{bmatrix}
0 y 1 y 0 \\
1 y 0 y 1 \\
0 y 1 y 0 \\
\fin{bmatrix}
\;\;
\mathbf{Y} =
\begin{array}{l}
1\\
2\\
3\\
4\\
5\\
\fin{matriz}
\begin{bmatrix}
0 y 1 y 1 y 1 y 0\\
1 y 0 y 0 y 0 y 0\\
1 y 0 y 0 y 0 y 0\\
1 y 0 y 0 y 0 y 1\\
0 y 0 y 0 y 1 y 0\\
\fin{bmatrix}
\fin{alinear}
$$

La matriz de coincidencia para la asignación en {numref}`Matching2` está dada por

$$
\begin{align}
\mathbf{M} =
\begin{array}{l}
a\\
b\\
do\\
\fin{matriz}
\begin{bmatrix}
1 y 0 y 0 y 0 y 0\\
0 y 0 y 0 y 1 y 0\\
0 y 0 y 0 y 0 y 1\\
\fin{bmatrix}
\;\;\text{donde}\;\;
\mathbf{M}^T =
\begin{array}{l}
1\\
2\\
3\\
4\\
5\\
\fin{matriz}
\begin{bmatrix}
1 y 0 y 0 \\
0 y 0 y 0 \\
0 y 0 y 0 \\
0 y 1 y 0 \\
0 y 0 y 1 \\
\fin{bmatrix}
\fin{alinear}
$$

Arreglemos la versión matricial de $F(\mathbf{M})$.
1) **Mapeo**. Comenzamos analizando el producto $\mathbf{X}\mathbf{M}$, que mapea los nodos en $X$ con los de $Y$ mediante la matriz de correspondencia $\mathbf{M}$:

$$
(\mathbf{X}\mathbf{M})_{ai} = \mathbf{X}_{a:}\mathbf{M}_{:i} = \sum_{a}\sum_{b}\mathbf{X}_{ab}\mathbf{M}_{bi}
$$

En nuestro ejemplo:

$$
\mathbf{X}\mathbf{M} =
\begin{array}{l}
a\\
b\\
do\\
\fin{matriz}
\begin{bmatrix}
0 y 1 y 0 \\
1 y 0 y 1 \\
0 y 1 y 0 \\
\fin{bmatrix}
\cdot
\begin{bmatrix}
1 y 0 y 0 y 0 y 0\\
0 y 0 y 0 y 1 y 0\\
0 y 0 y 0 y 0 y 1\\
\fin{bmatrix}
=
\begin{bmatrix}
0 y 0 y 0 y 1 y 0\\
1 y 0 y 0 y 0 y 1\\
0 y 0 y 0 y 1 y 0\\
\fin{bmatrix}
$$

Cada columna de $\mathbf{M}$ tiene *como máximo* un $1$, tenemos:

$$
(\mathbf{X}\mathbf{M})_{ai} = \mathbf{X}_{ab^{\ast}}\mathbf{M}_{b^{\ast}i}
$$

donde $b^{\ast}\in {\cal N}_a$ es el vecino de $a$ que coincide con $i$, si lo hay. Por lo tanto:

$$
(\mathbf{X}\mathbf{M})_{ai} = \mathbf{X}_{ab^{\ast}}\mathbf{M}_{b^{\ast}i}=1\Rightarrow \exists\; \text{ruta}\; a\rightarrow b^{\ast}\rightarrow i\in {\cal M}\;,
$$

donde ${\cal M}$ es el <span style="color:#f88146">**gráfico coincidente**</span> (incluye enlaces de $X$, $Y$ y $M$ como en {numref}`Matching2`).

Por lo tanto, $\mathbf{X}\mathbf{M}$ tiene los siguientes caminos en ${\cal M}$ (uno por cada $1$ en la matriz):

$$
\begin{align}
(\mathbf{X}\mathbf{M})_{a4}&=a\rightarrow b\rightarrow 4\\
(\mathbf{X}\mathbf{M})_{b1}&=b\rightarrow a\rightarrow 1\\
(\mathbf{X}\mathbf{M})_{b5}&=b\rightarrow c\rightarrow 5\\
(\mathbf{X}\mathbf{M})_{c4}&=c\rightarrow b\rightarrow 4\\
\fin{alinear}
$$

Por ejemplo, mostramos las rutas anteriores en {numref}`MPaths1` y {numref}`MPaths2`.

```{figura} ./images/Topic2/MatchingPaths1-Photoroom.png
---
nombre: MPaths1
ancho: 600px
alinear: centro
altura: 400px
---
Rutas coincidentes $b\rightarrow a\rightarrow 1$ y $b\rightarrow c\rightarrow 5$.
```

```{figura} ./images/Topic2/MatchingPaths2-Photoroom.png
---
nombre: MPaths2
ancho: 600px
alinear: centro
altura: 400px
---
Rutas coincidentes $a\rightarrow b\rightarrow 4$ y $c\rightarrow b\rightarrow 4$.
```

2) **Caminos**. Continuamos analizando el producto $(\mathbf{X}\mathbf{M})\mathbf{Y}$. Intuición: dado que $\mathbf{X}\mathbf{M}$ proporciona caminos en ${\cal M}$ entre nodos adyacentes en $X$ y luego atraviesa el $\mathbf{M}$ correspondiente hasta llegar a nodos en $Y$, el producto $(\mathbf{X}\mathbf{M})\mathbf{Y}$ simplemente *continúa estos caminos*: algunos terminarán en $Y$ *definiendo $3/4$ lados de un rectángulo* (ver más abajo) y otros simplemente pasan por $Y$ sin definir ningún rectángulo.

En nuestro ejemplo:

$$
(\mathbf{X}\mathbf{M})\mathbf{Y} =
\begin{array}{l}
a\\
b\\
do\\
\fin{matriz}
\begin{bmatrix}
0 y 0 y 0 y 1 y 0\\
1 y 0 y 0 y 0 y 1\\
0 y 0 y 0 y 1 y 0\\
\fin{bmatrix}
\cdot\;
\begin{array}{l}
1\\
2\\
3\\
4\\
5\\
\fin{matriz}
\begin{bmatrix}
0 y 1 y 1 y 1 y 0\\
1 y 0 y 0 y 0 y 0\\
1 y 0 y 0 y 0 y 0\\
1 y 0 y 0 y 0 y 1\\
0 y 0 y 0 y 1 y 0\\
\fin{bmatrix} =
\begin{bmatrix}
\mathbf{1} y 0 y 0 y 0 y 1\\
0 y 1 y 1 y \mathbf{2} y 0\\
1 y 0 y 0 y 0 y \mathbf{1}\\
\fin{bmatrix}
$$

Entonces, los siguientes caminos **sí** forman $3/4$ de un rectángulo (en negrita en $(\mathbf{X}\mathbf{M})\mathbf{Y}$):

$$
\begin{align}
((\mathbf{X}\mathbf{M})\mathbf{Y})_{a1} &= a\rightarrow b\rightarrow 4\rightarrow 1\\
((\mathbf{X}\mathbf{M})\mathbf{Y})_{b4} &= b\rightarrow a\rightarrow 1\rightarrow 4 + b\rightarrow c\rightarrow 5\rightarrow 4\\
((\mathbf{X}\mathbf{M})\mathbf{Y})_{a1} &= a\rightarrow b\rightarrow 4\rightarrow 1\\
\fin{alinear}
$$

donde son significativos los $2$ caminos de $((\mathbf{X}\mathbf{M})\mathbf{Y})_{b4}$ entre los nodos $b\in V$ y $4\in V'$ (ver {numref}`MPaths3`):

```{figura} ./images/Topic2/MatchingPaths3-Photoroom.png
---
nombre: MPaths3
ancho: 600px
alinear: centro
altura: 400px
---
Dos caminos coincidentes $3/4$ $b\rightarrow a\rightarrow 1\rightarrow 4$ y $b\rightarrow c\rightarrow 5\rightarrow 4$.
```


Por otro lado, estos otros caminos **no** forman $3/4$ de un rectángulo:

$$
\begin{align}
((\mathbf{X}\mathbf{M})\mathbf{Y})_{a5} &= a\rightarrow b\rightarrow 4\rightarrow 5\\
((\mathbf{X}\mathbf{M})\mathbf{Y})_{b2} &= b\rightarrow a\rightarrow 1\rightarrow 2\\
((\mathbf{X}\mathbf{M})\mathbf{Y})_{b3} &= b\rightarrow a\rightarrow 1\rightarrow 3\\
((\mathbf{X}\mathbf{M})\mathbf{Y})_{c1} &= c\rightarrow b\rightarrow 4\rightarrow 1\\
\fin{alinear}
$$

Por ejemplo, los caminos $a\gg b\rightarrow 4\gg 5$ y $c\gg b\rightarrow 4\gg 1$ divergen de los rectángulos.
donde la notación $\gg$ denota el primer y el último borde de las rutas (ver {numref}`MPaths4`).

```{figura} ./images/Topic2/MPaths4-Photoroom.png
---
nombre: MPaths4
ancho: 600px
alinear: centro
altura: 400px
---
Los caminos $a\gg b\rightarrow 4\gg 5$ y $c\gg b\rightarrow 4\gg 1$ divergen de los rectángulos.
```

De manera similar, los caminos $b\gg a\rightarrow 1\gg 2$ y $b\gg a\rightarrow 1\gg 3$ divergen aún más claramente de terminar en rectángulos (ver {numref}`MPaths5`).

```{figura} ./images/Topic2/MPaths5-Photoroom.png
---
nombre: MPaths5
ancho: 600px
alinear: centro
altura: 400px
---
Caminos divergentes restantes en ${\cal M}$.
```

3) **Cerrar rectángulos**. Una vez que tenemos $(\mathbf{X}\mathbf{M})\mathbf{Y}$, simplemente realizamos una multiplicación *punto a punto* (producto de Hadamard) para cerrar el rectángulo:

$$
((\mathbf{X}\mathbf{M})\mathbf{Y})\odot \mathbf{M}\;.
$$

En nuestro ejemplo:

$$
((\mathbf{X}\mathbf{M})\mathbf{Y})\odot \mathbf{M} =
\begin{bmatrix}
\mathbf{1} y 0 y 0 y 0 y 1\\
0 y 1 y 1 y \mathbf{2} y 0\\
1 y 0 y 0 y 0 y \mathbf{1}\\
\end{bmatrix}\odot
\begin{bmatrix}
1 y 0 y 0 y 0 y 0\\
0 y 0 y 0 y 1 y 0\\
0 y 0 y 0 y 0 y 1\\
\fin{bmatrix} =
\begin{bmatrix}
\mathbf{1} y 0 y 0 y 0 y 0\\
0 y 0 y 0 y \mathbf{2} y 0\\
0 y 0 y 0 y 0 y \mathbf{1}\\
\fin{bmatrix}
$$

Tenga en cuenta que $a$ cierra el rectángulo $1$, $c$ cierra $1$ y $b$ cierra $2$ (uno para $a$ y otro para $c$). Por lo tanto, la multiplicación $((\mathbf{X}\mathbf{M})\mathbf{Y})\odot \mathbf{M}$ simplemente **filtra** los rectángulos imposibles. El resultado está en {numref}`MPaths6`.

```{figura} ./images/Topic2/MPaths6-Photoroom.png
---
nombre: MPaths6
ancho: 600px
alinear: centro
altura: 400px
---
Rectángulos finales en ${\cal M}$.
```

4) **Contando**. Tenga en cuenta que el número de rectángulos proviene naturalmente de

$$
F(\mathbf{M}) = \frac{1}{2}\sum_{a}\sum_{i}(((\mathbf{X}\mathbf{M})\mathbf{Y})\odot \mathbf{M})_{ai}\;,
$$

Que en este caso es 2, como era de esperar. Repasemos estos conceptos en el siguiente ejercicio:

<br></br>
<span style="color:#d94f0b">
**Ejercicio**. Dados los siguientes gráficos $X$ e $Y$:
</span>
<br></br>
<span style="color:#d94f0b">
$
\begin{alineado}
&\begin{matriz}{cll}
\text{Gráfico} y \text{Nodos} y \text{Aristas}\\
X y V=\{a,b,c\} y E=\{(a,b),(b,c)\}\\
Y & V'=\{1,2,3,4,5\} & E=\{(1,2),(1,3),(2,4),(3,4),(1,5),(2,5)\}\\
\fin{matriz}
\end{alineado}
$
</span>
<br></br>
<span style="color:#d94f0b">
**a)** Dibújalos de modo que la asignación $f=[(a,1),(b,2),(c,3)]$ sea claramente visible. ¿Es $X$ un subgrafo de $Y$? De ser así, ¿cuál es el número máximo de rectángulos que se deben cerrar en ${\cal M}(f^{\ast})$ y encontrar una asignación óptima $f^{\ast}$?
</span>
<br></br>
```{figura} ./images/Topic2/MiniMatch-Photoroom.png
---
nombre: Mini
ancho: 600px
alinear: centro
altura: 400px
---
Gráfico coincidente ${\cal M}$ para $f=[(a,1),(b,2),(c,3)]$.
```
<br></br>
<span style="color:#d94f0b">
En {numref}`Mini`, mostramos una proyección 3D de ambos grafos donde la asignación es claramente visible. Claramente, $X$ es un subgrafo de $Y$. Como resultado, podemos mapear todos los vértices y aristas de $X$ a $Y$, cerrando como máximo $3$ rectángulos.
</span>
<br></br>
<span style="color:#d94f0b">
**b)** ¿Esa asignación óptima es única? Calcule el número máximo de rectángulos evaluando matricialmente $M^{\ast}$, la matriz coincidente correspondiente a una asignación óptima. Indique las **rutas coincidentes** en cada paso.
</span>
<br></br>
<span style="color:#d94f0b">
En este caso la asignación óptima es única: proviene de hacer coincidir los vértices notables entre ambos grafos y es $f=[(a,1),(b,2),(c,5)]$ ya que esta es la única manera de incrustar $X$ en $Y$ completamente (ver {numref}`Mini2`).
</span>
<br></br>
```{figura} ./images/Topic2/MiniMatch2-Photoroom.png
---
nombre: Mini2
ancho: 600px
alinear: centro
altura: 400px
---
Gráfico coincidente ${\cal M}$ para $f=[(a,1),(b,2),(c,5)]$.
```
<br></br>
<span style="color:#d94f0b">
Matricularmente, tenemos
</span>
<br></br>
<span style="color:#d94f0b">
$
\begin{align}
\mathbf{X} =
\begin{array}{l}
a\\
b\\
do\\
\fin{matriz}
\begin{bmatrix}
0 y 1 y 1 \\
1 y 0 y 1 \\
1 y 1 y 0 \\
\fin{bmatrix}
\;\;
\mathbf{Y} =
\begin{array}{l}
1\\
2\\
3\\
4\\
5\\
\fin{matriz}
\begin{bmatrix}
0 y 1 y 1 y 0 y 1\\
1 y 0 y 0 y 1 y 1\\
1 y 0 y 0 y 1 y 0\\
0 y 1 y 1 y 0 y 0\\
1 y 1 y 0 y 0 y 0\\
\fin{bmatrix}
\;\;\texto{y}\;\;
\mathbf{M}^{\ast} = \begin{array}{l}
a\\
b\\
do\\
\fin{matriz}
\begin{bmatrix}
1 y 0 y 0 y 0 y 0 \\
0 y 1 y 0 y 0 y 0 \\
0 y 0 y 0 y 0 y 1 \\
\fin{bmatrix}
\fin{alinear}
$
</span>
<br></br>
<span style="color:#d94f0b">
Luego procedemos a evaluar
</span>
<br></br>
<span style="color:#d94f0b">
 $
F(\mathbf{M}^{\ast}) = \frac{1}{2}\sum_{a}\sum_{i}(((\mathbf{X}\mathbf{M}^{\ast})\mathbf{Y})\odot \mathbf{M}^{\ast})_{ai}\;,
 $
</span>
<br></br>
<span style="color:#d94f0b">
**Paso 1:** Calcular $\mathbf{X}\mathbf{M}^{\ast}$:
</span>
<br></br>
<span style="color:#d94f0b">
$
\begin{align}
\mathbf{X}\mathbf{M}^{\ast} =
\begin{array}{l}
a\\
b\\
do\\
\fin{matriz}
\begin{bmatrix}
0 y 1 y 1 \\
1 y 0 y 1 \\
1 y 1 y 0 \\
\fin{bmatrix}
\;\cdot \;
\begin{array}{l}
a\\
b\\
do\\
\fin{matriz}
\begin{bmatrix}
1 y 0 y 0 y 0 y 0 \\
0 y 1 y 0 y 0 y 0 \\
0 y 0 y 0 y 0 y 1 \\
\fin{bmatrix} =
\begin{bmatrix}
0 y 1 y 0 y 0 y 1\\
1 y 0 y 0 y 0 y 1\\
1 y 1 y 0 y 0 y 0\\
\fin{bmatrix}
\fin{alinear}
$
</span>
<br></br>
<span style="color:#d94f0b">
Y los caminos hasta ahora son:
</span>
<br></br>
<span style="color:#d94f0b">
$
\begin{align}
(\mathbf{X}\mathbf{M}^{\ast})_{a2} &= a\rightarrow b\rightarrow 2\\
(\mathbf{X}\mathbf{M}^{\ast})_{a5} &= a\rightarrow c\rightarrow 5\\
(\mathbf{X}\mathbf{M}^{\ast})_{b1} &= b\rightarrow a\rightarrow 1\\
(\mathbf{X}\mathbf{M}^{\ast})_{b5} &= b\rightarrow c\rightarrow 5\\
(\mathbf{X}\mathbf{M}^{\ast})_{c1} &= c\rightarrow a\rightarrow 1\\
(\mathbf{X}\mathbf{M}^{\ast})_{c2} &= c\rightarrow b\rightarrow 2\\
\fin{alinear}
$
</span>
<br></br>
<span style="color:#d94f0b">
**Paso 2:** Calcular $(\mathbf{X}\mathbf{M}^{\ast})\mathbf{Y}$:
</span>
<br></br>
<span style="color:#d94f0b">
$
\begin{align}
(\mathbf{X}\mathbf{M}^{\ast})\mathbf{Y} =
\begin{array}{l}
a\\
b\\
do\\
\fin{matriz}
\begin{bmatrix}
0 y 1 y 0 y 0 y 1\\
1 y 0 y 0 y 0 y 1\\
1 y 1 y 0 y 0 y 0\\
\fin{bmatrix}
\cdot\;
\begin{array}{l}
1\\
2\\
3\\
4\\
5\\
\fin{matriz}
\begin{bmatrix}
0 y 1 y 1 y 0 y 1\\
1 y 0 y 0 y 1 y 1\\
1 y 0 y 0 y 1 y 0\\
0 y 1 y 1 y 0 y 0\\
1 y 1 y 0 y 0 y 0\\
\fin{bmatrix} =
\begin{bmatrix}
2 y 1 y 0 y 1 y 1\\
1 y 2 y 1 y 0 y 1\\
1 y 1 y 1 y 1 y 2\\
\fin{bmatrix}
\fin{alinear}
$
</span>
<br></br>
<span style="color:#d94f0b">
Y los caminos de $3/4$ rectángulos son:
</span>
<br></br>
<span style="color:#d94f0b">
$
\begin{align}
((\mathbf{X}\mathbf{M}^{\ast})\mathbf{Y})_{a1} &= a\rightarrow b\rightarrow 2\rightarrow 1 + a\rightarrow c\rightarrow 5\rightarrow 1\\
((\mathbf{X}\mathbf{M}^{\ast})\mathbf{Y})_{a2} &= a\rightarrow c\rightarrow 5\rightarrow 2\\
((\mathbf{X}\mathbf{M}^{\ast})\mathbf{Y})_{a4} &= a\rightarrow b\rightarrow 2\rightarrow 4\\
((\mathbf{X}\mathbf{M}^{\ast})\mathbf{Y})_{a5} &= a\rightarrow b\rightarrow 2\rightarrow 5\\
((\mathbf{X}\mathbf{M}^{\ast})\mathbf{Y})_{b1} &= b\rightarrow c\rightarrow 5\rightarrow 1\\
((\mathbf{X}\mathbf{M}^{\ast})\mathbf{Y})_{b2} &= b\rightarrow a\rightarrow 1\rightarrow 2 +
b\flecha derecha c\flecha derecha 5\flecha derecha 2\\
((\mathbf{X}\mathbf{M}^{\ast})\mathbf{Y})_{b3} &= b\rightarrow a\rightarrow 1\rightarrow 3\\
((\mathbf{X}\mathbf{M}^{\ast})\mathbf{Y})_{b5} &= b\rightarrow a\rightarrow 1\rightarrow 5\\
((\mathbf{X}\mathbf{M}^{\ast})\mathbf{Y})_{c1} &= c\rightarrow b\rightarrow 2\rightarrow 1\\
((\mathbf{X}\mathbf{M}^{\ast})\mathbf{Y})_{c2} &= c\rightarrow a\rightarrow 1\rightarrow 2\\
((\mathbf{X}\mathbf{M}^{\ast})\mathbf{Y})_{c3} &= c\rightarrow a\rightarrow 1\rightarrow 3\\
((\mathbf{X}\mathbf{M}^{\ast})\mathbf{Y})_{c4} &= c\rightarrow b\rightarrow 2\rightarrow 4\\
((\mathbf{X}\mathbf{M}^{\ast})\mathbf{Y})_{c5} &= c\rightarrow a\rightarrow 1\rightarrow 5 +
c\flecha derecha b\flecha derecha 2\flecha derecha 5\\
\fin{alinear}
$
</span>
<br><br>
<span style="color:#d94f0b">
**Paso 3**. Resaltamos las coincidencias correctas y aplicamos el producto Hadamard:
</span>
<br></br>
<span style="color:#d94f0b">
$
\begin{align}
((\mathbf{X}\mathbf{M}^{\ast})\mathbf{Y})\odot \mathbf{M}^{\ast} =
\begin{bmatrix}
\mathbf{2} y 1 y 0 y 1 y 1\\
1 y \mathbf{2} y 1 y 0 y 1\\
1 y 1 y 1 y 1 y \mathbf{2}\\
\fin{bmatrix}
\odot\;
\begin{bmatrix}
1 y 0 y 0 y 0 y 0 \\
0 y 1 y 0 y 0 y 0 \\
0 y 0 y 0 y 0 y 1 \\
\fin{bmatrix}
\fin{alinear}
$
</span>
<br></br>
<span style="color:#d94f0b">
Finalmente, si sumamos todos los componentes del producto de Hadamard y dividimos entre 2, obtenemos 3 rectángulos, como se muestra en {numref}`Mini2`. ¡Listo!
</span>

### Restricciones de números enteros: QAP
Hemos aclarado la interpretación de una función objetivo de MCS (correspondencia de grafos) $F(\mathbf{M})$ para un $\mathbf{M}\in\{0,1\}^{n\times m}$ (número de rectángulos) particular. La función es <span style="color:#f88146">**cuadrática** en $\mathbf{M}$</span>, ya que requiere dos multiplicaciones de la matriz de correspondencia para su evaluación, pero su evaluación requiere $O(n^4)$.

Además, la estructura de $\mathbf{M}$ no es simplemente binaria. Dado que cada asignación candidata $f$ codificada por esta matriz debe ser una función inyectiva (uno a uno) $f:V\rightarrow V'$, tenemos que para $m\le n$:

$$
\para todo a\en V:\suma_{i\en V'}\mathbf{M}_{ai}\le 1\;\text{y}\; \para todo i\en V':\suma_{a\en V}\mathbf{M}_{ai}\le 1\;,
$$

Es decir, cada fila/columna no puede tener más de un 1. Algunas precisiones:
- Formalmente, todas las filas/columnas pueden ser todos ceros, pero si lo son, entonces no tenemos una solución.
En particular, necesitamos unir un par de vértices para cerrar un solo rectángulo. Por lo tanto, necesitamos al menos dos columnas con una sola vértice en filas diferentes.  
- Por lo tanto, la notación anterior significa que si una fila/columna es todo ceros, solo hay una de ellas que no lo es.
- Idealmente, para $m\le n$ deberíamos tener $m$ columnas con un $1$ todas ubicadas en filas diferentes.

Esta naturaleza restringida del llamado <span style="color:#f88146">**Problema de Asignación Cuadrática (QAP)**</span> es lo que lo convierte en NP:

$$
\begin{align}
\mathbf{M}^{\ast}= & \arg\max_{{\cal P}}F(\mathbf{M}) = \frac{1}{2}\sum_{a\in V}\sum_{i\in V'}\sum_{b\in V}\sum_{j\in V'}\mathbf{M}_{ai}\mathbf{M}_{bj}\mathbf{X}_{ab}\mathbf{Y}_{ij}\\
{\cal P}=&\left\{\mathbf{M}\en \{0,1\}^{m\times n}:\para todo a\en V:\sum_{i\en V'}\mathbf{M}_{ai}\le 1\;\text{y}\; \para todo i\en V':\sum_{a\en V}\mathbf{M}_{ai}\le 1\;\right\}
\fin{alinear}
$$

Por lo tanto, el QAP (utilizamos este nombre en lo sucesivo) se plantea originalmente en términos de <span style="color:#f88146">**Programación Entera (IP)**</span>
ya que las *incógnitas* a descubrir son matrices binarias $m\times n$ $\mathbf{M}\in\{0,1\}^{m\times n}$ sujetas a estar en ${\cal P}$.

En particular, si $m=n$ (ambos gráficos tienen el mismo número de nodos), entonces:
- ${\cal P}$ se convierte en $\Pi_n$, el espacio de *permutaciones* de orden $n$ y tenemos $n!$ *biyecciones* $f=\pi:V\rightarrow V'$.
- Cada matriz $\mathbf{M}$ codifica una permutación $\pi(a),\pi(b),\ldots$, donde $V=\{a,b,\ldots\}$ con $|V|=n$ son las filas de $\mathbf{M}$ (cada una con un $1$ único en diferentes columnas.
- Entonces $V'=\{\pi(i):i\in\{a,b,c,\ldots\}\}$ con $|V'|=n$ y $\pi^{-1}(i)\in V$ existe y es único.

Más formalmente:

$$
\begin{align}
\Pi_n=&\left\{\mathbf{M}\en \{0,1\}^{m\times n}:\para todo a\en V:\sum_{i\en V'}\mathbf{M}_{ai}= 1\;\text{y}\; \para todo i\en V':\sum_{a\en V}\mathbf{M}_{ai}= 1\;\right\}
\fin{alinear}
$$

¡Donde hemos transformado las restricciones de desigualdad en restricciones de igualdad!

El [permutoedro](https://en.wikipedia.org/wiki/Permutohedron) es un método útil para visualizar el espacio de soluciones $\Pi_n$. Cada punto es una permutación $\pi$ y tiene $n-1$ vecinos. Dado $\pi$, sus permutaciones vecinas $\pi'\in {\cal N}_{\pi}$ difieren de $\pi$ en *una transposición*, es decir, un intercambio entre dos componentes.

Por ejemplo, en {numref}`PiN` mostramos $\Pi_4$. Tiene $n!=24$ nodos con $n-1=3$ vecinos cada uno. Por ejemplo, los vecinos de $\pi=[3,4,2,1]$ son ${\cal N}_{\pi}=\{[2,4,3,1],[3,4,1,2],[4,3,2,1]\}$, donde $\pi'=[2,4,3,1]$ es el resultado de intercambiar (transponer) $2$ y $3$ en $\pi=[3,4,2,1]$.

```{figura} ./images/Topic2/PiN-Photoroom.png
---
nombre: PiN
ancho: 600px
alinear: centro
altura: 500px
---
Permutoedro de orden n=4. Por favor, defina los nodos sin etiquetar.
```

## Recocido simulado

El permutoedro proporciona una visión del <span style="color:#f88146">**espacio de búsqueda discreto**</span>, especialmente porque resalta su topología, es decir, su estructura local.

Con este instrumento a mano, es natural <span style="color:#f88146">imaginar la **búsqueda inteligente** como un paseo aleatorio entre una permutación inicial $\pi^0$ y una final $\pi^{\ast}$</span>:
- La *inteligencia* es proporcionada parcialmente por la **función objetivo** $F(\pi)$ que discrimina entre soluciones buenas y malas.
La *estrategia de búsqueda* aprovecha el conocimiento proporcionado por la función objetivo. Una de las estrategias más sencillas es la de un **paseo aleatorio (PA)** $\pi^0\rightarrow\pi^1\rightarrow\ldots\rightarrow \pi^{\ast}$ dentro de $\Pi_n$.

El recocido simulado (SA) es una forma basada en principios que combina inteligencia y búsqueda de RW. Funciona de la siguiente manera:

Sea $\Omega$ el **espacio de búsqueda** y $\omega\in \Omega$ un **estado discreto**, entonces definimos una **cadena de Markov** $X_0,X_1,\ldots$ para un *problema de maximización* de la siguiente manera:

$$
p(X_{t+1}=\omega'|X_{t}=\omega) =
\begin{casos}
     1 &\;\text{si}\; \Delta F\ge 0 \\[2ex]
     \exp(\beta(t)\cdot \Delta F)&\;\text{de lo contrario}\\[2ex]
\fin{casos}
$$

donde $\Delta F:=F(\omega')-F(\omega)$ y $\beta(t):=\frac{1}{T(t)}$, donde $T$ es la **temperatura computacional**. Algunas explicaciones:

Dado que estamos maximizando $F$, tener $\Delta F:=F(\omega')-F(\omega)\ge 0$ para $\omega'\in {\cal N}_{\omega}$ significa que $F(\omega')\ge F(\omega)$, es decir, que estamos en el *camino correcto* (¡o al menos no en el incorrecto!). En este caso, deberíamos **aceptar** (con probabilidad $1$) $\omega'$ como el nuevo estado de la búsqueda.
Si $F(\omega') < F(\omega)$, un método **excesivo** o un método de **ramificación y acotación** debería rechazar $\omega'$ como una dirección prometedora. Sin embargo, el SA ofrece una **probabilidad de aceptación** proporcional a qué tan prometedor es $\omega'$, que es $\Delta F = F(\omega')-F(\omega) < 0$.

Sin embargo, si $F(\omega') < F(\omega)$, la probabilidad de aceptar $\omega'$ depende de la **etapa del proceso de búsqueda** en la que se toma la decisión. Esta etapa está parametrizada por la temperatura computacional $\beta(t)=\frac{1}{T(t)}$

Supongamos que la temperatura computacional $T(t)$ es una **función monótona decreciente** con $t$, como $T(t)=\frac{1}{\log(1+t)}$. Por eso se denomina **programa de recocido**. Entonces:

En $t\rightarrow 0$ (etapas iniciales de la búsqueda), la probabilidad debería ser alta. En ese caso, solemos fijar $T(0)\rightarrow\infty$ (temperatura alta). Como $\Delta F<0$, $\exp(\beta(t)\cdot \Delta F)$ no decae demasiado, ya que está atenuado. Por lo tanto, las soluciones $\omega'$ con $\Delta F<0$ suelen aceptarse si $|\Delta F<0|$ es suficientemente pequeño. Cuanto mayor sea $|\Delta F<0|$, más probable es que $\omega'$ se considere un **evento extremo** (parte de la cola de la exponencial) y, por lo tanto, se descarte.

Sin embargo, para $t\rightarrow \infty$, tenemos $T(t)\rightarrow 0$ (temperatura baja). El mismo decremento $|\Delta F<0|$ que era admisible para valores menores de $t$ aún no se acepta porque el SA se comporta como un método voraz.

[//]: https://sphinx-proof.readthedocs.io/en/latest/syntax.html

[//]: https://pypi.org/project/sphinxcontrib-pseudocode/


```{prf:algoritmo} Metrópolis-Hastings
:label: Metrópolis

**Entradas** Dada una función $F(\omega)$, un programa de recocido $T(t)$ y un estado inicial $\omega_0$\
**Salida** $\omega^{\ast}=\arg\max_{\omega\in\Omega} F(\omega)$

1. convegencia = Falso
2. $\omega_{old}\leftarrow \omega_0$
3. $t\leftarrow 0$
4. **mientras** $\neg$ convergencia:
    
    1. Seleccione $\omega'\in {\cal N}_{\omega}$
    2. Calcular $\Delta F=F(\omega')-F(\omega_{old})$
    3. **si** $\Delta F\ge 0$ **entonces** $\omega_{new}\leftarrow \omega'$
    4. **de lo contrario**:
          1. Dibuje $p\in [0,1]$
          2. $q\leftarrow \exp\left(\frac{\Delta F}{T(t)}\right)$
          2. **si** $q\ge p$ **entonces** $\omega_{new}\leftarrow \omega'$
    5. $t\leftarrow t+1$
    6. $T(t)\leftarrow \frac{1}{\log(1 + t)}$
    7. convergencia = $(T(t)<T_{min})$ **o** $(t>t_{max})$
4. **retorno** $\omega_{new}$
```

### Aproximación de QAP con SA
Apliquemos SA para aproximar el QAP. Para ello, **igualaremos la estructura de la aspirina** (véase {numref}`SA-Aspirina`-Izquierda) con una permutación aleatoria de sus vértices ({numref}`SA-Aspirina`-Derecha). El grafo izquierdo, con nodos $V=\{a,b,\ldots,m\}$ y enlaces, imita la estructura de la aspirina. En este primer enfoque, descartamos, por el momento, tanto las etiquetas de los nodos (átomos) ($\text{C}$,$\text{O}$ y $\text{OH}$) como las etiquetas de las aristas (enlaces) (simples, dobles).

A la derecha, el grafo tiene nodos $V'=\{1,2,\ldots,13\}$. Como $|V|=|V'|=13$, su **espacio de estados** $\Omega$ está dado por el permutoedro $\Pi_{n=13}$, con $n!\approx 6\times 10^{9}$ estados, cada uno con $n-1=12$ aristas.  

Sabemos que la permutación óptima $\pi^{\ast}$ viene dada por $\pi^{\ast}(a)=1,\pi^{\ast}(b)=2,\ldots, \pi^{\ast}(m)=13$, es decir, $\mathbf{M}^{\ast}=\mathbf{I}_n$ es la matriz identidad de dimensión $n$. Sin embargo, suponemos un caso realista donde la permutación de entrada $\pi^0$ es bastante diferente de la óptima:

$$
\pi^0 =
\begin{bmatrix}
\overbrace{7}^a & \overbrace{12}^b & \overbrace{5}^{c} & \overbrace{11}^{d} & \overbrace{3}^e & \overbrace{9}^f & \overbrace{2}^g & \overbrace{8}^h & \overbrace{10}^i & \overbrace{4}^j & \overbrace{1}^k & \overbrace{6}^l & \overbrace{13}^m\\
\fin{bmatrix}
$$

**1) Emparejamiento inicial**. Sin embargo, en lugar de iniciar el análisis de similitud con un $\pi^0$ aleatorio, es recomendable calcular una <span style="color:#f88146">**aproximación voraz**</span>. En el caso del emparejamiento de grafos o QAP, un algoritmo voraz puede basarse en emparejar $a,b,c,\ldots$ con los nodos $1,2,3,\ldots$ de tal manera que <span style="color:#f88146">*prefiera emparejar nodos con el mayor número de vecinos (grado) posible*</span>.

Entonces, la coincidencia codiciosa conduce a

$$
\pi^0 =
\begin{bmatrix}
\overbrace{3}^a & \overbrace{4}^b & \underline{\overbrace{5}^{c}} & \overbrace{9}^{d} & \underline{\overbrace{1}^e} & \overbrace{6}^f & \overbrace{8}^g & \overbrace{10}^h & \overbrace{12}^i & \overbrace{2}^j & \overbrace{7}^k & \overbrace{10}^l & \overbrace{13}^m\\
\fin{bmatrix}
$$

Comprobamos {numref}`SA-Aspirina`, donde graficamos la *aproximación final de SA* con $10$ rectángulos de cierre, que el codicioso $\pi^0$ es consistente con nodos coincidentes con grados mutuamente mayores:
- Subrayamos las coincidencias con mayores grados (el grado máximo es $3$): $c\rightarrow 5$, $e\rightarrow 1$.
- Uno de los riesgos del emparejamiento codicioso es que podemos quedar **atascados en un máximo local**, lo que realmente sucede (SA aquí se recupera de $e\rightarrow 1$ pero no de $c\rightarrow 5$).
- Sin embargo, la programación de recocido adecuada generalmente **saca la búsqueda de los óptimos locales** en las primeras etapas de la búsqueda.  

**2) Vecindad**. El segundo aspecto a definir al aplicar SA al QAP es cómo <span style="color:#f88146">**garantizar vecindades adecuadas ${\cal N}_{\omega}$**</span>. En otras palabras, si dado $\omega$ elegimos como $\omega'$ una variación aleatoria arbitrariamente grande, *<span style="color:#f88146">podríamos pasar por alto la propiedad de irreducibilidad de la cadena de Markov (se deben alcanzar todos los estados)*</span>.

Entonces, una buena manera de navegar adecuadamente a través del espacio de búsqueda (el permutoedro $\Pi_n$ en este caso) es:
1) **Elija** aleatoriamente si vamos a intercambiar filas o columnas en $\mathbf{M}_{\omega}$.
2) **Intercambiar** dos filas (o columnas) cuyos índices se eligen aleatoriamente. El resultado es $\mathbf{M}_{\omega'}$

Esto es **equivalente** a realizar una transposición en el permutoedro $\Pi_n$.

**3) Programa de recocido**. El último paso es establecer un <span style="color:#f88146">**enfriamiento a temperatura adecuada (programa de recocido)**</span> y los valores específicos $T_0$ y $T_f$.
- En este ejemplo, simplemente hacemos $T(t+1)=T(t)-\alpha\cdot T(t)=(1-\alpha)\cdot T(t)$ con $\alpha\ll 1$.
- Esto conduce a una disminución negativa-exponencial ya que:

$$
\begin{align}
T(1)&=(1-\alpha)\cdot T(0)\\
T(2)&=(1-\alpha)\cdot T(1)=(1-\alpha)^2\cdot T(0)\\
    &\vpuntos\\
T(n)&=(1-\alpha)\cdot T(n-1)=(1-\alpha)^n\cdot T(0)\\
\fin{alinear}
$$

Esta sucesión es decreciente, ya que solo multiplicamos $T(0)$ por una fracción decreciente. De hecho, hemos establecido $T(0)=1/5=0.2$ y $\alpha = 1/1.075\approx 0.93$. La disminución exponencial se puede observar observando la **transformación logarítmica** (las exponenciales son líneas en el espacio logarítmico):

$$
T(n) = (1-\alpha)^n\cdot T(0)\Rightarrow \log(T(n))=n\cdot log(1-\alpha) + \log T(0)\;.
$$

Dado que $(1-\alpha)<1$ entonces su logaritmo es negativo.

Este programa es un **poco agresivo** pero jugando un poco con $\alpha$ podemos cerrar $10-11$ rectángulos de $13$ posibles (este es el número de aristas del gráfico de Aspirina).

En {numref}`Curvas SA`, trabajamos con diferentes valores de $\alpha$. Para mayor claridad, solo representamos el **mejor coste obtenido hasta el momento**. Cabe destacar que, para diferentes regímenes, obtenemos resultados diferentes; en este caso, entre $0$ y $11$ rectángulos. Es interesante observar que:

- El mejor resultado se obtiene con uno de los $\alpha$ más pequeños ($\alpha=0.85$)
- Los programas de recocido tienden a aumentar más la función objetivo $F$ en las primeras etapas de la búsqueda, donde SA es más libre para explorar.
Nótese que el programa más estricto ($\alpha=0.93$) alcanza $9$ rectángulos en las etapas intermedias y finalmente alcanza un máximo de $10$ rectángulos. Esta es la solución que se muestra en {numref}`SA-Aspirina`.

La imagen de la derecha muestra las diferencias insignificantes entre los programas de recocido en el dominio logarítmico-logarítmico.

```{figura} ./images/Topic2/SA-Curves-Photoroom.png
---
nombre: SA-Curves
ancho: 800px
alinear: centro
altura: 400px
---
Jugando con $\alpha$ para diferentes programas de recocido.
```

**4) Comprender la solución**. Por último, pero no menos importante, debemos interpretar hasta qué punto nuestra $F$ alcanza o no una *solución interesante*. En este caso, <span style="color:#f88146">*interesante* significa **global**</span>. Por ejemplo:
- La solución en {numref}`SA-Aspirin` captura principalmente el hexágono central, aunque bajo una rotación alrededor del eje $gi$ y una inversión o torsión respecto de la vertical: el borde $fe$ se convierte en $8-10$, pero el borde $hi$ se convierte en $3-9$.
- La parte superior de la molécula de la izquierda coincide con la parte inferior de la de la derecha, lo que indica una deformación global.
- Además, la parte inferior izquierda de la molécula de la izquierda coincide con la parte superior de la de la derecha (nuevamente una deformación).
- En general, los subgráficos más grandes coinciden correctamente, pero los más pequeños están mal ubicados.

Por lo tanto, aunque la solución obtenida parece **cuantitativamente global**, es parcialmente **cualitativamente global**. Esto revela la necesidad de hacer que la función objetivo sea <span style="color:#f88146">**más informativa**</span> (volveremos a este punto más adelante).


```{figura} ./images/Topic2/SA-Aspirin-Photoroom.png
---
nombre: SA-Aspirina
ancho: 800px
alinear: centro
altura: 600px
---
Aproximación del isomorfismo de la aspirina con SA.
```



### Interpretación de SA

**Interpretación intuitiva**. Desde un punto de vista intuitivo, el SA puede describirse de la siguiente manera [Hoffmann y Buhmann 1997](https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=645602):
1) Las diferencias de costos entre estados vecinos actúan como un **campo de fuerza**.
2) El efecto de la temperatura computacional puede interpretarse como una fuerza aleatoria con una **amplitud proporcional a T**.
3) Los valles y picos con una diferencia de costo menor que T se difuminan y desaparecen en la búsqueda estocástica. Es más probable que esto ocurra en las primeras etapas de la búsqueda, donde necesitamos evitar soluciones locales (subóptimas).

**Interpretación metodológica**. En la jerga de la IA, $F$ se considera una <span style="color:#f88146">**heurística**</span> y SA se considera una <span style="color:#f88146">**metaheurística**</span>:
- [Heurística](https://en.wikipedia.org/wiki/Heuristic). Este término fue introducido por Herbert Simon y significa, en términos generales, "atajo de búsqueda", es decir, un mecanismo para decidir qué solución es interesante y cuál no lo es en un espacio de soluciones potencialmente amplio. Este concepto es nuestro tema. En este caso, se refiere al número de rectángulos.
Las [metaheurísticas](https://en.wikipedia.org/wiki/Metaheuristic) son procedimientos que modulan la aplicación de una heurística. La AS es una metaheurística porque determina cuándo la búsqueda es más estocástica y cuándo se vuelve más voraz.


**Interpretación formal**. Recuerde que el [Algoritmo de Metrópolis](https://arxiv.org/pdf/1504.01896) implementa una cadena de Markov irreducible $X_0,X_1,\ldots,X_t$ a lo largo de $\Omega$. Esta cadena de Markov es **estacionaria**, es decir, converge a una distribución de probabilidad dada $G$, lo que significa que después de un intervalo de tiempo dado $t$, si $X_{t}\sim G(\omega)$, entonces también $X_{t+1}\sim G(\omega)$. La distribución estacionaria es

$$
\lim_{t\rightarrow\infty}p(X^{t+1}|X^{t})=G(\omega)\;,
$$

independientemente de la elección de $X_0$. En este caso, la distribución estacionaria $G(\omega)$ es

$$
G(\omega) = \frac{\exp(\beta\cdot F(\omega))}{Z},\;\; \text{con}\;\; Z = \sum_{\omega\in\Omega}\exp(\beta\cdot F(\omega))\;,
$$

Lo que se conoce como la <span style="color:#f88146">**distribución de Gibbs**</span>. Observe, por ejemplo, la variable $q$ en el paso $4.2.$ del algoritmo de Metropolis-Hastings:

$$
q\leftarrow \exp\left(\frac{\Delta F}{T(t)}\right) =
\exp\left(\beta(t)\Delta F\right) = \frac{\exp\left(\beta(t)F(\omega')\right)}{\exp\left(\beta(t) F(\omega_{old})\right)} = \frac{\frac{\exp\left(\beta(t)F(\omega')\right)}{Z(t)}}{\frac{\left(\beta(t) F(\omega_{old})\right)}{Z(t)}}=\frac{G(\omega')}{G(\omega_{old})}\;.
$$

Por lo tanto, la llamada **probabilidad de aceptación** es un cociente entre dos probabilidades gibbsianas. Nótese que, en la distribución de Gibbs, para una $\beta$ dada, los estados $\omega\in \Omega$ con mayor $F(\omega)$ son más probables. En consecuencia, $q$ es el máximo posible cuando $F(\omega')\gg F(\omega_{old})$ (por supuesto, para esta $\beta$).

En consecuencia, el SA puede considerarse un <span style="color:#f88146">**proceso de muestreo** que converge al óptimo global $\omega^{\ast}$ de $F(\omega)$</span> si el programa de recocido es adecuado. Sin embargo, ¿cuál es el **rol formal** de la temperatura (o su inverso: $\beta$)? Resolver esta pregunta es una buena excusa para profundizar en la **Teoría de la Información**, una disciplina matemática basada en la probabilidad y fundamental para comprender la búsqueda inteligente.

### Muestreo de Gibbs
El SA muestra que la búsqueda inteligente puede concebirse como el uso de paseos aleatorios para explorar espacios combinatorios como $\Pi_n$. Para esta sección, necesitamos un concepto probabilístico clave: la esperanza de una variable aleatoria.   

Recuerde que la **esperanza** de una variable aleatoria discreta $\omega$ se define de la siguiente manera:

$$
E(X)=\sum_{\omega\in \Omega}\omega\cdot p(X=\omega)\;.
$$

La esperanza nos da una idea de la **concentración espacial** de los valores $\omega\in\Omega$ correspondientes a $p(X=\omega)$. De hecho, $E(X)$ puede considerarse el *más representativo* de estos valores (es decir, el *más probable*).

Para determinar $E(X)$ es obligatorio conocer todas las probabilidades $p(X=\omega)$.

Sin embargo, <span style="color:#f88146">¿qué pasa si $p(X=\omega)=G(X)$, es decir, si $X$ es **gibbsiano**?</span>. Este es el caso de $X=F(\omega)$, el valor de la función de costo. En este último caso,

$$
E(X) = \sum_{\omega\en \Omega}\omega\cdot G(X=\omega) = \sum_{\omega\en \Omega}\omega\cdot \frac{\exp\left(\beta\cdot F(\omega)\right)}{Z}\;,
$$

Es el **costo esperado**. ¿Podemos realmente calcularlo? Bueno, es imposible hacerlo analíticamente porque:

1) Debemos conocer todos los valores de $F(\omega)$. Esto equivale a resolver el problema codificado por esta función de coste mediante **fuerza bruta**. Recordemos que, para el QAP, esto implica evaluar **todos los estados del permutoedro**, es decir, $n!$ estados cuya evaluación individual requiere $O(n^4)$.

2) La distribución de Gibbs parece estar restringida a una $\beta$ dada. Deberíamos evaluar $Z=\sum_{\omega\in\Omega}G(\omega)$, una suma muy grande, para esa $\beta$ en particular. Por lo tanto, $E(X)$ también parece ser $\beta-$dependiente.

En cambio, el algoritmo Metropolis-Hastings nos permite **aproximar** $E(X)$ de la siguiente manera:

$$
E(X)\aprox \frac{1}{R}\sum_{r=1}^{R}F(\omega_r)\;,
$$

Donde $\omega_1,\omega_2,\ldots, \omega_r$ son los estados que visita el algoritmo cuando sigue una **programación de anulación admisible** como $T(t)=\frac{C}{\log(1+t)}$, donde $C$ es una constante. Esto significa que $\omega_r$ se **acepta** en $T(r)$.

Algunas consideraciones relacionadas:
1) La secuencia $\omega_1,\omega_2,\ldots,$ es un **paseo aleatorio** a lo largo de $\Omega$ que es impulsado por $F(\omega)$ y converge a la probabilidad de Gibbs.

2) Cuanto menor sea la temperatura $T(t)$, más nos acercamos a la distribución de Gibbs. Por lo tanto, <span style="color:#f88146">la temperatura computacional funciona como un **parámetro de Lagrange** para reforzar la convergencia</span> hacia la distribución de Gibbs.

3) Formalmente, no todas las **muestras** $\omega_1,\omega_2,\ldots,\omega_r$ son generadas por $G(\omega)$ ya que todo paseo aleatorio tiene un **periodo transitorio** (valores inestables) y no sabemos exactamente en qué instante de tiempo tenemos la convergencia, es decir $\omega_t$ se convierten en muestras propias de $G(\omega)$.

4) Siguiendo [Entendiendo el muestreo de Gibbs](https://eml.berkeley.edu/reprints/misc/understanding.pdf), una buena estrategia es iniciar diferentes recorridos aleatorios en diferentes $X_0$s (permutaciones iniciales en QAP) y rastrear las muestras hasta que podamos observar algún **consenso**.

En {numref}`SA-Expectations`, mostramos tres recorridos aleatorios generados a partir de diferentes $X_0$, para el recocido admisible (logaritmo inverso) con $C=3$. Ninguno de ellos alcanza el óptimo global en $R=7,000$ iteraciones. En realidad, sus expectativas aproximadas $E(X)$ son, respectivamente, $8.637$, $8.178$ y
$9.371$ si eliminamos las primeras $1,000$ muestras (consideradas como régimen transitorio), mientras que tenemos $9.051$, $8.466$ y $9.791$ si se incluyen todas las muestras.

Lo interesante aquí es que <span style="color:#f88146">**es bastante difícil alcanzar el óptimo global**</span> ya que:
1) En general, hay menos estados con ese valor y la mayoría son subóptimos. Esto se indica por el hecho de que $E(X)\ll \omega^{\ast}$ para $X=F(\omega)$.
2) En problemas combinatorios como QAP, la función de coste tiene un número discreto de **niveles de energía**, lo que suele conducir a **mesetas** (regiones de coste constante) a medida que avanza el enfriamiento. Por ejemplo, en {numref}`SA-Expectations`, la búsqueda aleatoria parece estar bloqueada en un estado subóptimo, al menos para dicho número de iteraciones $R$.


```{figura} ./images/Topic2/SA-Expectations-Photoroom.png
---
nombre: SA-Expectativas
ancho: 800px
alinear: centro
altura: 600px
---
Tres paseos aleatorios a lo largo de $\Pi_n$ con diferentes $X_0$.
```

Tenga en cuenta también que aquí hemos destacado las principales características de SA. Consulte el excelente artículo de los hermanos Geman: Relajación Estocástica, [Distribución de Gibss y la Restauración Bayesiana de Imágenes](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=4767596), uno de los artículos más influyentes de todos los tiempos.

### Limitaciones de SA
El SA resulta atractivo para la IA, ya que nos permite rastrear el óptimo global en una especie de recorrido aleatorio. Sin embargo:

1) La calidad o "inteligencia" del paseo aleatorio depende del <span style="color:#f88146">**cuán informativa**</span> sea la función de coste. ¿Cómo se mide la información? Abordaremos esta cuestión más adelante.    
2) El <span style="color:#f88146">óptimo global solo se garantiza para un recocido **lento**</span> $T(t)=\frac{C}{\log(1+t)}\rightarrow 0$. El SA debe ser lo suficientemente lento como para no perder dicho óptimo global; de lo contrario, el SA se vuelve voraz prematuramente. Esta es una **limitación importante** del SA: recuerde que para QAP debemos evaluar $F(\omega)$ en cada instante $t$ y requiere $O(n^4)$.


## Agrupación central
El recocido determinista (AD) resulta ser un método más rápido que el SA. Para justificar esta técnica, es más conveniente considerar otro problema de NP. Este problema es el de agrupamiento central (o <span style="color:#f88146">agrupamiento k-centrado</span>), y se formula de la siguiente manera:

*Dado un conjunto ${\cal X}=\{\mathbf{x}_1,\mathbf{x_2},\ldots,\mathbf{x}_m\}\subset \mathbb{R}^d$ (puntos de dimensión $d) y un parámetro entero $k>1$, *encuentre un conjunto de $k$ centros* ${\cal C}=\{\mathbf{c}_1,\mathbf{c}_2,\ldots,\mathbf{c}_k\}\subset \mathbb{R}^d$ tal que la distancia euclidiana $D(\mathbf{x},\mathbf{c})$ de cada punto $\mathbf{x}_a$ a su centro más cercano $\mathbf{c}_i$ sea mínima.*

### Clústeres y prototipos
Una formulación más intuitiva es la siguiente. Sea

$$
\text{cluster}(\mathbf{c}_i) = \{\mathbf{x}_a\in{\cal X}: D(\mathbf{x}_a,\mathbf{c}_i)\le D(\mathbf{x}_a,\mathbf{c}_j),j\neq i\}\;,
$$

Sea un <span style="color:#f88146">**clúster**</span>, es decir, un subconjunto de ${\cal X}$ donde sus elementos $\mathbf{x}_a$ están más cerca del <span style="color:#f88146">**prototipo**</span> $\mathbf{c}_i$ del clúster que de cualquier otro. Entonces, el problema también se formula de la siguiente manera:

*Partición ${\cal X}$ en $k$ grupos (disjuntos) tales que la suma de las distancias entre los puntos y los prototipos sea mínima.*

Algunas aclaraciones:
1) El problema es un problema de <span style="color:#f88146">**huevo y la gallina**</span>: a) Necesitamos conocer los $k$ centros $\mathbf{c}_i$ de antemano para determinar los conglomerados $\text{cluster}(\mathbf{c}_i)$ pero b) los prototipos tienen que determinarse una vez que los conglomerados se hacen de acuerdo con el criterio de distancias mínimas.

2) La NP-dureza del problema viene dada por la <span style="color:#f88146">**sabor de partición**</span>. En realidad, la complejidad en el peor caso es $O(k^m)$, ya que cada uno de los $m$ puntos diferentes puede asignarse exclusivamente a $k$ centros (**r-permutaciones con repetición** $P_{\sigma}(m,k)=k^m)$.

3) Los prototipos $\mathbf{c}_i$ <span style="color:#f88146">**no necesariamente pertenecen a**</span> ${\cal X}$ y deben ser descubiertos.

Véase, por ejemplo, un problema bien definido en {numref}`KM-clusters` donde los puntos rojos son centros ideales $\mathbf{c}_i$ que son las expectativas $\mu_i$ de gaussianas bidimensionales $N(\mu_i,\sigma\mathbf{I})$ con $\sigma=0.5$.

```{figura} ./images/Topic2/KM-clusters-Photoroom.png
---
nombre: clústeres KM
ancho: 800px
alinear: centro
altura: 600px
---
Clústeres y prototipos estimados en $\mathbb{R}^2$.
```

### Funciones de costo
#### Atractores
Una primera función de coste compacta podría ser:  

$$
F({\cal C}) = \sum_{a=1}^m\min_{1\le i\le k}D(\mathbf{x}_a,\mathbf{c}_i)\;.
$$

donde nos interesa ${\cal C}^{\ast}$, el conjunto $k$ centros/prototipos <span style="color:#f88146">**minimizando la distancia total**</span>.

En {numref}`KM-clusters`, dos centros $\mathbf{c}_1=[-1,-1]^T$ y $\mathbf{c}_2=[1,-1]^T$ son mutuamente más cercanos que el tercero $\mathbf{c}_3=[0,2]^T$. Entonces, si representamos el costo individual de cada punto $\mathbf{x}_a$ con respecto a cada centro, es decir, $min_{1\le i\le k}D(\mathbf{x}_a,\mathbf{c}_i)$ (véase {numref}`KM-dist`), observe que hay un mínimo bien definido en $\mathbf{c}_1=[-1,-1]^T$ que interpretamos como un <span style="color:#f88146">**atractor** o **estado metaestable**</span>, ya que distorsiona las ubicaciones de los otros dos mínimos. Tenga en cuenta también que la función de costo es claramente **no convexa** y tiene muchos **puntos de silla** (ver, por ejemplo, la vista 3D en {numref}`KM-dist3D`)


```{figura} ./images/Topic2/KM-dist-removebg-preview.png
---
nombre: KM-dist
ancho: 800px
alinear: centro
altura: 600px
---
Costo individual respecto a los centros más cercanos.
```

```{figura} ./images/Topic2/KM-dist3D-removebg-preview.png
---
nombre: KM-dist3D
ancho: 800px
alinear: centro
altura: 600px
---
Costo individual respecto de los centros más cercanos (vista 3D).
```

Sin embargo, si también incluimos las <span style="color:#f88146">**variables de asignación**</span> $\mathbf{M}_{ai}$ de punto a grupo, nuestro objetivo es minimizar **conjuntamente**:   

$$
F({\cal C},\mathbf{M}) = \sum_{a=1}^m\mathbf{M}_{ai}D(\mathbf{x}_a,\mathbf{c}_i)\;,\text{st}\;\sum_{i=1}^k\mathbf{M}_{ai}=1\;,\forall a\in \{1,\ldots,m\}\;,
$$

donde cada punto sólo se puede asignar a un único grupo y todos los puntos deben ser asignados (cada fila tiene un único $1$).


#### Independencia
Nótese que la distribución de Gibbs para $F({\cal C},\mathbf{M})$ es

$$
G({\cal C},\mathbf{M})=\frac{\exp(-\beta F({\cal C},\mathbf{M}))}{Z}\;\;\text{con}\;\;\; Z=\sum_{{\cal C},\mathbf{M}}\exp(-\beta F({\cal C},\mathbf{M}))\;,
$$

donde el exponencial negativo significa que <span style="color:#f88146">la probabilidad de una solución **decae exponencialmente con las distancias**</span> entre los puntos y los centros de los grupos o prototipos.


En lugar de muestrear $\Omega={\cal C}\times{\cal P}$ con SA, donde

$$
{\cal P} =\left\{\mathbf{M}\en \{0,1\}^{m\times k}:\forall a\en\{1,\ldots,m\}:\sum_{i=1}^k\mathbf{M}_{ai}=1,\right\}
$$

Vamos a <span style="color:#f88146">suponer que las variables ${\cal C}$ y $\mathbf{M}$ son **estadísticamente independientes**</span>. Luego, siguiendo el **Apéndice**, calculamos la **marginal** de la distribución de Gibbs con respecto a las matrices de asignación:

$$
\begin{align}
G({\cal C})&=\sum_{\mathbf{M}\in{\cal P}} G({\cal C},\mathbf{M})\\
           &=\frac{1}{Z}\sum_{\mathbf{M}\in{\cal P}}\exp(-\beta F({\cal C},\mathbf{M}))\\
           &=\frac{1}{Z}\sum_{\mathbf{M}\in{\cal P}}\exp\left(-\beta \sum_{a=1}^m\sum_{i=1}^k\mathbf{M}_{ai}D(\mathbf{x}_a,\mathbf{c}_i)\right)\\
           &=\frac{1}{Z}\sum_{\mathbf{M}\in{\cal P}}Q(\mathbf{M})\;.
\fin{alinear}
$$

Ahora, al observar la suma de exponenciales negativos, observamos que la suma se encuentra sobre las <span style="color:#f88146">matrices de asignación legal**</span> $\mathbf{M}\in{\cal P}$ (cada punto debe asignarse a un prototipo único). Esto significa que cualquier matriz legal será un conjunto de filas que cumplen:   

$$
\text{filas}(\mathbf{M})\in {\cal C}_k=\overbrace{\{\underbrace{(1,0,\ldots,0)}_{I_1:k\;\text{elementos}},\underbrace{(0,1,\ldots,0)}_{I_2:k\;\text{elementos}},\ldots,\underbrace{(0,0,\ldots,1)}_{I_k:k\;\text{elementos}}\}}^{m\;\text{elementos}}\;.
$$

Esto significa que para cada una de las $m$ filas de $\mathbf{M}$ tenemos $k$ opciones para $m$ posiciones, lo que resulta en $k^m$ **matrices legales totales**, es decir, términos en $\sum_{\mathbf{M}\in {\cal P}}Q(\mathbf{M})$. Sin embargo, este número se puede reducir si aplicamos un <span style="color:#f88146">**segundo supuesto de independencia**: la asignación de un punto a un grupo es independiente de la de otro punto</span> (lógicamente, esto no se cumple para puntos cercanos, pero simplifica los cálculos).

Esto nos permite expresar la suma neg-exp como la siguiente suma, implementando un $\lor$ lógico:

$$
\sum_{\mathbf{M}\in{\cal P}} Q(\mathbf{M})=\sum_{\text{filas}(\mathbf{M}^{(1)})}\sum_{\text{filas}(\mathbf{M}^{(2)})}\ldots\sum_{\text{filas}(\mathbf{M}^{(m)})}Q(\mathbf{M})
$$

donde $\mathbf{M}^{(1)},\mathbf{M}^{(2)},\ldots,\mathbf{M}^{(m)}$ son las matrices de asignación que se pueden elegir para cualquier punto particular $\mathbf{x}_1,\mathbf{x}_2,\ldots,\mathbf{x}_m$.

Dado que **independencia significa factorización** tenemos $\sum\sum\ldots\sum = \sum\cdot\sum\ldots\sum$ como en la integración múltiple, es decir:

$$
Z = \sum_{\mathbf{M}\in{\cal P}} Q(\mathbf{M})=\prod_{a=1}^m\sum_{\text{filas}(\mathbf{M}^{(a)})}Q(\mathbf{M}^{(a)}) = \prod_{a=1}^m\sum_{\text{filas}(\mathbf{M}^{(a)})}\exp\left(-\beta\sum_{i=1}^k\mathbf{M}^{(a)}_{ai}D(\mathbf{x}_a,\mathbf{c}_i)\right)\;.
$$

donde el producto $\prod_{a=1}^m$ absorbe las sumas $\sum_{a=1}^m$ dentro de cada exponencial.  

¡Presten atención! En este punto, usamos el hecho de que $\sum_{i=1}^k\mathbf{M}^{(a)}_{ai}=1,\forall a$ (¡para cada fila!), es decir, solo se elegirá un clúster. ¡De hecho, tenemos un XOR! Esto nos lleva a:

$$
Z=\sum_{\mathbf{M}\in{\cal P}} Q(\mathbf{M})=\prod_{a=1}^m\sum_{\text{filas}(\mathbf{M}^{(a)})}Q(\mathbf{M}^{(a)}) = \prod_{a=1}^m\sum_{i=1}^k\exp\left(-\beta D(\mathbf{x}_a,\mathbf{c}_i)\right)\;.
$$

**Resultado final**. Para capturar la factorización anterior, la función de costo original $F({\cal C},\mathbf{M})$ debe transformarse de la siguiente manera:

$$
F_{\beta}({\cal C}) = -\frac{1}{\beta}\log Z = -\frac{1}{\beta}\sum_{a=1}^m \log\sum_{i=1}^k \exp\left(-\beta D(\mathbf{x}_a,\mathbf{c}_i)\right)\;.
$$

que se puede calcular en $O(nk)$. En realidad, $F_{\beta} = -\frac{1}{\beta}\log Z$ se suele denominar [Energía Libre](https://en.wikipedia.org/wiki/Gibbs_free_energy#:~:text=In%20traditional%20use%2C%20the%20term,non%2Dpressure%2Dvolume%20work).

#### Derivación
El siguiente algoritmo DA para agrupamiento central resulta de la **minimización de la energía libre** de la siguiente manera:

Calculemos la derivada de

$$
F_{\beta}({\cal C})=-\frac{1}{\beta}\sum_{a=1}^m \log\underbrace{\sum_{i=1}^k \exp\left(-\beta D(\mathbf{x}_a,\mathbf{c}_i)\right)}_{Q(\mathbf{x}_a)}
$$


con respecto a cada centro $\mathbf{c}_i$:

$$
\begin{align}
\frac{\parcial F_{\beta}}{\parcial \mathbf{c}_i} &= -\frac{1}{\beta} \sum_{a=1}^m\frac{\parcial \log Q(\mathbf{x}_a)}{\parcial \mathbf{c}_i}\\
&= -\frac{1}{\beta}\sum_{a=1}^m\frac{1}{Q(\mathbf{x}_a)}\cdot \frac{\parcial Q(\mathbf{x}_a)}{\parcial \mathbf{c}_i}\\
&= -\frac{1}{\beta}\sum_{a=1}^m\frac{1}{Q(\mathbf{x}_a)}\cdot \left(-e^{-\beta D(\mathbf{x}_a,\mathbf{c}_i)}\right)\cdot\frac{\partial D(\mathbf{x}_a,\mathbf{c}_i)}{\mathbf{c}_i}\;.\\
\fin{alinear}
$$

Para $D(\mathbf{x}_a,\mathbf{c}_i)=||\mathbf{x}_a-\mathbf{c}_i||^2$ tenemos:

$$
\begin{align}
\frac{\partial D(\mathbf{x}_a,\mathbf{c}_i)}{\mathbf{c}_i}=2(\mathbf{x}_a-\mathbf{c}_i)
\fin{alinear}
$$

Luego, introduciendo esta derivada en la fórmula principal y desarrollando $Q(\mathbf{x}_a)$, obtenemos:

$$
\begin{align}
\frac{\partial F_{\beta}}{\partial \mathbf{c}_i} &= -\frac{1}{\beta}\sum_{a=1}^m\frac{1}{Q(\mathbf{x}_a)}\cdot \left(-e^{-\beta D(\mathbf{x}_a,\mathbf{c}_i)}\right)\cdot 2(\mathbf{x}_a-\mathbf{c}_i)\\
&= \frac{2}{\beta}\sum_{a=1}^m\frac{e^{-\beta D(\mathbf{x}_a,\mathbf{c}_i)}}{\sum_{i'=1}^ke^{-\beta D(\mathbf{x}_a,\mathbf{c}_{i'})}}\cdot (\mathbf{x}_a-\mathbf{c}_i)\;.
\fin{alinear}
$$

Tenga en cuenta que

$$
\langle \mathbf{M}_{ai} \rangle = \frac{e^{-\beta D(\mathbf{x}_a,\mathbf{c}_i)}}{\sum_{i'=1}^ke^{-\beta D(\mathbf{x}_a,\mathbf{c}_{i'})}}\;.
$$

Entonces,

$$
\begin{align}
\frac{\partial F_{\beta}}{\partial \mathbf{c}_i} &=
\frac{2}{\beta}\sum_{a=1}^m\langle \mathbf{M}_{ai} \rangle\cdot (\mathbf{x}_a-\mathbf{c}_i)\;.
\fin{alinear}
$$

Como el óptimo se obtiene cuando el gradiente es cero, tenemos:

$$
\frac{\partial F_{\beta}}{\partial \mathbf{c}_i} = \mathbf{0}\Rightarrow \sum_{a=1}^m\langle \mathbf{M}_{ai} \rangle\cdot (\mathbf{x}_a-\mathbf{c}_i)=\mathbf{0}\Rightarrow
\mathbf{c}_i = \frac{1}{\sum_{a=1}^m\langle \mathbf{M}_{ai} \rangle}\sum_{a=1}^m\mathbf{x}_a\langle \mathbf{M}_{ai} \rangle\;.
$$

Por lo tanto, el algoritmo de DA para la agrupación central se deriva simplemente del gradiente de energía libre. En resumen, DA consiste en <span style="color:#f88146">**realizar un descenso de gradiente** con respecto a cada temperatura inversa $\beta$</span>.


### Recocido determinista
El recocido determinista (AD)](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=726788) es una técnica de búsqueda fácilmente aplicable al problema de agrupamiento central (ver más detalles en la [tesis doctoral de Kenneth Rose](https://thesis.library.caltech.edu/2858/1/Rose_k_1991.pdf)).

La idea básica de DA es que para cada valor de $\beta=\frac{1}{T}$ <span style="color:#f88146">**interactuamos dos fases**</span> para minimizar
la energía libre $F_{\beta}({\cal C})$:

1) **Expectativa**. Para centros fijos $\mathbf{c}_i$, estimamos la <span style="color:#f88146">**probabilidad**</span> de que cualquier punto $\mathbf{x}_a$ pertenezca a cada conglomerado ("pertenencia"). Denotamos estas probabilidades como $\langle \mathbf{M}_{ai} \rangle$ y se expresan por:

$$
\langle \mathbf{M}_{ai} \rangle = \frac{\exp(-\beta D(\mathbf{x}_a,\mathbf{c}_i))}{\sum_{i'=1}^k \exp(-\beta D(\mathbf{x}_a,\mathbf{c}_{i'}))}\;.
$$

2) **Actualización**. Para <ins>probabilidades fijas</ins> $\langle \mathbf{M}_{ai} \rangle$, actualizamos los <span style="color:#f88146">**centers**</span>. Si $D(\mathbf{x}_a,\mathbf{c}_i)=||\mathbf{x}_q-\mathbf{c}_i||^2$ (distancia euclidiana al cuadrado), entonces tenemos

$$
\mathbf{c}_i = \frac{\sum_{a=1}^m \mathbf{x}_a \langle \mathbf{M}_{ai}\rangle}{\sum_{a=1}^m\langle \mathbf{M}_{ai}\rangle}\;,
$$

es decir, los nuevos centros ("difusos") son los centros esperados según las probabilidades fijas o ("membresías").


```{prf:algorithm} Recocido determinista [Agrupamiento]
:label: DA-alg

**Entradas** Dado un conjunto de puntos ${\cal X}=\{\mathbf{x}_1,\ldots,\mathbf{x}_m\}$, la energía libre $F_{\beta}({\cal C})$, un programa de recocido $\beta =1/T(t)$ y un estado inicial ${\cal C}^0=(\mathbf{c}^0_1,\ldots,\mathbf{c}^0_k)$\
**Salidas** ${\cal C}^{\ast}=\arg\min_{{\cal C}\in\Omega} F_{\beta\rightarrow\infty}({\cal C})$ y $\langle \mathbf{M}^{\ast}_{ai}\rangle$

1. convegencia = Falso
2. $\langle \mathbf{M}^{viejo}_{ai}\rangle\leftarrow 1$
3. $t\leftarrow 0$
4. **mientras** $\neg$ convergencia:
    
    1. **para** $\mathbf{x}_a\in {\cal X}$, $\mathbf{c}_i\in {\cal C}$:

       $
       \langle \mathbf{M}_{ai} \rangle = \frac{\exp(-\beta D(\mathbf{x}_a,\mathbf{c}_i))}{\sum_{i'=1}^k \exp(-\beta D(\mathbf{x}_a,\mathbf{c}_{i'}))}
       $

    2. **para** $\mathbf{c}_i\in {\cal C}$:

       $
       \mathbf{c}_i = \frac{\sum_{a=1}^m \mathbf{x}_a \langle \mathbf{M}_{ai}\rangle}{\sum_{a=1}^m\langle \mathbf{M}_{ai}\rangle}
       $

    3. $t\leftarrow t+1$
    4. $T(t)\leftarrow \frac{1}{\log(1 + t)}$
    5. convergencia = $(T(t)<T_{min})$ **o** $(t>t_{max})$ **o** $(\sum_{ai}|\langle \mathbf{M}_{ai}\rangle - \langle \mathbf{M}^{old}_{ai}\rangle|\le\epsilon )$
    6. $\langle \mathbf{M}^{antiguo}_{ai}\rangle\leftarrow \langle \mathbf{M}_{ai}\rangle$
5. **devuelve** ${\cal C}^{\ast}$, $\langle M^{\ast}\rangle$
```



Algunas consideraciones sobre el algoritmo anterior:
- Es **determinista**, es decir, no extraemos números aleatorios en ningún paso del algoritmo.
- La **temperatura inicial (inversa)** $\beta=1/T_{max}$, donde $T_{max}=T(0)$, se utiliza como en el SA para que todas las asignaciones sean casi igualmente probables: nótese que $e^{-\beta D(\mathbf{x}_a,\mathbf{c}_i)}\rightarrow 1$, si $\beta\rightarrow 0$. En estas condiciones, tenemos $\langle M_{ai}\rangle\approx 1/k$.
- **Inicialización**. $T_{max}$ se establece en la varianza máxima $\sigma^2_{max}$ de los datos. Si los datos son multidimensionales, como suele ocurrir, $\sigma^2_{max}$ tiene una interpretación espectral (PCA).
- Sin embargo, a medida que el algoritmo evoluciona, $\beta$ aumenta y la **decaimiento exponencial se vuelve más selectiva**: dado $D(\mathbf{x}_a,\mathbf{c}_i)\le D(\mathbf{x}_a,\mathbf{c}_j)+\alpha$, la segunda distancia decae exponencialmente más rápido que la primera a medida que $\beta$ aumenta.
**Expectativa y actualización alternas**. Dadas las probabilidades $\langle M_{ai}\rangle$, actualizamos los centros $\mathbf{c}_i$ y luego recalculamos las probabilidades hasta alcanzar un punto fijo (asignación/centros estables).
- **Convergencia**. El algoritmo converge al óptimo local más cercano de la energía libre al punto de inicialización ${\cal C}^0$. Añadimos la condición $\sum_{ai}|\langle \mathbf{M}_{ai}\rangle - \langle \mathbf{M}^{old}_{ai}\rangle|\le\epsilon$ con $\epsilon>0$, lo que significa que el algoritmo se detiene si los $\langle \mathbf{M}_{ai}\rangle$ son suficientemente estables. Por ejemplo, si empezamos estableciendo $\langle M_{ai}\rangle\approx 1/k$, el algoritmo solo realiza una iteración. ¿Por qué? Porque los centros del paso 4.2 no se modifican en absoluto.
**Complejidad**. Cada iteración requiere $O(mk)$ y el número de iteraciones puede acelerarse mediante un programa de recocido más rápido.
**Resultados**. El algoritmo devuelve los mejores centros ${\cal C}^{\ast}$ y las asignaciones óptimas $\langle \mathbf{M}_{ai}^{\ast}\rangle$ donde un punto $\mathbf{x}_a$ se asigna al clúster centrado en $\mathbf{c}_{i'}$ si:

$$
i' = \arg\max_{1\le i\le k}\langle \mathbf{M}_{ai}^{\ast}\rangle\;.
$$

Mostramos cómo funciona el algoritmo en puntos unidimensionales en el siguiente ejercicio:
<br></br>
<span style="color:#d94f0b">
**Ejercicio**. Dados los siguientes puntos ${\cal X}=\{1,2,3,7,7.5,8.25\}$ en $\mathbb{R}$, agrúpelos con $k=2$, comenzando desde un único grupo. Utilice la siguiente programación inversa de temperatura: $\beta(t+1)=\beta(t)\beta_r$, con $\beta_r = 1.075$.
<br><br>
Respuesta. Tenemos entonces un caso de agrupamiento central $(m=6,k=2)$. Primero, analizamos los datos. La media y la desviación estándar son, respectivamente, $\mu=4.79$ y $\sigma=2.87$. Podemos usar la media para codificar el centro único, por ejemplo: $c^0_1=c^0_2=\mu$. Sin embargo, esto resultaría en la terminación del algoritmo en una sola iteración con $\langle \mathbf{M}_{ai}\rangle = 0.5,\forall a,i$.
<br></br>
Una forma sencilla de evitar la configuración 50/50 es establecer $c^0_1=\mu + 0.01,\;\; c^0_2=\mu$. Entonces, los centros iniciales son $c_1^0 = \mathbf{4.801}$ y $c_2^0 = \mathbf{4.791}$.
<br></br>
Con respecto a $\beta(0)=1/T_{max}$ hacemos $T_{max}=\sig ma$ lo que resulta en $\beta(0)=1/2.87=0.34$.
</span>
<br></br>
<span style="color:#d94f0b">
Iteración 1. En cada iteración, recalculamos la matriz de distancias al cuadrado (transpuesta) $\mathbf{D}$, donde $\mathbf{D}_{ia}=(c_i-x_a)^2$ con $a\in\{1,\ldots,6\}$ e $i\in\{1,2\}$. La transponemos para visualizar mejor la distancia entre cada centro y cada punto de datos. Se visualiza mejor en forma de tabla:
</span>
<br></br>
<span style="color:#d94f0b">
$
\begin{alineado}
\begin{array}{c|ccc}
  \mathbf{D}^{(1)} & x_1 & x_2 & x_3 & x_4 & x_5 & x_6\\
  \hline
  c_1 y 14.452 y 7.849 y 3.246 y 4.832 y 7.281 y 11.891 \\
  c_2 y 14.376 y 7.793 y 3.210 y 4.876 y 7.335 y 11.960 \\  
  \hline
\fin{matriz}
\end{alineado}
$
</span>
<br></br>
<span style="color:#d94f0b">
Luego calculamos los exponenciales negativos (transpuestos) y la suma de cada columna para su posterior normalización:
<br></br>
<span style="color:#d94f0b">
$
\begin{alineado}
\begin{array}{c|cccccc}
  \exp(-\beta(0)\mathbf{D}^{(1)}) & x_1 & x_2 & x_3 & x_4 & x_5 & x_6\\
  \hline
  c_1 y 0,007 y 0,069 y 0,331 y 0,193 y 0,084 y 0,017 \\
  c_2 y 0,007 y 0,070 y 0,335 y 0,190 y 0,082 y 0,017 \\  
  \hline
  \suma & 0,014 & 0,139 & 0,666 & 0,383 & 0,166 & 0,034 \\
\fin{matriz}
\end{alineado}
$
</span>
<br></br>
<span style="color:#d94f0b">
Luego procedemos a normalizar las columnas, y también sumamos las filas resultantes para preparar el cálculo de los nuevos centros:
</span>
<br></br>
<span style="color:#d94f0b">
$
\begin{alineado}
\begin{array}{c|cccccc|c}
 \langle \mathbf{M}^{(1)}\rangle & x_1 & x_2 & x_3 & x_4 & x_5 & x_6 &\sum_{a=1}^m \langle \mathbf{M}^{(1)}_{ai}\rangle\\
  \hline
  c_1 y 0,493 y 0,495 y 0,496 y 0,503 y 0,504 y 0,505 y 2,996 \\
  c_2 y 0,506 y 0,504 y 0,503 y 0,496 y 0,495 y 0,494 y 2,998 \\  
  \hline
\fin{matriz}
\end{alineado}
$
</span>
<br></br>
<span style="color:#d94f0b">
Entonces los nuevos centros pasan a ser:
</span>
<br></br>
<span style="color:#d94f0b">
$
\begin{align}
\mathbf{c}_1^{(1)} &= \frac{1}{2.996}\left(\mathbf{1}\cdot 0.493 + \mathbf{2}\cdot 0.495 + \ldots + \mathbf{8.25}\cdot 0.505\right) = \mathbf{4.819}\\
\mathbf{c}_2^{(1)} &= \frac{1}{2.998}\left(\mathbf{1}\cdot 0.506 + \mathbf{2}\cdot 0.504 + \ldots + \mathbf{8.25}\cdot 0.494\right) = \mathbf{4.763}
\fin{alinear}
$
</span>
<br></br>
<span style="color:#d94f0b">
donde el primer centro $c_1$ comienza a atraer los valores más grandes de ${\cal X}$ y $c_2$ atrae los más bajos.
</span>
<br></br>
<span style="color:#d94f0b">
Iteración 2. Dados los nuevos centros, recalculamos sus distancias con respecto a todos los puntos en ${\cal X}$. La nueva distancia (transpuesta) es:
</span>
<br></br>
<span style="color:#d94f0b">
$
\begin{alineado}
\begin{array}{c|cccccc}
  \mathbf{D}^{(2)} & x_1 & x_2 & x_3 & x_4 & x_5 & x_6\\
  \hline
  c_1 y 14.590 y 7.950 y 3.311 y 4.753 y 7.183 y 11.766 \\
  c_2 y 14.164 y 7.637 y 3.110 y 5.001 y 7.487 y 12.155 \\  
  \hline
\fin{matriz}
\end{alineado}
$
</span>
<br></br>
<span style="color:#d94f0b">
Entonces, los exponenciales negativos normalizados para $\beta(2)=0.365$ son:
</span>
<br></br>
<span style="color:#d94f0b">
$
\begin{alineado}
\begin{array}{c|cccccc|c}
 \langle \mathbf{M}^{(2)}\rangle & x_1 & x_2 & x_3 & x_4 & x_5 & x_6 &\sum_{a=1}^m \langle \mathbf{M}^{(2)}_{ai}\rangle\\
  \hline
  c_1 y 0,461 y 0,471 y 0,481 y 0,522 y 0,527 y 0,535 y 2,997 \\
  c_2 y 0,538 y 0,528 y 0,518 y 0,477 y 0,472 y 0,464 y 2,997 \\  
  \hline
\fin{matriz}
\end{alineado}
$
</span>
<br></br>
<span style="color:#d94f0b">
Entonces los nuevos centros pasan a ser:
</span>
<br></br>
<span style="color:#d94f0b">
$
\begin{align}
\mathbf{c}_1^{(2)} &= \frac{1}{2.997}\left(\mathbf{1}\cdot 0.461 + \mathbf{2}\cdot 0.471 + \ldots + \mathbf{8.25}\cdot 0.535\right) = \mathbf{4.960}\\
\mathbf{c}_2^{(2)} &= \frac{1}{2.997}\left(\mathbf{1}\cdot 0.538 + \mathbf{2}\cdot 0.528 + \ldots + \mathbf{8.25}\cdot 0.464\right) = \mathbf{4.622}
\fin{alinear}
$
</span>
<br></br>
<span style="color:#d94f0b">
Iteración 3. Esta es la iteración **más informativa** hasta el momento, ya que los dos centros están claramente separados. Definen lo que posteriormente llamamos un **cambio de fase**. Las distancias dan una pista de ello:
</span>
<br></br>
<span style="color:#d94f0b">
$
\begin{alineado}
\begin{array}{c|cccccc}
  \mathbf{D}^{(3)} & x_1 & x_2 & x_3 & x_4 & x_5 & x_6\\
  \hline
  c_1 y 15,689 y 8,767 y 3,845 y 4,157 y \mathbf{6,446} y 10,817\\
  c_2 y 13.121 y \mathbf{6.876} y 2.632 y 5.653 y 8.280 y 13.159\\  
  \hline
\fin{matriz}
\end{alineado}
$
</span>
<br></br>
<span style="color:#d94f0b">
donde los valores más grandes son atraídos por $c_2$ y los más pequeños por $c_2$ (ver por ejemplo los datos en negrita).
Entonces, los exponenciales negativos normalizados para $\beta(3)=0.392$ son:
</span>
<br></br>
<span style="color:#d94f0b">
$
\begin{alineado}
\begin{array}{c|cccccc|c}
 \langle \mathbf{M}^{(3)}\rangle & x_1 & x_2 & x_3 & x_4 & x_5 & x_6 &\sum_{a=1}^m \langle \mathbf{M}^{(3)}_{ai}\rangle\\
  \hline
  c_1 y 0,267 y 0,322 y 0,383 y 0,642 y \mathbf{0,672} y 0,715 y 3,001 \\
  c_2 y 0,732 y \mathbf{0,677} y 0,616 y 0,357 y 0,327 y 0,284 y 2,993 \\  
  \hline
\fin{matriz}
\end{alineado}
$
</span>
<br></br>
<span style="color:#d94f0b">
y luego los nuevos centros más "polarizados":
</span>
<br></br>
<span style="color:#d94f0b">
$
\begin{align}
\mathbf{c}_1^{(3)} &= \frac{1}{3.001}\left(\mathbf{1}\cdot 0.267 + \mathbf{2}\cdot 0.322 + \ldots + \mathbf{8.25}\cdot 0.715\right) = \mathbf{5.828}\\
\mathbf{c}_2^{(3)} &= \frac{1}{2.993}\left(\mathbf{1}\cdot 0.732 + \mathbf{2}\cdot 0.677 + \ldots + \mathbf{8.25}\cdot 0.284\right) = \mathbf{3.752}
\fin{alinear}
$
</span>
<br></br>
<span style="color:#d94f0b">
Iteraciones 4 y 5. En estas iteraciones, las distancias intragrupo (en negrita) se reducen y se estabilizan.  
</span>
<br></br>
<span style="color:#d94f0b">
$
\begin{alineado}
\begin{array}{c|cccccc}
  \mathbf{D}^{(4)} & x_1 & x_2 & x_3 & x_4 & x_5 & x_6\\
  \hline
  c_1 y 23.317 y 14.659 y 8.002 y \mathbf{1.371} y \mathbf{2.792} y \mathbf{5.862} \\
  c_2 y \mathbf{7.575} y \mathbf{3.070} y \mathbf{0.565} y 10.547 y 14.045 y 20.229\\  
  \hline
\fin{matriz}
\end{alineado}
$
</span>
<br></br>
<span style="color:#d94f0b">
$
\begin{alineado}
\begin{array}{c|cccccc}
  \mathbf{D}^{(5)} & x_1 & x_2 & x_3 & x_4 & x_5 & x_6\\
  \hline
  c_1 y 42,347 y 30,332 y 20,317 y \mathbf{0,257} y \mathbf{0,000} y \mathbf{0,551} \\
  c_2 y \mathbf{1.0841} y \mathbf{0.001} y \mathbf{0.919} y 24.589 y 29.798 y 38.548 \\  
  \hline
\fin{matriz}
\end{alineado}
$
</span>
<br></br>
<span style="color:#d94f0b">
y los centros son respectivamente
</span>
<br></br>
<span style="color:#d94f0b">
$
\begin{align}
c_1^{(4)}&=7.507,\; c_2^{(4)}=2.041\\
c_1^{(5)}&=7.583,\; c_2^{(5)}=1.999\\
\fin{alinear}
$
<span>
<br></br>
<span style="color:#d94f0b">
<ins>Última iteración</ins>. Curiosamente, al final de la iteración 5, tenemos la siguiente matriz de asignación:
</span>
<br></br>
<span style="color:#d94f0b">
$
\begin{alineado}
\begin{array}{c|cccccc|c}
 \langle \mathbf{M}^{(5)}\rangle & x_1 & x_2 & x_3 & x_4 & x_5 & x_6 &\sum_{a=1}^m \langle \mathbf{M}^{(5)}_{ai}\rangle\\
  \hline
  c_1 y 0,000 y 0,000 y 0,000 y 0,999 y 0,999 y 0,999 y 2,997 \\
  c_2 y 0,999 y 0,999 y 0,999 y 0,000 y 0,000 y 0,000 y 2,997 \\  
  \hline
\fin{matriz}
\end{alineado}
$
</span>
<br></br>
<span style="color:#d94f0b">
Nótese que los primeros 3 puntos pertenecen al grupo 2 y los segundos 3 al grupo 1. ¿Es esto suficiente para converger? Veamos. Primero, recalculamos las distancias:
</span>
<br></br>
$
\begin{alineado}
\begin{array}{c|cccccc}
  \mathbf{D}^{(6)} y x_1 y x_2 ​​y x_3 y x_4 y x_5 y x_6\\
  \hline
  c_1 y 43,337 y 31,171 y 21,004 y 0,340 y 0,006 y 0,444 \\
  c_2 y 0,999 y 0,000 y 1,000 y 25,000 y 30,250 y 39,062 \\  
  \hline
\fin{matriz}
\end{alineado}
$
</span>
<br></br>
<span style="color:#d94f0b">
Entonces, los exponenciales negativos normalizados para $\beta(6)=0.488$ son:
</span>
<br></br>
<span style="color:#d94f0b">
$
\begin{alineado}
\begin{array}{c|cccccc|c}
 \langle \mathbf{M}^{(6)}\rangle & x_1 & x_2 & x_3 & x_4 & x_5 & x_6 &\sum_{a=1}^m \langle \mathbf{M}^{(3)}_{ai}\rangle\\
  \hline
  c_1 y 0,000 y 0,000 y 0,000 y 0,999 y 0,999 y 0,999 y 2,997 \\
  c_2 y 0,999 y 0,999 y 0,999 y 0,000 y 0,000 y 0,000 y 2,997 \\  
  \hline
\fin{matriz}
\end{alineado}
$
</span>
<br></br>
<span style="color:#d94f0b">
Esto está claramente "estabilizado" con respecto a $\langle \mathbf{M}^{(5)}\rangle$ (es idéntico). Como resultado, **los centros de los conglomerados serán idénticos** y el algoritmo **converge**, devolviendo estos centros de conglomerados $c_1^{(6)}=c_1^{(5)}$, $c_2^{(6)}=c_2^{(5)}$ y $\langle \mathbf{M}^{\ast}\rangle=\langle \mathbf{M}^{(6)}\rangle$.
</span>
<br></br>


#### Entropía y energía libre
El recocido determinista (DA) se basa en el siguiente **teorema**:

*Minimizar la energía libre $F(\omega)=-\frac{1}{\beta}\log Z$ es equivalente a maximizar la entropía $H(G)$ de la distribución de Gibbs $G(\omega)=\exp(-\beta{\cal E}(\omega))/Z$, donde ${\cal E}(\omega)$ es una función de costo (energía), como sigue:*

$$
F(\omega) = \langle {\cal E}(\omega) \rangle - \frac{1}{\beta}H(G)\;.  
$$

**Demostración**. Empecemos ampliando la definición de entropía (véase el **Apéndice**):

$$
\begin{align}
H(G) &:=-\sum_{\omega}G(\omega)\log G(\omega)\\
     &= -\sum_{\omega}\frac{\exp(-\beta{\cal E}(\omega))}{Z}\log \frac{\exp(-\beta{\cal E}(\omega))}{Z}\\
     &= -\sum_{\omega}\frac{\exp(-\beta{\cal E}(\omega))}{Z}\left[-\beta {\cal E}(\omega) - \log Z\right]\\
     &= -\sum_{\omega}G(\omega)\left[-\beta {\cal E}(\omega) - \log Z\right]\;.\\
\fin{alinear}
$$

Dado que $\langle {\cal E}(\omega) \rangle$ es la expectativa

$$
\langle {\cal E}(\omega) \rangle = \sum_{\omega}G(\omega){\cal E}(\omega)\;,
$$

tenemos

$$
\begin{align}
H(G) &= -\sum_{\omega}G(\omega)\left[-\beta {\cal E}(\omega) - \log Z\right]\\
     &= \beta\langle {\cal E}(\omega) \rangle + \sum_{\omega}G(\omega)\log Z\;.\\
\fin{alinear}
$$

Como $G(\omega)$ es una distribución de probabilidad, tenemos $\sum_{\omega}G(\omega)=1$ y por lo tanto

$$
H(G) = \beta\langle {\cal E}(\omega) \rangle + \log Z\;,
$$

Y por último,

$$
\begin{align}
-\log Z &= \beta\langle {\cal E}(\omega) \rangle - H(G)\\
-\frac{1}{\beta}\log Z &= \langle {\cal E}(\omega) \rangle -\frac{1}{\beta}H(G)\\
F(\omega) &= \langle {\cal E}(\omega)\rangle -\frac{1}{\beta}H(G)\;.\\
\fin{alinear}
$$

En consecuencia, como $H(G)\ge 0$, tenemos que minimizar $F(\omega)$ implica minimizar $\langle {\cal E}(\omega)\rangle$ (conocido como <span style="color:#f88146">**costo promedio**</span> o <span style="color:#f88146">**distorsión promedio**</span>) así como maximizar (es decir, -minimizar) la entropía $H(G)$ si el costo promedio se mantiene constante.

#### Entropía máxima
La expansión de la energía libre $F(\omega)$ como

$$
F(\omega) = \langle {\cal E}(\omega) \rangle - \frac{1}{\beta}H(G)\;.  
$$

sugiere cómo se minimiza:
1) Al principio, donde $T_{max}$ y $\beta\rightarrow 0$, el término dominante es el negativo de la entropía $-H(G)$. Esto significa que, en las primeras etapas del algoritmo, **la entropía se maximiza**.

2) La [Entropía Máxima](https://en.wikipedia.org/wiki/Principle_of_maximum_entropy) es un principio fundamental de la Teoría de la Información. Establece que: *<span style="color:#f88146">de todas las distribuciones de probabilidad que satisfacen un conjunto dado de restricciones, elegir la que maximice la entropía*</span>.

3) Las probabilidades de pertenencia, $\langle\mathbf{M}_{ai}\rangle$ pueden interpretarse como **probabilidades condicionales**  

$$
\langle\mathbf{M}_{ai}\rangle = p(\mathbf{x}_a\in \text{cluster}(\mathbf{c}_i))=p(C=
i|X=a)\;,
$$

es decir, dado un punto $\mathbf{x}_a$, $p(C=
i|X=a)$ denota <span style="color:#f88146">*la probabilidad de que $\mathbf{c}_i$ sea el verdadero centro de este punto*</span>. Esto suele llamarse <span style="color:#f88146">**probabilidad**</span>: qué tan bueno es que este centro sea una <span style="color:#f88146">**palabra clave**</span> de ese punto.

4) Como resultado, la **entropía condicional** $H(C|X)$ se maximiza en las primeras etapas de DA:

$$
\begin{align}
H(C|X)&= \sum_{\mathbf{x}_a}p(X=a)H(C|X=a)\\
      &\aprox \frac{1}{m}\sum_{\mathbf{x}_a}H(C|X=a)\\
      &= -\frac{1}{m}\sum_{\mathbf{x}_a}\sum_{\mathbf{c}_i}p(C=i|X=a)\log p(C=i|X=a)\\
      &= -\frac{1}{m}\sum_{a}\sum_{i}\langle\mathbf{M}_{ai}\rangle\log \langle\mathbf{M}_{ai}\rangle\\
\fin{alinear}
$$

Sin embargo, sería interesante calcular también la entropía condicional $H(X|C)$ para poder visualizar la **entropía por cúmulo** en lugar de la **entropía por punto** como en $H(C|X)$. Para ello, observe el teorema de Bayes:

$$
p(X|C)=\frac{p(C|X)p(X)}{p(C)}\;.
$$

Suponemos $p(X=a)=\frac{1}{m}$, ya que desconocemos de antemano la probabilidad de un dato específico. Sin embargo, para estimar $p(C)$, utilizamos la siguiente propiedad:

$$
\begin{align}
p(C=i) &= \sum_{\mathbf{x}_a}p(X=a)p(C=i|X=a)\\
       &= \frac{1}{m}\sum_{\mathbf{x}_a}p(C=i|X=a)\\
       &= \frac{1}{m}\sum_{a}\langle\mathbf{M}_{ai}\rangle\\
\fin{alinear}
$$

Entonces, tenemos eso

$$
p(X=a|C=i)=\frac{\frac{1}{m}\langle\mathbf{M}_{ai}\rangle}{\frac{1}{m}\sum_{a}\langle\mathbf{M}_{ai}\rangle} = \frac{\langle\mathbf{M}_{ai}\rangle}{\sum_{a}\langle\mathbf{M}_{ai}\rangle}
$$

Y por último

$$
\begin{align}
H(X|C) &= \sum_{\mathbf{c}_i}p(C=i)H(X|C=i)\\
       &\aprox \frac{1}{m}\sum_{\mathbf{c}_i}\sum_{a}\langle\mathbf{M}_{ai}\rangle H(X|C=i)\;,\\
\fin{alinear}
$$

dónde

$$
H(X|C=i) &= -\sum_{\mathbf{x}_a}p(X=a|C=i)\log p(X=a|C=i)\\
         &= -\sum_{a}\frac{\langle\mathbf{M}_{ai}\rangle}{\sum_{a}\langle\mathbf{M}_{ai}\rangle}\log \frac{\langle\mathbf{M}_{ai}\rangle}{\sum_{a}\langle\mathbf{M}_{ai}\rangle}\;.
$$

es la <span style="color:#f88146">**entropía por clúster** $i$</span> y es una buena cantidad para analizar la **convergencia del algoritmo**.

Observe, por ejemplo, {numref}`KM-entropy-example` las soluciones del ejercicio anterior, donde $\langle M_{ai}\rangle$ se comportan como variables de Bernouilli cuando tenemos dos clústeres. En la última iteración, la **entropía máxima por clúster** es menor que la inicial: ronda $1$ bit (es decir, $\log 3=1.09$ nats) porque la mitad de los puntos pertenecen a cada clúster y la otra mitad no. Esto **indica una buena convergencia**.

```{figura} ./images/Topic2/KM-entropy-example-removebg-preview.png
---
nombre: KM-entropía-ejemplo
ancho: 800px
alinear: centro
altura: 600px
---
DA como minimización de entropía en el ejemplo del ejercicio.
```

Sin embargo, como mostramos en {numref}`KM-entropy-example-K3` en el ejemplo de motivación para $k=3$ clústeres, la **entropía máxima final por clúster** es de alrededor de $4-5$ bits (es decir, $\log 10² = 4.62$ nats). Esto indica que los datos <span style="color:#f88146">**no están bien cuantificados**</span> con $k=3$ centros.


```{figura} ./images/Topic2/KM-entropy-example-K3-removebg-preview.png
---
nombre: KM-entropía-ejemplo-K3
ancho: 800px
alinear: centro
altura: 600px
---
DA como minimización de entropía el ejemplo motivador (K=3).
```

Sin embargo, como mostramos en {numref}`KM-entropy-example-K2` en el ejemplo que motiva para $k=3$ clústeres, la **entropía máxima final por clúster** es de alrededor de $5$ bits (es decir, $\log 201 = 5.30$ nats). Esto indica que los datos están <span style="color:#f88146">**mejor cuantificados**</span> con $k=2$ centros: <span style="color:#f88146">¡obtenemos (casi) la misma entropía con menos centros!</span>

```{figura} ./images/Topic2/KM-entropy-example-K2-removebg-preview.png
---
nombre: KM-entropía-ejemplo-K2
ancho: 800px
alinear: centro
altura: 600px
---
DA como minimización de entropía el ejemplo motivador (K=2).
```

En realidad, los nuevos centros son $\mathbf{c}_1=[0,-1]^T$ y $\mathbf{c}_2=[0,2]^T$ (ver {numref}`KM-clusters-K2`).

```{figura} ./images/Topic2/KM-clusters-K2-removebg-preview.png
---
nombre: KM-clusters-K2
ancho: 800px
alinear: centro
altura: 600px
---
Clústeres y prototipos estimados en $\mathbb{R}^2$ (K=2).
```

Como resultado, <span style="color:#f88146">**la entropía es crucial** para la interpretación de los problemas de agrupamiento.</span>


## SoftMax para correspondencia de gráficos

### Máxima suavidad
#### Métodos de continuación
Volviendo al problema de correspondencia de grafos o MCS (Subgrafo Común Máximo), lo hemos formulado en
<span style="color:#f88146">**Términos discretos** a través de SA</span>:
1) El espacio de búsqueda ${\cal P}$ es el conjunto de **matrices binarias**
$\mathbf{M}\in\{0,1\}^{m\times n}$ cuyas filas y columnas tienen un único $1$. Cuando $m=n$ tenemos que el espacio de búsqueda es
el permutoedro $\Pi_n$, es decir, el conjunto de **matrices de permutación**.
2) SA explora el espacio de búsqueda a través de **caminatas aleatorias** que eventualmente alcanzan el **máximo global**
bajo un **programa de recocido lento**. Cada iteración requiere $O(n^4)$ para evaluar la
función de costo cuadrática $F(\mathbf{M})$.

Hemos visto que la agrupación central se puede plantear, sin embargo, en <span style="color:#f88146">**términos continuos** a través de DA</span>:
1) El espacio de búsqueda es $\mathbb{R}^d\times {\cal P}$: tenemos que encontrar conjuntamente $k$ centros
$\mathbf{c}_i\in\mathbb{R}^d$ y una matriz binaria $\mathbf{M}\in\{0,1\}^{m\times k}$ que indica
cómo se asignan los $m$ puntos $\mathbf{x}_a\in\mathbb{R}^d$ al grupo más probable.

2) DA **desacopla la optimización** de la energía libre $F({\cal C},\mathbf{M})$: dado un sistema de alta entrópica
(casi uniforme) asignación inicial alternamos **expectativa** (actualizar las asignaciones mientras
los centros son fijos) y **actualizan** los centros. Cada iteración toma $O(m\times k)$ y
**Permite programas de recocido más rápidos**.

3) <span style="color:#f88146">**Recuerde**</span> que el éxito de DA depende de la posibilidad de evaluar $Z$
(la función de partición de Gibbs) gracias al **supuesto de independencia**: se supone que los puntos
ser asignados independientemente a cualquier grupo.  


En el [marco de Gurobi](https://gurobi-optimods.readthedocs.io/es/latest/index.html),
Para la optimización, donde la coincidencia de gráficos se considera una camarilla máxima, muchos algoritmos combinatorios comparten
las siguientes características con DA:

1) **Transformar** el problema discreto original en uno continuo.

2) **Optimizar** la función objetivo en el espacio continuo mediante un método polinomial.

3) **Revertir** el resultado al espacio discreto a través de una heurística de *limpieza*.
 
Estos métodos se denominan <span style="color:#f88146">**método de continuación**</span>.

#### Operador SoftMax
En 1996, [Steven Gold y Anand Rangarajan](https://www.cise.ufl.edu/~anand/pdf/pamigm3.pdf)
Explotó el siguiente **algoritmo simple** para encontrar el elemento máximo en una lista
de números:

```{prf:algorithm} Máximo suave
:label: Algoritmo Softmax

**Entradas** Una lista de elementos $L=[X_1,\ldots,X_m]$ con $X_i\in\mathbb{R}$, $\beta_0>0$\
**Salidas** $m_i>0$ si $X_i=\max_{L}$ y $0$ en caso contrario.

1. Inicializar $\beta\leftarrow \beta_0$
2. **mientras** $\beta < \beta_f$:  

    1. **para** $i=1,\ldots, m$:
    
          $m_i\leftarrow \exp(\beta X_i)$
    
    2. **para** $i=1,\ldots, m$:
    
          $m_i\leftarrow \frac{m_i}{\sum_{i=1}^m_i}$

    3. Aumentar $\beta$

3. **devuelve** $\{m_i\}$ donde $\sum_{i=1}^m m_i=1$
```

Este algoritmo es equivalente a dar el $\{m_i\}$ que maximiza
$\sum_{i=1}^m m_iX_i$, ahora formulado en términos continuos a través del **parámetro de control**
$\beta>0$. Este es el operador **softmax**:

$$
m_j = \frac{\exp(\beta X_j)}{\sum_{i=1}^m\exp(\beta X_i)}\;,
$$

¡Cuál es el mecanismo clásico para seleccionar la pertenencia a una clase en la última capa de una red neuronal!

Mostramos este mecanismo en {numref}`DAExample`. A medida que aumentamos $\beta$, el $m_i$ correspondiente al $X_i$ máximo
(tenga en cuenta que puede haber muchos valores máximos) tienden a $1$, mientras que los $m_i$ para los valores no máximos caen a $0$.
En la jerga de las redes neuronales, este mecanismo se denomina **el ganador se lo lleva todo** o **WTA**.

```{figura} ./images/Topic2/DAExample-Photoroom.png
---
nombre: DAExample
ancho: 800px
alinear: centro
altura: 800px
---
Softmaxizar una lista de elementos con valores reales.
```

### Tarea graduada
#### Asignación lineal
La asignación lineal (AL) es un problema polinomial con muchas aplicaciones en informática e inteligencia artificial.
Dado un **gráfico bipartito** $G=(V,E)$ donde: a) $V = V_1\cup V_2$,$V_1\cap V_2=\emptyset$ es
una partición de vértices y b) $E=V_1\times V_2$, es decir, solo hay aristas entre $V_1$ y $V_2$.
Además, el gráfico está **ponderado** ya que se nos da una matriz de variables.
$\mathbf{X}\in\mathbb{R}^{m\times n}$, con $m=|V_1|$, $n=|V_2|$, donde $\mathbf{X}_{ai}$ mide la **afinidad**
entre $i\in V_1$ y $j\in V_2$ y su significado depende del problema (compatibilidad entre procesos y
CPU, similitud local entre puntos de dos formas, etc.).  

La <span style="color:#f88146">versión **discreta** (original)</span> de Los Ángeles es bastante obvia:

$$
\begin{align}
\mathbf{M}^{\ast} &= \arg\max_{{\cal P}} E(\mathbf{M})=\sum_{a\in V_1}\sum_{i\in V_2}\mathbf{M}_{ai}\mathbf{X}_{ai}\\
{\cal P}=&\left\{\mathbf{M}\en \{0,1\}^{m\times n}:\para todo a\en V_1:\sum_{i\en V_2}\mathbf{M}_{ai}\le 1\;\text{y}\; \para todo i\en V_2:\sum_{a\en V_1}\mathbf{M}_{ai}\le 1\;\right\}
\fin{alinear}
$$

En otras palabras, <span style="color:#f88146">LA es la **versión lineal** de QAP</span> donde $\mathbf{X}$ tiene **valor real**
En lugar de ser una matriz de adyacencia. Respecto al espacio de búsqueda, si $m=n$ entonces ${\cal P}=\Pi_n$
El espacio es el permutoedro. Sin embargo, no está en NP y, de hecho, se puede resolver en $O(n^3)$ con
el llamado [algoritmo húngaro] (https://en.wikipedia.org/wiki/Hungarian_algorithm).

Sin embargo, aquí vamos a presentar la <span style="color:#f88146">versión **suave/continua**</span> que
es básicamente una extensión de **SoftMax** que incorpora:
**Asignaciones continuas**. En lugar de $\mathbf{M}\in \{0,1\}^{m\times n}$, tenemos $\mathbf{M}\in [0,1]^{m\times n}$.
**Restricciones bidireccionales**. Cada $i\in V_1$ tiene una **probabilidad** de ser asignado a $a\in V_2$ y viceversa. Por lo tanto:

$$
\para todo a:\sum_{i=1}^n\mathbf{M}_{ai}=1\;\;\text{y}\;\;\para todo i:\sum_{a=1}^m\mathbf{M}_{ai}=1\;.
$$

es decir, nuestro espacio de búsqueda es una generalización matricial del <span style="color:#f88146">**simplex**(vectorial)</span>:

$$
\Delta_n =\left\{\{m_i\}\in\mathbb{R}^n:\sum_{i=1}^nm_i=1\right\}\;.
$$

En realidad, si $m=n$ el espacio de búsqueda no es el Permutoedro $\Pi_n$ sino el
[Politopo de Birkhoff](https://en.wikipedia.org/wiki/Doubly_stochastic_matrix) $\mathbb{B}_n$. en matricial
En términos, $\mathbb{B}_n$ es el conjunto de matrices **doblemente estocásticas** (matrices cuyas filas y columnas suman $1$).
En este sentido, recuerda que $\Pi_n\subset \mathbb{B}_n$ ya que toda matriz de permutación es doblemente estocástica.
Por lo tanto, los vértices del politopo de Birkhoff son los elementos de $\Pi_n$ (soluciones al problema discreto)
pero durante la resolución del problema <span style="color:#f88146">**soluciones continuas** que se encuentran en el
Los bordes y lados del politopo están **permitidos**.</span>

Algorítmicamente, **SoftLA** debe **aplicar las restricciones bidireccionales** en cada iteración de la siguiente manera:

```{prf:algoritmo} SoftLA
:label: Algoritmo SoftLA

**Entradas** Matriz de afinidad $\mathbf{X}\in\mathbb{R}^{m\times n}$, $\beta_0>0$\
**Salidas** $\mathbf{M}^{\ast}$ asignación máxima.

1. Inicializar $\beta\leftarrow \beta_0$
2. **mientras** $\beta < \beta_f$:  

    1. $\mathbf{M}_{ai}\leftarrow \exp(\beta \mathbf{X}_{ai})$
    
    2. $\mathbf{M}\leftarrow\text{Cuerno de sumidero}(\mathbf{M})$
   
    3. Aumentar $\beta$

3. **devuelve** $\mathbf{M}^{\ast}$ matriz doblemente estocástica óptima.
```
donde $\text{Sinkhorn}(\mathbf{M})$ es un proceso iterativo de normalización de filas y columnas que
converge a una matriz estocástica:

```{prf:algoritmo} Sinkhorn
:label: Sinkhorn-alg

**Entradas** Matriz de asignación exponencial: $\mathbf{M}=\exp(\beta\mathbf{X})$\
**Salidas** $\mathbf{M}$ matriz doblemente estocástica.

1. $t\leftarrow 0$

2. convergencia$\leftarrow$ Falso

3. **mientras** $\neg$convergencia:

    1. $\mathbf{M}^{old}_{ai}\leftarrow \mathbf{M}_{ai}$

    2. **para** $a=1,2,\ldots,m$ (Normalizar filas)

        $\mathbf{M}_{ai}\leftarrow \frac{\mathbf{M}_{ai}}{\sum_{i=1}^n \mathbf{M}_{ai}}$
    
    3. **para** $i=1,2,\ldots,n$ (Normalizar columnas)

        $\mathbf{M}_{ai}\leftarrow \frac{\mathbf{M}_{ai}}{\sum_{i=a}^m \mathbf{M}_{ai}}$

    4. $t\leftarrow t + 1$
    5. convergencia = $(t>t_{max})$ **o** $(\sum_{ai}|\mathbf{M}_{ai}- \mathbf{M}^{old}_{ai}|\le\epsilon )$
  
  

3. **devuelve** $\mathbf{M}$ matriz doblemente estocástica.
```

Curiosamente, la estructura de $\text{SoftLa}$ es bastante simple y esencialmente es similar a la de
de $\text{SoftMax}$ pero para matrices, tomando $O(n^2)$ en lugar de $O(n^3)$ como el algoritmo húngaro.

En {numref}`Húngaro` mostramos cómo $\text{SoftLa}$ resuelve un problema en un par de
iteraciones

```{figura} ./images/Topic2/SA-Hungarian-removebg-preview.png
---
nombre: húngaro
ancho: 800px
alinear: centro
altura: 600px
---
Solución SoftLA para una instancia $m=n=5$ con costos aleatorios.
```

Tenga en cuenta que:
1) La inicialización general es $\mathbf{M}^0=\mathbf{1}^T\mathbf{1}+ \epsilon\mathbf{I}$,
es decir, la matriz de unos con una ligera perturbación: $\mathbf{M}^0_{ai}=1+\epsilon$. Esta
La inicialización se conoce como **baricentro** o **neutral**.
2) En el ejemplo anterior, $\mathbf{X}$ se extrae de $n\times n$ números enteros **aleatorios** entre $0$ y $n^2-1$.
3) El papel de $\text{Sinkhorn}$ es hacer cumplir las restricciones bidireccionales y, a veces, puede conducir a
a una matriz doblemente estocástica muy entrópica como mostramos en el siguiente ejercicio.
<br></br>
<span style="color:#d94f0b">
**Ejercicio**. Demuestre que al aplicar $\text{Sinkhorn}$ a la exponenciación de la matriz anterior
Converge a una asignación de entropía máxima. No utilice $\beta$. Explique **por qué**.
</span>
<br></br>
<span style="color:#d94f0b">
$
\mathbf{X}=
\begin{bmatrix}
x y x+\épsilon\\
x-\épsilon y x\\
\fin{bmatrix}
$
</span>
<br></br>
<span style="color:#d94f0b">
A priori, parece que la asignación óptima es $(a=1)\rightarrow (i=2)$ y $(a=2)\rightarrow (i=2)$
Pero esto no es posible debido a la restricción de doble sentido. Apliquemos la exponencial:
</span>
<br></br>
<span style="color:#d94f0b">
$
\mathbf{M}=
\begin{bmatrix}
e^x y e^{x+\épsilon}\\
e^{x-\epsilon} y e^x\\
\fin{bmatrix}
$
</span>
<br></br>
<span style="color:#d94f0b">
La <ins>normalización de filas</ins> hace que las cosas sean independientes de $x$:
</span>
<br></br>
<span style="color:#d94f0b">
$
\begin{align}
\mathbf{M} &=
\begin{bmatrix}
\frac{e^x}{e^x + e^{x+\epsilon}} & \frac{e^{x+\epsilon}}{e^x + e^{x+\epsilon}}\\
\frac{e^{x-\epsilon}}{e^x + e^{x-\epsilon}} & \frac{e^x}{e^x + e^{x-\epsilon}}\\
\fin{bmatrix}
=\begin{bmatrix}
\frac{1}{1 + e^{\epsilon}} & \frac{e^{\epsilon}}{1 + e^{\epsilon}}\\
\frac{e^{-\epsilon}}{1 + e^{-\epsilon}} & \frac{1}{1 + e^{-\epsilon}}\\
\fin{bmatrix}
\fin{alinear}
$
</span>
<br></br>
<span style="color:#d94f0b">
<ins>Normalización de columnas</ins>:
</span>
<br></br>
<span style="color:#d94f0b">
$
\begin{align}
\mathbf{M}_{:1} &= \frac{1}{1 + e^{\epsilon}} + \frac{e^{-\epsilon}}{1 + e^{-\epsilon}}
                 = \frac{(1 + e^{-\epsilon})+e^{-\epsilon}(1 + e^{\epsilon})}{(1 + e^{\epsilon})(1 + e^{-\epsilon})}
                 = \frac{(1 + e^{-\epsilon}) + (1 + e^{-\epsilon})}{(1 + e^{\epsilon})(1 + e^{-\epsilon})}
                 = \frac{2}{1 + e^{\epsilon}}\\
\mathbf{M}_{:2} &= \frac{e^{\epsilon}}{1 + e^{\epsilon}} + \frac{1}{1 + e^{-\epsilon}}
                 = \frac{e^{\epsilon}(1 + e^{-\epsilon}) + (1 + e^{\epsilon})}{(1 + e^{\epsilon})(1 + e^{-\epsilon})}
                 = \frac{(1 + e^{\epsilon}) + (1 + e^{\epsilon})}{(1 + e^{\epsilon})(1 + e^{-\epsilon})}
                 = \frac{2}{1 + e^{-\epsilon}}
\fin{alinear}   
$
</span>
<br></br>
<span style="color:#d94f0b">
$
\begin{align}
\mathbf{M} &=
\begin{bmatrix}
\frac{\mathbf{M}_{a1}}{\mathbf{M}_{:1}} & \frac{\mathbf{M}_{a2}}{\mathbf{M}_{:2}} \\
\frac{\mathbf{M}_{b1}}{\mathbf{M}_{:1}} & \frac{\mathbf{M}_{b2}}{\mathbf{M}_{:2}} \\
\fin{bmatrix}
= \begin{bmatrix}
\frac{1}{1 + e^{\epsilon}}:\frac{2}{1 + e^{\epsilon}} & \frac{e^{\epsilon}}{1 + e^{\epsilon}}:\frac{2}{1 + e^{-\epsilon}}\\
\frac{e^{-\epsilon}}{1 + e^{-\epsilon}}:\frac{2}{1 + e^{\epsilon}} & \frac{1}{1 + e^{-\epsilon}}:\frac{2}{1 + e^{-\epsilon}}\\
\fin{bmatrix}
= \begin{bmatrix}
\frac{1}{2} y \frac{1}{2}\\
\frac{1}{2} y \frac{1}{2}\\
\fin{bmatrix}
\fin{alinear}
$
</span>
<br></br>
<span style="color:#d94f0b">
Lo cual prueba la afirmación. ¿Por qué? Bueno, añadiendo una $\epsilon$ en una columna y
Restarlo en la columna opuesta conduce a una incertidumbre máxima con respecto a la diagonal.
que se conserva. Esto no es obvio, e incluso **contra-intuitivo**, pero se aclara un poco con la eliminación de
$x$ después de la normalización de filas.
</span>
<br></br>

#### Asignación suave
La extensión de $\text{SoftLa}$ a la correspondencia de grafos es casi directa. Ahora, en lugar de
Al tener una función de costo lineal, la función de costo coincidente con el gráfico es **cuadrática** en $\mathbf{M}$
(es el problema de asignación cuadrática QAP). Entonces, el <span style="color:#f88146">**QAP relajado**</span> se convierte en

$$
\begin{align}
\mathbf{M}^{\ast}= & \arg\max_{{\cal B}}F(\mathbf{M}) = \frac{1}{2}\sum_{a\in V}\sum_{i\in V'}\sum_{b\in V}\sum_{j\in V'}\mathbf{M}_{ai}\mathbf{M}_{bj}\mathbf{X}_{ab}\mathbf{Y}_{ij}\\
{\cal B}=&\left\{\mathbf{M}\en [0,1]^{(m+1)\times (n+1)}:\para todo a\en V:\sum_{i\en V'}\mathbf{M}_{ai}=1\;\text{y}\; \para todo i\en V':\sum_{a\en V}\mathbf{M}_{ai}=1\;\right\}
\fin{alinear}
$$

dónde
1) ${\cal B}$ es el conjunto de matrices doblemente estocásticas de dimensión $(m+1)\times (n+1)$, y
el politopo de Birkhoff u orden $n+1$, es decir ${\cal B}_{n+1}$, si $m=n$.

2) ¿Por qué una **dimensión extra**? Si $m<n$, por ejemplo, solo podemos tener $m$ asignaciones uno a uno.
y $nm$ nodos no asignados. Para solucionar esto, asumimos que estos nodos no asignados
coincide con un <span style="color:#f88146">nodo **slack** o **virtual**</span>.
Por lo tanto, añadir una dimensión extra da cabida a dos dimensiones virtuales.
Nodos (uno por grafo). Razonamiento similar para $m>n$.

Tenga en cuenta que $\text{SoftLA}$ es solo un recocido determinista (DA) aplicado a la asignación lineal.
Si es así, una de las características principales de DA es <span style="color:#f88146">asumir la **independencia de asignación**</span>,
es decir, podemos suponer que la *asignación de $a\in V$ a $i\in V'$ es independiente de la de
otro $a'\in V$ a $i'\in V'$*.

**Expansión de Taylor**. [Steven Gold y Anand Rangarajan](https://www.ciseufl.edu/~anand/pdf/pamigm3.pdf) utilizaron un principio similar.
Para aproximar la función de costo cuadrática. Nótese que $f(x)\approx f(a) + f'(a)(xa)$ es
La expansión de Taylor de primer orden. Entonces  

$$
F(\mathbf{M})\approx F(\mathbf{M}^0) + F'(\mathbf{M}^0)\cdot\sum_{a\in V}\sum_{i\in V}(\mathbf{M}_{ai}-\mathbf{M}^0_{ai})\;.
$$

dónde

$$
F'(\mathbf{M}^0):={\frac{\partial F}{\partial\mathbf{M}_{a_i}}}\bigg|_{\mathbf{M}^0}=\underbrace{\sum_{b\in V}\sum_{j\in V'}\mathbf{M}_{bj}\mathbf{X}_{ab}\mathbf{Y}_{ij}}_{\mathbf{Q}_{ai}}\\
$$

Es decir, ¡la derivada de una función cuadrática es lineal! Entonces, para un $\mathbf{M}^0$ fijo,
tener eso

$$
\max F(\mathbf{M}) = \max \sum_{a\in V}\sum_{i\in V}\mathbf{M}_{ai}\mathbf{Q}_{ai}\;,
$$

es decir, un **problema de asignación lineal**.
En otras palabras:
1) $\mathbf{Q}_{ai}=\sum_{b\in V}\sum_{j\in V'}\mathbf{M}_{bj}\mathbf{X}_{ab}\mathbf{Y}_{ij}$ funciona como
una **matriz de afinidad temporal** para cada $\beta$.
2) Dado $\mathbf{Q}_{ai}$ iteramos para obtener la mejor asignación (máxima) $\mathbf{M}_{ai}$ para esto
$\beta$, es decir, resolvemos un **nuevo problema de asignación**.
3) ¡Aumenta $\beta$ y comienza de nuevo!

Esta es la típica **estructura desacoplada** de los problemas de DA y conduce a la
Algoritmo $\text{SoftAssign}$ detallado a continuación.

```{prf:algoritmo} SoftAssign
:label: Algoritmo de asignación suave

**Entradas** Matrices de adyacencia $\mathbf{X}\in\{0,1\}^{m\times m}$, $\mathbf{Y}\in\{0,1\}^{n\times n}$, $\beta_0>0$\
**Salidas** $\hat{\mathbf{M}}^{\ast}$ asignación cuadrática máxima (extendida).

1. Inicializar $\beta\leftarrow \beta_0$, $\hat{\mathbf{M}}_{ai}\leftarrow 1+\epsilon$
2. **mientras** $\beta < \beta_f$:  
    
    1. $t\leftarrow 0$

    2. convergencia$\leftarrow$ Falso

    3. **mientras** $\neg$convergencia:

        1. $\hat{\mathbf{M}}^{viejo}_{ai}\leftarrow \hat{\mathbf{M}}_{ai}$

        2. $\mathbf{Q}_{ai}\leftarrow \sum_{b=1}^m\sum_{j=1}^n\mathbf{M}_{bj}\mathbf{X}_{ab}\mathbf{Y}_{ij}$
      
        3. $\mathbf{M}^0_{ai}\leftarrow \exp(\beta \mathbf{Q}_{ai})$
    
        4. Expande $\mathbf{M}^0\rightarrow \hat{\mathbf{M}}^0$

        5. $\hat{\mathbf{M}}^0\leftarrow\text{Sinkhorn}(\hat{\mathbf{M}}^0)$

        6. $t\leftarrow t + 1$

        7. convergencia = $(t>t_{max})$ **o** $(\sum_{ai}|\hat{\mathbf{M}}_{ai}- \hat{\mathbf{M}}^{old}_{ai}|\le\epsilon' )$
   
    3. Aumentar $\beta$

3. **devuelve** $\hat{\mathbf{M}}^{\ast}$ matriz doblemente estocástica óptima.
```

Algunas notas:

1) Si $m\neq n$ siempre asumimos que $m\le n$, es decir, $\mathbf{X}$ es el gráfico más pequeño.

2) Dado el $\hat{\mathbf{M}}$ expandido en el paso $1$, implícitamente usamos su
$\mathbf{M}$ matriz $m\times n$ en los pasos $3.2$ y $3.3$.

2) En el paso $3.4$ expandimos explícitamente $\mathbf{M}^0$ incorporando una fila y una columna adicionales
de ceros. Nótese que $\text{Sinkhorn}$ **siempre necesita** una matriz $(m+1)\times (n+1)$ si $m\neq n$!

**Complejidad**. No es difícil ver que la complejidad de $\text{SoftAssign}$ es
aproximadamente $O(n^3)$, o más precisamente $O(|E|n)$, si $m=n$ y $|E|$ es el número de aristas.
Esta complejidad se debe al paso 3.2 (el cálculo de $\mathbf{Q}$ que implica la
producto de 3 matrices).

#### Limpieza
Recuerde que los métodos de continuación se **resuelven en el continuo** pero nuestro **método original**
es discreto**. Dada la solución $\text{SoftAssign}$ $\hat{\mathbf{M}}^{\ast}$, que puede
sea ​​muy entrópico, debemos recuperar la matriz discreta más cercana (que no es única, en general).
Esta tarea se realiza mediante una <span style="color:#f88146">**heurística de limpieza** o algoritmo</span> como el que se detalla
abajo:


```{prf:algorithm} Limpieza
:label: Algoritmo de limpieza

**Entradas** $\hat{\mathbf{M}}\in[0,1]^{(m+1)\times (n+1)}$ matriz doblemente estocástica óptima\
**Salidas** Matriz discreta más cercana $\mathbf{M}\in\{0,1\}^{(m+1)\times (n+1)}$

1. todavía_asignado $\leftarrow 0$
2. $\mathbf{M}[a,i]\leftarrow 0$
3. $\epsilon \leftarrow 10^{-6}$

4. **mientras** aún_asignado$< m$:  
    
    1. cambios_hechos$\leftarrow$ Falso

    2. **para** $a\in\{1,2,\ldots,m+1\}$:

        1. candidatos $\leftarrow \emptyset$

        2. fila_máxima $\leftarrow \max\:\hat{\mathbf{M}}[a,:]$

        3. capacidad_de_filas $\leftarrow$ fila_máxima $- \epsilon$

        4. **para** $i\in\{1,2,\ldots,n+1\}$:
        
            1. columna máxima $\leftarrow \max\;\hat{\mathbf{M}}[i,:]$

            2. capacidad_de_columna $\leftarrow$ máxima_columna $- \epsilon$

            3. **si** $(\mathbf{M}[a,i]>$capacidad_fila$)$ **y** $(\mathbf{M}[a,i]>$capacidad_columna$)$:

                candidatos $\leftarrow$ candidatos $\cup \{i\}$
        
        5. **si** $|$candidatos$|$>0:

            1. máx_val $\leftarrow$ $\max \mathbf{M}[a,$candidatos$]$

            2. selección $\leftarrow$ $\arg\max$ $\mathbf{M}[a,$candidatos$]$

            3. col $\leftarrow$ candidatos[selección]

            4. todavía_asignado $\leftarrow$ todavía_asignado + 1

            5. $\mathbf{M}[a,$col$]\leftarrow$ 1

            6. $\mathbf{M}[a,:]\leftarrow-\infty$

            7. $\mathbf{M}[:,col]\leftarrow-\infty$

            8. cambios_hechos $\leftarrow$ Verdadero
    
    3. **si** $\neg$ cambios_hechos:

          **romper**

5. **devuelve** $\mathbf{M}$ matriz binaria.
```

El algoritmo, básicamente una <span style="color:#f88146">versión **codiciosa** del algoritmo húngaro</span>, procede de la siguiente manera:
1) <ins>Pasos 2.1-2.4</ins>. Para cada fila $a$, construimos una lista de *candidatos*, manteniendo un registro tanto de la fila como de la columna.
capacidades.
2) <ins>Paso 2.5</ins>. Si la lista de candidatos no está vacía, procedemos a seleccionar al mejor (paso 5.5) y luego procedemos.
para excluir la fila y columna correspondientes (pasos 5.6 y 5.7).

Esto requiere $O(n^2)$ y podría reemplazarse con una ejecución de $\text{SoftLA}$. Recuerde que si el algoritmo
encuentra alguna coincidencia con un vértice flojo, estas coincidencias deben borrarse.

**Resultados**. Volviendo al isomorfismo de la aspirina, utilizamos la configuración recomendada.
en el artículo de Gold y Rangarajan: $\epsilon = 0.1$, $\epsilon'=0.5$, $\beta_0=0.5$,
$\beta_f=10.0$, $\beta_r=1.075$ y $I_0=4$, $I_1=30$, donde los dos últimos números
son las iteraciones máximas del bucle interno **while** y $\text{Sinkhorn}$,
respectivamente.

El resultado en {numref}`DA-Aspirina` es casi perfecto y podemos afirmar que Aspirina
¡es isomorfo con respecto a una permutación de sí mismo!

```{figura} ./images/Topic2/DA-Aspirnin-removebg-preview.png
---
nombre: DA-Aspirina
ancho: 800px
alinear: centro
altura: 600px
---
Detección del isomorfismo de la aspirina con DA.
```

Dejamos para las clases prácticas la ampliación del algoritmo para incorporar
ambos <span style="color:#f88146">atributos** de nodo y borde</span>.


## Apéndice
### Independencia
**Independencia estadística**. Es bien sabido que dos variables aleatorias $A$ y $B$ son **independientes** si y solo si:

$$
p(A,B) = p(A)\cdot p(B)\;.
$$

O, en otras palabras, aplicando el teorema de Bayes tenemos que $A$ y $B$ son independientes si y solo si

$$
p(A,B) = p(B|A)p(A) = p(A|B)p(B)\Rightarrow p(B|A)=p(B)\;\text{y}\;p(A|B)=p(B)\;.
$$

En otras palabras:
- La independencia implica factorizar la distribución conjunta $p(A,B)$
- $A$ y $B$ son independientes si el conocimiento de uno de ellos no influye en la probabilidad del otro, es decir, $p(A|B)=p(A)$ y $p(B|A)=p(B)$.

**Marginación**. Alternativamente, podemos definir la independencia estadística comprobando las probabilidades marginales. Sean $a_1,a_2,\ldots,a_m$ los valores discretos de $A$ y $b_1,b_2,\ldots,b_n$ de forma similar para $B$. Entonces:

$$
\begin{align}
&&\sum_{a_i}\sum_{b_j}p(A=a_i,B=b_j)=1\;\text{probabilidad total}\\
&& p(A=a_i)=\sum_{b_j}p(A=a_i,B=b_j)\;\text{marginal wrt}\; A\\
&& p(B=b_i)=\sum_{a_i}p(A=a_i,B=b_j)\;\text{marginal wrt}\; B\\
\fin{alinear}
$$

Entonces, $A$ y $B$ son independientes si podemos escribir una distribución conjunta como el producto de dos distribuciones marginales:

$$
p(A=a_i,B=b_j) = p(A=a_i)\cdot p(B=b_j)\;\para todo a_i,b_j\;.
$$

Practiquemos un poco este concepto en el siguiente ejercicio.

<br></br>
<span style="color:#d94f0b">
**Ejercicio**. Dada la tabla anterior que representa la distribución conjunta de dos variables aleatorias discretas $A$ y $B$, determine si son independientes o no. **a)** Utilice las marginales. **b)** Utilice las probabilidades condicionales.
</span>
<span style="color:#d94f0b">
$
\begin{alineado}
\begin{array}{c|ccc}
         & B=b_1 & B=b_2 & B=b_3 \\
  \hline
  A=a_1 y 0,1 y 0,2 y 0,3\\
  A=a_2 & 0,1 & 0,2 & 0,1\\  
  \hline
\fin{matriz}
\end{alineado}
$
</span>
<br></br>
<span style="color:#d94f0b">
**a)** En primer lugar, observe que $\sum_{a_i,b_j}p(A=a_i,B=b_j)=1$. Ahora, calculemos las marginales sumando las filas de $A$ y las columnas de $B$:
</span>
<br></br>
<span style="color:#d94f0b">
$
\begin{align}
p(A=a_1) &= \sum_{b_j}p(A=a_1,B=b_j)=0,1 + 0,2 + 0,3 = \mathbf{0,6}\\
p(A=a_2) &= \sum_{b_j}p(A=a_2,B=b_j)=0,1 + 0,2 + 0,1 = \mathbf{0,4}\\
p(B=b_1) &= \sum_{a_i}p(A=a_i,B=b_1)=0.1 + 0.1 = \mathbf{0.2}\\
p(B=b_2) &= \sum_{a_i}p(A=a_i,B=b_2)=0.2 + 0.2 = \mathbf{0.4}\\
p(B=b_3) &= \sum_{a_i}p(A=a_i,B=b_3)=0,3 + 0,1 = \mathbf{0,4}\\
\fin{alinear}
$
</span>
<br></br>
<span style="color:#d94f0b">
Ahora comprobamos la independencia:
</span>
<br></br>
<span style="color:#d94f0b">
$
\begin{align}
p(A=a_1,B=b_1) &=0,1\neq p(A=a_1)p(B=b_1) = \mathbf{0,6}\times\mathbf{0,2}=0,12\\
p(A=a_1,B=b_2) &=0.2\neq p(A=a_1)p(B=b_2) = \mathbf{0.6}\times\mathbf{0.4}=0.24\\
p(A=a_1,B=b_3) &=0,3\neq p(A=a_1)p(B=b_3) = \mathbf{0,6}\times\mathbf{0,4}=0,24\\
p(A=a_2,B=b_1) &=0,1\neq p(A=a_2)p(B=b_1) = \mathbf{0,4}\times\mathbf{0,2}=0,08\\
p(A=a_2,B=b_2) &=0,2\neq p(A=a_2)p(B=b_2) = \mathbf{0,4}\times\mathbf{0,4}=0,16\\
p(A=a_2,B=b_3) &=0,1\neq p(A=a_2)p(B=b_3) = \mathbf{0,4}\times\mathbf{0,4}=0,16\\
\fin{alinear}
$
</span>
<br></br>
<span style="color:#d94f0b">
Sin embargo, tenga en cuenta que en todos los casos $p(A=a_i,B=b_j)\approx p(A=a_i)p(B=b_j)$.
</span>
<br></br>
<span style="color:#d94f0b">
**b)** Ahora, podemos calcular las probabilidades condicionales usando el teorema de Bayes: $p(A=a_i|B=b_j)=p(A=a_i,B=b_j)/p(B=b_j)$
</span>
<br></br>
<span style="color:#d94f0b">
$
\begin{alineado}
\begin{array}{c|ccc}
                  & B=b_1 & B=b_2 & B=b_3 \\
  \hline
  p(A=a_1|B=b_j) y \frac{0,1}{0,2}=0,5 y \frac{0,2}{0,4}=0,5 y \frac{0,3}{0,4}=0,75\\
  p(A=a_2|B=b_j) y \frac{0,1}{0,2}=0,5 y \frac{0,2}{0,4}=0,5 y \frac{0,1}{0,4}=0,25\\  
  \hline
                & \suma = 1 & \suma = 1 & \suma=1\\
\fin{matriz}
\end{alineado}
$
</span>
<br></br>
<span style="color:#d94f0b">
y $p(B=b_j|A=a_i)=p(A=a_i,B=b_j)/p(A=a_i)$
</span>
<br></br>
<span style="color:#d94f0b">
$
\begin{alineado}
\begin{array}{c|ccc|c}
                  & p(B=b_1|A=a_i) & p(B=b_2|A=a_i) & p(B=b_3|A=a_i) \\
  \hline
  A=a_1 y \frac{0,1}{0,6}=0,17 y \frac{0,2}{0,6}=0,33 y \frac{0,3}{0,6}=0,5 y \suma = 1\\
  A=a_2 y \frac{0,1}{0,4}=0,25 y \frac{0,2}{0,4}=0,5 y \frac{0,1}{0,4}=0,25 y \suma = 1\\  
  \hline
\fin{matriz}
\end{alineado}
$
</span>
<br></br>
<span style="color:#d94f0b">
Nótese que las probabilidades condicionales suman $1$ con respecto a la variable "influenciada", es decir
</span>
<br></br>
<span style="color:#d94f0b">
$
\para todo a_i: \sum_{b_j} p(A=a_i|B=b_j)= 1\;\text{y}\;
\para todo b_j: \suma_{a_i} p(B=b_j|A=a_i)= 1
$
</span>
<br></br>
### Entropía
Este es el **primer punto** de la asignatura donde hablamos de <span style="color:#f88146">**Teoría de la Información**</span>, la principal matemática auxiliar de este curso. Para ello, les remitimos al [libro del autor sobre el tema](https://link.springer.com/book/10.1007/978-1-84882-297-9).

#### Definición y propiedades
El ejercicio anterior revela una propiedad esencial de DA: <span style="color:#f88146">no podemos converger sin mantener la **maximización de la entropía**</span>. Pero, ¿qué es la entropía?

**La entropía** es la medida última de incertidumbre definida por [Shannon](https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf) de la siguiente manera:

Dada una variable aleatoria discreta $X$, con valores posibles $\{x_1,\ldots,x_n\}$, su **entropía** está dada por:

$$
H(X) = -\sum_{i=1}^np(X=x_i)\log p(X=x_i)\;.
$$

De manera similar, podemos expresar la entropía en términos de las probabilidades de los **eventos discretos** $p_i=p(X=x_i)$, es decir

$$
H(p_1,p_2,\ldots,p_n)=-\sum_{i=1}^n p_i\log p_i\;.
$$

Entonces, tenemos las siguientes **propiedades**:
1) $H$ es continua, cóncava y no negativa en $p_i$.
2) Si todos los $p_i$ son igualmente probables, es decir, $p_i=1/n$, entonces la entropía es **máxima** para este $n$ e igual a $\log n$. Cuanto mayor sea $n$, mayor será la **incertidumbre** de los eventos igualmente probables.
3) Si tenemos $\log_2$ la entropía se mide en **bits**, mientras que si es $\ln$ se mide en **nats**.
4) Como $E(f(x))=\sum_x x\cdot f(x)$ es la **esperanza** de $f(x)$, entonces la entropía es la expectativa del logaritmo.

**Entropía de Bernouilli**. Un ejemplo interesante es la medida de la entropía de $X\sim \text{Bernouilli}(p)$.

$X$ tiene valor $x=1$ con probabilidad $p(X=1)=p$ y $x=0$ con probabilidad $p(X=0)=q=1-p$.
Entonces:

$$
\begin{align}
H(X) &= -\sum_{x}p(X=x)\log p(X=x)\\
     &= -p(X=0)\log p(X=0) - p(X=1)\log p(X=1)\\
     &= -p\log p - q\log q\\
     &= -p\log p - (1-p)\log (1-p)\;.
\fin{alinear}
$$

Por lo tanto, la entropía máxima (incertidumbre) de una variable de Bernouilli es cuando $p=q=1/2$ (por ejemplo la probabilidad de una moneda justa):

$$
H(X) = -p\log p -p\log p = -2p\log p = -\log\frac{1}{2} = -(\log 1 - \log 2) = \log 2\;.
$$

que es $\log_2 2=1$ bits, como podemos ver en {numref}`KM-entropy-Bern`. Nótese que la función es cóncava con respecto a $p$. La entropía mínima se alcanza en los dos puntos extremos: $p=0$ y $p=1$, donde la **incertidumbre** es mínima (moneda completamente sesgada).

```{figura} ./images/Topic2/KM-entropy-Bern-removebg-preview.png
---
nombre: KM-entropía-Berna
ancho: 800px
alinear: centro
altura: 600px
---
Entropía de Bernouilli respecto de $p$.
```

#### Entropía y codificación
La relación entre la entropía y la longitud del código es clave para entender por qué la <span style="color:#f88146">entropía mide el contenido de la información</span>.

El código Morse sigue el principio de *asignar menos bits a las letras más frecuentes que a las menos frecuentes*. Aquí, los bits son claros: $0$ para los puntos "." y $1$ para el
Guión "." Por ejemplo, según la frecuencia de las letras en inglés, las "palabras clave" más cortas son las de $E=.$ y $T=-$. Las más largas son las de los dígitos $0-9$ (cinco bits en total). La tabla a continuación muestra estas longitudes y probabilidades.


$$
\begin{alineado}
&\begin{array}{|c|c|c|c|}
\hline
\text{Letra} & \text{Código Morse} & \text{Longitud del código} & \text{Probabilidad} \\
\hline
A & .- & 2 & 0.06381 \\
B & -... & 4 & 0.01166 \\
C & -.-. & 4 & 0.02173 \\
D & -.. & 3 & 0.03323 \\
E & . & 1 & 0.09924 \\
F & ..-. & 4 & 0.01741 \\
G & --. & 3 & 0.01574 \\
H & .... & 4 & 0.04761 \\
Yo y .. y 2 y 0,05442 \\
J & .--- & 4 & 0.00120 \\
K & -.- & 3 & 0,00603 \\
L & .-.. & 4 & 0.03145 \\
M & -- & 2 & 0,01880 \\
N & -. & 2 & 0.05273 \\
O & --- & 3 & 0.05865 \\
P & .--. & 4 & 0.01507 \\
Q & --.- & 4 & 0.00074 \\
R & .-. & 3 & 0.04677 \\
S & ... & 3 & 0.04943 \\
T & - & 1 & 0.07075 \\
U & ..- & 3 & 0.02155 \\
V & ...- & 4 & 0,00764 \\
W & .-- & 3 & 0.01844 \\
X & -..- & 4 & 0.00117 \\
Y & -.-- & 4 & 0.01542 \\
Z & --.. & 4 & 0.00058 \\
0 y ----- y 5 y 0,01563 \\
1 y .---- y 5 y 0,05469 \\
2 y ..--- y 5 y 0.02344 \\
3 y ...-- y 5 y 0,02344 \\
4 y ....- y 5 y 0,02344 \\
5 y ..... y 5 y 0,01563 \\
6 y -.... y 5 y 0,01563 \\
7 y --... y 5 y 0,01563 \\
8 y ---.. y 5 y 0,01563 \\
9 y ----. y 5 y 0,01563 \\
\hline
\fin{matriz}
\end{alineado}
$$

Téngase en cuenta que, debido a razones tradicionales, no siempre ocurre que los códigos más cortos correspondan a las frecuencias (probabilidades) más altas, pero esta es la tendencia mundial.  

Por supuesto, cada mensaje debe tener un espacio entre las letras para que se descifre correctamente. Por ejemplo: ".... . .-.. .-.. --- .-- --- .-. .-.. -.." significa HOLA MUNDO en Morse.


[//]: https://courses.grainger.illinois.edu/cs573/fa2012/lec/lec/25_entropy.pdf

**Códigos y árboles**. Una forma interesante de caracterizar los códigos (en particular, los códigos binarios) es intentar colocar los símbolos del código en un árbol. Véase, por ejemplo, {numref}`Morse-tree`, donde la raíz se marca como "\#". Señalamos lo siguiente:
- <span style="color:#f88146">**Decodificar significa**</span> navegar por el árbol de arriba a abajo, tomando decisiones (dit o slash para códigos binarios), es decir, construir una "ruta", hasta llegar al símbolo deseado. Dicha ruta es la "palabra clave".
- <span style="color:#f88146">**La longitud de la palabra clave**</span> $l_i$ es el número de decisiones tomadas para decodificarla, es decir, la profundidad del símbolo en el árbol.
- <span style="color:#f88146">**Un código es similar a una coma**</span> si todos los símbolos se colocan en las hojas del árbol. Este no es el caso del código Morse.
- <span style="color:#f88146">**Un código es similar a un prefijo**</span> si cualquier símbolo está precedido por una secuencia única de otros códigos (el prefijo). Por ejemplo, para decodificar "O" en Morse, deberíamos decodificar "T" y "M". Por lo tanto, el prefijo de "O" es "TM".


En el código Morse, se colocan pocas letras en las hojas del árbol. Cabe destacar que son las que tienen la mayor longitud de palabra clave. Aquí, seguimos la receta de asignar las letras menos frecuentes a los niveles más profundos del árbol. El propósito de esta estrategia es doble: (a) ahorrar espacio de almacenamiento y (b) una decodificación rápida.

**Longitud de código esperada**. Supongamos que tenemos $n$ letras, cada una con frecuencia $p_i$ y longitud de código $l_i$, $i=1,\ldots,n$. Entonces, la longitud de código esperada es

$$
E(l) = \sum_{i}l_i p_i = l_1p_1 + l_2p_2 + \ldots + l_np_n\;.
$$

Para el código Morse, $E_{Morse}(l)=3.0794539323542267$. Ahora, el árbol en {numref}`Morse-tree` se construye bajo la restricción de colocar las letras más probables en la parte superior del árbol (binario). En otras palabras, podemos asumir que

$$
p_i \aprox \frac{1}{2^{l_i}}\;.
$$

Si es así, $E(l)\approx H(p_1,p_2,\ldots,p_n)$ ya que

$$
\log_2 p_i \approx \log_2 \frac{1}{2^{l_i}} = \log_2 1 - \log_2 2^{l_i} = - \log_2 2^{l_i} = - l_i\;.
$$

Entonces

$$
-p_i\log_2 p_i \approx \frac{1}{2^{l_i}}l_i = \frac{l_i}{2^{l_i}}\;.
$$

En términos generales, <span style="color:#f88146">**la longitud del código esperada coincide con la entropía**</span>.

Más precisamente, para códigos de tipo coma, tenemos $E(l)\le H(p_1,p_2,\ldots,p_n)$. Aunque Morse no es de tipo coma, satisface este límite, ya que $E_{Morse}(l) = 3.0794539323542267\le H_{Morse} = 4.713102340698242$.

```{figura} ./images/Topic2/Morse-Photoroom.png
---
nombre: Árbol Morse
ancho: 800px
alinear: centro
altura: 600px
---
Árbol de decodificación del código Morse.
```

[//]: https://stackoverflow.com/questions/21853101/why-huffman-coding-is-good

**Códigos Huffman**. Como código alternativo, destacamos un <span style="color:#f88146">**código de prefijo**</span> (ningún código es el prefijo de otro). Los códigos de prefijo son fácilmente decodificables y, además, permiten (por definición) suprimir el espacio " " entre palabras (véase la tabla a continuación).

$$
\begin{alineado}
\begin{array}{|c|c|c|c|}
\hline
\text{Letra} & \text{Código de Huffman} & \text{Longitud} & \text{Probabilidad} \\
\hline
A & 1010 & 4 & 0.06381 \\
B & 001110 & 6 & 0.01166 \\
C & 111001 & 6 & 0.02173 \\
D & 10111 & 5 & 0.03323 \\
E & 000 & 3 & 0.09924 \\
F & 110101 & 6 & 0.01741 \\
G & 100111 & 6 & 0.01574 \\
H & 11111 & 5 & 0.04761 \\
I & 0101 & 4 & 0.05442 \\
J & 1101001011 & 10 & 0.00120 \\
K & 11010011 & 8 & 0.00603 \\
L y 10110 y 5 y 0,03145 \\
M & 110111 & 6 & 0.01880 \\
N y 0100 y 4 y 0,05273 \\
O & 0111 & 4 & 0.05865 \\
P & 001111 & 6 & 0.01507 \\
Q & 1101001001 & 10 & 0.00074 \\
R & 11101 & 5 & 0.04677 \\
S & 0010 & 4 & 0.04943 \\
T y 1100 y 4 y 0,07075 \\
U y 111000 y 6 y 0,02155 \\
V & 1101000 & 7 & 0.00764 \\
W y 110110 y 6 y 0,01844 \\
X & 1101001010 & 10 & 0.00117 \\
Y & 100000 & 6 & 0.01542 \\
Z y 1101001000 y 10 y 0,00058 \\
0 y 100001 y 6 y 0,01563 \\
1 y 0110 y 4 y 0,05469 \\
2 y 111100 y 6 y 0,02344 \\
3 y 111101 y 6 y 0,02344 \\
4 y 00110 y 5 y 0,02344 \\
5 y 100011 y 6 y 0,01563 \\
6 y 100010 y 6 y 0,01563 \\
7 y 100110 y 6 y 0,01563 \\
8 y 100100 y 6 y 0,01563 \\
9 y 100101 y 6 y 0,01563 \\
\hline
\fin{matriz}
\end{alineado}
$$

Por ejemplo, el código Huffman para HELLOW WORLD es

$$
1111100010110101100111\;1101100111111011011010111
$$

Respecto a $E_{Huffman}(l)$ y $H_{Huffman}=$, son idénticos: $4.7$. Véase el árbol de codificación en {numref}`Huffman-tree`.

```{figura} ./images/Topic2/Huffman-Photoroom.png
---
nombre: Huffman-tree
ancho: 800px
alinear: centro
altura: 600px
---
Árbol de decodificación del código Huffman de las frecuencias Morse.
```

Por último, este código no sólo es útil para el inglés sino para cualquier idioma como el chino.


#### Entropía conjunta vs. condicional
La entropía se define para cualquier función de probabilidad (discreta), y en particular para la **probabilidad conjunta**. Por lo tanto, si $A$ y $B$ son dos variables discretas con valores respectivos $a_1,\ldots, a_m$ y $b_1,\ldots,b_n$ y existe la probabilidad $p(A,B)$, la <span style="color:#f88146">**entropía conjunta**</span> $H(A,B)$ se define como sigue:

$$
H(A,B) = -\suma_{a_i}\suma_{b_j}p(A=a_i,B=b_j)\log p(A=a_i,B=b_j)\;.
$$

Recuerde que el teorema de Bayes conduce a $p(A,B)=p(A|B)p(B)=p(B|A)p(A)$.
Como resultado, podemos definir entropías para $p(A|B)$ y $p(B|A)$, es decir, <span style="color:#f88146">**entropías condicionales**</span>.

Recuerde que *la entropía es una expectativa*, entonces  

$$
H(A|B=b_j) = -\sum_{a_i}p(A=a_i|B=b_j)\log p(A=a_i|B=b_j)\;,
$$

es la <span style="color:#f88146">**entropía de la esperanza condicional** de $A$ con respecto a $B=b_j$</span>. Ahora bien, si promediamos esta cantidad con respecto a todos los valores $b_j$, obtenemos que la *entropía condicional* se obtiene mediante la siguiente suma ponderada:

$$
H(A|B) = \sum_{b_j}p(B=b_j)\cdot H(A|B=b_j)\;,
$$

Y lo mismo ocurre con $H(B|A)$. En realidad, tenemos varias **propiedades** que vinculan las entropías condicionales y las entropías conjuntas:
1) **Valor cero**: $H(A|B)=0$ si el valor de $A$ está *completamente determinado* por $B$. En otras palabras, $H(A|B)$ mide cuánta incertidumbre añade $B$ a $A$. Entonces, si $p(A|B)=1$, se espera que conocer $B$ sea lo mismo que conocer $A$.   
2) **Independencia**: $H(A|B)=H(A)$ y $H(B|A)=H(A)$ si y solo si $A$ y $B$ son *independientes*, como sucede con $p(A|B)=p(A)$ y $p(B|A)=p(A)$.  
3) **Regla de la cadena**: las entropías condicionales se pueden derivar de la entropía conjunta $H(A,B)$ restando la entropía de la variable condicionante:

$$
H(A|B) = H(A,B)-H(B)\;\;\text{y}\;\; H(B|A) = H(A,B)-H(A)\;.
$$
<br></br>
<span style="color:#d94f0b">
**Ejercicio**. Dadas las variables aleatorias discretas $A$ y $B$, en el ejercicio anterior: **a)** determine la entropía conjunta y **b)** las entropías condicionales. **c)** Interprete la incertidumbre que cada variable añade o elimina con respecto a la otra y la incertidumbre eliminada de la entropía conjunta. **d)** ¿Son $A$ y $B$ independientes en función de sus entropías?
</span>
<br></br>
<span style="color:#d94f0b">
**a)** En primer lugar, para la entropía conjunta necesitamos la distribución conjunta:
</span>
<br></br>
<span style="color:#d94f0b">
$
\begin{alineado}
\begin{array}{c|ccc}
         & B=b_1 & B=b_2 & B=b_3 \\
  \hline
  A=a_1 y 0,1 y 0,2 y 0,3\\
  A=a_2 & 0,1 & 0,2 & 0,1\\  
  \hline
\fin{matriz}
\end{alineado}
$
</span>
<br></br>
<span style="color:#d94f0b">
$
\begin{align}
H(A,B) &= -\suma_{a_i}\suma_{b_j}p(A=a_i,B=b_j)\log p(A=a_i,B=b_j)\\
       &= -[3(0,1\log 0,1) + 2(0,2\log 0,2) + 0,3\log 0,3]\\
       &= \mathbf{1.695}\;\text{nats}\;.
\fin{alinear}
$
</span>
<br></br>
<span style="color:#d94f0b">
Nótese que la entropía máxima (en este caso con $m\cdot n=6$ eventos) se da cuando
todos los eventos son equiprobables, es decir $p(A=a_i,B=b_j)=\frac{1}{m\cdot n}=\frac{1}{2\cdot 3}=\frac{1}{6}$, y es $H_{max}(A,B)=\log n = \log 6$
</span>
<br></br>
<span style="color:#d94f0b">
$
\begin{align}
H_{máx}(A,B) &= -\suma_{a_i}\suma_{b_j}\frac{1}{m\cdot n}\log \frac{1}{m\cdot n}\\
       &= -6\cdot \frac{1}{6}\log\frac{1}{6}\\
       &= -\log\frac{1}{6}\\
       &= -(\log 1 - \log 6)\\
       &= \log 6 = 1.791\;\text{nats}\;.
\fin{alinear}
$
</span>
<br></br>
<span style="color:#d94f0b">
Entonces $H(A,B)=1.695$ está bastante cerca de $H_{max}(A,B)=1.791$.
</span>
<br></br>
<span style="color:#d94f0b">
**b1)** Para $H(A|B)$ necesitamos la distribución condicional $p(A|B)$:
</span>
<br></br>
<span style="color:#d94f0b">
$
\begin{alineado}
\begin{array}{c|ccc}
                  & B=b_1 & B=b_2 & B=b_3 \\
  \hline
  p(A=a_1|B=b_j) y \frac{0,1}{0,2}=0,5 y \frac{0,2}{0,4}=0,5 y \frac{0,3}{0,4}=0,75\\
  p(A=a_2|B=b_j) y \frac{0,1}{0,2}=0,5 y \frac{0,2}{0,4}=0,5 y \frac{0,1}{0,4}=0,25\\  
  \hline
                & \suma = 1 & \suma = 1 & \suma=1\\
\fin{matriz}
\end{alineado}
$
</span>
<br></br>
<span style="color:#d94f0b">
Entonces, atendiendo a la definición $H(A|B)=\sum_{b_j}p(B=b_j)H(A|B=b_j)$, tenemos:
</span>
<span style="color:#d94f0b">
$
\begin{align}
H(A|B=b_1) &= -\sum_{a_i}p(A=a_i|B=b_1)\log p(A=a_i|B=b_1)\\
           &= -(0,5\log 0,5 + 0,5\log 0,5) = 0,693\\
H(A|B=b_2) &= -\sum_{a_i}p(A=a_i|B=b_2)\log p(A=a_i|B=b_2)\\
           &= -(0,5\log 0,5 + 0,5\log 0,5) = 0,693\\
H(A|B=b_3) &= -\sum_{a_i}p(A=a_i|B=b_3)\log p(A=a_i|B=b_3)\\
           &= -(0,75\log 0,75 + 0,25\log 0,25) = 0,562\\
\fin{alinear}
$
</span>
<br></br>
<span style="color:#d94f0b">
Entonces, $H(A|B)$ viene dado por un promedio ponderado, donde necesitamos los marginales $p(B=b_j)=[0.2\;0.4\;0.4]$ (ver el ejercicio correspondiente):
</span>
<br></br>
<span style="color:#d94f0b">
$
\begin{align}
H(A|B) &= \sum_{b_j}p(B=b_j)H(A|B=b_j)\\
       &= p(B=b_1)H(A|B=b_1) + p(B=b_2)H(A|B=b_2) + p(B=b_3)H(A|B=b_3)\\
       &= 0,2\cdot H(A|B=b_1) + 0,4\cdot H(A|B=b_2) + 0,4\cdot H(A|B=b_3)\\
       &= 0,2\cdot 0,693 + 0,4\cdot 0,693 + 0,4\cdot 0,562\\
       &= \mathbf{0.640}\;.
\fin{alinear}
$
</span>
<br></br>
<span style="color:#d94f0b">
**b2)** Para $H(B|A)$ necesitamos la distribución condicional $p(B|A)$:
</span>
<br></br>
<span style="color:#d94f0b">
$
\begin{alineado}
\begin{array}{c|ccc|c}
                  & p(B=b_1|A=a_i) & p(B=b_2|A=a_i) & p(B=b_3|A=a_i) \\
  \hline
  A=a_1 y \frac{0,1}{0,6}=0,17 y \frac{0,2}{0,6}=0,33 y \frac{0,3}{0,6}=0,5 y \suma = 1\\
  A=a_2 y \frac{0,1}{0,4}=0,25 y \frac{0,2}{0,4}=0,5 y \frac{0,1}{0,4}=0,25 y \suma = 1\\  
  \hline
\fin{matriz}
\end{alineado}
$
</span>
<br></br>
<span style="color:#d94f0b">
Entonces, atendiendo a la definición $H(B|A)=\sum_{a_i}p(A=a_i)H(B|A=a_i)$, tenemos:
</span>
<span style="color:#d94f0b">
$
\begin{align}
H(B|A=a_1) &= -\sum_{b_j}p(B=b_j|A=a_1)\log p(B=b_j|A=a_1)\\
           &= -(0,17\log 0,17 + 0,33\log 0,33 + 0,5\log 0,5) = 1,013\\
H(B|A=a_2) &= -\sum_{b_j}p(B=b_j|A=a_2)\log p(B=b_j|A=a_2)\\
           &= -(0,25\log 0,25 + 0,5\log 0,5 + 0,25\log 0,25) = 1,039\\
\fin{alinear}
$
</span>
<br></br>
<span style="color:#d94f0b">
Entonces, $H(B|A)$ viene dado por un promedio ponderado, donde necesitamos los marginales $p(A=a_i)=[0.6\;0.4]$ (ver el ejercicio correspondiente):
</span>
<br></br>
<span style="color:#d94f0b">
$
\begin{align}
H(B|A) &= \sum_{a_i}p(A=a_i)H(B|B=a_i)\\
       &= p(A=a_1)H(B|A=a_1) + p(A=a_2)H(B|A=a_2)\\
       &= 0,6\cdot H(B|A=a_1) + 0,4\cdot H(B|A=a_2)\\
       &= 0,6\cdot 1,013 + 0,4\cdot 1,039 \\
       &= \mathbf{1.023}\;.
\fin{alinear}
$
</span>
<br></br>
<span style="color:#d94f0b">
**c)** Como resultado, $H(B|A)=\mathbf{1.023}>H(A|B)=\mathbf{0.640}$. Esto significa que **$B$ contiene más información sobre $A$ que $A$ sobre $B$**.
<br></br>
Finalmente, calculemos las entropías individuales $H(A)$ y $H(B)$:
</span>
<br></br>
<span style="color:#d94f0b">
$
\begin{align}
H(A) & = -\sum_{a_i}p(A=a_i)\log p(A=a_i)\\
       & = -(0,6\log 0,6 + 0,4\log 0,4)\\
       & = \mathbf{0.673}\;.\\
H(B) & = -\sum_{b_j}p(B=b_j)\log p(B=b_j)\\
       & = -(0,2\log 0,2 + 0,4\log 0,4 + 0,4\log 0,4)\\
       & = \mathbf{1.054}\;.\\
\fin{alinear}
$
</span>
<br></br>
<span style="color:#d94f0b">
Dado que $H(A|B)=H(A,B)-H(B)$ y $H(B|A)=H(A,B)-H(A)$ y $H(B)>H(A)$ ($B$ es más incierto que $A$), entonces $H(B)$ reduce más la incertidumbre de $H(A,B)$ que $H(A)$. Esto explica por qué $H(A|B)\ll H(B|A)$.
<br><br>
Comprobemos el cálculo:
</span>
<span style="color:#d94f0b">
$
H(A|B) = \mathbf{0.640} = 1.695 - 1.054\;\;\text{y}\;\; H(B|A) = \mathbf{1.023} = 1.695 - 0.673\;.
$
</span>
<br></br>
<span style="color:#d94f0b">
**d)** Dado que $H(A|B)=0,640\approx H(A)= 0,673$ y $H(B|A)=1,023\approx H(B)=1,054$, concluimos que $A$ y $B$ son *próximamente independientes, aunque no lo son*. Esto es consistente con el ejercicio previo sobre marginales.
<br></br>
<span style="color:#d94f0b">
En este ejercicio, hemos ilustrado cómo calcular las entropías condicionales, ya sea directamente o mediante las entropías individuales y la entropía conjunta. Sin embargo, la clave de este ejercicio reside en **interpretar correctamente qué es una entropía condicional**: *una cuantificación de cuánta información tiene una variable sobre otra*.
</span>





