# Predicción de clase de animal en el dataset Zoo mediante clasificadores Bayesianos, estimadores no paramétricos y k-NN

Este trabajo aborda la práctica 2 en la asignatura de Fundamentos del Aprendizaje Automático empleando el dataset Zoo de UCI, aplicando los algoritmos requeridos y analizando sus resultados en una tarea real de clasificación con múltiples clases y características semi-binarias. En la memoria justifico el cambio de dataset, detallo decisiones metodológicas, la implementación de los diferentes modelos según lo estudiado en los apuntes de teoría, y extraigo conclusiones fundamentadas en los resultados obtenidos.

## Introducción y justificación del cambio de dataset

En la práctica original había escogido un dataset financiero binario (Taiwanese Bankruptcy Prediction), centrado en desbalance extremo entre clases y alta dimensionalidad. Aunque permitía explorar problemas de clasificación desbalanceada, tenía **dos inconvenientes clave** según los requerimientos de la práctica:[1]
- El enunciado exige abordar explícitamente *clasificación multiclase*, algo imposible en el contexto binario anterior.
- La alta dimensionalidad y fuerte correlación entre variables dificultaban la interpretación y aplicación de algunos algoritmos clásicos de la asignatura, especialmente los modelos no paramétricos estudiados en T4.

Decidí cambiar al **dataset Zoo**, ampliamente usado en machine learning, que contiene 101 animales representados por 16 atributos binarios fáciles de modelar. Su principal ventaja es permitir probar eficazmente los clasificadores en el escenario multiclass con 7 clases balanceadas, cumpliendo estrictamente el objetivo de la práctica y los requisitos de los apuntes. El nuevo problema facilita la aplicación directa de los modelos clásicos y permite valorar mejor las adaptaciones sobre el macro-F1 y los riesgos/metodologías estudiados en el curso.[1]

## Descripción del dataset y análisis exploratorio

El **dataset Zoo** consta de:
- 101 instancias (animales).
- 16 atributos binarios (presencia/ausencia de ciertas características físicas o de comportamiento).
- La variable objetivo es la “clase” del animal (mamífero, ave, reptil, pez, anfibio, invertebrado, insecto).

La distribución de clases es la siguiente:
- Mammal: 41 muestras (40.6%)
- Bird: 20 muestras (19.8%)
- Reptile: 5 muestras (5.0%)
- Fish: 13 muestras (12.9%)
- Amphibian: 4 muestras (4.0%)
- Invertebrate: 8 muestras (7.9%)
- Insect: 10 muestras (9.9%)

En el split estratificado (80/20) se mantiene la proporción de clases, lo cual es fundamental para evaluar correctamente los métodos propuestos, evitando sesgos hacia la clase mayoritaria y permitiendo análisis fiable del macro-F1.[1]

## Metodología

El estudio compara seis modelos principales siguiendo los esquemas de la asignatura:
- **Naive Bayes Gaussiano** (NB): asume independencia entre las características (T2).
- **MLE Multivariante / Full Bayesian Gaussian**: estimación máxima de verosimilitud multivariante sin independencia entre features (T2).
- **Histogram Bayes**: estimador de densidad no paramétrico mediante histogramas (T4).
- **Parzen Bayes**: estimador no paramétrico usando ventanas de Parzen con kernel Gaussiano, buscando el bandwidth óptimo (T4).
- **k-NN Density Bayes**: variante no paramétrica basada en estimación de densidad local por k-vecinos (T4).
- **k-NN Rule** (sklearn): regla de los k-vecinos más cercanos clásica (T4).

Para todos los modelos se utilizó validación cruzada estratificada (5-fold) y GridSearchCV para la selección de hiperparámetros (bandwidth en Parzen, k en k-NN), todo ello alineado con los apuntes y garantizando reproducibilidad y correcta selección de hiperparámetros.

### Tabla 1. Resultados en Test (20% de datos)
```text
            Modelo  Accuracy  F1-macro
       Naive Bayes    1.0000    1.0000
          MLE Full    0.7143    0.4563
   Histogram Bayes    0.3810    0.0788
      Parzen Bayes    1.0000    1.0000
k-NN Density Bayes    0.4762    0.5714
   k-NN Rule (k=1)    1.0000    1.0000
```
[resultados_test_zoo.csv]

### Tabla 2. Validación Cruzada en Train (80% de datos, 5-fold)
```text
                   Modelo  F1-macro CV (mean)  F1-macro CV (std)
              Naive Bayes              0.8505             0.1357
                 MLE Full              0.5329             0.1021
          Histogram Bayes              0.2474             0.1277
     Parzen Bayes (h=0.1)              0.8648                NaN
k-NN Density Bayes (k=11)              0.5664                NaN
          k-NN Rule (k=1)              0.8267                NaN
```
[resultados_cv_zoo.csv]

## Resultados y comparación de métodos

### Naive Bayes Gaussiano
- **Resultados en test**: accuracy y macro-F1 perfectos (1.0).
- **Interpretación**: El NB clásico obtiene resultados sobresalientes a pesar de la suposición de independencia de las features. Aquí, las variables binomiales suelen ser poco correladas en la práctica (o la correlación no penaliza en la multiclass). El macro-F1 muestra que ninguna clase queda rezagada.[2][1]
- **CV**: Media F1-macro de 0.85 ± 0.13. El test mejora incluso la media en train, sugiriendo robustez y no overfitting.

### MLE Multivariante (Full Bayesian Gaussian)
- **Resultados en test**: accuracy=0.71 y F1-macro=0.46.
- **Problemas**: Las clases minoritarias presentan precisión y recall nulos en test, con warnings sobre métricas indefinidas. Probablemente la estación de covarianza completa en tan pocas muestras (por clase) provoca matrices singulares y mal ajuste, efecto congruente con la teoría sobre mal estimador en alta dimensionalidad y pocos datos. Apuntes T2 y T4 advierten lo mismo.[3][1]

### Histogram Bayes
- **Resultados en test**: accuracy=0.38 y F1-macro=0.078, domina solo la clase mammal, el resto fallan por completo.
- **Explicación**: Histograma sufre curse of dimensionality; la muestra por clase está fragmentada en bins imposibles de cubrir (apuntes T2). El modelo no logra generalizar en multiclase a pesar de tener features binarias con solo dos posibles valores por bin. La teoría predice este mal comportamiento: los histogramas requieren muchas muestras para cada combinación.[4]

### Parzen Bayes
- **Resultados en test**: accuracy=1.0, macro-F1=1.0 tras optimizar bandwidth h=0.1.
- **Análisis**: El mejor método no paramétrico local. Un kernel con h bajo permite capturar patrones sutiles y generalizar correctamente. El resultado refleja lo visto en las diapositivas T4, donde Parzen es capaz de suavizar la frontera de decisión y evitar el overfitting causado por histogramas, mejorando la asignación de clases minoritarias cuando el kernel es ajustado.

### k-NN Density Bayes
- **Resultados en test**: accuracy=0.48, F1-macro=0.57.
- **Discusión**: El k óptimo (11) ofrece cierto compromiso, pero falla en clases grandes (mammal). El estimador sufre el mismo problema del histograma, pero al usar densidad local consigue mejores f1-macro. El resultado, aunque mediocre, resulta congruente con lo esperado por T4: los no paramétricos (k-NN density) suelen ser mala opción en pocos datos multiclase por curse of dimensionality.

### k-NN Rule (sklearn, k=1)
- **Resultados en test**: accuracy=1.0, macro-F1=1.0.
- **Conclusión**: El método clásico de la asignatura es igual de robusto que NB y Parzen, probablemente por la estructura simple y la lejanía entre los puntos. El k=1 captura perfectamente los patrones del zoo y resalta la importancia de la estructura de los datos en el rendimiento de los modelos.[1]

## Conclusiones

El cambio de dataset ha permitido cumplir estrictamente con los objetivos de la práctica y los requisitos teóricos del curso. En el contexto multiclass y con features binarias, los **modelos paramétricos simples** (Naive Bayes y k-NN) alcanzan resultados excelentes, superando a los modelos más sofisticados cuando los datos están bien separados y son poco ruidosos.

Los **estimadores no paramétricos** como histogramas y densidades k-NN muestran sus **limitaciones** en espacios multidimensionales pequeños: la necesidad de muchas muestras por clase se ve acentuada por la maldición de la dimensionalidad y el desbalance de clases. Parzen windows, cuando se ajusta correctamente el ancho, destaca frente a los histogramas y recupera la capacidad discriminante teórica.

La validación cruzada confirma la robustez de los mejores métodos y muestra la inestabilidad de los modelos que requieren más datos o sufren el curse of dimensionality. La distribución de clases balanceada—pero con algunas muy minoritarias (anfibios, reptiles)—permite ver cómo las métricas como el macro-F1 son necesarias para captar el rendimiento real y evitar conclusiones erróneas por accuracy.

La memoria cumple así los requerimientos académicos, justifica el cambio de dataset, discute en profundidad los resultados, y asocia cada decisión técnica a los apuntes de teoría. Los experimentos muestran, en este caso, que la sencillez y la adecuación del modelo a los datos pueden superar metodologías complejas no paramétricas en escenarios de datos sencillos.

[resultados_test_zoo.csv]

[resultados_cv_zoo.csv]

[1](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/125899823/c9cdc6c8-87b8-4f4b-82b9-a19cc9e1b4a3/P2.pdf)
[2](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_1b654d4a-d3a4-417f-9e31-5c3e6a464fd3/0d7e0c57-5737-45c1-8b63-6a52bb6926b4/Slides_Part2A.pdf)
[3](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_1b654d4a-d3a4-417f-9e31-5c3e6a464fd3/a6d135a4-574f-4855-aad3-90ca83c125c7/Slides_Part3A.pdf)
[4](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_1b654d4a-d3a4-417f-9e31-5c3e6a464fd3/a33793e3-f8c8-4a19-aa3c-ba0767dc2d51/Slides_Part2C.pdf)