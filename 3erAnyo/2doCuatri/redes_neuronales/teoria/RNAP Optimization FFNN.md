# Redes Neuronales y Aprendizaje Profundo

## Bloque 1: Feedforward Neural Networks - Optimization

### Objetivos del Bloque
*   **Analizar fenómenos de Overfitting y Underfitting:** Entender cómo la complejidad del modelo afecta al rendimiento de la generalización.
*   **Investigar técnicas de regularización:** Prevenir una pobre generalización.
*   **Evaluar la Inicialización de Parámetros:** Mantener el flujo del gradiente y prevenir inestabilidad numérica en arquitecturas profundas.
*   **Entender Early Stopping:** Detener estratégicamente el proceso de optimización en el punto de máxima generalización.
*   **Explorar Quantization:** Mapear parámetros de alta precisión a espacios discretos para inferencia eficiente en dispositivos *edge*.

---

## 1. Overfitting y Underfitting

### Definiciones
*   **Overfitting (Sobreajuste):** El modelo aprende los datos de entrenamiento "demasiado bien" pero tiene una pobre generalización en la inferencia. Se ajusta al ruido local.
*   **Underfitting (Subajuste):** El modelo no aprende los datos de entrenamiento y pierde características y patrones clave, llevando a un pobre rendimiento tanto en entrenamiento como en test.

### Relación con Épocas (Epochs)
*   En el entrenamiento, si se usan **demasiadas épocas**, el modelo puede caer en **overfitting** con el dataset de entrenamiento.
*   Gráficamente:
    *   **Under-fitting:** Línea que no captura la tendencia (ej. lineal en datos curvos).
    *   **Appropriate-fitting:** Curva que sigue la tendencia general.
    *   **Over-fitting:** Curva excesivamente compleja que toca todos los puntos, incluyendo outliers.

### Soluciones Posibles
*   **K-fold cross-validation:** Validación cruzada.
*   **Data augmentation:** Aumento de datos.
*   **Model selection:** Selección de modelo adecuado.
*   **Hyperparameters selection:** Ajuste de hiperparámetros.

---

## 2. Técnicas de Regularización

### Dropout
*   Técnica de regularización para **prevenir overfitting**.
*   Funciona **desactivando aleatoriamente** (o haciendo "drop out") una fracción de neuronas durante el entrenamiento.
*   Fuerza al modelo a aprender características más robustas y generalizables, evitando que dependa excesivamente de neuronas específicas.

### Weight Decay (Decaimiento de Pesos)
*   Penaliza la suma de los pesos al cuadrado.
*   Previene que los pesos se vuelvan **demasiado grandes**, llevando a modelos más estables.
*   **Fórmula de actualización:**
    \[ w = (1 - \lambda)w - \alpha \Delta C_0 \]
*   Útil si no queremos que el modelo se centre en ruido local de nuevas entradas. Fuerza a la red a aprender solo características relevantes.

### Data Augmentation (Aumento de Datos)
*   Genera ejemplos **adicionales** y reduce el overfitting incrementando la **variabilidad** del dataset.
*   En datasets tabulares pequeños, se puede aplicar generando muestras con la misma distribución o añadiendo ruido.

### Early Stopping (Parada Temprana)
*   Un número muy alto de épocas puede reducir el error de entrenamiento pero **aumentar el error de generalización**.
*   **Estrategia:** Detener el entrenamiento cuando el error de generalización (validación) deja de bajar y empieza a subir, aunque el error de entrenamiento siga bajando.
*   Se busca el punto de "Generalization error" mínimo antes de que diverja del "Training set error".

---

## 3. Inicialización de Parámetros

La forma en que se inicializan los pesos influye en la convergencia y estabilidad del entrenamiento.

### Tipos de Inicialización

1.  **Zero Initialization (Inicialización a Cero):**
    *   Inicializa todos los pesos a 0.
    *   **Problema:** Todas las neuronas aprenden lo mismo (simetría no rota), impidiendo que la red aprenda características complejas.

2.  **Constant Initialization (Inicialización Constante):**
    *   Inicializa pesos con el mismo valor (distinto de 0).
    *   **Problema:** Tiene el mismo problema que la inicialización a cero.

3.  **Random Normal Initialization (Inicialización Aleatoria Normal):**
    *   Inicializa con valores aleatorios de una distribución Gaussiana.
    *   Ayuda a romper la simetría, pero puede llevar a gradientes que desvanecen o explotan si no se controla la varianza.

4.  **Xavier Initialization (Glorot):**
    *   Objetivo: Asegurar que los gradientes durante el entrenamiento no sean ni muy grandes ni muy pequeños.
    *   Ideal para funciones de activación como **Sigmoide** o **Tanh**.

5.  **He Initialization:**
    *   Optimizada para capas que usan función de activación **ReLU**.
    *   Mantiene la misma varianza para entradas y salidas en la red.

6.  **Lecun Initialization:**
    *   Optimizada para capas que usan funciones de activación **SELU**, **Sigmoide** o **Tanh**.

---

## 4. Quantization (Cuantización)

### Concepto
*   Técnica que **reduce la precisión** de los pesos y activaciones.
*   Ejemplo: Pasar de **Float32** (32 bits) a formatos más pequeños como **INT8** (8 bits).
*   **Ventaja:** Eficiencia. 8 bits = 1 byte, mientras que FP32 = 4 bytes. Reduce el uso de memoria y cómputo (hasta 32x más barato en teóricos extremos de 1-bit).
*   Estudios recientes (ej. "The Era of 1-bit LLMs") muestran buenos resultados incluso con cuantización agresiva (1.58 bits).

### Tipos de Cuantización
1.  **Post-Training Quantization (PTQ):** Cuantiza un modelo ya entrenado.
2.  **Quantization-Aware Training (QAT):** Simula la cuantización durante el entrenamiento para reducir la pérdida de precisión.
3.  **Weight Quantization:** Solo se reduce la precisión de los pesos.
4.  **Activation Quantization:** Se reduce la precisión de las activaciones.
5.  **Bias Quantization:** Cuantiza los sesgos (menos común).

### Ejercicio de Cuantización Simétrica Uniforme

**Ejercicio 1:** Calcular la cuantización para una entrada dada.

**Datos y Fórmulas:**
*   **Dominio:**
    *   \( n = 8 \) (número de bits).
    *   \( q \in \mathbb{Z} \) (valores cuantizados son enteros).
    *   \( q_{min} = -2^{n-1} \)
    *   \( q_{max} = 2^{n-1} - 1 \)

*   **Escala (Scale):**
    *   \( \alpha = \max(\text{abs}(x)) \) (valor absoluto máximo en datos originales).
    *   \( s = \frac{\alpha}{q_{max}} \) (factor de escala).

*   **Cuantización:**
    *   \( q = \text{round}(\frac{x}{s}) \) (redondear al entero más cercano).

**Entrada (Input):**
*   \( x = [1.23, -0.87] \)
