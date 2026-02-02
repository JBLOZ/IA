#!/usr/bin/env python3
"""Script to generate the practice notebook programmatically."""

import json

def create_cell(cell_type, source, metadata=None):
    """Create a notebook cell."""
    cell = {
        "cell_type": cell_type,
        "metadata": metadata or {},
        "source": source if isinstance(source, list) else [source]
    }
    if cell_type == "code":
        cell["execution_count"] = None
        cell["outputs"] = []
    return cell

# Define all cells
cells = []

# Section 0: Setup
cells.append(create_cell("markdown", [
    "# Práctica 1: Experimentación con Graph Neural Networks\n",
    "\n",
    "**Autor:** Jordi Blasco Lozano\n",
    "**Universidad:** Universidad de Alicante\n",
    "**Fecha:** 2026-02-02\n",
    "\n",
    "## Objetivos\n",
    "- Crear un dataset sintético custom con grafos\n",
    "- Comparar MLPs vs GCNs en clasificación de nodos\n",
    "- Experimentar sistemáticamente con hiperparámetros\n",
    "- Analizar resultados en benchmarks (Cora, Citeseer)\n"
]))

cells.append(create_cell("markdown", ["## 0. Configuración e Imports"]))

cells.append(create_cell("code", [
    "# Imports\n",
    "import numpy as np\n",
    "import networkx as nx\n",
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns\n",
    "from sklearn.manifold import TSNE\n",
    "import pandas as pd\n",
    "\n",
    "import torch\n",
    "import torch.nn as nn\n",
    "import torch.nn.functional as F\n",
    "from torch_geometric.data import Data\n",
    "from torch_geometric.nn import GCNConv\n",
    "from torch_geometric.datasets import Planetoid\n",
    "from torch_geometric.utils import degree\n",
    "\n",
    "# Seeds para reproducibilidad\n",
    "np.random.seed(42)\n",
    "torch.manual_seed(42)\n",
    "\n",
    "# Configuración de visualización\n",
    "plt.style.use('seaborn-v0_8-darkgrid')\n",
    "sns.set_palette(\"husl\")\n",
    "\n",
    "print(\"Librerías importadas correctamente\")\n",
    "print(f\"PyTorch version: {torch.__version__}\")\n"
]))

# Section 1: Custom Dataset
cells.append(create_cell("markdown", [
    "## 1. Ejercicio 1: Dataset Sintético Custom\n",
    "\n",
    "### 1.1 Generación del Grafo\n",
    "Crearemos un grafo con estructura de comunidades usando Stochastic Block Model.\n"
]))

cells.append(create_cell("code", [
    "# Parámetros del dataset\n",
    "num_nodes = 2000\n",
    "num_classes = 4\n",
    "nodes_per_class = num_nodes // num_classes\n",
    "feature_dim = 32\n",
    "\n",
    "# Crear grafo con estructura de comunidades\n",
    "sizes = [nodes_per_class] * num_classes\n",
    "p_intra = 0.02  # Probabilidad dentro de comunidad\n",
    "p_inter = 0.002  # Probabilidad entre comunidades\n",
    "probs = np.full((num_classes, num_classes), p_inter)\n",
    "np.fill_diagonal(probs, p_intra)\n",
    "\n",
    "G = nx.stochastic_block_model(sizes, probs, seed=42)\n",
    "\n",
    "print(f\"Número de nodos: {G.number_of_nodes()}\")\n",
    "print(f\"Número de aristas: {G.number_of_edges()}\")\n",
    "print(f\"Densidad del grafo: {nx.density(G):.4f}\")\n"
]))

cells.append(create_cell("markdown", ["### 1.2 Creación de Características con Señal Débil"]))

cells.append(create_cell("code", [
    "# Labels basados en comunidades\n",
    "node_labels = np.array([i // nodes_per_class for i in range(num_nodes)])\n",
    "\n",
    "# Crear características con señal DÉBIL + ruido FUERTE\n",
    "# Esto hace que la estructura del grafo sea esencial\n",
    "class_centers = np.random.randn(num_classes, feature_dim) * 0.3\n",
    "node_features = np.zeros((num_nodes, feature_dim))\n",
    "\n",
    "for i in range(num_nodes):\n",
    "    label = node_labels[i]\n",
    "    noise = np.random.randn(feature_dim) * 1.0  # Ruido fuerte\n",
    "    weak_signal = class_centers[label] * 0.2  # Señal débil\n",
    "    node_features[i] = weak_signal + noise\n",
    "\n",
    "print(f\"Shape de características: {node_features.shape}\")\n",
    "print(f\"Media: {node_features.mean():.3f}, Std: {node_features.std():.3f}\")\n"
]))

# Add visualization
cells.append(create_cell("markdown", ["### 1.3 Visualización del Grafo"]))

cells.append(create_cell("code", [
    "# Visualizar el grafo (subsample para claridad)\n",
    "sample_nodes = 500\n",
    "G_sample = G.subgraph(list(range(sample_nodes)))\n",
    "colors = ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3']\n",
    "node_colors = [colors[node_labels[i]] for i in range(sample_nodes)]\n",
    "\n",
    "plt.figure(figsize=(12, 10))\n",
    "pos = nx.spring_layout(G_sample, seed=42, k=0.5)\n",
    "nx.draw(G_sample, pos, node_color=node_colors, node_size=30,\n",
    "        edge_color='gray', alpha=0.6, width=0.3)\n",
    "plt.title(f\"Grafo Sintético ({sample_nodes} nodos de muestra)\")\n",
    "plt.tight_layout()\n",
    "plt.savefig('images/custom_graph_structure.png', dpi=150, bbox_inches='tight')\n",
    "plt.show()\n"
]))

# Continue with more sections...
# (Due to token limits, I'll create the script to generate the rest)

# Create test
nb = {
    "cells": cells,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "name": "python",
            "version": "3.11.0"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

with open('practica_01.ipynb', 'w') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("Notebook created successfully!")
