# Redes Neuronales y Aprendizaje Profundo

## Bloque 1: Feedforward Neural Networks - From Shallow to Deep NN

### 1. Conceptos Básicos: Shallow vs Deep Neural Network
*   **Shallow Neural Network (Red Neuronal Superficial):**
    *   Consta de una capa de entrada (Input layer), una única capa oculta (Hidden layer) y una capa de salida (Output layer).
    *   Puede modelar relaciones simples.
*   **Deep Neural Network (Red Neuronal Profunda):**
    *   Consta de múltiples capas ocultas que procesan características jerárquicas.
    *   Permite aprender patrones complejos y abstracciones (ej. reconocimiento de imágenes).

---

## Objetivos del Tema

1.  Entender los fundamentos del **Perceptrón Multicapa (MLP)** o red neuronal superficial.
2.  Comprender el concepto de **"neurona básica"** y los términos:
    *   **Función de activación**.
    *   **Función de pérdida (Loss function)**.
    *   **Función de coste (Cost function)**.
3.  Entender el concepto de **Gradient Descent** (descenso de gradiente) mediante derivadas y la regla de la cadena.
4.  Comprender la **Propagación hacia adelante (Forward propagation)** y **hacia atrás (Backward propagation)** para buscar mínimos.
5.  Analizar las redes neuronales profundas y sus **hiperparámetros**.

---

## Fundamentos de Aprendizaje Supervisado

### Aprendizaje Supervisado vs No Supervisado
*   **Aprendizaje Supervisado:** Se proporciona un dataset con características (*features*) y etiquetas (*labels*). El modelo debe predecir las etiquetas a partir de las características.
*   **Aprendizaje No Supervisado:** El modelo recibe datos sin etiquetar para descubrir patrones sin guía explícita.

### Datasets: Entrenamiento, Test y Validación
1.  **Training dataset (Conjunto de entrenamiento):** Usado para entrenar el modelo. El modelo ajusta sus pesos internos basándose en estos datos. Es típicamente más grande que el de test.
2.  **Test dataset (Conjunto de prueba):** Usado para evaluar el rendimiento tras el entrenamiento. Contiene datos nunca vistos por el modelo para asegurar una evaluación imparcial.
3.  **Validation set (Conjunto de validación):** A veces usado entre entrenamiento y test para ajustar hiperparámetros (ej. tasa de aprendizaje) y evitar el *overfitting*.

### Error de Entrenamiento y Generalización
*   **Training error:** El error que el modelo comete sobre los datos de entrenamiento.
*   **Generalización error:** El error medido en datos nuevos no vistos (test/validación). Se estima aplicando el modelo a un conjunto de prueba independiente.

### Regresión Lineal y Clasificación
*   **Regresión Lineal:** Predice una salida continua basada en características de entrada (responde "¿cuánto?").
*   **Clasificación:** Responde a "¿qué categoría?".

### Cross Validation (Validación Cruzada)
*   Técnica usada cuando los datos de entrenamiento son escasos.
*   Los datos originales se dividen en subconjuntos no superpuestos. El entrenamiento y validación se ejecutan múltiples veces, entrenando en unos subconjuntos y validando en otro diferente en cada ronda.

---

## La Neurona Perceptrón

### Modelo Matemático
Una neurona calcula una suma ponderada de sus entradas más un sesgo, y aplica una función de activación:

\[ z = (\sum_{i=1}^{n} x_i \cdot w_i + b) \]
\[ a = \sigma(z) \]

*   \( x_i \): Características de entrada.
*   \( w_i \): Pesos (*weights*).
*   \( b \): Sesgo (*bias*).
*   \( \sigma \): Función de activación.

### Propósito del Bias (\( b \))
*   Permite expresar funciones lineales que no pasan necesariamente por el origen \((0,0)\).
*   Determina el valor de la estimación cuando todas las características son cero.

### Funciones de Activación
Deciden si una neurona debe activarse o no e introducen **no linealidades**, permitiendo al modelo aprender patrones complejos.

#### Funciones Comunes
1.  **Step (Escalón)**.
2.  **Sigmoid (Sigmoide):**
    \[ f(x) = \frac{1}{1+e^{-x}} \]
3.  **ReLU (Rectified Linear Unit):**
    \[ f(x) = \max(0, x) \]
4.  **pReLU (Parameterized ReLU):**
    \[ f(x) = \max(0, x) + \alpha \cdot \min(0, x) \]

---

## Redes Neuronales Profundas (Deep L-layer Neural Networks)

### Definiciones
*   **Shallow Neural Network:** Contiene solo una capa oculta. Solo puede modelar relaciones simples (si es perceptrón simple, solo lineales).
*   **Deep Neural Network:** Contiene 2 o más capas ocultas. Permite aprender patrones jerárquicos complejos.

### Hiperparámetros
Parámetros constantes fijados antes del proceso de aprendizaje:
*   Número de capas.
*   Número de neuronas por capa.
*   Tipo de función de activación.
*   Tipo de función de pérdida.
*   Método de optimización.
*   Tasa de aprendizaje (*Learning rate*).
*   Tamaño del lote (*Batch size*).

### Forward y Backward Propagation
*   **Forward propagation:** Cálculo y almacenamiento de variables intermedias desde la entrada hasta la salida.
*   **Back-propagation:** Recorre la red desde la salida hacia la entrada almacenando variables intermedias (derivadas parciales) según la regla de la cadena.

### Función de Pérdida y Coste
*   **Loss function (Pérdida):** Cuantifica la distancia entre el valor real y el predicho para **un solo ejemplo**.
*   **Cost function (Coste):** Promedia las pérdidas de todo el **conjunto de entrenamiento**.

#### Fórmulas Comunes
*   **Mean Absolute Error (Regresión):** \(\frac{1}{N} \sum |y_i - \hat{y}_i|\)
*   **Mean Square Error (Regresión):** \(\frac{1}{N} \sum (y_i - \hat{y}_i)^2\)
*   **Cross-entropy (Clasificación):** \(-\frac{1}{N} \sum (y_i \log(\hat{y}_i) + (1-y_i)\log(1-\hat{y}_i))\)

---

## Gradient Descent (Descenso de Gradiente)

Método para encontrar el mínimo de la función de pérdida \( L \) actualizando iterativamente los parámetros (\( w, b \)). Se mueve en la dirección marcada por las derivadas de \( L \).

### Regla de la Cadena (Chain Rule)
Base del método de **back-propagation**. Permite calcular la derivada parcial de la función de pérdida respecto a cada parámetro para su correcta actualización.

### Actualización de Parámetros
\[ \theta^{n+1} = \theta^n - \alpha \nabla L(\theta) \]
*   \( \theta^{n+1} \): Siguiente posición.
*   \( \theta^n \): Posición actual.
*   \( \alpha \): **Learning rate (Tasa de aprendizaje)**. Dimensión de los pasos dados hacia el mínimo.
*   \( \nabla L(\theta) \): Dirección del gradiente (máximo crecimiento).

### Epochs (Épocas)
Una iteración completa de entrenamiento del modelo sobre todo el dataset.

---

## Ejercicio de Backpropagation

**Ejercicio 1:** Calcular el Forward pass y Backward pass para la red propuesta.

**Datos:**
*   Entrada \( x = 1 \)
*   Pesos iniciales: \( W^{(L-2)} = 0.32 \), \( W^{(L-1)} = 0.18 \), \( W^{(L)} = 0.23 \)
*   Bias iniciales: \( b^{(L-2)} = 0 \), \( b^{(L-1)} = 0 \), \( b^{(L)} = 0 \)
*   Learning rate \( \alpha = 0.1 \)

**Fórmulas:**
*   Coste: \( L = C_0 = (\hat{y} - y)^2 \)
*   Sigmoide: \( \sigma(x) = \frac{1}{1+e^{-x}} \)
*   Derivada Sigmoide: \( \sigma'(x) = \sigma(x)(1 - \sigma(x)) \)
*   Entrada neurona: \( z^{(L)} = W^{(L)}a^{(L-1)} + b^{(L)} \)
*   Activación: \( a^{(L)} = \sigma(z^{(L)}) \)

**Objetivo:**
1.  Obtener las salidas (\( z, a \)) y la predicción.
2.  Actualizar \( W^{(L)} \) y \( b^{(L-1)} \) usando el gradiente.
