# Memoria P2 – Fundamentos del Aprendizaje Automático

**Nombre:** Tu Nombre  
**ID:** Tu ID  
**Correo:** tu.email@dominio.com

## Introducción
He decidido realizar la práctica usando el dataset “Taiwanese Bankruptcy Prediction” porque corresponde a un problema clásico de clasificación binaria con fuerte desbalance y datos financieros reales. Presento el proceso completo detallando el preprocesado, particionado, implementación, optimización y resultados, explicando cada paso en primera persona e incluyendo los códigos utilizados.

## Dataset y Preprocesado
He descargado el dataset desde UCI. El conjunto tiene 6819 ejemplos y 95 variables (todo continuo y sin valores faltantes). Realizo el análisis exploratorio y compruebo el desbalance:

```python
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
print(df.info())
print(df['Bankrupt?'].value_counts())
print(f"\nPorcentaje de bancarrotas: {df['Bankrupt?'].mean() * 100:.2f}%")
```

## Particionado y Validación Cruzada
Realizo un particionado estratificado para mantener la proporción original entre clases y utilizo validación cruzada 5-fold. Es fundamental usar `cross_val_predict` para obtener predicciones correctas en validación cruzada:
```python
# Preparar datos
X = df.drop(columns=['Bankrupt?'])
y = df['Bankrupt?']

# Configurar validación cruzada estratificada
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
```

## Clasificadores
Comparo los siguientes métodos usando validación cruzada correctamente:
- Naive Bayes Gaussiano
- k-Nearest Neighbors (k-NN)

### Naive Bayes Gaussiano
Implemento el clasificador usando scikit-learn con validación cruzada. Utilizo `cross_val_predict` para obtener predicciones robustas sobre todos los datos manteniendo la separación train/test:
```python
# Entrenar Naive Bayes con validación cruzada
nb = GaussianNB()
nb_preds = cross_val_predict(nb, X, y, cv=skf)

print(f"Accuracy: {accuracy_score(y, nb_preds):.4f}")
print(classification_report(y, nb_preds))
print(confusion_matrix(y, nb_preds))

# Entrenar modelo final con todos los datos
nb.fit(X, y)
```

### k-Nearest Neighbors
Implemento el algoritmo k-NN siguiendo el mismo esquema de validación cruzada:
```python
# Evaluar con el mejor k encontrado
best_knn = KNeighborsClassifier(n_neighbors=k_optimo)
knn_preds = cross_val_predict(best_knn, X, y, cv=skf)

print(f"Accuracy: {accuracy_score(y, knn_preds):.4f}")
print(classification_report(y, knn_preds))
print(confusion_matrix(y, knn_preds))

# Entrenar modelo final con todos los datos
best_knn.fit(X, y)
```

## Optimización de Hiperparámetros
Utilizo GridSearchCV para optimizar el valor de k en k-NN. Es importante usar una métrica apropiada para datos desbalanceados como `f1_macro`:
```python
# Búsqueda de hiperparámetros con GridSearchCV
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
```

## Resultados
Recojo métricas de accuracy, precision, recall, F1-score y matriz de confusión para cada algoritmo usando validación cruzada. Las predicciones obtenidas con `cross_val_predict` garantizan que cada ejemplo se predice usando un modelo entrenado sin ese ejemplo:
```python
# Comparación final
print(f"Naive Bayes - Accuracy: {accuracy_score(y, nb_preds):.4f}")
print(f"KNN (k={grid_knn.best_params_['n_neighbors']}) - Accuracy: {accuracy_score(y, knn_preds):.4f}")
```

## Discusión y Conclusiones
Analizo el comportamiento de cada tipo de clasificador y justifico las diferencias en los resultados. El fuerte desbalance de clases (96.8% no quiebra vs 3.2% quiebra) afecta significativamente el rendimiento de los modelos.

He implementado correctamente la validación cruzada usando `cross_val_predict`, lo cual es crucial para evitar sobreajuste y obtener métricas realistas. En lugar de evaluar sobre todo el conjunto de datos (lo que daría resultados optimistas y engañosos), cada predicción se hace con un modelo que no ha visto ese ejemplo durante el entrenamiento.

Para k-NN, la optimización de hiperparámetros usando `f1_macro` como métrica es más apropiada que accuracy para datos desbalanceados, ya que balancea el rendimiento entre ambas clases. El mejor valor de k encontrado refleja el trade-off entre sesgo y varianza en este problema específico.

Ambos clasificadores muestran diferentes comportamientos frente al desbalance: Naive Bayes tiende a ser más conservador en sus predicciones de la clase minoritaria, mientras que k-NN puede capturar mejor patrones locales si el valor de k es apropiado.