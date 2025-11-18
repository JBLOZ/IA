# Análisis del Dataset Zoo - Clasificación Multiclase
# Este script implementa y evalúa 6 algoritmos de clasificación en el dataset Zoo de UCI

import pandas as pd
import numpy as np
import os
import warnings
from sklearn.model_selection import StratifiedKFold
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier, NearestNeighbors
from sklearn.neighbors import KernelDensity
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, f1_score
from scipy.stats import multivariate_normal

# Silenciar warnings
os.environ['LOKY_MAX_CPU_COUNT'] = '4'
warnings.filterwarnings('ignore', category=UserWarning, module='joblib')

print("✓ Librerías importadas correctamente")

# ============================================================================
# 1. CARGA Y ANÁLISIS EXPLORATORIO DEL DATASET
# ============================================================================

# Clases del Zoo dataset (1-7 -> labels para report)
class_names = ['mammal', 'bird', 'reptile', 'fish', 'amphibian', 'invertebrate', 'insect']

print("=" * 80)
print("ANÁLISIS DEL DATASET ZOO (Multiclass Classification)")
print("=" * 80)

# Cargar datos: zoo.data (col 0: animal name (ignorar), col 1-17: features, col 18: class 1-7)
df = pd.read_csv('./data_zoo/zoo.csv')
# df = pd.read_csv('./data_zoo/zoo.csv')
df.columns = ['animal'] + [f'feature_{i}' for i in range(1, 17)] + ['class']
X = df.iloc[:, 1:-1]  # Features 1-17
y = df.iloc[:, -1].values - 1  # Clase 0-6 para sklearn

print("\nInformación del dataset:")
print(f"Forma: {X.shape} (instancias x features)")
print(f"Clases: {len(np.unique(y))} (multiclass: {class_names})")
print("\nDistribución de clases:")
unique, counts = np.unique(y, return_counts=True)
for i, (cls, count) in enumerate(zip(class_names, counts)):
    print(f"Clase {i+1} ({cls}): {count} muestras ({count/len(y)*100:.1f}%)")

print("\nPrimeras 5 filas del dataset:")
print(df.head())

# ============================================================================
# 2. CONFIGURACIÓN DE VALIDACIÓN CRUZADA
# ============================================================================

# Configuración: CV estratificado 5-fold sobre TODO el dataset
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=41)

print(f"\nTotal de muestras: {len(X)}")
print(f"Estrategia: Cross-Validation 5-fold sobre todo el conjunto")
print(f"Cada fold: ~{len(X)*0.8:.0f} train+val (~80%), ~{len(X)*0.2:.0f} test (~20%)")
print("\nDistribución de clases en el conjunto completo:")
print(pd.Series(y).value_counts().sort_index())

print("\n✓ Configuración de validación cruzada: 5-fold estratificada sobre todo el dataset")

# ============================================================================
# 3. FUNCIONES AUXILIARES PARA EVALUACIÓN CON CV
# ============================================================================

# Función para evaluar modelo en un fold específico
def evaluate_fold(model, X_test, y_test, fold_num):
    """Evalúa el modelo en el conjunto de test del fold"""
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    f1_mac = f1_score(y_test, preds, average='macro')
    cm = confusion_matrix(y_test, preds)
    return acc, f1_mac, cm, preds

# Función para imprimir resultados agregados de CV
def print_cv_results(model_name, accuracies, f1_scores, all_preds, all_true):
    """Imprime resultados agregados de cross-validation"""
    print(f"\n{'='*80}")
    print(f"RESULTADOS CV: {model_name}")
    print(f"{'='*80}")
    print(f"\nAccuracy por fold: {[f'{acc:.4f}' for acc in accuracies]}")
    print(f"Accuracy promedio: {np.mean(accuracies):.4f} ± {np.std(accuracies):.4f}")
    print(f"\nF1-macro por fold: {[f'{f1:.4f}' for f1 in f1_scores]}")
    print(f"F1-macro promedio: {np.mean(f1_scores):.4f} ± {np.std(f1_scores):.4f}")
    
    # Reporte global (concatenando todas las predicciones)
    print(f"\n--- Reporte de clasificación global (todos los folds) ---")
    print(classification_report(all_true, all_preds, target_names=class_names))
    
    # Matriz de confusión global
    cm_global = confusion_matrix(all_true, all_preds)
    print(f"\nMatriz de confusión global:")
    print(cm_global)
    
    return np.mean(accuracies), np.mean(f1_scores)

print("✓ Funciones de evaluación definidas")

# ============================================================================
# 4. MODELO 1: NAIVE BAYES GAUSSIANO
# ============================================================================

print("\n" + "=" * 80)
print("1. NAIVE BAYES GAUSSIANO")
print("=" * 80)

nb_accuracies = []
nb_f1_scores = []
nb_all_preds = []
nb_all_true = []

for fold, (train_val_idx, test_idx) in enumerate(skf.split(X, y), 1):
    print(f"\n--- Fold {fold}/5 ---")
    
    # Dividir en train+val y test
    X_train_val, X_test_fold = X.iloc[train_val_idx], X.iloc[test_idx]
    y_train_val, y_test_fold = y[train_val_idx], y[test_idx]
    
    # Entrenar Naive Bayes (sin hiperparámetros)
    nb = GaussianNB()
    nb.fit(X_train_val, y_train_val)
    
    # Evaluar en test del fold
    acc, f1, cm, preds = evaluate_fold(nb, X_test_fold, y_test_fold, fold)
    nb_accuracies.append(acc)
    nb_f1_scores.append(f1)
    nb_all_preds.extend(preds)
    nb_all_true.extend(y_test_fold)
    
    print(f"Accuracy: {acc:.4f}, F1-macro: {f1:.4f}")

# Resultados agregados
nb_mean_acc, nb_mean_f1 = print_cv_results("Naive Bayes", nb_accuracies, nb_f1_scores, 
                                            nb_all_preds, nb_all_true)

# ============================================================================
# 5. MODELO 2: MLE MULTIVARIANTE (FULL BAYESIAN GAUSSIAN)
# ============================================================================

print("\n" + "=" * 80)
print("2. MLE MULTIVARIANTE (Full Bayesian Gaussian)")
print("=" * 80)

class FullGaussianBayes:
    def __init__(self):
        self.priors = None
        self.means = None
        self.covs = None
        self.classes = None
    
    def fit(self, X, y):
        self.classes = np.unique(y)
        self.priors = np.bincount(y) / len(y)
        self.means = np.array([X[y == c].mean(axis=0) for c in self.classes])
        self.covs = np.array([np.cov(X[y == c].T) + 1e-6 * np.eye(X.shape[1]) for c in self.classes])
        return self
    
    def predict(self, X):
        n_samples = X.shape[0]
        ll = np.zeros((n_samples, len(self.classes)))
        for i, c in enumerate(self.classes):
            ll[:, i] = multivariate_normal(mean=self.means[i], cov=self.covs[i]).logpdf(X)
        posteriors = np.exp(ll) * self.priors
        posteriors /= posteriors.sum(axis=1, keepdims=True)
        return np.argmax(posteriors, axis=1)

print("✓ Clase FullGaussianBayes definida")

mle_accuracies = []
mle_f1_scores = []
mle_all_preds = []
mle_all_true = []

for fold, (train_val_idx, test_idx) in enumerate(skf.split(X, y), 1):
    print(f"\n--- Fold {fold}/5 ---")
    
    # Dividir en train+val y test
    X_train_val, X_test_fold = X.iloc[train_val_idx], X.iloc[test_idx]
    y_train_val, y_test_fold = y[train_val_idx], y[test_idx]
    
    # Entrenar MLE Full
    mle = FullGaussianBayes()
    mle.fit(X_train_val.values, y_train_val)
    
    # Evaluar en test del fold
    acc, f1, cm, preds = evaluate_fold(mle, X_test_fold.values, y_test_fold, fold)
    mle_accuracies.append(acc)
    mle_f1_scores.append(f1)
    mle_all_preds.extend(preds)
    mle_all_true.extend(y_test_fold)
    
    print(f"Accuracy: {acc:.4f}, F1-macro: {f1:.4f}")

# Resultados agregados
mle_mean_acc, mle_mean_f1 = print_cv_results("MLE Full Gaussian", mle_accuracies, mle_f1_scores,
                                              mle_all_preds, mle_all_true)

# ============================================================================
# 6. MODELO 3: HISTOGRAM BAYES
# ============================================================================

print("\n" + "=" * 80)
print("3. DENSIDAD NO PARAMÉTRICA - HISTOGRAMA")
print("=" * 80)

class HistogramBayes:
    def __init__(self, bins=2):
        self.bins = bins
        self.priors = None
        self.hist_per_class = None
        self.edges = None
    
    def fit(self, X, y):
        self.classes = np.unique(y)
        self.priors = np.bincount(y) / len(y)
        self.hist_per_class = {}
        for c in self.classes:
            X_c = X[y == c]
            hists = []
            edges_list = []
            for feat in range(X.shape[1]):
                hist, edges = np.histogram(X_c.iloc[:, feat], bins=self.bins, density=True)
                hists.append(hist)
                edges_list.append(edges)
            self.hist_per_class[c] = (np.array(hists), edges_list)
        self.edges = edges_list[0] if edges_list else None
        return self
    
    def _density_hist(self, x, c):
        hists, edges = self.hist_per_class[c]
        dens = 1.0
        for i, feat_val in enumerate(x):
            bin_idx = np.digitize(feat_val, edges[i]) - 1
            if 0 <= bin_idx < len(hists[i]):
                dens *= hists[i][bin_idx]
            else:
                dens *= 0
        return dens
    
    def predict(self, X):
        n_samples = len(X)
        preds = np.zeros(n_samples, dtype=int)
        for i in range(n_samples):
            posteriors = []
            for c in self.classes:
                dens = self._density_hist(X.iloc[i], c)
                post = self.priors[c] * dens
                posteriors.append(post)
            preds[i] = self.classes[np.argmax(posteriors)]
        return preds

print("✓ Clase HistogramBayes definida")

hist_accuracies = []
hist_f1_scores = []
hist_all_preds = []
hist_all_true = []

for fold, (train_val_idx, test_idx) in enumerate(skf.split(X, y), 1):
    print(f"\n--- Fold {fold}/5 ---")
    
    # Dividir en train+val y test
    X_train_val, X_test_fold = X.iloc[train_val_idx], X.iloc[test_idx]
    y_train_val, y_test_fold = y[train_val_idx], y[test_idx]
    
    # Entrenar Histogram Bayes (bins=2 fijo para datos binarios)
    hist_bayes = HistogramBayes(bins=2)
    hist_bayes.fit(pd.DataFrame(X_train_val), y_train_val)
    
    # Evaluar en test del fold
    acc, f1, cm, preds = evaluate_fold(hist_bayes, pd.DataFrame(X_test_fold), y_test_fold, fold)
    hist_accuracies.append(acc)
    hist_f1_scores.append(f1)
    hist_all_preds.extend(preds)
    hist_all_true.extend(y_test_fold)
    
    print(f"Accuracy: {acc:.4f}, F1-macro: {f1:.4f}")

# Resultados agregados
hist_mean_acc, hist_mean_f1 = print_cv_results("Histogram Bayes", hist_accuracies, hist_f1_scores,
                                                hist_all_preds, hist_all_true)

# ============================================================================
# 7. MODELO 4: PARZEN WINDOWS
# ============================================================================

print("\n" + "=" * 80)
print("4. DENSIDAD NO PARAMÉTRICA - PARZEN WINDOWS")
print("=" * 80)

class ParzenBayes:
    def __init__(self, bandwidth=0.5):
        self.bandwidth = bandwidth
        self.priors = None
        self.kdes = None
        self.classes = None
    
    def fit(self, X, y):
        self.classes = np.unique(y)
        self.priors = np.bincount(y) / len(y)
        self.kdes = {}
        for c in self.classes:
            X_c = X[y == c].values.reshape(-1, X.shape[1])
            kde = KernelDensity(kernel='gaussian', bandwidth=self.bandwidth).fit(X_c)
            self.kdes[c] = kde
        return self
    
    def predict(self, X):
        X_val = X.values.reshape(-1, X.shape[1])
        n_samples = len(X_val)
        ll = np.zeros((n_samples, len(self.classes)))
        for i, c in enumerate(self.classes):
            ll[:, i] = np.exp(self.kdes[c].score_samples(X_val))
        posteriors = ll * self.priors
        posteriors /= posteriors.sum(axis=1, keepdims=True) + 1e-10
        return np.argmax(posteriors, axis=1)

print("✓ Clase ParzenBayes definida")

params_parzen = [0.05, 0.1, 0.5, 1.0, 1.5, 2.0]

# Matriz para almacenar resultados: [hiperparámetro][fold] = (acc, f1, preds)
parzen_results = {h: {'accuracies': [], 'f1_scores': [], 'all_preds': [], 'all_true': []} 
                  for h in params_parzen}

print("\nEvaluando todos los hiperparámetros en cada fold...")
print("=" * 80)

# Para cada fold, evaluar todos los hiperparámetros
for fold, (train_val_idx, test_idx) in enumerate(skf.split(X, y), 1):
    print(f"\n--- Fold {fold}/5 ---")
    
    # Dividir en train+val y test
    X_train_val, X_test_fold = X.iloc[train_val_idx], X.iloc[test_idx]
    y_train_val, y_test_fold = y[train_val_idx], y[test_idx]
    
    # Evaluar cada hiperparámetro en este fold
    for h in params_parzen:
        # Entrenar con este h
        parzen = ParzenBayes(bandwidth=h)
        parzen.fit(pd.DataFrame(X_train_val), y_train_val)
        
        # Evaluar en test del fold
        acc, f1, cm, preds = evaluate_fold(parzen, pd.DataFrame(X_test_fold), y_test_fold, fold)
        
        # Guardar resultados para este hiperparámetro y fold
        parzen_results[h]['accuracies'].append(acc)
        parzen_results[h]['f1_scores'].append(f1)
        parzen_results[h]['all_preds'].extend(preds)
        parzen_results[h]['all_true'].extend(y_test_fold)
        
        print(f"  h={h}: Accuracy={acc:.4f}, F1-macro={f1:.4f}")

print("\n" + "=" * 80)
print("RESUMEN POR HIPERPARÁMETRO:")
print("=" * 80)

# Calcular promedios y encontrar el mejor
best_h = None
best_f1_mean = -np.inf

for h in params_parzen:
    acc_mean = np.mean(parzen_results[h]['accuracies'])
    acc_std = np.std(parzen_results[h]['accuracies'])
    f1_mean = np.mean(parzen_results[h]['f1_scores'])
    f1_std = np.std(parzen_results[h]['f1_scores'])
    
    print(f"\nh={h}:")
    print(f"  Accuracy por fold: {[f'{a:.4f}' for a in parzen_results[h]['accuracies']]}")
    print(f"  Accuracy: {acc_mean:.4f} ± {acc_std:.4f}")
    print(f"  F1-macro por fold: {[f'{f:.4f}' for f in parzen_results[h]['f1_scores']]}")
    print(f"  F1-macro: {f1_mean:.4f} ± {f1_std:.4f}")
    
    if f1_mean > best_f1_mean:
        best_f1_mean = f1_mean
        best_h = h

print("\n" + "=" * 80)
print(f"✓ MEJOR HIPERPARÁMETRO: h={best_h}")
print(f"  F1-macro: {best_f1_mean:.4f} ± {np.std(parzen_results[best_h]['f1_scores']):.4f}")
print("=" * 80)

# Usar los resultados del mejor hiperparámetro para el reporte final
parzen_accuracies = parzen_results[best_h]['accuracies']
parzen_f1_scores = parzen_results[best_h]['f1_scores']
parzen_all_preds = parzen_results[best_h]['all_preds']
parzen_all_true = parzen_results[best_h]['all_true']

parzen_mean_acc, parzen_mean_f1 = print_cv_results(f"Parzen Windows (h={best_h})", 
                                                    parzen_accuracies, parzen_f1_scores,
                                                    parzen_all_preds, parzen_all_true)

# ============================================================================
# 8. MODELO 5: K-NN DENSITY ESTIMATOR
# ============================================================================

print("\n" + "=" * 80)
print("5. DENSIDAD NO PARAMÉTRICA - k-NN DENSITY ESTIMATOR")
print("=" * 80)

class KNNDensityBayes:
    """
    Clasificador Bayesiano usando estimación de densidad k-NN.
    
    La densidad se estima como:
        p(x|ω) = k / (|D_ω| * V_k(x))
    
    donde V_k(x) es el volumen de la hiper-esfera que contiene
    los k vecinos más cercanos de x en la clase ω.
    """
    def __init__(self, k=5):
        self.k = k
        self.priors = None
        self.nn_models = {}  # Un modelo de vecinos por clase
        self.classes = None
        self.class_data = {}  # Datos de entrenamiento por clase
    
    def fit(self, X, y):
        """Entrena el modelo guardando los datos de cada clase."""
        self.classes = np.unique(y)
        self.priors = np.bincount(y) / len(y)
        
        # Para cada clase, guardamos sus datos y entrenamos un NearestNeighbors
        for c in self.classes:
            X_c = X[y == c].values if hasattr(X, 'values') else X[y == c]
            self.class_data[c] = X_c
            
            # Crear modelo de vecinos más cercanos para esta clase
            nn_model = NearestNeighbors(n_neighbors=min(self.k, len(X_c)), 
                                        algorithm='auto', 
                                        metric='euclidean')
            nn_model.fit(X_c)
            self.nn_models[c] = nn_model
        
        return self
    
    def _estimate_density(self, X_val, class_idx):
        """
        Estima p(x|ω) para cada muestra en X_val usando k-NN density.
        
        p(x|ω) = k / (N_ω * V_k(x))
        donde V_k(x) es el volumen de la hiper-esfera de radio r_k(x)
        (distancia al k-ésimo vecino más cercano).
        """
        nn_model = self.nn_models[class_idx]
        N_class = len(self.class_data[class_idx])
        d = X_val.shape[1]  # dimensionalidad
        
        # Obtener distancias a los k vecinos más cercanos
        distances, _ = nn_model.kneighbors(X_val)
        
        # La distancia al k-ésimo vecino más cercano define el radio
        r_k = distances[:, -1]  # última columna = k-ésimo vecino
        
        # Volumen de hiper-esfera en d dimensiones: V_d(r) = π^(d/2) / Γ(d/2 + 1) * r^d
        # Para simplificar usamos solo r^d (la constante π^(d/2)/Γ(d/2+1) se cancela en el ratio)
        V_k = r_k ** d
        
        # Evitar divisiones por cero
        V_k = np.maximum(V_k, 1e-10)
        
        # Densidad: k / (N_class * V_k)
        density = self.k / (N_class * V_k)
        
        return density
    
    def predict(self, X):
        """Predice las clases usando la regla de Bayes."""
        X_val = X.values if hasattr(X, 'values') else X
        n_samples = len(X_val)
        
        # Calcular p(x|ω) * P(ω) para cada clase
        posteriors = np.zeros((n_samples, len(self.classes)))
        
        for i, c in enumerate(self.classes):
            likelihood = self._estimate_density(X_val, c)
            posteriors[:, i] = likelihood * self.priors[c]
        
        # Normalizar (aunque no es necesario para argmax)
        posteriors /= posteriors.sum(axis=1, keepdims=True) + 1e-10
        
        return np.argmax(posteriors, axis=1)

params_knn_density = [1, 3, 5, 7, 9, 11]

# Matriz para almacenar resultados: [hiperparámetro][fold] = (acc, f1, preds)
knn_d_results = {k: {'accuracies': [], 'f1_scores': [], 'all_preds': [], 'all_true': []} 
                 for k in params_knn_density}

print("\nEvaluando todos los hiperparámetros en cada fold...")
print("=" * 80)

# Para cada fold, evaluar todos los hiperparámetros
for fold, (train_val_idx, test_idx) in enumerate(skf.split(X, y), 1):
    print(f"\n--- Fold {fold}/5 ---")
    
    # Dividir en train+val y test
    X_train_val, X_test_fold = X.iloc[train_val_idx], X.iloc[test_idx]
    y_train_val, y_test_fold = y[train_val_idx], y[test_idx]
    
    # Evaluar cada hiperparámetro en este fold
    for k in params_knn_density:
        # Entrenar con este k
        knn_density = KNNDensityBayes(k=k)
        knn_density.fit(pd.DataFrame(X_train_val), y_train_val)
        
        # Evaluar en test del fold
        acc, f1, cm, preds = evaluate_fold(knn_density, pd.DataFrame(X_test_fold), y_test_fold, fold)
        
        # Guardar resultados para este hiperparámetro y fold
        knn_d_results[k]['accuracies'].append(acc)
        knn_d_results[k]['f1_scores'].append(f1)
        knn_d_results[k]['all_preds'].extend(preds)
        knn_d_results[k]['all_true'].extend(y_test_fold)
        
        print(f"  k={k}: Accuracy={acc:.4f}, F1-macro={f1:.4f}")

print("\n" + "=" * 80)
print("RESUMEN POR HIPERPARÁMETRO:")
print("=" * 80)

# Calcular promedios y encontrar el mejor
best_k_density = None
best_f1_mean = -np.inf

for k in params_knn_density:
    acc_mean = np.mean(knn_d_results[k]['accuracies'])
    acc_std = np.std(knn_d_results[k]['accuracies'])
    f1_mean = np.mean(knn_d_results[k]['f1_scores'])
    f1_std = np.std(knn_d_results[k]['f1_scores'])
    
    print(f"\nk={k}:")
    print(f"  Accuracy por fold: {[f'{a:.4f}' for a in knn_d_results[k]['accuracies']]}")
    print(f"  Accuracy: {acc_mean:.4f} ± {acc_std:.4f}")
    print(f"  F1-macro por fold: {[f'{f:.4f}' for f in knn_d_results[k]['f1_scores']]}")
    print(f"  F1-macro: {f1_mean:.4f} ± {f1_std:.4f}")
    
    if f1_mean > best_f1_mean:
        best_f1_mean = f1_mean
        best_k_density = k

print("\n" + "=" * 80)
print(f"✓ MEJOR HIPERPARÁMETRO: k={best_k_density}")
print(f"  F1-macro: {best_f1_mean:.4f} ± {np.std(knn_d_results[best_k_density]['f1_scores']):.4f}")
print("=" * 80)

# Usar los resultados del mejor hiperparámetro para el reporte final
knn_d_accuracies = knn_d_results[best_k_density]['accuracies']
knn_d_f1_scores = knn_d_results[best_k_density]['f1_scores']
knn_d_all_preds = knn_d_results[best_k_density]['all_preds']
knn_d_all_true = knn_d_results[best_k_density]['all_true']

knn_d_mean_acc, knn_d_mean_f1 = print_cv_results(f"k-NN Density Bayes (k={best_k_density})", 
                                                  knn_d_accuracies, knn_d_f1_scores,
                                                  knn_d_all_preds, knn_d_all_true)

# ============================================================================
# 9. MODELO 6: K-NN RULE (DIRECTO)
# ============================================================================

print("\n" + "=" * 80)
print("6. K-NEAREST NEIGHBORS RULE (Directo)")
print("=" * 80)

params_knn = [1, 3, 5, 7, 9, 11]

# Matriz para almacenar resultados: [hiperparámetro][fold] = (acc, f1, preds)
knn_results = {k: {'accuracies': [], 'f1_scores': [], 'all_preds': [], 'all_true': []} 
               for k in params_knn}

print("\nEvaluando todos los hiperparámetros en cada fold...")
print("=" * 80)

# Para cada fold, evaluar todos los hiperparámetros
for fold, (train_val_idx, test_idx) in enumerate(skf.split(X, y), 1):
    print(f"\n--- Fold {fold}/5 ---")
    
    # Dividir en train+val y test
    X_train_val, X_test_fold = X.iloc[train_val_idx], X.iloc[test_idx]
    y_train_val, y_test_fold = y[train_val_idx], y[test_idx]
    
    # Evaluar cada hiperparámetro en este fold
    for k in params_knn:
        # Entrenar con este k
        knn = KNeighborsClassifier(n_neighbors=k, metric='euclidean')
        knn.fit(X_train_val, y_train_val)
        
        # Evaluar en test del fold
        acc, f1, cm, preds = evaluate_fold(knn, X_test_fold, y_test_fold, fold)
        
        # Guardar resultados para este hiperparámetro y fold
        knn_results[k]['accuracies'].append(acc)
        knn_results[k]['f1_scores'].append(f1)
        knn_results[k]['all_preds'].extend(preds)
        knn_results[k]['all_true'].extend(y_test_fold)
        
        print(f"  k={k}: Accuracy={acc:.4f}, F1-macro={f1:.4f}")

print("\n" + "=" * 80)
print("RESUMEN POR HIPERPARÁMETRO:")
print("=" * 80)

# Calcular promedios y encontrar el mejor
best_k_knn = None
best_f1_mean = -np.inf

for k in params_knn:
    acc_mean = np.mean(knn_results[k]['accuracies'])
    acc_std = np.std(knn_results[k]['accuracies'])
    f1_mean = np.mean(knn_results[k]['f1_scores'])
    f1_std = np.std(knn_results[k]['f1_scores'])
    
    print(f"\nk={k}:")
    print(f"  Accuracy por fold: {[f'{a:.4f}' for a in knn_results[k]['accuracies']]}")
    print(f"  Accuracy: {acc_mean:.4f} ± {acc_std:.4f}")
    print(f"  F1-macro por fold: {[f'{f:.4f}' for f in knn_results[k]['f1_scores']]}")
    print(f"  F1-macro: {f1_mean:.4f} ± {f1_std:.4f}")
    
    if f1_mean > best_f1_mean:
        best_f1_mean = f1_mean
        best_k_knn = k

print("\n" + "=" * 80)
print(f"✓ MEJOR HIPERPARÁMETRO: k={best_k_knn}")
print(f"  F1-macro: {best_f1_mean:.4f} ± {np.std(knn_results[best_k_knn]['f1_scores']):.4f}")
print("=" * 80)

# Usar los resultados del mejor hiperparámetro para el reporte final
knn_accuracies = knn_results[best_k_knn]['accuracies']
knn_f1_scores = knn_results[best_k_knn]['f1_scores']
knn_all_preds = knn_results[best_k_knn]['all_preds']
knn_all_true = knn_results[best_k_knn]['all_true']

knn_mean_acc, knn_mean_f1 = print_cv_results(f"k-NN Rule (k={best_k_knn})", 
                                              knn_accuracies, knn_f1_scores,
                                              knn_all_preds, knn_all_true)

# ============================================================================
# 10. COMPARACIÓN FINAL DE TODOS LOS MODELOS
# ============================================================================

print("\n" + "=" * 80)
print("COMPARACIÓN FINAL DE MODELOS - CROSS VALIDATION 5-FOLD")
print("=" * 80)

# Compilar todos los resultados
results = {
    'Naive Bayes': {
        'acc_mean': np.mean(nb_accuracies),
        'acc_std': np.std(nb_accuracies),
        'f1_mean': np.mean(nb_f1_scores),
        'f1_std': np.std(nb_f1_scores)
    },
    'MLE Full': {
        'acc_mean': np.mean(mle_accuracies),
        'acc_std': np.std(mle_accuracies),
        'f1_mean': np.mean(mle_f1_scores),
        'f1_std': np.std(mle_f1_scores)
    },
    'Histogram Bayes': {
        'acc_mean': np.mean(hist_accuracies),
        'acc_std': np.std(hist_accuracies),
        'f1_mean': np.mean(hist_f1_scores),
        'f1_std': np.std(hist_f1_scores)
    },
    'Parzen Windows': {
        'acc_mean': np.mean(parzen_accuracies),
        'acc_std': np.std(parzen_accuracies),
        'f1_mean': np.mean(parzen_f1_scores),
        'f1_std': np.std(parzen_f1_scores)
    },
    'k-NN Density Bayes': {
        'acc_mean': np.mean(knn_d_accuracies),
        'acc_std': np.std(knn_d_accuracies),
        'f1_mean': np.mean(knn_d_f1_scores),
        'f1_std': np.std(knn_d_f1_scores)
    },
    'k-NN Rule': {
        'acc_mean': np.mean(knn_accuracies),
        'acc_std': np.std(knn_accuracies),
        'f1_mean': np.mean(knn_f1_scores),
        'f1_std': np.std(knn_f1_scores)
    }
}

print(f"\n{'Modelo':<25} {'Accuracy (mean±std)':>25} {'F1-macro (mean±std)':>25}")
print("-" * 80)
for model, metrics in results.items():
    acc_str = f"{metrics['acc_mean']:.4f} ± {metrics['acc_std']:.4f}"
    f1_str = f"{metrics['f1_mean']:.4f} ± {metrics['f1_std']:.4f}"
    print(f"{model:<25} {acc_str:>25} {f1_str:>25}")
print("-" * 80)

# Mejor modelo por F1-macro (prioridad para multiclass)
best_model = max(results, key=lambda k: results[k]['f1_mean'])
print(f"\n✓ Mejor modelo (por F1-macro promedio): {best_model}")
print(f"  F1-macro: {results[best_model]['f1_mean']:.4f} ± {results[best_model]['f1_std']:.4f}")

print("\n" + "=" * 80)
print("✓ Análisis completo finalizado con Cross-Validation 5-fold")
print("=" * 80)
