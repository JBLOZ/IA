# Graph Matching with Topological Features

## Practical Session 1.4: Graph Matching with Topological Features

## Introduction
En esta práctica se mejora el matching de grafos incorporando características topológicas mediante embeddings obtenidos con node2vec y tiempos de hitting.

## Theoretical Background
- **Node2vec:** Genera embeddings que capturan la estructura del grafo.
- **Hitting Time:** Mide el tiempo esperado para alcanzar un nodo desde otro, ofreciendo una visión global del grafo.

## Enhanced Matching Algorithm
Se debe modificar la estrategia de matching anterior (práctica 3) para:
1. Calcular embeddings de node2vec y tiempos de hitting.
2. Combinar la matriz de costos usando:
   - Distancia espacial.
   - Distancia de embeddings (node2vec).
   - Distancia entre perfiles de hitting time.
3. Utilizar la función `scipy.optimize.linear_sum_assignment` para la asignación.

## Exercise Outline
- Implementar las funciones auxiliares:
  - `compute_node2vec_embeddings`
  - `hitting_time` y `compute_hitting_time_matrix`
  - `enhanced_spatial_matching`
- Visualizar el matching con líneas entre keypoints.
- Evaluar la precisión del matching y realizar análisis comparativos con la solución espacial original.

## Submission Format
Se espera la misma estructura que en la práctica 3, agregando este notebook (practica4.ipynb) y los resultados de los análisis.