import pandas as pd
import numpy as np
import os
import warnings
from sklearn.model_selection import StratifiedKFold, GridSearchCV, cross_val_predict
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

# Silenciar warnings de joblib en Windows
os.environ['LOKY_MAX_CPU_COUNT'] = '4'
warnings.filterwarnings('ignore', category=UserWarning, module='joblib')

# Cargar datos
df = pd.read_csv('data.csv')
print("=" * 80)
print("INFORMACIÓN DEL DATASET")
print("=" * 80)
print(df.info())
print("\nDistribución de clases:")
print(df['Bankrupt?'].value_counts())
print(f"\nPorcentaje de bancarrotas: {df['Bankrupt?'].mean() * 100:.2f}%")

# Preparar datos
X = df.drop(columns=['Bankrupt?'])
y = df['Bankrupt?']

# Configurar validación cruzada estratificada
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

print("\n" + "=" * 80)
print("1. NAIVE BAYES GAUSSIANO")
print("=" * 80)

# Entrenar Naive Bayes con validación cruzada
nb = GaussianNB()
nb_preds = cross_val_predict(nb, X, y, cv=skf)

print("\nResultados de validación cruzada (5-fold):")
print(f"Accuracy: {accuracy_score(y, nb_preds):.4f}")
print("\nReporte de clasificación:")
print(classification_report(y, nb_preds))
print("Matriz de confusión:")
print(confusion_matrix(y, nb_preds))

# Entrenar modelo final con todos los datos
nb.fit(X, y)

print("\n" + "=" * 80)
print("2. K-NEAREST NEIGHBORS")
print("=" * 80)

# Búsqueda de hiperparámetros con GridSearchCV
print("\nBuscando mejor valor de k...")
params_knn = {'n_neighbors': [3, 5, 7, 9, 11, 15]}
grid_knn = GridSearchCV(
    KNeighborsClassifier(), 
    params_knn, 
    cv=skf, 
    scoring='f1_macro',
    n_jobs=-1
)
grid_knn.fit(X, y)

print(f"Mejor k encontrado: {grid_knn.best_params_['n_neighbors']}")
print(f"Mejor F1-score macro: {grid_knn.best_score_:.4f}")

# Evaluar mejor modelo con validación cruzada
best_knn = KNeighborsClassifier(n_neighbors=grid_knn.best_params_['n_neighbors'])
knn_preds = cross_val_predict(best_knn, X, y, cv=skf)

print("\nResultados de validación cruzada (5-fold):")
print(f"Accuracy: {accuracy_score(y, knn_preds):.4f}")
print("\nReporte de clasificación:")
print(classification_report(y, knn_preds))
print("Matriz de confusión:")
print(confusion_matrix(y, knn_preds))

# Entrenar modelo final con todos los datos
best_knn.fit(X, y)

print("\n" + "=" * 80)
print("COMPARACIÓN DE MODELOS")
print("=" * 80)
print(f"Naive Bayes - Accuracy: {accuracy_score(y, nb_preds):.4f}")
print(f"KNN (k={grid_knn.best_params_['n_neighbors']}) - Accuracy: {accuracy_score(y, knn_preds):.4f}")
print("=" * 80)
