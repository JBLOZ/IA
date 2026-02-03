# FUNDAMENTOS DEL APRENDIZAJE AUTOMÁTICO - GUÍA COMPLETA DE ESTUDIO

## Tabla de Contenidos
1. [Tema 1: Introducción al Aprendizaje Automático](#tema-1-introducción-al-aprendizaje-automático)
2. [Tema 2: Aprendizaje Computacional](#tema-2-aprendizaje-computacional)
3. [Tema 3: Evaluación de Modelos](#tema-3-evaluación-de-modelos)
4. [Tema 4: Métodos no Paramétricos y Basados en Distancia](#tema-4-métodos-no-paramétricos-y-basados-en-distancia)
5. [Tema 5: Métodos Lineales y Perceptrón](#tema-5-métodos-lineales-y-perceptrón)
6. [Tema 6: Aprendizaje no Supervisado](#tema-6-aprendizaje-no-supervisado)
7. [Tema 7: Comparación Estadística de Modelos](#tema-7-comparación-estadística-de-modelos)

---

# TEMA 1: INTRODUCCIÓN AL APRENDIZAJE AUTOMÁTICO

## 1.1 Definición del Aprendizaje Automático

El **Aprendizaje Automático (Machine Learning)** es una disciplina que forma parte de la Inteligencia Artificial y se enfoca en el diseño de algoritmos capaces de **inferir conocimiento a partir de datos mediante medios computacionales**. Es un campo grounded en el razonamiento estadístico.

### Relación con otros campos:

| Campo | Definición | Subtemas |
|-------|-----------|----------|
| **Inteligencia Artificial** | Imitar la inteligencia/comportamiento inteligente humano | Puede usar reglas manuales |
| **Machine Learning** | Inferir conocimiento de datos automáticamente | Algoritmos que aprenden |
| **Pattern Recognition** | Detectar y categorizar patrones con características manuales | Enfoque en clasificación |
| **Deep Learning** | Aprender tanto características como relaciones con redes profundas | Redes neuronales profundas |

## 1.2 Etapas Conceptuales del Aprendizaje Automático

El proceso de ML atraviesa cuatro etapas conceptuales fundamentales:

### a) Fuente (Source)
- Datos capturados mediante sensores (fotografías, grabaciones, documentos escaneados)
- **Extracción de características (Feature Extraction)**: Obtención de descriptores adecuados para la tarea

### b) Conjunto de Datos (Dataset)
- Colección de elementos de la Fuente representados como descriptores
- Estructura: D = {(x₁, ω₁), ..., (xₙ, ωₙ)} con xᵢ ∈ Rᵈ

### c) Modelo (Model)
- Conocimiento extraído del Dataset usando un algoritmo de ML
- Representa patrones y relaciones en los datos

### d) Predicción (Prediction)
- Estimación sobre datos nuevos no vistos en etapas anteriores
- Aplicación práctica del modelo

## 1.3 Procesos Prácticos del Aprendizaje Automático

### Proceso de Entrenamiento
- **Objetivo**: Extraer conocimiento de los datos conocidos
- El modelo aprende patrones y relaciones
- Utiliza datos etiquetados

### Proceso de Prueba
- **Objetivo**: Explotar el conocimiento adquirido para nuevos datos
- Evalúa la capacidad de generalización
- Usa datos no vistos durante el entrenamiento

## 1.4 Estrategias de Representación de Características

### Representación Estadística (Feature-based)
- **Vector de características**: Cada elemento se representa como un vector de características numérico
- Estructura: `<peso, altura, color>`
- **Ventaja**: Todos los elementos tienen el mismo número de características
- **Limitación**: Capacidad de representación limitada

### Representación Estructural
- **Codificación de la estructura**: Se codifica la forma/estructura del objeto
- Estructura variable según el objeto: strings, árboles, grafos
- **Ventaja**: Generalmente logra mejor desempeño
- **Limitación**: Número limitado de algoritmos que pueden procesarlos

## 1.5 Taxonomía del Aprendizaje Automático

### Por tipo de tarea:

| Tipo | Descripción | Ejemplos |
|------|-------------|----------|
| **Clasificación** | Asignar elementos a clases predefinidas | Reconocimiento de dígitos, clasificación de emails |
| **Regresión** | Predecir valores continuos | Predicción de precios, pronóstico del tiempo |
| **Clustering** | Agrupar elementos similares | Segmentación de clientes |
| **Etiquetado de secuencias** | Etiquetar elementos en secuencias | Etiquetado de partes del discurso |

### Por tipo de aprendizaje:

| Enfoque | Datos | Objetivo |
|---------|-------|----------|
| **Supervisado** | D = {(xᵢ, ωᵢ)} (etiquetados) | Aprender P(ω\|x) |
| **No supervisado** | D = {xᵢ} (sin etiquetar) | Encontrar patrones/estructura |
| **Semi-supervisado** | Mezcla de datos etiquetados y sin etiquetar | Aprovechar ambos |

---

# TEMA 2: APRENDIZAJE COMPUTACIONAL

## 2.1 Definiciones Fundamentales

### Aprendizaje Computacional vs Teoría de Decisión

- **Aprendizaje Computacional**: Estudia los límites del aprendizaje a partir de datos
  - Qué se puede aprender y con qué eficiencia
  - También llamado "Statistical Learning Theory"

- **Teoría de Decisión**: Tomar decisiones óptimas bajo incertidumbre
  - Marco matemático fundamental para ML
  - Pattern Classification es su aplicación más importante

## 2.2 Teoría de Decisión Bayesiana

### Problema de Dos Clases

**Elementos básicos:**
- Estado de naturaleza (ω): Evento futuro no controlable
  - En nuestro caso: ω₁ (manzana) y ω₂ (pera)
  
- Probabilidad a priori P(ω): Probabilidad de observar cada clase sin evidencia adicional
  - Basada en datos históricos, región geográfica, estación, etc.

- **Regla de decisión inicial**: 
  ```
  ω = ω₁ si P(ω₁) > P(ω₂)
  ω = ω₂ si P(ω₁) < P(ω₂)
  ```

### Introducción de Información Adicional

Los diferentes frutos produce diferentes lecturas (ej: color)

- **Descriptor/Característica**: x ∈ ℝ (ejemplo: lectura de color)

- **Densidad de probabilidad condicional de la clase**: p(x|ω)
  - Probabilidad de observar el valor x dado que la clase es ω
  - Propiedad: ∫ p(x|ωᵢ) dx = 1 para cada i ∈ {1, 2}

### Probabilidad Conjunta

Si las variables son estadísticamente dependientes:
- p(ωⱼ, x) = P(ωⱼ|x) · p(x) = p(x|ωⱼ) · P(ωⱼ)

### Teorema de Bayes

La fórmula fundamental que relaciona todas estas probabilidades:

```
         p(x|ωⱼ) · P(ωⱼ)
P(ωⱼ|x) = ─────────────────
              p(x)
```

Donde:
- **P(ωⱼ|x)** = Probabilidad a posteriori (lo que queremos)
- **p(x|ωⱼ)** = Likelihood (verosimilitud)
- **P(ωⱼ)** = Probabilidad a priori
- **p(x) = Σⱼ p(x|ωⱼ) · P(ωⱼ)** = Evidencia (factor normalizador)

### Regla de Decisión Bayesiana

Elegir la clase con mayor probabilidad a posteriori:
```
ω* = arg max P(ω|x)
      ω∈W
```

## 2.3 Generalización de la Teoría de Decisión

### Espacio de características multidimensional
- x ∈ Rᵈ (vector de d características)

### Múltiples estados de naturaleza
- W = {ω₁, ω₂, ..., ω|W|} (conjunto finito de clases)

### Acciones más allá de clasificación
- A = {α₁, α₂, ..., α|A|} (conjunto de acciones posibles)
- Cada acción αᵢ: Rᵈ → W

### Función de Pérdida (Loss Function)
Generalización del concepto de error - no todos los errores son igual de importantes

- λ(αᵢ|ωⱼ): Costo de realizar acción αᵢ cuando el verdadero estado es ωⱼ

### Riesgo Condicional

Pérdida esperada para cada acción dado x:

```
         |W|
R(αᵢ|x) = Σ λ(αᵢ|ωⱼ) · P(ωⱼ|x)
         j=1
```

### Regla de Decisión de Bayes de Mínimo Riesgo

```
γ(x) = arg min R(αᵢ|x)
       αᵢ∈A
```

### Caso especial: Clasificación Binaria

Cuando A = {α₁, α₂} y W = {ω₁, ω₂} con función de pérdida simétrica:

**Razón de verosimilitud**:
```
p(x|ω₁)     λ₁₂ - λ₂₂      P(ω₂)
───────  >  ─────────  ·  ─────── = θ
p(x|ω₂)     λ₂₁ - λ₁₁      P(ω₁)
```

Esta razón es **independiente de x** - es solo un umbral fijo.

## 2.4 Estimación de Máxima Verosimilitud (MLE)

### Contexto

En la práctica no conocemos p(x|ω) y P(ω). Debemos **estimarlos** a partir de datos:

- **Dataset**: D = {D₁, ..., Dₖ} donde Dᵢ ~ p(x|ωᵢ)
- **Supuesto**: p(x|ωᵢ) tiene forma paramétrica conocida: p(x|ωᵢ, θᵢ)

### Concepto de Verosimilitud

Medida de qué tan probable es obtener exactamente este dataset dado los parámetros:

```
       |D|
p(D|θ) = ∏ p(xₙ|θ)
       n=1
```

(Asumiendo que las muestras son i.i.d.)

### Problema MLE

```
θ̂ = arg max p(D|θ) = arg max ln p(D|θ)
    θ                 θ
```

En práctica, se usa el logaritmo de la verosimilitud (log-likelihood):

```
l(θ) = ln p(D|θ)
```

### Solución (condiciones necesarias)

```
∇_θ l(θ) = 0
```

### Caso Gaussiano

Para distribuciones Gaussianas, la solución es analítica:

**Univariado**: x ∈ ℝ con θ = (μ, σ²)

```
         1  |D|
μ̂ = ──── Σ xₙ
       |D| n=1

         1  |D|
σ̂² = ──── Σ (xₙ - μ̂)²
       |D| n=1
```

**Multivariado**: x ∈ Rᵈ con θ = (μ, Σ)

```
         1  |D|
μ̂ = ──── Σ xₙ
       |D| n=1

         1  |D|
Σ̂ = ──── Σ (xₙ - μ̂)(xₙ - μ̂)ᵀ
       |D| n=1
```

## 2.5 Problemas en el Aprendizaje Computacional

### 2.5.1 Generalización y Error

**Generalización**: Qué tan bien un algoritmo predice en datos nuevos no vistos

- **Riesgo Verdadero** R(γ): Error esperado bajo la verdadera distribución P(x, ω)
  - Teórico, no computable

- **Riesgo Esperado** R_D(γ): Promedio sobre todos los posibles datasets D
  - Teórico, no computable

- **Riesgo Empírico** R̂(γ): Estimación usando datos finitos disponibles
  - Práctico, computable: R̂(γ) = (1/|D|) Σ L(γ(xᵢ), ωᵢ)

### 2.5.2 Descomposición Sesgo-Varianza

En problemas de regresión, el error se descompone en:

```
Error(x) = Bias² + Varianza + Ruido Irreducible
```

Donde:

- **Bias²**: Desviación sistemática del modelo respecto a la función verdadera
  - Indica underfitting (el modelo es demasiado simple)
  
- **Varianza**: Sensibilidad del modelo a cambios en los datos de entrenamiento
  - Indica overfitting (el modelo es demasiado complejo)

- **Ruido Irreducible (σ²ₑ)**: Error debido a la aleatoriedad inherente en los datos

### Dilema Sesgo-Varianza

```
    Error
      ↑
      │     Varianza
      │    /
      │   /
      │  / \ Sesgo
      │ /   \
      │/     \
      └───────────────────→ Complejidad del Modelo
      Complejidad Óptima
```

- **Underfitting**: Bajo sesgo pero alta varianza (modelo simple)
- **Overfitting**: Bajo sesgo pero alta varianza (modelo complejo)
- **Punto óptimo**: Balance entre sesgo y varianza

### 2.5.3 Maldición de la Dimensionalidad (Curse of Dimensionality)

**Problema**: Cuando aumenta el número de características d:

- Teóricamente: El estimador se beneficia de más características
- En práctica: Surgen problemas graves
  - **Escasez de datos**: Los datos se hacen cada vez más dispersos en espacios de mayor dimensión
  - **Riesgo severo de overfitting**: El modelo tiene demasiada libertad
  - **Aumento exponencial de complejidad**: Recursos computacionales crecen exponencialmente

**Estrategias de Mitigación:**

1. **Diseño adecuado de características**: Seleccionar features relevantes
2. **Selección de características**: Elegir un subconjunto d' < d
3. **Regularización del modelo**: Añadir restricciones/penalizaciones
4. **Reducción de dimensionalidad**: Proyectar a espacios de menor dimensión

---

# TEMA 3: EVALUACIÓN DE MODELOS

## 3.1 Introducción a la Evaluación

### Diferencia entre Pérdida y Métrica

- **Pérdida (Loss)**: Función usada durante entrenamiento
  - Guía el proceso de optimización
  - Facilita la optimización matemática
  
- **Métrica (Figure of Merit)**: Mide el desempeño real en el mundo
  - Refleja lo que realmente nos importa
  - Puede ser diferente a la pérdida

### Ejemplo: Predicción del Clima

Dos ingenieros con 365 días de datos (355 soleados, 10 lluviosos):

- **Ingeniero 1** (modelo bien diseñado):
  - Días soleados: 350 correctos, 5 incorrectos
  - Días lluviosos: 5 correctos, 5 incorrectos
  - Precisión = (350+5)/365 = 97%

- **Ingeniero 2** (siempre predice soleado):
  - Días soleados: 355 correctos, 0 incorrectos
  - Días lluviosos: 0 correctos, 10 incorrectos
  - Precisión = 355/365 = 97%

**Conclusión**: Ambos tienen 97% de precisión, pero el Ingeniero 2 es inútil. El problema es el desbalance de clases.

## 3.2 Principios Generales de Evaluación

### 3.2.1 Tipos de Riesgo/Error

**Riesgo Verdadero** R(γ):
```
R(γ) = E_(x,ω)~P(x,ω) [λ(γ(x)|ω)]
```
- Puramente teórico (no computable)

**Riesgo Esperado** R_D(γ):
```
R_D(γ) = E_(xᵢ,ωᵢ)∈D~P(x,ω) [λ(γ(xᵢ; D)|ωᵢ)]
```
- Promedio sobre todos los posibles datasets (no computable)

**Riesgo Empírico** R̂(γ):
```
R̂(γ) = (1/|D|) Σ_(xᵢ,ωᵢ)∈D λ(γ(xᵢ)|ωᵢ)
```
- Estimable a partir de datos finitos (COMPUTABLE)

### 3.2.2 Partición de Datos

**Problema**: Usar los mismos datos para entrenar, ajustar y evaluar → Data Leakage

**Solución**: Dividir D en subconjuntos disjuntos:

```
D = D_train ∪ D_validation ∪ D_test
(Disjuntos: D_train ∩ D_validation ∩ D_test = ∅)
```

| Subset | Propósito | Ratio típico |
|--------|-----------|-------------|
| **D_train** | Ajustar parámetros del modelo | 60-80% |
| **D_validation** | Ajustar hiperparámetros, selección de modelo | 10-20% |
| **D_test** | Evaluar desempeño final en datos no vistos | 10-20% |

**Consideraciones importantes:**
- D_train debe ser el mayor: Más datos para aprender
- Mantener estratificación (proporciones de clases) en cada subset
- Consideración de aleatorización en la división

## 3.3 Procedimientos de Validación Cruzada

### 3.3.1 Hold-out Validation (Validación de Retención)

- Simplest case: partición única fija en train, validation, test
- Error se computa solo una vez
- **Ventajas**: Rápido
- **Desventajas**: Alta varianza (dependiente de la división)

### 3.3.2 k-fold Cross-Validation

Divide los datos en k "pliegues" aproximadamente iguales:

1. Para cada pliegue i:
   - Usa k-1 pliegues para entrenar
   - Usa 1 pliegue para evaluar
2. Repite k veces (una por cada pliegue)
3. Reporta el promedio de los k errores

**Ventajas**:
- Reduce varianza respecto a hold-out
- Usa todos los datos para entrenamiento y validación

**Desventajas**:
- Ligero sesgo (D_train más pequeño que con hold-out)

### 3.3.3 Stratified k-fold Cross-Validation

Variante de k-fold que **preserva proporciones de clases** en cada pliegue
- Crucial cuando hay **desbalance de clases**

### 3.3.4 Leave-One-Out Cross-Validation (LOOCV)

Caso extremo: k = |D|

- Entrena con |D|-1 puntos
- Evalúa en 1 punto
- Repite |D| veces

**Ventajas**:
- Muy bajo sesgo (entrena con casi todo el dataset)

**Desventajas**:
- Muy alta varianza (cambios pequeños en datos afectan mucho)
- Computacionalmente muy costoso

### 3.3.5 Leave-p-out Cross-Validation

Generalización: deja p muestras fuera

- Número de iteraciones: (|D| choose p)
- Infactible para p > 1 en la mayoría de casos
- Usado principalmente en estudios teóricos

### Resumen de Estrategias

| Estrategia | Sesgo | Varianza | Coste |
|-----------|-------|----------|-------|
| Hold-out | Medio | Alto | 1 ajuste |
| k-fold | Bajo | Medio | k ajustes |
| LOOCV | Muy bajo | Alto | \|D\| ajustes |
| Leave-p-out | Muy bajo | Muy alto | (D choose p) ajustes |

## 3.4 Evaluación en Clasificación

### 3.4.1 Matriz de Confusión

Para problema binario W = {ω, ω̄}:

```
                Predicción
             ω      ω̄
Verdad    ω   TP    FN    |TP + FN|
          ω̄   FP    TN    |FP + TN|
```

Donde:
- **TP (True Positive)**: Predictor dice ω, verdad es ω
- **TN (True Negative)**: Predictor dice ω̄, verdad es ω̄
- **FP (False Positive)**: Predictor dice ω, verdad es ω̄ (falsa alarma)
- **FN (False Negative)**: Predictor dice ω̄, verdad es ω

### 3.4.2 Métricas de Clasificación Binaria

**1. Exactitud (Accuracy)**
```
       TP + TN
Acc = ─────────────────────
      TP + FN + TN + FP
```
- Proporción de predicciones correctas
- **Problema**: Penaliza igual falsos positivos y falsos negativos
- **Uso**: Escenarios balanceados

**2. Precisión (Precision)**
```
        TP
P = ─────────
    TP + FP
```
- De todas las predicciones positivas, cuántas son correctas
- **Penaliza**: Falsas alarmas
- **Uso**: Cuando los FP son costosos

**3. Exhaustividad (Recall)**
```
        TP
R = ─────────
    TP + FN
```
- De todos los casos positivos verdaderos, cuántos detectamos
- **Penaliza**: Casos perdidos
- **Uso**: Cuando los FN son costosos

**4. F-Medida (F-measure)**
```
           P · R
F1 = 2 · ─────────
         P + R
```
- Media armónica de Precision y Recall
- Equilibrio entre ambas métricas
- **Uso**: Cuando necesitamos un balance

### 3.4.3 Métricas Adicionales

**5. Tasa Positiva Verdadera (TPR - Sensibilidad)**
```
       TP
TPR = ─────────
      TP + FN
```

**6. Tasa Negativa Verdadera (TNR - Especificidad)**
```
       TN
TNR = ─────────
      TN + FP
```

**7. Tasa Falsa Positiva (FPR)**
```
       FP
FPR = ─────────
      FP + TN
```

**8. Tasa Falsa Negativa (FNR)**
```
       FN
FNR = ─────────
      FN + TP
```

**Propiedad importante**: TPR + FNR = 1 y TNR + FPR = 1

### 3.4.4 Curva ROC y AUC

**ROC Curve** (Receiver Operating Characteristic):
- Grafica FPR (eje x) vs TPR (eje y)
- Cada punto representa un umbral de decisión diferente
- **Punto ideal**: Esquina superior izquierda (FPR=0, TPR=1)
- **Diagonal**: Clasificación aleatoria

**AUC** (Area Under the Curve):
- Área bajo la curva ROC
- **Rango**: 0 a 1
  - AUC = 0.5: Clasificación aleatoria
  - AUC = 1.0: Clasificador perfecto
  - 0.5 < AUC < 1.0: Desempeño adecuado

**Ventajas**: Independiente del desbalance de clases, métrica libre de umbral

## 3.5 Evaluación en Clasificación Multiclase

### 3.5.1 Adaptaciones Necesarias

En multiclase (|W| > 2):
- Cada clase puede ser considerada como "positiva"
- Se aplica one-vs-all approach
- Metrics se calculan por clase

### 3.5.2 Estrategias de Promediado

**Micro-Average**:
```
         Σᵢ TPᵢ
Micro-P = ─────────────
         Σᵢ (TPᵢ + FPᵢ)
```
- Agrega a nivel de predicciones
- Favorece clases mayoritarias
- Equivalente a Accuracy global

**Macro-Average (con pesos)**:
```
          1   |W|
Macro-P = ─── Σ εᵢ · Pᵢ
         |W| i=1
```
Donde εᵢ = |Dᵢ|/|D| (con pesos) o εᵢ = 1 (sin pesos)
- Agrega a nivel de métricas
- Trata todas las clases igual (sin pesos)
- Destaca desempeño en clases minoritarias

## 3.6 Evaluación en Regresión

### 3.6.1 Error Medio Absoluto (MAE)

```
        1  |Dtest|
MAE = ─────  Σ |f̂(xᵢ) - ωᵢ|
      |Dtest| i=1
```
- Suma valores absolutos de errores
- Robusto a outliers

### 3.6.2 Error Cuadrático Medio (MSE)

```
        1  |Dtest|
MSE = ─────  Σ (f̂(xᵢ) - ωᵢ)²
      |Dtest| i=1
```
- Penaliza más los errores grandes
- Sensible a outliers
- En unidades cuadradas

### 3.6.3 Raíz del Error Cuadrático Medio (RMSE)

```
RMSE = √MSE
```
- En las mismas unidades que el objetivo
- Más interpretable que MSE

---

# TEMA 4: MÉTODOS NO PARAMÉTRICOS Y BASADOS EN DISTANCIA

## 4.1 Introducción a Métodos No Paramétricos

### Contexto: Aprendizaje Bayesiano Estadístico

Recuerdo del Tema 2:
```
        p(x|ω) · P(ω)
P(ω|x) = ──────────────
           p(x)
```

**Dos escenarios:**

1. **Estimar likelihoods p(x|ω) y priors P(ω)**
   - Clave: Estimación de densidad de probabilidad
   - Reconstruir p(x) sin asumir forma paramétrica

2. **Estimar posteriors P(ω|x) directamente**
   - Evita estimación de likelihood y prior
   - Métodos discriminativos

### Comparación: Paramétrico vs No Paramétrico

| Aspecto | Paramétrico (T2) | No Paramétrico (T4) |
|---------|------------------|-------------------|
| **Distribución** | Forma conocida (Gaussiana) | Sin asumir forma |
| **Supuestos** | Independencia estadística | Ninguno específico |
| **Estimación** | MLE | Histogramas, Parzen, kNN |
| **Módulo** | T2 | T4 |

## 4.2 Estimación de Densidad

### 4.2.1 Enfoque de Histogramas

**Principio**: Dividir el espacio en regiones y contar muestras

**Procedimiento**:
1. Dividir el espacio en regiones {R₁, ..., R_N}
2. Contar muestras en cada región: kⱼ = |{xᵢ : xᵢ ∈ Rⱼ}|
3. Estimar densidad: p̂(x|ω) = kⱼ / (|D| · V)

Donde V es el volumen de la región.

**Ejemplo - Peso masculino (|D| = 500 muestras)**:
- Rango [90, 95] kg contiene 23 muestras
- p̂(91 kg | hombre) = 23 / (500 · 5) = 0.0092

**Problemas**:
- Muy sensible a la resolución
- V pequeño → Estimación ruidosa (alta varianza, bajo sesgo)
- V grande → Estimación suave (bajo varianza, alto sesgo)
- Discontinua: cambios abruptos en los límites

### 4.2.2 Ventanas de Parzen

**Mejora del histograma**: Usar función kernel suave

**Formulación**:
```
         1     |D|       x - xᵢ
p̂(x|ω) = ─────  Σ K(───────)
        |D|·hᵈ  i=1       h
```

Donde:
- K(u): Función kernel
- h: Ancho de ventana (bandwidth)
- d: Dimensionalidad

**Funciones kernel comunes**:

1. **Rectangular**: K(u) = 1/2 si |u| ≤ 1, 0 en otro caso
2. **Triangular**: K(u) = 1 - |u| si |u| ≤ 1, 0 en otro caso
3. **Epanechnikov**: K(u) = (3/4)(1 - u²) si |u| ≤ 1, 0 en otro caso
4. **Gaussiano**: K(u) = (1/√(2π)) exp(-u²/2)

**Ventajas respecto a histogramas**:
- Suave y continuo
- Mejor manejo del sesgo-varianza

**Limitación principal**: h es fijo independientemente de x
- Densidad alta → ventana demasiado grande → sobresueño
- Densidad baja → ventana demasiado pequeña → subordsueño

### 4.2.3 Estimador k-Vecino Más Cercano

**Solución a la limitación de Parzen**: Fijar número de muestras k, dejar variar el volumen

**Formulación**:
```
         k
p̂(x|ω) = ──────────
         |D| · V(x)
```

Donde V(x) es el volumen requerido para incluir k muestras más cercanas a x

**Ventajas**:
- Adapta el ancho de ventana localmente
- Buen balance sesgo-varianza

## 4.3 Regla del Vecino Más Cercano

### 4.3.1 Formulación

Dado una consulta q = (xq, ωq), asignar la etiqueta del vecino más cercano:

```
ω̂q = ωᵢ : arg min D(xq, xᵢ)
          1≤i≤|T|
```

Donde D: ℝᵈ × ℝᵈ → ℝ es una función de distancia/similitud

**Características principales**:
- Solo requiere definir una medida de (dis)similitud
- Útil para representaciones feature-based y estructurales
- No deriva modelo explícito del entrenamiento
  - Ventaja: Adaptativo
  - Desventaja: Ineficiente para datasets grandes

### 4.3.2 Teselación de Voronoi

La regla NN divide el espacio en regiones Voronoi:

```
Vᵢ = {x ∈ ℝᵈ : D(x, xᵢ) ≤ D(x, xⱼ) ∀j ≠ i}
```

**Interpretación**: Cualquier punto en Vᵢ es más cercano a xᵢ que a cualquier otro punto

### 4.3.3 Análisis de Error

**Caso binario** (W = {ω₁, ω₂}):

Con infinitas muestras, la probabilidad de error de NN es:

```
R_NN(x) = 2P(ω₁|x) · P(ω₂|x) = 2P(ω₁|x)[1 - P(ω₁|x)]
```

**Cota de error para NN**:
```
R* ≤ R_NN ≤ 2R*(1 - R*)
```

Donde R* es el riesgo de Bayes (óptimo)

**Caso multiclase**:
```
R* ≤ R_NN ≤ R*[2 - (c/(c-1))R*]
```

Conclusión: Error de NN está acotado por el doble del error óptimo (en el peor caso)

### 4.3.4 Métricas de Distancia

Las reglas de distancia requieren métrica o medida de similitud

**Propiedades de una métrica**:
1. No-negatividad: D(a, b) ≥ 0
2. Reflexividad: D(a, b) = 0 sii a = b
3. Simetría: D(a, b) = D(b, a)
4. Desigualdad triangular: D(a, b) + D(b, c) ≥ D(a, c)

**Distancia de Minkowski** (unifica muchas métricas):

```
           d
D(a, b) = [Σ |aᵢ - bᵢ|ᵖ]^(1/p)    con p ≥ 1
          i=1
```

**Casos especiales**:
- p = 1: Distancia Manhattan (suma de diferencias absolutas)
- p = 2: Distancia Euclidiana (raíz cuadrada de suma de cuadrados)
- p = ∞: Distancia de Chebyshev (máxima diferencia)

### 4.3.5 Regla del k-Vecino Más Cercano (k-NN)

**Generalización**: Considerar los k vecinos más cercanos en lugar de solo uno

**Procedimiento**:
1. Encontrar los k puntos más cercanos a xq
2. Contar votos por clase entre esos k puntos
3. Asignar la clase con más votos

**Ventajas sobre NN**:
- Más robusto a ruido
- Mejora la estabilidad

**Desventajas**:
- Requiere seleccionar k (hiperparámetro)
- Más costo computacional (buscar k vecinos)

## 4.4 Otros Modelos: Árboles de Decisión y SVM

### 4.4.1 Árboles de Decisión

**Estructura**: Árbol donde:
- Nodos internos: Tests sobre features
- Ramas: Resultados de tests
- Hojas: Predicciones (clases)

**Ejemplo - Clasificar género por peso y altura**:
```
            Altura ≥ 200 cm?
           /              \
         Sí                No
        / \              /    \
    Macho  Macho    Peso ≤ 80 kg?
                      /      \
                     Sí        No
                   Mujer     Hombre
```

**Ventajas**:
- Interpretable (decisiones transparentes)
- Maneja features categóricas naturalmente
- Sin necesidad de normalización

**Desventajas**:
- Tendencia a overfitting
- Complejidad computacional para búsqueda óptima

### 4.4.2 Máquinas de Vectores de Soporte (SVM)

**Concepto**: Clasificador lineal binario usando hiperplano separador

**Características principales**:
- Usa hiperplano para separar clases
- Vectores de soporte: Elementos que definen el hiperplano (los más cercanos al límite)
- Margen: Distancia entre hiperplano y puntos más cercanos
- Objetivo: Maximizar margen (robusto contra perturbaciones)

**Kernel**: Transforma datos a espacio de mayor dimensión
- Permite encontrar fronteras de decisión no-lineales
- Kernels comunes: lineal, polinómico, RBF

**Adaptaciones multiclase**:
- One-vs-All: |W| clasificadores binarios
- One-vs-One: |W|(|W|-1)/2 clasificadores binarios

---

# TEMA 5: MÉTODOS LINEALES Y PERCEPTRÓN

## 5.1 Modelos Lineales

### 5.1.1 Función Discriminante Lineal Binaria

**Modelo más simple**: Salida es combinación lineal de entrada

**Caso binario** (W = {ω₁, ω₂}):
```
g(x) = θᵀx + θ₀

x ∈ ℝᵈ:     Vector de características
θ ∈ ℝᵈ:     Vector de pesos
θ₀ ∈ ℝ:     Bias/threshold
```

**Regla de decisión**:
- Si g(x) > 0 → Región R₁ → ω̂ = ω₁
- Si g(x) < 0 → Región R₂ → ω̂ = ω₂

**Superficie de decisión**: H donde g(x) = 0 (hiperplano d-1 dimensional)

**Interpretación geométrica**:
- Vector θ: Normal a la superficie H, define orientación
- Bias θ₀: Desplaza H a lo largo de θ

### 5.1.2 Extensión a Multiclase

**Generalización**: Un clasificador por clase

```
gk(x) = θkᵀx + θ0k    para k = 1, 2, ..., |W|
```

**Regla de decisión**:
```
ω̂ = arg max gk(x)
     k=1,...,|W|
```

**Superficies de decisión**: Hiperplanos definidos por pares de clases
```
gᵢ(x) = gⱼ(x)  ⟹  (θᵢ - θⱼ)ᵀx + (θ0ᵢ - θ0ⱼ) = 0
```

## 5.2 Estimación de Parámetros

### 5.2.1 Problema de Optimización

**Dado**: Dataset D = {(xᵢ, ωᵢ)}

**Objetivo**: Minimizar discrepancia entre predicciones y verdad

```
min J(θ) = min  1    Σ L(g(xᵢ; θ), ωᵢ)
 θ         θ  |D| i=1
```

Donde L es una función de pérdida

**Solución**:
- En algunos casos: Analítica (ecuación cerrada)
- En general: Iterativa (optimización numérica)

### 5.2.2 Descenso por Gradiente

**Algoritmo iterativo para minimización**:

```
θ₀ = arbitrario
θ(k+1) = θ(k) - η(k) ∇J(θ(k))

Hasta convergencia: ||η(k) ∇J(θ(k))|| < δ
```

Donde:
- η(k): Tasa de aprendizaje (learning rate)
  - Valores típicos: Constante o η(k) = η₀/k
- ∇J(θ): Gradiente de la función objetivo

**Interpretación**:
1. Calcular gradiente (dirección de máximo aumento)
2. Mover en dirección opuesta (descenso)
3. Repetir hasta convergencia

**Ejemplo**:
- Función: J(θ) = (θ - 3)²
- θ₀ = -2, η = 0.1
- Iteraciones: θ se mueve hacia 3

## 5.3 El Perceptrón

### 5.3.1 Introducción

**Histórico**: Introducido por Rosenblatt en 1958

**Idea**: Envolver modelo lineal en función escalón para clasificación

**Estructura**:
```
         ⎧ ω₁  si g(x) > 0
ω̂ = ⎨
         ⎩ ω₂  si g(x) < 0
```

Es un clasificador lineal binario práctico.

### 5.3.2 Entrenamiento del Perceptrón

**Función de pérdida del Perceptrón**:
- Penaliza solo muestras mal clasificadas
- Intuitivo: Los puntos bien clasificados no importan

**Algoritmo**:
```
Inicializar θ
Mientras existan muestras mal clasificadas:
    Para cada muestra (xᵢ, ωᵢ):
        Si g(xᵢ; θ) · ωᵢ ≤ 0 (mal clasificado):
            θ = θ + η · ωᵢ · xᵢ
```

**Propiedades**:
- Converge para datos linealmente separables
- No converge para datos no separables

### 5.3.3 Limitaciones

**Problema principal**: Solo puede aprender funciones linealmente separables

**Ejemplo clásico - XOR**:
```
Entrada       Salida
(0, 0) → 0
(0, 1) → 1
(1, 0) → 1
(1, 1) → 0
```

No existe hiperplano que separe correctamente (puntos no son linealmente separables)

### 5.3.4 Perceptrón Multiclase

**Extensiones a multiclase**:

1. **One-VS-Rest**:
   - Usa |W| perceptrones
   - Perceptrón con mayor activación determina clase

2. **One-VS-One**:
   - Usa |W|(|W|-1)/2 perceptrones
   - Clase estimada por votación

3. **Múltiples vectores de peso**:
   - Un solo perceptrón con matriz θ
   - Un vector por clase
   - Actualizar solo vector de clase durante entrenamiento

## 5.4 Perceptrón Multicapa (MLP)

### 5.4.1 Introducción

**Motivación**: Superar limitación de separabilidad lineal del Perceptrón

**Idea fundamental**:
- Stack de unidades Perceptrón
- Aproximar funciones no-lineales
- Caso especial de Feedforward Neural Networks

**Teorema de Aproximación Universal**:
> Una red neuronal feedforward con al menos una capa oculta, usando activaciones no-lineales, puede aproximar cualquier función continua con exactitud arbitraria, dado suficientes neuronas en la capa oculta.

### 5.4.2 Arquitectura de MLP

**Capas**:

1. **Capa de Entrada**:
   - d neuronas (dimensionalidad de x)
   - Entrada al modelo

2. **Capas Ocultas**:
   - I capas
   - Jᵢ neuronas en capa i-ésima
   - Activaciones no-lineales
   - Completamente conectadas

3. **Capa de Salida**:
   - m neuronas
   - Configuración depende de la tarea
   - Para clasificación: |W| neuronas (una por clase)

### 5.4.3 Funciones de Activación

Las activaciones no-lineales son críticas para la aproximación universal

**Sigmoid**:
```
σ(x) = 1 / (1 + e^(-x))
```
- Rango: (0, 1)
- Diferenciable
- Problema: Saturación en extremos

**Tanh (Tangente Hiperbólica)**:
```
σ(x) = (e^x - e^(-x)) / (e^x + e^(-x))
```
- Rango: (-1, 1)
- Media cero (mejor para redes profundas)

**ReLU (Rectified Linear Unit)**:
```
σ(x) = max{0, x}
```
- Computacionalmente eficiente
- Mitiga vanishing gradients
- Problema: Dead neurons

**Leaky ReLU**:
```
σ(x) = ⎧ x        si x ≥ 0
        ⎩ α·x      si x < 0    (α ∈ [0.1, 0.3])
```
- Soluciona dead neurons
- Gradientes negativos pequños pero no cero

### 5.4.4 Capa de Salida

**Para Regresión**:
- Un regresor por unidad de salida
- Activación lineal típica

**Para Clasificación**:
- Una unidad por clase (m = |W|)
- Salida cruda o probabilidades

**Softmax (para probabilidades)**:
```
P̂(ω|x) = e^(yω) / Σ_j e^(yj) ∈ [0, 1]
```
- Convierte salidas a distribución de probabilidad
- Suma a 1

### 5.4.5 Entrenamiento de MLP

**Forward-Backward Propagation**:

1. **Forward Pass**:
   - Dato x pasa por red input → output
   - Pesos θ modifican x en cada capa

2. **Pérdida Computation**:
   - Comparar estimación ŷ con verdad y
   - Regresión: MAE, MSE
   - Clasificación: Categorical Cross Entropy

3. **Backward Pass (Backpropagation)**:
   - Calcular gradiente ∂Loss/∂θ
   - Usar regla de cadena para derivadas anidadas
   - Propagar gradientes output → input

4. **Weight Update**:
   - Actualizar parámetros
   - Métodos: SGD, Momentum, RMSProp, Adam

**Pérdida Categorical Cross Entropy** (clasificación):
```
L(y, ŷ) = -Σ_j yⱼ·log(ŷⱼ)
```

Donde y es one-hot encoding: [0, 1, 0, ...] para clase 2 de 3

### 5.4.6 Consideraciones Prácticas

**Problemas comunes**:

1. **Overfitting**: Memorizar datos vs generalizar

2. **Vanishing Gradients**: Gradientes se hacen muy pequeños
   - Acumulación de derivadas en chain rule
   - Especialmente en redes profundas

3. **Exploding Gradients**: Lo opuesto - gradientes muy grandes

**Estrategias de Regularización**:

- **L1/L2 Regularization**: Penalidades en pesos
  ```
  J_total = J_original + λ·||θ||_p
  ```

- **Dropout**: Desconectar neuronas aleatoriamente durante entrenamiento
  - Previene co-adaptación

- **Early Stopping**: Parar cuando validation loss aumenta
  - Indica overfitting

- **Data Augmentation**: Expandir dataset artificialmente
  - Aplicar transformaciones a datos

**Prevención de Vanishing/Exploding Gradients**:

- **Activaciones**: ReLU/Leaky ReLU vs Sigmoid/Tanh

- **Inicialización de Pesos**: Xavier, He initialization

- **Batch/Layer Normalization**: Mantener activaciones en rangos estables

- **Gradient Clipping**: Limitar magnitud del gradiente

---

# TEMA 6: APRENDIZAJE NO SUPERVISADO

## 6.1 Introducción al Aprendizaje No Supervisado

### Diferencia con Aprendizaje Supervisado

| Aspecto | Supervisado | No Supervisado |
|--------|------------|-----------------|
| **Datos** | D = {(xᵢ, ωᵢ)} | D = {xᵢ} |
| **Meta** | Aprender P(ω\|x) | Encontrar estructura/patrones |
| **Guía** | Etiquetas disponibles | Sin etiquetas |
| **Validación** | Métricas de error | Métricas internas/externas |

### Tareas Principales

1. **Clustering**: Agrupar datos similares
   - Identificar/caracterizar patrones
   - Ejemplo: Segmentación de clientes

2. **Dimensionality Reduction**: Representaciones compactas
   - Reducir complejidad
   - Visualización
   - Ejemplo: PCA, t-SNE

3. **Anomaly/Outlier Detection**: Identificar elementos anómalos
   - Remover ruido
   - Detectar comportamientos inesperados
   - Ejemplo: Detección de fraude

## 6.2 Clustering

### 6.2.1 Definición

**Objetivo**: Dividir conjunto D en C = {C₁, ..., C_|C|} clusters

Propiedades:
- Cobertura: ∪|C|_j=1 Cⱼ = D (cubre todos los datos)
- Política de división depende de definición de cluster

### 6.2.2 Taxonomía de Clustering

**Partitional Clustering**:
- Estructura plana (sin jerarquía)
- Genera clusters para recuperar grupos naturales
- Ejemplo: k-means

**Hierarchical Clustering**:
- Estructura jerárquica (dendrograma)
- Árbol que muestra cómo se agrupan elementos
- Dos enfoques:
  - **Top-down (Divisive)**: Partir grandes clusters
  - **Bottom-up (Agglomerative)**: Fusionar clusters pequeños

**Partitional Clustering - Subtipología**:

1. **Hard Clustering**: Asignación exclusiva a un cluster
2. **Mixture Resolving**: Probabilística (soft assignment)
3. **Fuzzy Clustering**: Membresía difusa a múltiples clusters

### 6.2.3 Algoritmo k-means

**Objetivo**: Particionar D en k clusters minimizando varianza intra-cluster

**Algoritmo de Lloyd** (iterativo):

```
1. Inicializar centroides μ₁, ..., μ_k

2. Repetir hasta convergencia:
   
   a) Asignación (Assignment Step):
      Asignar cada xᵢ al cluster con centroide más cercano
      Cⱼ = {xᵢ ∈ D : arg min_(1≤m≤k) d(xᵢ, μm)}
   
   b) Actualización (Update Step):
      Recalcular centroides
      μⱼ = (1/|Cⱼ|) · Σ_(x∈Cⱼ) x
```

**Criterio de Convergencia**: WCSS (Within-Cluster Sum of Squares)

```
        k   
WCSS = Σ  Σ  d(x, μⱼ)²
       j=1 x∈Cⱼ
```

**Propiedades**:
- Converge localmente (puede quedar en mínimo local)
- Sensible a inicialización
- Complejidad: O(nkdI) donde I es número de iteraciones

### 6.2.4 Inicialización de k-means

**k-means clásico**:
- Selecciona k puntos aleatorios de D como centroides iniciales
- **Problema**: Sensible a inicialización

**k-means++**:
- Selecciona primer centroide aleatoriamente
- Selecciona siguientes centroides lejos de centroides existentes
- Probabilidad proporcional a distancia cuadrada
- **Ventaja**: Reduce sensibilidad a inicialización

### 6.2.5 Consideraciones sobre k-means

**Ventajas**:
- Maneja representaciones feature-based y estructurales
- Solo requiere métrica de distancia
- Relativamente eficiente

**Desventajas**:
- Operador de media es sensible a outliers
- **Alternativa**: k-Medoids (usa elemento más cercano a media)

### 6.2.6 Determinación del Número de Clusters

**Problema**: ¿Cuántos clusters hay en los datos?

#### Método del Codo (Elbow Method)

**Procedimiento**:
1. Ejecutar k-means para k = 2, 3, 4, ..., k_max
2. Graficar k vs WCSS
3. Identificar "codo" (cambio de pendiente)
4. El codo sugiere k óptimo

**Interpretación**:
- WCSS disminuye con k (más clusters = menos varianza)
- Después del codo: mejoras pequeñas (overfitting)
- Antes del codo: mejoras significativas (estructura real)

#### Método de Silueta (Silhouette Method)

Mide qué tan bien cada punto cabe en su cluster vs otros clusters

**Para punto xm en cluster Cⱼ**:

1. **Cohesión** a(xm):
   ```
   a(xm) = (1/(|Cⱼ|-1)) · Σ_(xn∈Cⱼ, xm≠xn) d(xm, xn)
   ```
   Distancia promedio dentro del cluster

2. **Separación** b(xm):
   ```
   b(xm) = min_(l≠j) (1/|Cₗ|) · Σ_(xn∈Cₗ) d(xm, xn)
   ```
   Distancia mínima promedio a otros clusters

3. **Coeficiente de Silueta**:
   ```
   s(xm) = (b(xm) - a(xm)) / max{a(xm), b(xm)}
   ```
   Rango: [-1, 1]
   - +1: Bien colocado (lejos de otros clusters)
   - 0: En el límite
   - -1: Mal colocado (mejor en otro cluster)

**Decisión**: Elegir k que maximiza silhouette promedio

## 6.3 Reducción de Dimensionalidad

### 6.3.1 Motivación: Maldición de la Dimensionalidad

Cuando d (número de features) es grande:
- Datos se vuelven escasos en espacio de alta dimensión
- Riesgo severo de overfitting
- Complejidad computacional aumenta

**Soluciones**:
1. **Selección de características**: Elegir subset d' < d
2. **Extracción de características**: Proyectar a d' < d
3. **Reducción de dimensionalidad**: Representación compacta

### 6.3.2 Análisis de Componentes Principales (PCA)

**Tipo**: Proyección lineal de Rᵈ a Rᵈ'

**Objetivo**: Encontrar direcciones que capturen la máxima varianza

**Idea Intuitiva**:
- Datos varían mucho en algunas direcciones
- Poco varían en otras
- Mantener direcciones de alta varianza

**Formulación Matemática**:

**Entrada**: D = {xᵢ}|D|_i=1 con xᵢ ∈ Rᵈ

**Preprocesado**: Centrar datos (media cero por columna)

**Matriz de covarianza**:
```
Σ = (1/(|D|-1)) · DᵀD
```

**Principales componentes**: Eigenvectores de Σ

**Primer eigenvector v₁**:
```
v₁ = arg max_(||v||=1) vᵀΣv
```
(Dirección de máxima varianza)

**Segundo eigenvector v₂**:
```
v₂ = arg max_(||v||=1, v⊥v₁) vᵀΣv
```
(Máxima varianza ortogonal a v₁)

**Posteriores**: Continuar ortogonales a anteriores

**Proyección**:
```
x_proj = x · V
```
Donde V = [v₁, ..., v_d'] ∈ Rᵈˣᵈ'

**Varianza Acumulada**:
```
        Σᵈ'ᵢ₌₁ λᵢ
CumVar(d') = ───────
             Σᵈⱼ₌₁ λⱼ
```

Donde λⱼ = vʲᵀΣvʲ es la varianza en dirección j

**Interpretación**: Qué fracción de información original se retiene

### 6.3.3 t-SNE (t-Stochastic Neighbor Embedding)

**Tipo**: Proyección no-lineal a Rᵈ' (típicamente 2D o 3D)

**Uso Principal**: Visualización

**Objetivo Principal**: Preservar vecindades locales
- Puntos cercanos en Rᵈ permanecen cercanos en Rᵈ'
- Estructura global puede distorsionarse

**Enfoque**:
1. Distribucion P: Similitudes en espacio original
2. Distribución Q: Similitudes en espacio proyectado
3. Minimizar divergencia KL(P||Q)

**Ventajas**:
- Excelente visualización
- Preserva estructura local

**Desventajas**:
- Computacionalmente costoso
- Estructura global puede no preservarse
- No apto para proyecciones predictivas

---

# TEMA 7: COMPARACIÓN ESTADÍSTICA DE MODELOS

## 7.1 Pruebas de Hipótesis Estadísticas

### 7.1.1 Conceptos Fundamentales

**Hipótesis Nula (H₀)**: Afirmación sobre población
- Ejemplo: "No hay diferencia entre modelos"

**Hipótesis Alternativa (H₁)**: Negación de H₀
- Ejemplo: "Hay diferencia entre modelos"

**Nivel de Significancia (α)**: Umbral para rechazar H₀
- Valores típicos: 0.05, 0.01
- Probabilidad de rechazar H₀ siendo verdadera (error tipo I)

**p-valor**: Probabilidad de obtener resultados tan extremos asumiendo H₀

**Decisión**:
- Si p-valor < α: Rechazar H₀ (diferencia significativa)
- Si p-valor ≥ α: No rechazar H₀ (diferencia no significativa)

## 7.2 Comparación Pairwise (Dos Modelos)

### 7.2.1 Prueba t-Pareada

Compara dos modelos sobre múltiples datasets

**Escenario**:
- Modelos f₁, f₂
- Múltiples conjuntos de datos D₁, ..., D_M
- Métrica de desempeño evaluada en cada conjunto

**Procedimiento**:
1. Calcular diferencias: dᵢ = Perf_f₁(Dᵢ) - Perf_f₂(Dᵢ)
2. Calcular media: d̄ = (1/M) Σ dᵢ
3. Calcular desviación estándar: s = √[(1/(M-1)) Σ (dᵢ - d̄)²]
4. Estadístico t: t = d̄ / (s/√M)
5. Comparar con valor crítico t_{α,M-1}

**Supuestos**:
- Diferencias siguen distribución normal
- Muestras independientes

### 7.2.2 Prueba de Wilcoxon Signed-Rank

**Tipo**: No-paramétrica (sin supuesto de normalidad)

**Basada en**: Ranking de valores absolutos de diferencias

**Ventaja**: Más robusta que prueba t
- No requiere normalidad
- Usa información de rangos (más robusta a outliers)

## 7.3 Comparación Múltiple (3+ Modelos)

### 7.3.1 Motivación

**Problema con comparaciones pairwise**:
- Si comparamos C modelos: (C choose 2) = C(C-1)/2 tests
- Hacer muchos tests aumenta probabilidad de errores falsos positivos

**Solución**: Tests diseñados para múltiples comparaciones simultáneamente

### 7.3.2 ANOVA (Analysis of Variance)

**Tipo**: Paramétrico

**Objetivo**: Analizar si 3+ modelos difieren significativamente en desempeño promedio

**Hipótesis Nula (H₀)**: Todas las medias poblacionales son iguales

**Test**: F-test

**Supuestos**:
- Mediciones siguen distribución normal
- Independencia entre observaciones

**Procedimiento**:
1. Calcular varianza entre grupos
2. Calcular varianza dentro de grupos
3. F = Var_entre / Var_dentro
4. Comparar con valor crítico F_{α,C-1,M·C-C}

### 7.3.3 Prueba de Friedman

**Tipo**: No-paramétrica (alternativa a ANOVA)

**Basada en**: Ranking (como Wilcoxon pero para múltiples)

**Supuesto**: Paired measurements

**Hipótesis Nula (H₀)**: No hay diferencias entre modelos

**Procedimiento**:

1. **Ranking** para cada dataset:
   - Ordenar modelos f₁, ..., f_C de mejor a peor
   - Asignar rangos 1 (mejor) a C (peor)

2. **Promedio de rangos** por modelo:
   ```
   R̄ⱼ = (1/M) Σ_(i=1)^M R_{i,j}
   ```

3. **Estadístico de Friedman**:
   ```
          12·M    C        
   χ²_F = ────── Σ R̄²_j - 3·M·(C+1)
         C(C+1)  j=1
   ```

4. **Comparación** con valor crítico χ²_{α,C-1}

5. **Decisión**: Si χ²_F > χ²_{α,C-1}: Rechazar H₀

### 7.3.4 Tests Post-Hoc

Después de encontrar diferencias significativas, necesitamos saber CUÁLES pares difieren

#### Test de Nemenyi

Compara todos los pares de modelos

**Critical Difference (CD)**:
```
         √[C(C+1)]
CD = q_α(C) · ────────
              √(6M)
```

Donde q_α: Valores críticos del rango studentizado

**Decisión**: Modelos i, j difieren significativamente si:
```
|R̄ᵢ - R̄ⱼ| > CD
```

#### Test de Bonferroni-Dunn

Compara todos los modelos contra UN modelo de referencia

**Critical Difference**:
```
         √[C(C+1)]
CD = q_{α/(C-1)} · ────────
                  √(6M)
```

**Ventaja**: Menos comparaciones (C-1 en lugar de C(C-1)/2)

## 7.4 Ejemplo Práctico Completo

### Scenario
6 datasets, 4 clasificadores, métrica = Accuracy

```
Dataset   Clf1   Clf2   Clf3   Clf4
D1        70     73     78     82
D2        68     76     75     80
D3        72     74     79     85
D4        69     72     78     81
D5        71     74     77     82
D6        67     70     73     79
```

### Test de Friedman

**Paso 1: Ranking por dataset**

```
D1: Clf4(1), Clf3(2), Clf2(3), Clf1(4)
D2: Clf4(1), Clf2(2), Clf3(3), Clf1(4)
D3: Clf4(1), Clf3(2), Clf2(3), Clf1(4)
D4: Clf4(1), Clf3(2), Clf2(3), Clf1(4)
D5: Clf4(1), Clf3(2), Clf2(3), Clf1(4)
D6: Clf4(1), Clf3(2), Clf2(3), Clf1(4)
```

**Paso 2: Promedio de rangos**
```
R̄₁ = (4+4+4+4+4+4)/6 = 4
R̄₂ = (3+2+3+3+3+3)/6 = 2.83
R̄₃ = (2+3+2+2+2+2)/6 = 2.17
R̄₄ = (1+1+1+1+1+1)/6 = 1
```

**Paso 3: Estadístico de Friedman**
```
χ²_F = (12·6)/(4·5) · (4² + 2.83² + 2.17² + 1²) - 3·6·5
     = 0.6 · 31.07 - 90
     = 18.64 - 1.64 = 17
```

**Paso 4: Comparación**
χ²_{0.05,3} = 7.815
Como 17 > 7.815: **Rechazar H₀** → Diferencias significativas

### Test Post-Hoc (Nemenyi)

**CD = 2.403 · √(4·5/(6·6)) = 2.403 · 0.745 = 1.79**

**Comparaciones pairwise** (|R̄ᵢ - R̄ⱼ|):
- |R̄₁ - R̄₂| = 1.17 < 1.79 → No significativo
- |R̄₁ - R̄₃| = 1.83 > 1.79 → **Significativo**
- |R̄₁ - R̄₄| = 3.00 > 1.79 → **Significativo**
- |R̄₂ - R̄₃| = 0.66 < 1.79 → No significativo
- |R̄₂ - R̄₄| = 1.83 > 1.79 → **Significativo**
- |R̄₃ - R̄₄| = 1.17 < 1.79 → No significativo

**Conclusiones**:
- Clf4 es significativamente mejor que Clf1 y Clf2
- Clf1, Clf2, Clf3 no son significativamente diferentes entre sí

---

## RESUMEN DE CONCEPTOS CLAVE

### Conceptos Matemáticos Fundamentales

1. **Probabilidades**:
   - P(ω): Probabilidad a priori
   - p(x|ω): Likelihood
   - P(ω|x): Probabilidad a posteriori (Bayes)

2. **Operaciones Matriciales**:
   - Producto punto: x · y
   - Proyección: x · V (V es matriz de proyección)
   - Eigenvectores/eigenvalores: propiedades especiales de matrices

3. **Optimización**:
   - Gradiente: Dirección de máxima pendiente
   - Descenso por gradiente: Iterativo hacia mínimo

### Algoritmos Principales

| Tema | Algoritmo | Clase |
|------|-----------|-------|
| T2 | MLE | Paramétrico |
| T3 | k-fold CV | Validación |
| T4 | k-NN | Distancia |
| T5 | Perceptrón | Lineal |
| T5 | MLP | Neural |
| T6 | k-means | Clustering |
| T6 | PCA | Reducción dim. |
| T7 | Friedman | Estadístico |

### Fortalezas y Debilidades

| Método | Fortalezas | Debilidades |
|--------|-----------|-------------|
| **Bayesiano** | Principios sólidos, probabilístico | Requiere conocer P(ω), p(x\|ω) |
| **k-NN** | Simple, adaptativo | Lento, sensible a escala |
| **Perceptrón** | Rápido, lineal | Solo linealmente separable |
| **MLP** | Universal, flexible | Overfitting, entrenamiento complejo |
| **k-means** | Rápido, escalable | Sensible inicialización, outliers |
| **PCA** | Interpretable, rápido | Solo lineal, requiere tunning |

---

## CONSEJOS PARA EL EXAMEN

1. **Entiende los conceptos, no solo memorices**
   - Por qué cada método funciona
   - Cuándo aplicar cada uno

2. **Domina Bayes**
   - Es el fundamento de todo ML
   - Aparece en casi todos los temas

3. **Matrices de confusión**
   - Aprende TPR, FPR, Precision, Recall
   - Entiende ROC/AUC

4. **Validación cruzada**
   - Sé que no es lo mismo entrenar y evaluar
   - k-fold es estándar

5. **Perceptrón → MLP**
   - Perceptrón lineal, MLP no-lineal
   - Backpropagation es fundamental

6. **Clustering y reducción**
   - k-means particional, hierarchical alternativo
   - PCA lineal, t-SNE no-lineal

7. **Tests estadísticos**
   - Friedman para múltiples comparaciones
   - Post-hoc tests para pares significativos

8. **Practica ejercicios**
   - Cálculos de métricas
   - Aplicación de algoritmos paso a paso
   - Interpretación de resultados

¡Éxito en el examen!
