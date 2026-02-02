import nbformat as nbf

# Create new notebook
nb = nbf.v4.new_notebook()

# Add cells
nb['cells'] = [
    # Title and objectives
    nbf.v4.new_markdown_cell("""# Práctica 1: Experimentación con Graph Neural Networks

**Autor:** Jordi Blasco Lozano  
**Universidad:** Universidad de Alicante  
**Curso:** Agentes Inteligentes  

## Objetivos de la Práctica

1. Crear un dataset sintético custom con estructura de grafos
2. Implementar y comparar MLPs vs GCNs para clasificación de nodos
3. Realizar experimentación sistemática con hiperparámetros
4. Analizar rendimiento en datasets benchmark (Cora y Citeseer)
5. Comprender el impacto de la estructura del grafo en el aprendizaje
"""),

    # Section 0: Setup
    nbf.v4.new_markdown_cell("""## 0. Configuración e Imports

Instalación de dependencias y configuración del entorno."""),

    nbf.v4.new_code_cell("""# Imports necesarios
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.manifold import TSNE
import pandas as pd
from tqdm import tqdm
import warnings
warnings.filterwarnings('ignore')

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.data import Data
from torch_geometric.nn import GCNConv
from torch_geometric.datasets import Planetoid
from torch_geometric.utils import degree

# Configuración de reproducibilidad
np.random.seed(42)
torch.manual_seed(42)
if torch.cuda.is_available():
    torch.cuda.manual_seed(42)

# Configuración de visualización
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

print(f"PyTorch version: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")
print("✓ Setup completado")"""),

    # Section 1
    nbf.v4.new_markdown_cell("""## 1. Ejercicio 1: Dataset Sintético Custom

### 1.1 Generación del Grafo con Stochastic Block Model

**Decisión de Diseño:**  
- **Método**: Stochastic Block Model (SBM)
- **Justificación**: Genera grafos con estructura de comunidades clara, ideal para demostrar el poder de GNNs
- **Nodos**: 2000 (escala suficiente para experimentación)
- **Clases**: 4 (balance entre complejidad y claridad)
- **Probabilidades**: p_intra=0.02, p_inter=0.002 (ratio 10:1 para comunidades distinguibles)"""),

    nbf.v4.new_code_cell("""# Parámetros del dataset custom
num_nodes = 2000
num_classes = 4
nodes_per_class = num_nodes // num_classes
feature_dim = 32

# Crear grafo con estructura de comunidades
sizes = [nodes_per_class] * num_classes
p_intra = 0.02   # Probabilidad de arista dentro de la misma comunidad
p_inter = 0.002  # Probabilidad de arista entre comunidades diferentes
probs = np.full((num_classes, num_classes), p_inter)
np.fill_diagonal(probs, p_intra)

G = nx.stochastic_block_model(sizes, probs, seed=42)

print(f"Número de nodos: {G.number_of_nodes()}")
print(f"Número de aristas: {G.number_of_edges()}")
print(f"Densidad del grafo: {nx.density(G):.6f}")
print(f"Promedio de grado: {sum(dict(G.degree()).values()) / G.number_of_nodes():.2f}")"""),

    nbf.v4.new_markdown_cell("""### 1.2 Creación de Características con Señal Débil + Ruido Fuerte

**Decisión Clave**: Crear features que tengan POCA correlación con las labels.  
Esto fuerza a los modelos a depender de la estructura del grafo para clasificar correctamente."""),

    nbf.v4.new_code_cell("""# Asignar labels basados en la estructura de bloques
node_labels = np.array([i // nodes_per_class for i in range(num_nodes)])

# Crear centros de clase con magnitud PEQUEÑA
class_centers = np.random.randn(num_classes, feature_dim) * 0.3

# Generar características: señal débil + ruido fuerte
node_features = np.zeros((num_nodes, feature_dim))
for i in range(num_nodes):
    label = node_labels[i]
    noise = np.random.randn(feature_dim) * 1.0        # Ruido FUERTE
    weak_signal = class_centers[label] * 0.2          # Señal DÉBIL
    node_features[i] = weak_signal + noise

print(f"Shape de características: {node_features.shape}")
print(f"Estadísticas - Media: {node_features.mean():.3f}, Std: {node_features.std():.3f}")
print(f"\\nDistribución de labels:")
unique, counts = np.unique(node_labels, return_counts=True)
for label, count in zip(unique, counts):
    print(f"  Clase {label}: {count} nodos")"""),

    nbf.v4.new_markdown_cell("""### 1.3 Conversión a Formato PyTorch Geometric"""),

   nbf.v4.new_code_cell("""# Convertir a tensors de PyTorch
x = torch.tensor(node_features, dtype=torch.float)
y = torch.tensor(node_labels, dtype=torch.long)

# Convertir edge list a formato COO
edge_list = list(G.edges())
edge_index = torch.tensor(edge_list, dtype=torch.long).t().contiguous()

# Para grafos no dirigidos, añadir aristas en ambas direcciones
edge_index = torch.cat([edge_index, edge_index.flip(0)], dim=1)

# Crear objeto Data de PyG
data = Data(x=x, edge_index=edge_index, y=y)

print(f"Número de nodos: {data.num_nodes}")
print(f"Número de aristas: {data.num_edges}")
print(f"Número de features por nodo: {data.num_node_features}")
print(f"Tiene nodos aislados: {data.has_isolated_nodes()}")
print(f"Tiene self-loops: {data.has_self_loops()}")
print(f"Es no dirigido: {data.is_undirected()}")"""),

    nbf.v4.new_markdown_cell("""### 1.4 Creación de 10 Splits Train/Val/Test"""),

    nbf.v4.new_code_cell("""def create_masks(num_nodes, num_classes, train_ratio=0.6, val_ratio=0.2, seed=0):
    \"\"\"Crear máscaras de train/val/test para clasificación de nodos.\"\"\"
    np.random.seed(seed)
    indices = np.random.permutation(num_nodes)
    train_size = int(num_nodes * train_ratio)
    val_size = int(num_nodes * val_ratio)
    
    train_idx = indices[:train_size]
    val_idx = indices[train_size:train_size + val_size]
    test_idx = indices[train_size + val_size:]
    
    train_mask = torch.zeros(num_nodes, dtype=torch.bool)
    val_mask = torch.zeros(num_nodes, dtype=torch.bool)
    test_mask = torch.zeros(num_nodes, dtype=torch.bool)
    
    train_mask[train_idx] = True
    val_mask[val_idx] = True
    test_mask[test_idx] = True
    
    return train_mask, val_mask, test_mask

# Crear 10 splits para evaluación robusta
num_runs = 10
all_masks = []

for run in range(num_runs):
    train_mask, val_mask, test_mask = create_masks(data.num_nodes, num_classes, seed=run)
    all_masks.append({'train': train_mask, 'val': val_mask, 'test': test_mask})

print(f"Creados {num_runs} splits diferentes")
print(f"Ejemplo split 0:")
print(f"  Train: {all_masks[0]['train'].sum().item()} nodos")
print(f"  Val: {all_masks[0]['val'].sum().item()} nodos")
print(f"  Test: {all_masks[0]['test'].sum().item()} nodos")"""),

    nbf.v4.new_markdown_cell("""### 1.5 Visualización del Grafo Custom"""),

    nbf.v4.new_code_cell("""# Visualizar subsample del grafo
sample_size = 500
G_sample = G.subgraph(list(range(sample_size)))
colors = ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3']
node_colors_viz = [colors[node_labels[i]] for i in range(sample_size)]

plt.figure(figsize=(14, 12))
pos = nx.spring_layout(G_sample, seed=42, k=0.5, iterations=50)
nx.draw(G_sample, pos, node_color=node_colors_viz, node_size=40,
        edge_color='gray', alpha=0.7, width=0.4)

# Añadir leyenda
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor=colors[i], label=f'Clase {i}') for i in range(num_classes)]
plt.legend(handles=legend_elements, loc='upper right', fontsize=12)
plt.title("Grafo Sintético Custom (500 nodos de muestra)", fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('images/custom_graph_structure.png', dpi=150, bbox_inches='tight')
plt.show()

print("✓ Grafo visualizado y guardado")"""),

    # Section 2: Models
    nbf.v4.new_markdown_cell("""## 2. Implementación de Modelos

### 2.1 MLP Baseline (Ignora Estructura del Grafo)"""),

    nbf.v4.new_code_cell("""class MLP(nn.Module):
    \"\"\"Multi-Layer Perceptron para clasificación de nodos.
    Este modelo ignora completamente la estructura del grafo.\"\"\"
    
    def __init__(self, in_channels, hidden_channels, out_channels, dropout=0.5):
        super(MLP, self).__init__()
        self.fc1 = nn.Linear(in_channels, hidden_channels)
        self.fc2 = nn.Linear(hidden_channels, out_channels)
        self.dropout = nn.Dropout(dropout)
    
    def forward(self, x):
        x = self.fc1(x)
        x = F.relu(x)
        x = self.dropout(x)
        x = self.fc2(x)
        return x

# Test
mlp_test = MLP(data.num_node_features, 64, num_classes)
print(mlp_test)
print(f"\\nNúmero de parámetros: {sum(p.numel() for p in mlp_test.parameters())}")"""),

    nbf.v4.new_markdown_cell("""### 2.2 GCN (Usa Paso de Mensajes)"""),

    nbf.v4.new_code_cell("""class GCN(nn.Module):
    \"\"\"Graph Convolutional Network para clasificación de nodos.
    Utiliza la estructura del grafo mediante message passing.\"\"\"
    
    def __init__(self, in_channels, hidden_channels, out_channels, dropout=0.5):
        super(GCN, self).__init__()
        self.conv1 = GCNConv(in_channels, hidden_channels)
        self.conv2 = GCNConv(hidden_channels, out_channels)
        self.dropout = nn.Dropout(dropout)
    
    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index)
        x = F.relu(x)
        x = self.dropout(x)
        x = self.conv2(x, edge_index)
        return x

# Test
gcn_test = GCN(data.num_node_features, 64, num_classes)
print(gcn_test)
print(f"\\nNúmero de parámetros: {sum(p.numel() for p in gcn_test.parameters())}")"""),

    # Training functions
    nbf.v4.new_markdown_cell("""### 2.3 Funciones de Entrenamiento y Evaluación"""),

    nbf.v4.new_code_cell("""def train_epoch(model, data, optimizer, criterion, train_mask):
    \"\"\"Entrenar el modelo por una época.\"\"\"
    model.train()
    optimizer.zero_grad()
    
    if isinstance(model, MLP):
        out = model(data.x)
    else:
        out = model(data.x, data.edge_index)
    
    loss = criterion(out[train_mask], data.y[train_mask])
    loss.backward()
    optimizer.step()
    return loss.item()

@torch.no_grad()
def evaluate(model, data, mask):
    \"\"\"Evaluar el modelo.\"\"\"
    model.eval()
    
    if isinstance(model, MLP):
        out = model(data.x)
    else:
        out = model(data.x, data.edge_index)
    
    pred = out.argmax(dim=1)
    correct = (pred[mask] == data.y[mask]).sum().item()
    return correct / mask.sum().item()

def run_experiment(model, data, masks, num_epochs=200, lr=0.01, weight_decay=5e-4, verbose=False):
    \"\"\"Ejecutar experimento completo.\"\"\"
    optimizer = torch.optim.Adam(model.parameters(), lr=lr, weight_decay=weight_decay)
    criterion = nn.CrossEntropyLoss()
    
    train_mask, val_mask, test_mask = masks['train'], masks['val'], masks['test']
    
    history = {'train_loss': [], 'train_acc': [], 'val_acc': [], 'test_acc': []}
    best_val_acc, best_test_acc = 0, 0
    
    for epoch in range(num_epochs):
        loss = train_epoch(model, data, optimizer, criterion, train_mask)
        train_acc = evaluate(model, data, train_mask)
        val_acc = evaluate(model, data, val_mask)
        test_acc = evaluate(model, data, test_mask)
        
        history['train_loss'].append(loss)
        history['train_acc'].append(train_acc)
        history['val_acc'].append(val_acc)
        history['test_acc'].append(test_acc)
        
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            best_test_acc = test_acc
        
        if verbose and (epoch + 1) % 50 == 0:
            print(f"Epoch {epoch+1:3d} | Loss: {loss:.4f} | Train: {train_acc:.4f} | Val: {val_acc:.4f} | Test: {test_acc:.4f}")
    
    return {'history': history, 'best_val_acc': best_val_acc, 'best_test_acc': best_test_acc}

print("✓ Funciones de entrenamiento definidas")"""),

    # Section 3: Base experiments
    nbf.v4.new_markdown_cell("""## 3. Experimentos Base en Dataset Custom

### 3.1 Experimento con Configuración Base

**Hiperparámetros base:**
- Hidden channels: 64
- Learning rate: 0.01
- Dropout: 0.5
- Weight decay: 5e-4
- Optimizer: Adam
- Epochs: 200"""),

    nbf.v4.new_code_cell("""# Configuración base
base_config = {
    'hidden_channels': 64,
    'lr': 0.01,
    'dropout': 0.5,
    'weight_decay': 5e-4,
    'num_epochs': 200
}

# Almacenar resultados
mlp_base_results = []
gcn_base_results = []

print("Ejecutando experimentos base en 10 splits...")
for run in tqdm(range(num_runs), desc="Runs"):
    # MLP
    mlp = MLP(data.num_node_features, base_config['hidden_channels'], num_classes, base_config['dropout'])
    mlp_result = run_experiment(mlp, data, all_masks[run], 
                                base_config['num_epochs'], base_config['lr'], base_config['weight_decay'])
    mlp_base_results.append(mlp_result)
    
    # GCN
    gcn = GCN(data.num_node_features, base_config['hidden_channels'], num_classes, base_config['dropout'])
    gcn_result = run_experiment(gcn, data, all_masks[run],
                                base_config['num_epochs'], base_config['lr'], base_config['weight_decay'])
    gcn_base_results.append(gcn_result)

# Estadísticas
mlp_accs = [r['best_test_acc'] for r in mlp_base_results]
gcn_accs = [r['best_test_acc'] for r in gcn_base_results]

print(f"\\n{'='*60}")
print("RESULTADOS BASE (Test Accuracy)")
print('='*60)
print(f"MLP: {np.mean(mlp_accs):.4f} ± {np.std(mlp_accs):.4f}")
print(f"GCN: {np.mean(gcn_accs):.4f} ± {np.std(gcn_accs):.4f}")
print(f"Mejora GCN sobre MLP: {(np.mean(gcn_accs) - np.mean(mlp_accs)):.4f} ({((np.mean(gcn_accs) / np.mean(mlp_accs)) - 1) * 100:.1f}%)")
print('='*60)"""),

    nbf.v4.new_markdown_cell("""### 3.2 Visualización de Curvas de Entrenamiento"""),

    nbf.v4.new_code_cell("""# Visualizar curvas del primer run
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

mlp_hist = mlp_base_results[0]['history']
gcn_hist = gcn_base_results[0]['history']

# Loss
axes[0].plot(mlp_hist['train_loss'], label='MLP', alpha=0.8, linewidth=2)
axes[0].plot(gcn_hist['train_loss'], label='GCN', alpha=0.8, linewidth=2)
axes[0].set_xlabel('Epoch', fontsize=12)
axes[0].set_ylabel('Loss', fontsize=12)
axes[0].set_title('Training Loss', fontsize=14, fontweight='bold')
axes[0].legend(fontsize=11)
axes[0].grid(True, alpha=0.3)

# Train Accuracy
axes[1].plot(mlp_hist['train_acc'], label='MLP', alpha=0.8, linewidth=2)
axes[1].plot(gcn_hist['train_acc'], label='GCN', alpha=0.8, linewidth=2)
axes[1].set_xlabel('Epoch', fontsize=12)
axes[1].set_ylabel('Accuracy', fontsize=12)
axes[1].set_title('Training Accuracy', fontsize=14, fontweight='bold')
axes[1].legend(fontsize=11)
axes[1].grid(True, alpha=0.3)

# Validation Accuracy
axes[2].plot(mlp_hist['val_acc'], label='MLP', alpha=0.8, linewidth=2)
axes[2].plot(gcn_hist['val_acc'], label='GCN', alpha=0.8, linewidth=2)
axes[2].set_xlabel('Epoch', fontsize=12)
axes[2].set_ylabel('Accuracy', fontsize=12)
axes[2].set_title('Validation Accuracy', fontsize=14, fontweight='bold')
axes[2].legend(fontsize=11)
axes[2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('images/custom_base_training_curves.png', dpi=150, bbox_inches='tight')
plt.show()

print("✓ Curvas guardadas")"""),

    # Continue with more sections...
]

# Write notebook
with open('practica_01.ipynb', 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print("✓ Notebook completo generado!")
