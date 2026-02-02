# Redes Neuronales de Grafos

## Sesión Práctica 1: Introducción a los Grafos y al Paso de Mensajes

### Introducción

En esta sesión práctica, exploraremos los fundamentos de las **Redes Neuronales de Grafos (GNNs)**, una poderosa clase de modelos de aprendizaje profundo diseñados para operar sobre datos estructurados en grafos. A diferencia de las redes neuronales tradicionales que asumen que los datos se encuentran en una cuadrícula regular (como las imágenes) o en secuencias (como el texto), las GNNs pueden manejar datos con patrones de conectividad arbitrarios, lo que las hace ideales para redes sociales, estructuras moleculares, redes de citas y muchos otros dominios.

El objetivo de este tutorial es guiarte a través del pipeline completo: desde la creación de datos de grafos sintéticos utilizando **NetworkX**, hasta la comprensión del mecanismo de **paso de mensajes** que subyace a todas las GNNs, y finalmente la implementación y entrenamiento de una Red Neuronal de Grafos utilizando **PyTorch Geometric (PyG)**.

### Requisitos Previos

Antes de comenzar, asegúrate de tener instaladas las bibliotecas necesarias. Utilizaremos NetworkX para la manipulación de grafos, PyTorch Geometric para las implementaciones de GNN y las bibliotecas científicas estándar de Python:

```{code-block} bash
pip install torch networkx torch_geometric matplotlib scikit-learn
```

### Fundamentos de los Grafos

Un grafo $G = (V, E)$ consiste en un conjunto de **nodos** (o vértices) $V$ y un conjunto de **aristas** (o bordes) $E$ que conectan pares de nodos. Cada nodo $v \in V$ puede tener un **vector de características** asociado $\mathbf{x}_v \in \mathbb{R}^d$, y en tareas de aprendizaje supervisado, cada nodo también puede tener una **etiqueta** $y_v$.

En el contexto del aprendizaje automático sobre grafos, normalmente representamos la estructura del grafo mediante una **matriz de adyacencia** $\mathbf{A} \in \{0, 1\}^{|V| \times |V|}$, donde $A_{ij} = 1$ si hay una arista entre los nodos $i$ y $j$, y $A_{ij} = 0$ en caso contrario. Las características de los nodos se apilan en una **matriz de características** $\mathbf{X} \in \mathbb{R}^{|V| \times d}$, donde cada fila corresponde al vector de características de un nodo.

```{figure} ./images/Practice0/graph_structure.png
---
name: GraphStructure
align: center
---
Un grafo con 6 nodos y su correspondiente representación en matriz de adyacencia.
```

## Parte 1: Creación de Datos de Grafos Sintéticos

### Construcción de un Grafo con NetworkX

NetworkX es una biblioteca de Python para la creación, manipulación y estudio de redes complejas. Ya deberías estar familiarizado con su funcionalidad básica. Empecemos creando un grafo sintético que utilizaremos a lo largo de este tutorial.

Crearemos un grafo con múltiples comunidades, donde los nodos dentro de la misma comunidad comparten características similares. Esta estructura facilitará la comprensión de cómo las GNNs pueden aprender a clasificar nodos basándose tanto en sus características como en su vecindario.

```{code-block} python
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# Establecer semilla aleatoria para reproducibilidad
np.random.seed(42)

# Parámetros para nuestro grafo sintético
num_nodes = 200
num_classes = 4
nodes_per_class = num_nodes // num_classes
feature_dim = 16

# Crear un grafo de modelo de bloques estocásticos
# Esto genera un grafo con estructura de comunidad
sizes = [nodes_per_class] * num_classes
# Matriz de probabilidad: mayor probabilidad dentro de las comunidades
p_intra = 0.3  # Probabilidad de arista dentro de la misma comunidad
p_inter = 0.01  # Probabilidad de arista entre diferentes comunidades
probs = np.full((num_classes, num_classes), p_inter)
np.fill_diagonal(probs, p_intra)

G = nx.stochastic_block_model(sizes, probs, seed = 42)

print(f"Número de nodos: {G.number_of_nodes()}")
print(f"Número de aristas: {G.number_of_edges()}")
```

### Visualización de la Estructura del Grafo

Antes de continuar, es importante visualizar nuestro grafo para entender su estructura:

```{code-block} python
# Obtener las asignaciones de comunidad reales (ground truth)
node_labels = np.array([i // nodes_per_class for i in range(num_nodes)])

# Crear un mapa de colores para la visualización
colors = ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3']
node_colors = [colors[label] for label in node_labels]

# Dibujar el grafo
plt.figure(figsize = (10, 8))
pos = nx.spring_layout(G, seed = 42, k = 0.5)
nx.draw(G, pos, node_color = node_colors, node_size = 50, 
        edge_color = 'gray', alpha = 0.7, width = 0.5)
plt.title("Grafo de Modelo de Bloques Estocásticos con 4 Comunidades")
plt.tight_layout()
plt.savefig("sbm_graph.png", dpi = 150)
plt.show()
```

```{figure} ./images/Practice0/sbm_graph.png
---
name: SBMGraph
align: center
---
Visualización del grafo de modelo de bloques estocásticos mostrando 4 comunidades.
```

### Creación de Características Sintéticas de los Nodos

Ahora necesitamos asignar vectores de características a cada nodo. **Crucialmente, crearemos características con una correlación muy débil con las etiquetas de los nodos.** Esta es la clave para demostrar por qué las GNNs superan a los MLPs: la estructura del grafo se vuelve esencial para la clasificación.

```{code-block} python
# Crear centros de clase en el espacio de características con magnitud PEQUEÑA
# La diferencia clave: centros de clase pequeños y mucho ruido
class_centers = np.random.randn(num_classes, feature_dim) * 0.3

# Asignar características a los nodos basándose en su clase
# Cada nodo recibe una señal de clase DÉBIL ahogada en un ruido GRANDE
node_features = np.zeros((num_nodes, feature_dim))
for i in range(num_nodes):
    label = node_labels[i]
    # El ruido grande domina la señal de clase débil
    noise = np.random.randn(feature_dim) * 1.0            # Ruido grande
    weak_signal = class_centers[label] * 0.2              # Señal débil
    node_features[i] = weak_signal + noise

print(f"Forma de la matriz de características: {node_features.shape}")
print(f"Estadísticas de las características - Media: {node_features.mean():.3f}, Desviación Estándar: {node_features.std():.3f}")
```

**Por qué esto es importante:** Con características débiles, un MLP entrenado solo con las características de los nodos logrará solo ~60-70% de precisión, mientras que una GCN que aproveche la fuerte estructura de comunidad en el grafo alcanzará ~90%+. Esto demuestra claramente el poder de la estructura del grafo.

### Asignación de Etiquetas a los Nodos

Ya hemos asignado etiquetas basándonos en la estructura de la comunidad. Verifiquemos la distribución de etiquetas:

```{code-block} python
# Contar etiquetas por clase
unique, counts = np.unique(node_labels, return_counts = True)
print("Distribución de etiquetas:")
for label, count in zip(unique, counts):
    print(f"  Clase {label}: {count} nodos")
```

## Parte 2: Conversión al Formato PyTorch Geometric

### Introducción a PyTorch Geometric

**PyTorch Geometric (PyG)** es una biblioteca construida sobre PyTorch que proporciona implementaciones eficientes de capas GNN y utilidades para manejar datos de grafos. La estructura de datos central en PyG es el objeto `Data`, que almacena toda la información sobre un solo grafo.

Un objeto `Data` de PyG normalmente contiene:

- `x`: Matriz de características de los nodos con forma `[num_nodes, num_features]`
- `edge_index`: Conectividad del grafo en formato COO con forma `[2, num_edges]`
- `y`: Etiquetas de los nodos con forma `[num_nodes]`
- Atributos adicionales según sea necesario (características de aristas, máscaras, etc.)

### Conversión de Grafo NetworkX a Datos PyG

```{code-block} python
import torch
from torch_geometric.data import Data
from torch_geometric.utils import from_networkx

# Convertir características y etiquetas a tensores de PyTorch
x = torch.tensor(node_features, dtype = torch.float)
y = torch.tensor(node_labels, dtype = torch.long)

# Convertir el grafo de NetworkX al formato edge_index
# PyG utiliza el formato COO: edge_index[0] contiene los nodos de origen, edge_index[1] contiene los nodos de destino
edge_list = list(G.edges())
edge_index = torch.tensor(edge_list, dtype = torch.long).t().contiguous()

# Para grafos no dirigidos, necesitamos aristas en ambas direcciones
edge_index = torch.cat([edge_index, edge_index.flip(0)], dim = 1)

# Crear el objeto Data de PyG
data = Data(x = x, edge_index = edge_index, y = y)

print(data)
print(f"Número de nodos: {data.num_nodes}")
print(f"Número de aristas: {data.num_edges}")
print(f"Número de características por nodo: {data.num_node_features}")
print(f"Tiene nodos aislados: {data.has_isolated_nodes()}")
print(f"Tiene bucles (self-loops): {data.has_self_loops()}")
print(f"Es no dirigido: {data.is_undirected()}")
```

### Creación de Divisiones de Entrenamiento/Validación/Prueba

Para las tareas de clasificación de nodos, necesitamos dividir nuestros nodos en conjuntos de entrenamiento, validación y prueba. A diferencia del aprendizaje automático tradicional donde dividimos las muestras, aquí creamos **máscaras** que indican a qué conjunto pertenece cada nodo. Esto se debe a que todos los nodos permanecen en el grafo durante el entrenamiento (necesitamos la estructura completa del grafo), pero solo calculamos la pérdida en los nodos de entrenamiento.

Crearemos divisiones para **10 ejecuciones diferentes** para asegurar una evaluación robusta:

```{code-block} python
def create_masks(num_nodes, num_classes, train_ratio = 0.6, val_ratio = 0.2, seed = 0):
    """
    Crear máscaras de entrenamiento/validación/prueba para la clasificación de nodos.
    
    Argumentos:
        num_nodes: Número total de nodos
        num_classes: Número de clases
        train_ratio: Fracción de nodos para entrenamiento
        val_ratio: Fracción de nodos para validación
        seed: Semilla aleatoria para reproducibilidad
    
    Retorna:
        train_mask, val_mask, test_mask como tensores booleanos
    """
    np.random.seed(seed)
    
    indices = np.random.permutation(num_nodes)
    train_size = int(num_nodes * train_ratio)
    val_size = int(num_nodes * val_ratio)
    
    train_idx = indices[:train_size]
    val_idx = indices[train_size:train_size + val_size]
    test_idx = indices[train_size + val_size:]
    
    train_mask = torch.zeros(num_nodes, dtype = torch.bool)
    val_mask = torch.zeros(num_nodes, dtype = torch.bool)
    test_mask = torch.zeros(num_nodes, dtype = torch.bool)
    
    train_mask[train_idx] = True
    val_mask[val_idx] = True
    test_mask[test_idx] = True
    
    return train_mask, val_mask, test_mask


# Crear máscaras para 10 ejecuciones diferentes
num_runs = 10
all_masks = []

for run in range(num_runs):
    train_mask, val_mask, test_mask = create_masks(
        data.num_nodes, num_classes, seed = run
    )
    all_masks.append({
        'train': train_mask,
        'val': val_mask,
        'test': test_mask
    })
    
# Verificar la primera división
print(f"Ejecución 0 - Nodos de entrenamiento: {all_masks[0]['train'].sum().item()}")
print(f"Ejecución 0 - Nodos de validación: {all_masks[0]['val'].sum().item()}")
print(f"Ejecución 0 - Nodos de prueba: {all_masks[0]['test'].sum().item()}")
```

## Parte 3: El Problema del Suavizado Excesivo (Over-Smoothing)

### Por qué la Agregación Repetida Causa Mezcla de Información

Antes de profundizar en la mecánica del paso de mensajes, debemos entender una limitación crítica: **¿qué sucede cuando agregamos información de los vecinos varias veces?**

Consideremos un escenario simple con dos nodos vecinos:

- **Nodo A** (Clase 0): Inicialmente tiene características distintivas de la Clase 0
- **Nodo B** (Clase 1): Inicialmente tiene características distintivas de la Clase 1
- **Arista A-B**: Estos nodos están conectados en el grafo

#### Evolución de las Representaciones de los Nodos a través de las Capas

Cuando realizamos el paso de mensajes, agregamos la información de los vecinos. Matemáticamente, esto se puede expresar como la multiplicación por una matriz de adyacencia normalizada $\tilde{\mathbf{A}}$:

$$\mathbf{H}^{(l+1)} = \tilde{\mathbf{A}} \mathbf{H}^{(l)}$$

Esta es esencialmente una **operación de promedio**. Vamos a rastrear qué sucede con nuestros dos nodos:

```
Capa 0:   h_A = [1.0, 0.0]  (clase 0 pura)    |  h_B = [0.0, 1.0]  (clase 1 pura)

Capa 1:   h_A ≈ [0.7, 0.3]  (mezclado)        |  h_B ≈ [0.3, 0.7]  (mezclado)

Capa 2:   h_A ≈ [0.55, 0.45]                  |  h_B ≈ [0.45, 0.55]

Capa 3:   h_A ≈ [0.52, 0.48]                  |  h_B ≈ [0.48, 0.52]

...

Capa 10:  h_A ≈ [0.5, 0.5]  (¡IDÉNTICOS!)      |  h_B ≈ [0.5, 0.5]  (¡IDÉNTICOS!)
```

**¡Las representaciones convergen al mismo valor!** Este fenómeno se llama **suavizado excesivo (over-smoothing)**: después de muchas capas de agregación, las representaciones de los nodos se vuelven casi idénticas, perdiendo toda la información discriminatoria.

#### Intuición Matemática

La matriz de adyacencia normalizada $\tilde{\mathbf{A}}$ es una matriz estocástica (las filas suman 1). Cuando multiplicamos repetidamente por ella:

$$\mathbf{H}^{(l)} = \tilde{\mathbf{A}}^l \mathbf{H}^{(0)}$$

A medida que $l \to \infty$, la matriz $\tilde{\mathbf{A}}^l$ converge a una matriz constante donde todas las filas son idénticas (la distribución estacionaria). Esto significa:

$$\lim_{l \to \infty} \mathbf{H}^{(l)} = \mathbf{1} \mathbf{c}^\top$$

Donde $\mathbf{1}$ es un vector de unos y $\mathbf{c}$ es un vector constante. **¡Todos los nodos terminan con representaciones idénticas!**

#### Implicaciones Prácticas

1. **Por qué 2-3 capas son típicas:** La mayoría de las GNNs utilizan solo 2-3 capas de paso de mensajes antes de que el suavizado excesivo se vuelva severo.
2. **Por qué más profundo no siempre es mejor:** Añadir más capas no mejora el rendimiento; lo perjudica debido al suavizado excesivo.
3. **Las conexiones de salto (skip connections) ayudan:** Técnicas como las conexiones residuales pueden mitigar el suavizado excesivo al preservar las características originales de los nodos.
4. **La estructura del grafo importa en las redes poco profundas:** Con una profundidad limitada, el grafo proporciona información distintiva que las características por sí solas no pueden ofrecer.

Es por esto que en nuestro desafiante conjunto de datos con características de nodo débiles, dependemos de la estructura del grafo, y por eso solo usamos 2 capas GCN, ¡no 10!

---

## Parte 4: Comprensión del Paso de Mensajes

### La Idea Central Detrás de las GNNs

La operación fundamental en las Redes Neuronales de Grafos es el **paso de mensajes** (también conocido como agregación de vecindario). La idea clave es que la representación de un nodo debe depender no solo de sus propias características sino también de las características de sus vecinos. Al agregar iterativamente información de los vecinos, cada nodo puede capturar información de porciones cada vez más grandes del grafo.

Formalmente, el marco de paso de mensajes consiste en tres pasos en cada capa $l$:

1. **Mensaje**: Cada nodo crea un mensaje para enviar a sus vecinos.
2. **Agregación**: Cada nodo agrega los mensajes de sus vecinos.
3. **Actualización**: Cada nodo actualiza su representación basándose en los mensajes agregados.

### Formulación Matemática

#### Forma Vectorial

Para un solo nodo $v$, la operación de paso de mensajes se puede escribir como:

$$
\mathbf{h}_v^{(l+1)} = \phi \left( \mathbf{h}_v^{(l)}, \bigoplus_{u \in \mathcal{N}(v)} \psi(\mathbf{h}_v^{(l)}, \mathbf{h}_u^{(l)}) \right)
$$

Donde:

- $\mathbf{h}_v^{(l)}$ es la representación del nodo $v$ en la capa $l$ (con $\mathbf{h}_v^{(0)} = \mathbf{x}_v$).
- $\mathcal{N}(v)$ es el conjunto de vecinos del nodo $v$.
- $\psi$ es la **función de mensaje** que calcula un mensaje del vecino $u$ al nodo $v$.
- $\bigoplus$ es una **función de agregación** invariante a las permutaciones (como suma, promedio o máximo).
- $\phi$ es la **función de actualización** que combina la representación actual del nodo con los mensajes agregados.

#### Forma Matricial

Para eficiencia computacional, el paso de mensajes normalmente se implementa en forma matricial. Consideremos un caso simple donde agregamos las características de los vecinos utilizando una suma y luego aplicamos una transformación lineal:

$$
\mathbf{H}^{(l+1)} = \sigma \left( \tilde{\mathbf{A}} \mathbf{H}^{(l)} \mathbf{W}^{(l)} \right)
$$

Donde:

- $\mathbf{H}^{(l)} \in \mathbb{R}^{|V| \times d_l}$ es la matriz de todas las representaciones de los nodos en la capa $l$.
- $\mathbf{W}^{(l)} \in \mathbb{R}^{d_l \times d_{l+1}}$ es una matriz de pesos aprendible.
- $\tilde{\mathbf{A}}$ es una versión normalizada de la matriz de adyacencia (a menudo $\mathbf{D}^{-1/2} \mathbf{A} \mathbf{D}^{-1/2}$ donde $\mathbf{D}$ es la matriz de grados).
- $\sigma$ es una función de activación no lineal.

La multiplicación de matrices $\tilde{\mathbf{A}} \mathbf{H}^{(l)}$ realiza efectivamente la agregación: cada fila del resultado contiene la suma (o suma ponderada) de las características de los vecinos de un nodo.

### Implementación del Paso de Mensajes desde Cero

Implementemos una capa simple de paso de mensajes manualmente para entender la mecánica:

```{code-block} python
import torch
import torch.nn.functional as F

def simple_message_passing(x, edge_index, weight_matrix):
    """
    Realizar un paso de paso de mensajes.
    
    Argumentos:
        x: Características de los nodos [num_nodes, in_features]
        edge_index: Conectividad del grafo [2, num_edges]
        weight_matrix: Pesos aprendibles [in_features, out_features]
    
    Retorna:
        Características de los nodos actualizadas [num_nodes, out_features]
    """
    num_nodes = x.size(0)
    
    # Paso 1: Transformar características
    x_transformed = x @ weight_matrix  # [num_nodes, out_features]
    
    # Paso 2: Agregar características de los vecinos
    # Inicializar salida con ceros
    out = torch.zeros_like(x_transformed)
    
    # Obtener nodos de origen y destino
    source_nodes = edge_index[0]  # Nodos que envían mensajes
    target_nodes = edge_index[1]  # Nodos que reciben mensajes
    
    # Agregar: para cada arista, añadir las características del nodo de origen al nodo de destino
    # Esto es equivalente a multiplicar por la matriz de adyacencia
    for i in range(edge_index.size(1)):
        src = source_nodes[i].item()
        tgt = target_nodes[i].item()
        out[tgt] += x_transformed[src]
    
    # Paso 3: Normalizar por el grado del nodo (agregación promedio)
    # Contar las aristas entrantes para cada nodo
    degree = torch.zeros(num_nodes)
    for i in range(edge_index.size(1)):
        tgt = target_nodes[i].item()
        degree[tgt] += 1
    
    # Evitar la división por cero
    degree = torch.clamp(degree, min = 1)
    
    # Normalizar
    out = out / degree.unsqueeze(1)
    
    # Paso 4: Aplicar no linealidad
    out = F.relu(out)
    
    return out


# Probar nuestra implementación
in_features = data.num_node_features
out_features = 8

# Inicializar pesos aleatorios
W = torch.randn(in_features, out_features) * 0.1

# Realizar paso de mensajes
h1 = simple_message_passing(data.x, data.edge_index, W)
print(f"Forma de entrada: {data.x.shape}")
print(f"Forma de salida: {h1.shape}")
```

### Implementación Eficiente con Matrices

La implementación basada en bucles anterior es intuitiva pero lenta. En la práctica, utilizamos operaciones de matrices dispersas:

```{code-block} python
from torch_geometric.utils import degree

def efficient_message_passing(x, edge_index, weight_matrix):
    """
    Paso de mensajes eficiente utilizando operaciones de dispersión (scatter).
    
    Argumentos:
        x: Características de los nodos [num_nodes, in_features]
        edge_index: Conectividad del grafo [2, num_edges]
        weight_matrix: Pesos aprendibles [in_features, out_features]
    
    Retorna:
        Características de los nodos actualizadas [num_nodes, out_features]
    """
    num_nodes = x.size(0)
    
    # Transformar características
    x_transformed = x @ weight_matrix
    
    # Obtener nodos de origen y destino
    source_nodes = edge_index[0]
    target_nodes = edge_index[1]
    
    # Recoger características del nodo de origen para cada arista
    messages = x_transformed[source_nodes]  # [num_edges, out_features]
    
    # Agregación por dispersión (scatter-add): agregar mensajes a los nodos de destino
    out = torch.zeros(num_nodes, x_transformed.size(1))
    out.scatter_add_(0, target_nodes.unsqueeze(1).expand_as(messages), messages)
    
    # Normalizar por el grado
    deg = degree(target_nodes, num_nodes = num_nodes)
    deg = torch.clamp(deg, min = 1)
    out = out / deg.unsqueeze(1)
    
    # Aplicar no linealidad
    out = F.relu(out)
    
    return out


# Verificar que ambas implementaciones dan el mismo resultado
h1_slow = simple_message_passing(data.x, data.edge_index, W)
h1_fast = efficient_message_passing(data.x, data.edge_index, W)
print(f"Las implementaciones coinciden: {torch.allclose(h1_slow, h1_fast, atol = 1e-6)}")
```

### Visualización del Efecto del Paso de Mensajes

Para entender qué logra el paso de mensajes, vamos a visualizar las representaciones de los nodos antes y después de aplicar el paso de mensajes utilizando **t-SNE** (t-distributed Stochastic Neighbor Embedding), una técnica de reducción de dimensionalidad que preserva la estructura local:

```{code-block} python
from sklearn.manifold import TSNE

def visualize_embeddings(embeddings, labels, title, filename):
    """
    Visualizar incrustaciones (embeddings) de nodos utilizando t-SNE.
    
    Argumentos:
        embeddings: Incrustaciones de nodos [num_nodes, embedding_dim]
        labels: Etiquetas de los nodos [num_nodes]
        title: Título del gráfico
        filename: Nombre del archivo de salida
    """
    # Aplicar t-SNE
    tsne = TSNE(n_components = 2, random_state = 42, perplexity = 30)
    embeddings_2d = tsne.fit_transform(embeddings.detach().numpy())
    
    # Graficar
    plt.figure(figsize = (10, 8))
    colors = ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3']
    
    for class_idx in range(num_classes):
        mask = labels == class_idx
        plt.scatter(
            embeddings_2d[mask, 0],
            embeddings_2d[mask, 1],
            c = colors[class_idx],
            label = f'Clase {class_idx}',
            alpha = 0.7,
            s = 50
        )
    
    plt.legend()
    plt.title(title)
    plt.xlabel('Dimensión t-SNE 1')
    plt.ylabel('Dimensión t-SNE 2')
    plt.tight_layout()
    plt.savefig(filename, dpi = 150)
    plt.show()


# Visualizar características originales
visualize_embeddings(
    data.x, 
    data.y.numpy(), 
    "Características de los Nodos Antes del Paso de Mensajes",
    "tsne_before_mp.png"
)

# Aplicar múltiples rondas de paso de mensajes
W1 = torch.randn(feature_dim, 32) * 0.1
W2 = torch.randn(32, 16) * 0.1

h1 = efficient_message_passing(data.x, data.edge_index, W1)
h2 = efficient_message_passing(h1, data.edge_index, W2)

# Visualizar después del paso de mensajes
visualize_embeddings(
    h2,
    data.y.numpy(),
    "Características de los Nodos Después de 2 Capas de Paso de Mensajes",
    "tsne_after_mp.png"
)
```
```{figure} ./images/Practice0/tsne_before_mp.png
---
name: TSNEBeforeMP
---
Visualización t-SNE que muestra las características de los nodos antes del paso de mensajes.
```

```{figure} ./images/Practice0/tsne_after_mp.png
---
name: TSNEAfterMP
---
Visualización t-SNE que muestra las características de los nodos después de 2 capas de paso de mensajes.
```

La observación clave es que después del paso de mensajes, los nodos de la misma clase tienden a agruparse más estrechamente. Esto se debe a que el paso de mensajes permite a los nodos incorporar información de sus vecinos, y en un grafo con estructura de comunidad, es probable que los vecinos pertenezcan a la misma clase.

## Parte 5: Perceptrones Multicapa (MLPs)

Antes de sumergirnos en las GNNs, revisemos brevemente los **Perceptrones Multicapa (MLPs)**, que constituyen los bloques de construcción de muchas arquitecturas de redes neuronales, incluidas las GNNs.

### ¿Qué es un MLP?

Un MLP es una red neuronal feedforward que consta de múltiples capas de neuronas. Cada capa realiza una transformación lineal seguida de una función de activación no lineal:

$$
\mathbf{h}^{(l+1)} = \sigma(\mathbf{W}^{(l)} \mathbf{h}^{(l)} + \mathbf{b}^{(l)})
$$

Donde:

- $\mathbf{h}^{(l)}$ es la entrada a la capa $l$.
- $\mathbf{W}^{(l)}$ es la matriz de pesos.
- $\mathbf{b}^{(l)}$ es el vector de sesgo.
- $\sigma$ es una función de activación no lineal (ReLU, Sigmoide, etc.).

### MLP para Clasificación de Nodos (Línea Base)

Una línea base importante para la clasificación de nodos es utilizar un MLP que procese las características de cada nodo de forma independiente, ignorando por completo la estructura del grafo:

```{code-block} python
import torch.nn as nn

class MLP(nn.Module):
    """
    Perceptrón Multicapa simple para clasificación de nodos.
    Esta línea base ignora la estructura del grafo.
    """
    
    def __init__(self, in_channels, hidden_channels, out_channels, dropout = 0.5):
        super(MLP, self).__init__()
        self.fc1 = nn.Linear(in_channels, hidden_channels)
        self.fc2 = nn.Linear(hidden_channels, out_channels)
        self.dropout = nn.Dropout(dropout)
    
    def forward(self, x):
        # Primera capa
        x = self.fc1(x)
        x = F.relu(x)
        x = self.dropout(x)
        # Segunda capa (salida)
        x = self.fc2(x)
        return x


# Crear modelo MLP
mlp_model = MLP(
    in_channels = data.num_node_features,
    hidden_channels = 64,
    out_channels = num_classes
)
print(mlp_model)
```

La limitación clave de los MLPs para datos de grafos es que tratan a cada nodo de forma independiente. No pueden aprovechar la información relacional codificada en la estructura del grafo, que a menudo es crucial para tareas como la clasificación de nodos en redes.

## Parte 6: Redes Neuronales de Grafos

### Del Paso de Mensajes a las GNNs

Una **Red Neuronal de Grafos** es esencialmente una red neuronal que utiliza el paso de mensajes para propagar información a través de la estructura del grafo. Al apilar múltiples capas de paso de mensajes (cada una con parámetros aprendibles), la red puede aprender funciones complejas que dependen tanto de las características de los nodos como de la topología del grafo.

### Red Convolucional de Grafos (GCN)

La **Red Convolucional de Grafos (GCN)** introducida por Kipf y Welling (2017) es una de las arquitecturas de GNN más utilizadas. Cada capa GCN realiza:

$$
\mathbf{H}^{(l+1)} = \sigma \left( \hat{\mathbf{D}}^{-1/2} \hat{\mathbf{A}} \hat{\mathbf{D}}^{-1/2} \mathbf{H}^{(l)} \mathbf{W}^{(l)} \right)
$$

Donde $\hat{\mathbf{A}} = \mathbf{A} + \mathbf{I}$ es la matriz de adyacencia con bucles (self-loops) y $\hat{\mathbf{D}}$ es su matriz de grados.

La adición de bucles asegura que las propias características de un nodo también se consideren durante la agregación.

### Implementación de una GNN con PyTorch Geometric

PyG proporciona implementaciones eficientes de capas GNN comunes. Construyamos una GCN simple de 2 capas:

```{code-block} python
from torch_geometric.nn import GCNConv

class GCN(nn.Module):
    """
    Red Convolucional de Grafos para clasificación de nodos.
    """
    
    def __init__(self, in_channels, hidden_channels, out_channels, dropout = 0.5):
        super(GCN, self).__init__()
        self.conv1 = GCNConv(in_channels, hidden_channels)
        self.conv2 = GCNConv(hidden_channels, out_channels)
        self.dropout = nn.Dropout(dropout)
    
    def forward(self, x, edge_index):
        # Primera capa GCN
        x = self.conv1(x, edge_index)
        x = F.relu(x)
        x = self.dropout(x)
        # Segunda capa GCN
        x = self.conv2(x, edge_index)
        return x


# Crear modelo GCN
gcn_model = GCN(
    in_channels = data.num_node_features,
    hidden_channels = 64,
    out_channels = num_classes
)
print(gcn_model)
```

Observa cómo la capa GCN toma como entrada tanto las características de los nodos `x` como la estructura del grafo `edge_index`. Esta es la diferencia clave con respecto a los MLPs.

### Pipeline de Entrenamiento

Utilizaremos el pipeline de entrenamiento estándar de PyTorch. Los pasos clave son:

1. Pase hacia adelante (Forward pass): Calcular predicciones.
2. Calcular la pérdida (solo en los nodos de entrenamiento).
3. Pase hacia atrás (Backward pass): Calcular gradientes.
4. Actualizar parámetros.

```{code-block} python
def train_epoch(model, data, optimizer, criterion, train_mask):
    """
    Entrenar el modelo durante una época.
    
    Argumentos:
        model: El modelo de red neuronal
        data: Objeto Data de PyG
        optimizer: Optimizador de PyTorch
        criterion: Función de pérdida
        train_mask: Máscara booleana para nodos de entrenamiento
    
    Retorna:
        Pérdida de entrenamiento
    """
    model.train()
    optimizer.zero_grad()
    
    # Pase hacia adelante
    if isinstance(model, MLP):
        out = model(data.x)
    else:
        out = model(data.x, data.edge_index)
    
    # Calcular la pérdida solo en los nodos de entrenamiento
    loss = criterion(out[train_mask], data.y[train_mask])
    
    # Pase hacia atrás
    loss.backward()
    optimizer.step()
    
    return loss.item()


@torch.no_grad()
def evaluate(model, data, mask):
    """
    Evaluar el modelo en un conjunto de nodos.
    
    Argumentos:
        model: El modelo de red neuronal
        data: Objeto Data de PyG
        mask: Máscara booleana para nodos de evaluación
    
    Retorna:
        Precisión en los nodos especificados
    """
    model.eval()
    
    # Pase hacia adelante
    if isinstance(model, MLP):
        out = model(data.x)
    else:
        out = model(data.x, data.edge_index)
    
    # Obtener predicciones
    pred = out.argmax(dim = 1)
    
    # Calcular precisión
    correct = (pred[mask] == data.y[mask]).sum().item()
    total = mask.sum().item()
    
    return correct / total
```

### Bucle de Entrenamiento Completo

```{code-block} python
def run_experiment(model, data, masks, num_epochs = 200, lr = 0.01, weight_decay = 5e-4):
    """
    Ejecutar un experimento de entrenamiento completo.
    
    Argumentos:
        model: El modelo de red neuronal
        data: Objeto Data de PyG
        masks: Diccionario con máscaras de entrenamiento/val/prueba
        num_epochs: Número de épocas de entrenamiento
        lr: Tasa de aprendizaje
        weight_decay: Fuerza de la regularización L2
    
    Retorna:
        Diccionario con el historial de entrenamiento y métricas finales
    """
    optimizer = torch.optim.Adam(model.parameters(), lr = lr, weight_decay = weight_decay)
    criterion = nn.CrossEntropyLoss()
    
    train_mask = masks['train']
    val_mask = masks['val']
    test_mask = masks['test']
    
    history = {
        'train_loss': [],
        'train_acc': [],
        'val_acc': [],
        'test_acc': []
    }
    
    best_val_acc = 0
    best_test_acc = 0
    
    for epoch in range(num_epochs):
        # Entrenamiento
        loss = train_epoch(model, data, optimizer, criterion, train_mask)
        
        # Evaluación
        train_acc = evaluate(model, data, train_mask)
        val_acc = evaluate(model, data, val_mask)
        test_acc = evaluate(model, data, test_mask)
        
        # Almacenar historial
        history['train_loss'].append(loss)
        history['train_acc'].append(train_acc)
        history['val_acc'].append(val_acc)
        history['test_acc'].append(test_acc)
        
        # Rastrear el mejor modelo basado en la precisión de validación
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            best_test_acc = test_acc
        
        # Imprimir progreso cada 50 épocas
        if (epoch + 1) % 50 == 0:
            print(f"Época {epoch + 1:3d} | Pérdida: {loss:.4f} | "
                  f"Entrenamiento: {train_acc:.4f} | Val: {val_acc:.4f} | Prueba: {test_acc:.4f}")
    
    return {
        'history': history,
        'best_val_acc': best_val_acc,
        'best_test_acc': best_test_acc
    }
```

### Ejecución de los Experimentos

Ahora ejecutemos experimentos tanto con MLP como con GCN a través de múltiples ejecuciones:

```{code-block} python
# Hiperparámetros
num_epochs = 200
hidden_channels = 64
lr = 0.01
weight_decay = 5e-4

# Almacenar resultados de todas las ejecuciones
mlp_results = []
gcn_results = []

for run in range(num_runs):
    print(f"\n{'=' * 50}")
    print(f"Ejecución {run + 1}/{num_runs}")
    print('=' * 50)
    
    # Crear nuevos modelos para cada ejecución
    mlp = MLP(data.num_node_features, hidden_channels, num_classes)
    gcn = GCN(data.num_node_features, hidden_channels, num_classes)
    
    # Obtener máscaras para esta ejecución
    masks = all_masks[run]
    
    # Entrenar MLP
    print("\nEntrenando MLP:")
    mlp_result = run_experiment(mlp, data, masks, num_epochs, lr, weight_decay)
    mlp_results.append(mlp_result)
    
    # Entrenar GCN
    print("\nEntrenando GCN:")
    gcn_result = run_experiment(gcn, data, masks, num_epochs, lr, weight_decay)
    gcn_results.append(gcn_result)

# Calcular estadísticas
mlp_test_accs = [r['best_test_acc'] for r in mlp_results]
gcn_test_accs = [r['best_test_acc'] for r in gcn_results]

print(f"\n{'=' * 50}")
print("Resultados Finales (Precisión de Prueba)")
print('=' * 50)
print(f"MLP: {np.mean(mlp_test_accs):.4f} +/- {np.std(mlp_test_accs):.4f}")
print(f"GCN: {np.mean(gcn_test_accs):.4f} +/- {np.std(gcn_test_accs):.4f}")
```

### Visualización del Progreso del Entrenamiento

```{code-block} python
def plot_training_curves(mlp_history, gcn_history, filename):
    """
    Graficar las curvas de entrenamiento para MLP y GCN.
    """
    fig, axes = plt.subplots(1, 3, figsize = (15, 4))
    
    # Curva de pérdida
    axes[0].plot(mlp_history['train_loss'], label = 'MLP', alpha = 0.8)
    axes[0].plot(gcn_history['train_loss'], label = 'GCN', alpha = 0.8)
    axes[0].set_xlabel('Época')
    axes[0].set_ylabel('Pérdida de Entrenamiento')
    axes[0].set_title('Pérdida de Entrenamiento')
    axes[0].legend()
    axes[0].grid(True, alpha = 0.3)
    
    # Precisión de entrenamiento
    axes[1].plot(mlp_history['train_acc'], label = 'MLP', alpha = 0.8)
    axes[1].plot(gcn_history['train_acc'], label = 'GCN', alpha = 0.8)
    axes[1].set_xlabel('Época')
    axes[1].set_ylabel('Precisión')
    axes[1].set_title('Precisión de Entrenamiento')
    axes[1].legend()
    axes[1].grid(True, alpha = 0.3)
    
    # Precisión de validación
    axes[2].plot(mlp_history['val_acc'], label = 'MLP', alpha = 0.8)
    axes[2].plot(gcn_history['val_acc'], label = 'GCN', alpha = 0.8)
    axes[2].set_xlabel('Época')
    axes[2].set_ylabel('Precisión')
    axes[2].set_title('Precisión de Validación')
    axes[2].legend()
    axes[2].grid(True, alpha = 0.3)
    
    plt.tight_layout()
    plt.savefig(filename, dpi = 150)
    plt.show()


# Graficar para la primera ejecución
plot_training_curves(
    mlp_results[0]['history'],
    gcn_results[0]['history'],
    "training_curves.png"
)
```
```{figure} ./images/Practice0/training_curves.png
---
name: TrainingCurves
---
Curvas de entrenamiento que comparan el rendimiento de MLP y GCN a lo largo de las épocas.
```


### Visualización de Incrustaciones Aprendidas

Visualicemos las incrustaciones de los nodos finales aprendidas por la GCN:

```{code-block} python
@torch.no_grad()
def get_embeddings(model, data):
    """
    Extraer incrustaciones de nodos del modelo (antes de la capa final).
    """
    model.eval()
    
    if isinstance(model, GCN):
        x = model.conv1(data.x, data.edge_index)
        x = F.relu(x)
        return x
    else:
        x = model.fc1(data.x)
        x = F.relu(x)
        return x


# Obtener incrustaciones de modelos entrenados
mlp = MLP(data.num_node_features, hidden_channels, num_classes)
gcn = GCN(data.num_node_features, hidden_channels, num_classes)

# Entrenar modelos (utilizando las máscaras de la primera ejecución)
masks = all_masks[0]
_ = run_experiment(mlp, data, masks, num_epochs, lr, weight_decay)
_ = run_experiment(gcn, data, masks, num_epochs, lr, weight_decay)

# Obtener y visualizar incrustaciones
mlp_emb = get_embeddings(mlp, data)
gcn_emb = get_embeddings(gcn, data)

visualize_embeddings(
    mlp_emb,
    data.y.numpy(),
    "Incrustaciones Aprendidas por MLP",
    "mlp_embeddings.png"
)

visualize_embeddings(
    gcn_emb,
    data.y.numpy(),
    "Incrustaciones Aprendidas por GCN",
    "gcn_embeddings.png"
)
```


## Parte 7: Carga de Conjuntos de Datos del Mundo Real

PyTorch Geometric proporciona un acceso fácil a muchos conjuntos de datos de referencia comúnmente utilizados en la investigación de GNN. Dos de los más populares son **Cora** y **Citeseer**, ambos redes de citas donde los nodos representan artículos y las aristas representan citas.

### El Conjunto de Datos Cora

```{code-block} python
from torch_geometric.datasets import Planetoid

# Cargar el conjunto de datos Cora
cora_dataset = Planetoid(root = './data', name = 'Cora')
cora_data = cora_dataset[0]

print("Estadísticas del Conjunto de Datos Cora:")
print(f"  Número de nodos: {cora_data.num_nodes}")
print(f"  Número de aristas: {cora_data.num_edges}")
print(f"  Número de características: {cora_data.num_node_features}")
print(f"  Número de clases: {cora_dataset.num_classes}")
print(f"  Tiene máscaras de entrenamiento/val/prueba: {hasattr(cora_data, 'train_mask')}")
```

### El Conjunto de Datos Citeseer

```{code-block} python
# Cargar el conjunto de datos Citeseer
citeseer_dataset = Planetoid(root = './data', name = 'Citeseer')
citeseer_data = citeseer_dataset[0]

print("Estadísticas del Conjunto de Datos Citeseer:")
print(f"  Número de nodos: {citeseer_data.num_nodes}")
print(f"  Número de aristas: {citeseer_data.num_edges}")
print(f"  Número de características: {citeseer_data.num_node_features}")
print(f"  Número de clases: {citeseer_dataset.num_classes}")
```


## Ejercicio 1: Conjunto de Datos Sintético Personalizado

### Objetivos

El objetivo de este ejercicio es consolidar tu comprensión de la creación de datos de grafos y el pipeline de GNN mediante la construcción de un conjunto de datos sintético personalizado desde cero.

### Descripción de la Tarea

Debes crear un conjunto de datos de grafos sintéticos con las siguientes especificaciones:

1. **Estructura del Grafo**: Crea un grafo con aproximadamente **2000 nodos**. Puedes utilizar cualquiera de los siguientes métodos:
   - Modelo de Bloques Estocásticos (como se muestra en el tutorial)
   - Modelo de adhesión preferencial Barabasi-Albert (`nx.barabasi_albert_graph`)
   - Modelo de mundo pequeño Watts-Strogatz (`nx.watts_strogatz_graph`)
   - Una combinación de diferentes generadores de grafos

2. **Características de los Nodos**: Diseña características sintéticas con una dimensionalidad entre 16 y 64. Las características deben tener alguna correlación con las etiquetas de los nodos pero incluir suficiente ruido para que la tarea sea desafiante.

3. **Etiquetas de los Nodos**: Asigna etiquetas a los nodos para una tarea de clasificación con **al menos 3 clases**. La asignación de etiquetas puede basarse en la estructura del grafo (comunidades), el grado del nodo o cualquier otro criterio significativo.

4. **Divisiones de Datos**: Crea divisiones de entrenamiento/validación/prueba con las siguientes proporciones: 60% entrenamiento, 20% validación, 20% prueba. Genera divisiones para **10 ejecuciones independientes**.

### Entregables

- El código completo para generar tu conjunto de datos personalizado.
- Visualizaciones de la estructura del grafo que muestren las diferentes clases.
- Una breve descripción (1-2 párrafos) que explique tus elecciones de diseño para la estructura del grafo, las características y las etiquetas.

### Criterios de Evaluación

- Correctitud de la implementación.
- Creatividad en el diseño del conjunto de datos.
- Calidad de las visualizaciones.
- Claridad de la descripción escrita.

## Ejercicio 2: Experimentos de Clasificación de Nodos

### Objetivos

El objetivo de este ejercicio es implementar y comparar diferentes modelos para la clasificación de nodos tanto en tu conjunto de datos personalizado como en conjuntos de datos de referencia estándar.

### Descripción de la Tarea

**Parte A: Conjunto de Datos Personalizado**

Utilizando el conjunto de datos sintético que creaste en el Ejercicio 1:

1. Implementa y entrena una **línea base MLP** que ignore la estructura del grafo.
2. Implementa y entrena una **GCN de 2 capas**.
3. Ejecuta experimentos a través de tus 10 divisiones de datos.
4. Reporta la media y la desviación estándar de la precisión de la prueba para ambos modelos.

**Parte B: Conjuntos de Datos de Referencia**

Utilizando los conjuntos de datos Cora y Citeseer cargados con PyTorch Geometric:

1. Entrena una **GCN de 2 capas** en ambos conjuntos de datos.
2. Utiliza las máscaras de entrenamiento/val/prueba proporcionadas.
3. Implementa una parada temprana (early stopping) adecuada basada en la precisión de la validación.
4. Reporta las precisiones de prueba finales.


### Hiperparámetros a Explorar

Experimenta con al menos los siguientes hiperparámetros y reporta sus efectos:

- Dimensiones de la capa oculta: 16, 32, 64, 128
- Tasa de aprendizaje: 0.001, 0.01, 0.1
- Tasa de dropout: 0.0, 0.3, 0.5
- Decaimiento de pesos (weight decay): 0, 1e-4, 5e-4
- Optimizador: Adam, SGD

### Entregables

- Código completo para todos los experimentos.
- Una tabla que resuma los resultados en todos los conjuntos de datos y modelos.
- Curvas de entrenamiento (pérdida y precisión) para al menos una configuración por conjunto de datos.
- Visualizaciones t-SNE de las incrustaciones aprendidas tanto para MLP como para GCN.
- Una discusión (3-4 párrafos) que compare el rendimiento de MLP vs GCN y analice por qué la GCN funciona mejor (o peor) en cada conjunto de datos.

### Preguntas de Análisis

En tu informe, aborda las siguientes preguntas:

1. ¿cómo varía la brecha de rendimiento entre MLP y GCN a través de los conjuntos de datos? ¿Qué podría explicar estas diferencias?
2. ¿Cómo afecta la elección de las dimensiones ocultas al rendimiento del modelo? ¿Existe un compromiso (trade-off) entre la capacidad del modelo y el sobreajuste?
3. ¿Cuál es el efecto del dropout en la estabilidad del entrenamiento y el rendimiento final?
4. Basándote en tus visualizaciones t-SNE, ¿en qué se diferencian las representaciones aprendidas entre MLP y GCN?
