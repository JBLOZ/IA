# FUNDAMENTOS DEL APRENDIZAJE AUTOMÁTICO
## Libro de Estudio Completo

---

# INTRODUCCIÓN GENERAL

El Aprendizaje Automático es una disciplina fundamental en el mundo moderno que ha revolucionado la forma en que procesamos información y tomamos decisiones basadas en datos. A diferencia de los programas convencionales que requieren instrucciones explícitas para cada tarea, los sistemas de aprendizaje automático tienen la capacidad de aprender patrones a partir de datos, permitiendo que se adapten y mejoren con la experiencia sin ser programados explícitamente para cada situación específica.

El campo del Aprendizaje Automático forma parte de la Inteligencia Artificial, pero con un enfoque particular: en lugar de codificar el conocimiento manualmente en reglas, los algoritmos de ML infieren conocimiento directamente de los datos mediante razonamiento estadístico. Esta es una distinción fundamental que separa el aprendizaje automático de otros enfoques de inteligencia artificial que dependen de representaciones manuales del conocimiento.

La importancia del Aprendizaje Automático radica en su capacidad para resolver problemas complejos donde es imposible definir reglas explícitas. Imaginemos que queremos clasificar imágenes de gatos y perros. Resulta prácticamente imposible describir todas las variaciones posibles de gatos y perros mediante reglas manuales. Sin embargo, mostrando a un algoritmo de ML miles de imágenes etiquetadas, el sistema puede aprender a identificar características que distinguen a los gatos de los perros, incluso cuando se encuentran en posiciones, iluminaciones o contextos nunca vistos antes.

---

# TEMA 1: INTRODUCCIÓN AL APRENDIZAJE AUTOMÁTICO

## 1.1 Definición y Contexto del Aprendizaje Automático

El Aprendizaje Automático puede definirse formalmente como una rama de la Inteligencia Artificial que se dedica al diseño y desarrollo de algoritmos que pueden inferir conocimiento a partir de datos mediante procesos computacionales. Esta definición subraya dos aspectos críticos: primero, que el conocimiento se extrae de los datos en lugar de ser codificado manualmente, y segundo, que este proceso es fundamentalmente computacional y puede automatizarse.

Es importante entender cómo se relaciona el Aprendizaje Automático con campos adyacentes. La Inteligencia Artificial es el concepto más amplio, que busca crear sistemas capaces de realizar tareas que típicamente requieren inteligencia humana. Esto puede lograrse de muchas formas: mediante reglas manuales (sistemas expertos), mediante búsqueda exhaustiva, o mediante aprendizaje automático. El Reconocimiento de Patrones es un campo más específico que se enfoca en la identificación y categorización de patrones en datos, generalmente utilizando características que han sido extraídas manualmente por expertos. El Deep Learning, por su parte, es un subconjunto especializado del Machine Learning que utiliza redes neuronales con múltiples capas para aprender tanto las características como las relaciones complejas entre ellas.

Lo que distingue fundamentalmente al Aprendizaje Automático es su automatismo: el sistema no solo aprende a partir de datos, sino que también puede mejorar automáticamente conforme recibe más información. Este es el verdadero poder de la disciplina.

## 1.2 Las Cuatro Etapas Conceptuales del Aprendizaje Automático

Todo proyecto de Aprendizaje Automático atraviesa cuatro etapas conceptuales bien definidas que forman un ciclo completo desde los datos sin procesar hasta la predicción final.

La primera etapa es la **Fuente** de datos. Los datos originales se capturan del mundo real mediante diversos sensores: cámaras digitales que generan fotografías, micrófonos que capturan audio, escáneres que digitalizan documentos, o bases de datos que registran transacciones. Estos datos sin procesar rara vez están en un formato que un algoritmo de machine learning pueda utilizar directamente. Por ejemplo, una imagen digital es simplemente un arreglo de píxeles con valores de intensidad; los algoritmos necesitan características más significativas. Por esta razón, la extracción de características es una parte crucial de esta etapa. Los expertos del dominio identifican características relevantes que capturan la esencia de lo que queremos predecir. Para clasificar frutas como manzanas o peras, las características podrían incluir el peso, el diámetro, el color dominante, o la textura de la piel.

La segunda etapa es la construcción del **Conjunto de Datos**. Una vez que hemos extraído características, agrupamos estos datos en una estructura organizada. Un conjunto de datos típico consiste en múltiples elementos, cada uno representado como un vector de características. Matemáticamente, representamos esto como D = {(x₁, ω₁), (x₂, ω₂), ..., (xₙ, ωₙ)}, donde cada xᵢ es un vector de características en el espacio d-dimensional Rᵈ, y ωᵢ es la etiqueta o clase verdadera asociada con ese elemento. Por ejemplo, si estamos clasificando frutas y hemos extraído dos características (peso y diámetro), nuestro conjunto de datos podría contener 1000 manzanas y 1000 peras, cada una representada como un par de números.

La tercera etapa es el desarrollo del **Modelo**. En esta fase, aplicamos un algoritmo de aprendizaje automático al conjunto de datos para extraer el conocimiento que representa. El modelo es una representación comprimida de los patrones y relaciones que existen en los datos. Si el algoritmo es exitoso, el modelo capturará las características que distinguen a las manzanas de las peras. El modelo no simplemente memoriza los datos de entrenamiento; debe ser capaz de generalizar a nuevas instancias nunca vistas.

La cuarta etapa es la **Predicción** o aplicación práctica. Una vez que tenemos un modelo entrenado, podemos usarlo para hacer predicciones sobre nuevos datos. Si presentamos al modelo una nueva fruta con características de peso = 150g y diámetro = 8cm, el modelo debería ser capaz de predecir si se trata de una manzana o una pera. Esta es la verdadera razón de existir del machine learning: permitir que los sistemas realicen predicciones útiles en situaciones del mundo real.

## 1.3 Procesos Prácticos: Entrenamiento y Prueba

En la práctica, el Aprendizaje Automático se divide en dos procesos distintos que realizamos en momentos diferentes y con propósitos diferentes. El primero es el **proceso de entrenamiento**, donde el objetivo es extraer y capturar conocimiento de los datos disponibles. Durante el entrenamiento, el algoritmo tiene acceso a datos etiquetados (datos donde conocemos la respuesta correcta) y ajusta sus parámetros internos para minimizar los errores en estos datos etiquetados. Este proceso es análogo a estudiar con un libro de texto o resolver problemas de práctica donde podemos verificar nuestras respuestas.

El segundo es el **proceso de prueba** o evaluación, donde el objetivo es explotar el conocimiento que hemos adquirido para realizar predicciones en datos nuevos que el modelo nunca ha visto antes. Es crítico que utilizemos datos completamente diferentes para la prueba que los que utilizamos para el entrenamiento. De lo contrario, podríamos engañarnos a nosotros mismos al pensar que nuestro modelo es mejor de lo que realmente es. Esta es la diferencia entre memorizar respuestas (lo que pasaría si probamos en los mismos datos de entrenamiento) y realmente comprender conceptos (lo que debería ocurrir cuando probamos en datos nuevos).

Imagina un estudiante que memoriza todas las respuestas de un libro de ejercicios. Cuando se le presentan los mismos ejercicios del libro, obtiene un 100% de precisión. Pero en un examen con preguntas diferentes que requieren los mismos conceptos, el estudiante falla. De manera similar, si entrenamos un modelo de ML y luego evaluamos su desempeño usando los mismos datos de entrenamiento, obtendremos métricas engañosamente optimistas que no reflejan la capacidad real de generalización del modelo.

## 1.4 Representación de Características

Una decisión fundamental en cualquier proyecto de Aprendizaje Automático es cómo representar los datos de forma que los algoritmos puedan procesarlos efectivamente. Existen dos enfoques principales que representan diferentes puntos en el espectro de representación.

El primer enfoque es la **representación feature-based** o basada en características estadísticas. En este enfoque, cada elemento se representa como un vector de características numéricas. Por ejemplo, un automóvil podría representarse mediante el vector [peso_kg, velocidad_máxima_kmh, consumo_combustible_l_100km, edad_años]. La ventaja de esta representación es que todos los elementos tienen exactamente el mismo número de características, lo que permite que los algoritmos procesen los datos de manera uniforme. Muchos algoritmos clásicos de machine learning, como los que estudiaremos en este libro, se han diseñado específicamente para trabajar con esta representación. Sin embargo, la limitación es clara: nuestra capacidad de representación es finita. Algunos aspectos complejos de los datos simplemente no pueden capturarse con un conjunto fijo de características numéricas.

El segundo enfoque es la **representación estructural**, donde la estructura del objeto en sí contiene información importante. Por ejemplo, en el reconocimiento de escritura manual, la topología y conectividad de los trazos es tan importante como sus características geométricas individuales. Similarmente, en la clasificación de moléculas químicas, la estructura de conexión entre átomos es fundamental. En estos casos, podemos representar los datos como strings, árboles, o grafos que preservan esta estructura. La ventaja de las representaciones estructurales es que pueden capturar información más compleja y matizada. Sin embargo, la desventaja es que el número de algoritmos que pueden procesar estas representaciones es limitado.

En este curso, nos enfocamos principalmente en la representación feature-based, ya que es la base de la mayoría de algoritmos de machine learning, pero es importante ser consciente de que para ciertos problemas, representaciones estructurales pueden ser más apropiadas.

## 1.5 Taxonomía del Aprendizaje Automático

El Aprendizaje Automático es un campo diverso con muchas variaciones diferentes. Es útil categorizar estos enfoques de varias maneras para entender mejor cuándo y cómo aplicar cada uno.

Cuando categorizamos por el **tipo de tarea**, identificamos varios paradigmas principales. La **clasificación** es la tarea de asignar elementos a clases predefinidas. Por ejemplo, determinar si un correo electrónico es spam o no es un problema de clasificación binaria, mientras que clasificar noticias en las categorías "política", "deportes", "entretenimiento" o "tecnología" es un problema de clasificación multiclase. La **regresión** es la tarea de predecir valores continuos. Ejemplos incluyen predecir el precio de una casa basado en sus características, o pronosticar la temperatura para mañana. El **clustering** o agrupamiento es la tarea de agrupar elementos similares sin que tengamos etiquetas predefinidas indicando a qué grupo pertenece cada elemento. Finalmente, el **etiquetado de secuencias** es una tarea especializada donde necesitamos etiquetar cada elemento dentro de una secuencia. Por ejemplo, en procesamiento de lenguaje natural, podríamos querer etiquetar cada palabra en una oración con su parte del habla (sustantivo, verbo, adjetivo, etc.).

Cuando categorizamos por el **tipo de aprendizaje**, la distinción más importante es entre aprendizaje **supervisado** y aprendizaje **no supervisado**. En el aprendizaje supervisado, nuestro conjunto de datos consta de pares entrada-salida: D = {(xᵢ, ωᵢ)}, donde sabemos cuál es la respuesta correcta para cada entrada. El objetivo es aprender una función que mapee entradas a salidas correctas, lo que nos permite predecir salidas para nuevas entradas. Esta es la configuración más común en las aplicaciones prácticas. En cambio, en el aprendizaje no supervisado, nuestro conjunto de datos solo contiene entradas: D = {xᵢ}, sin etiquetas de salida. El objetivo es encontrar estructura o patrones ocultos en los datos. Esto es útil para exploración de datos o para encontrar grupos naturales de elementos similares.

Existe también un enfoque intermedio llamado aprendizaje **semi-supervisado**, donde tenemos una mezcla de datos etiquetados y sin etiquetar. Este enfoque intenta aprovechar tanto los datos etiquetados como los no etiquetados para lograr un mejor desempeño. A menudo en el mundo real, obtener datos etiquetados es costoso (requiere expertos humanos) pero los datos sin etiquetar son abundantes, por lo que el aprendizaje semi-supervisado es altamente relevante.

---

# TEMA 2: APRENDIZAJE COMPUTACIONAL Y TEORÍA BAYESIANA

## 2.1 Fundamentos de la Teoría de Decisión Bayesiana

La Teoría de Decisión Bayesiana proporciona el fundamento matemático sólido sobre el cual se construye gran parte del Aprendizaje Automático. A diferencia de otros enfoques que pueden parecer más ad-hoc, la teoría bayesiana ofrece principios claros y justificables para tomar decisiones bajo incertidumbre.

Comencemos con un ejemplo concreto para entender los conceptos. Imaginemos que estamos en un mercado de frutas y queremos clasificar frutas que recibimos en una caja como manzanas o peras. Antes de examinar ninguna fruta específicamente, sabemos que históricamente el mercado recibe 60% manzanas y 40% peras. Esta es nuestra información previa sobre la distribución de clases en la población general, lo que en términos bayesianos llamamos la **probabilidad a priori**. Matemáticamente, escribimos P(ω₁) = 0.6 para manzanas y P(ω₂) = 0.4 para peras.

La pregunta fundamental que la teoría bayesiana responde es: cuando examinamos una fruta específica (por ejemplo, determinamos su color) y observamos que es de un cierto color x, ¿cómo debemos actualizar nuestra creencia sobre si es una manzana o una pera? La respuesta a esta pregunta es el núcleo del Teorema de Bayes.

Para aplicar el Teorema de Bayes, necesitamos información adicional: la **verosimilitud** o likelihood, que es la probabilidad de observar el color específico x dado que la fruta es una manzana, escrito como p(x|ω₁). De manera similar, necesitamos la probabilidad de observar ese color dado que es una pera, p(x|ω₂). Estas verosimilitudes capturan el conocimiento sobre cómo se distribuyen los colores dentro de cada clase. Por ejemplo, sabemos que las manzanas tienden a ser rojas, verdes o amarillas, mientras que las peras tienden a ser verdes o amarillo-marrón. Esto significaría que si observamos un color rojo intenso, la verosimilitud p(x=rojo_intenso|manzana) sería alta, mientras que p(x=rojo_intenso|pera) sería baja.

El Teorema de Bayes nos permite combinar nuestro conocimiento previo con la nueva evidencia que observamos para calcular la **probabilidad a posteriori**, que es exactamente lo que queremos: la probabilidad de que la fruta sea una manzana o una pera dado el color que observamos. La fórmula es elegantemente simple:

P(ωⱼ|x) = p(x|ωⱼ) · P(ωⱼ) / p(x)

Donde p(x) es un factor de normalización que asegura que las probabilidades posteriores sumen 1. Intuitivamente, esta fórmula dice que la creencia posterior es proporcional a la verosimilitud multiplicada por la creencia previa. Si tenemos una creencia previa fuerte de que es manzana y la evidencia (el color) es consistente con esa creencia, nuestra probabilidad posterior de que sea manzana será muy alta.

## 2.2 Regla de Decisión de Bayes

Una vez que tenemos las probabilidades posteriores, necesitamos decidir: ¿deberíamos clasificar esta fruta como manzana o pera? La respuesta bayesiana es simple y óptima: elegir la clase con mayor probabilidad posterior.

ω* = arg max P(ω|x)
      ω∈{ω₁, ω₂}

Esta regla, llamada la **Regla de Decisión de Bayes**, tiene una propiedad fundamental: minimiza la probabilidad de error. En otras palabras, si pudiéramos conocer exactamente las probabilidades verdaderas, esta regla de decisión produciría el menor número de errores posible. Esta es la razón por la cual es considerada óptima en la teoría bayesiana.

Sin embargo, en la práctica hay complicaciones. Primero, a menudo no conocemos las probabilidades posteriores exactamente. No sabemos exactamente cómo se distribuye el color dentro de la clase de manzanas. Segundo, a veces los diferentes tipos de errores tienen costos diferentes. Confundir una manzana por una pera es un error, pero confundir una pera por una manzana es un error diferente que podría tener una consecuencia distinta.

Para manejar estas complicaciones, la teoría bayesiana se extiende mediante la introducción de una **función de pérdida** λ(αᵢ|ωⱼ), que especifica el costo de tomar la acción αᵢ cuando el verdadero estado de la naturaleza es ωⱼ. Por ejemplo, podríamos decidir que confundir una pera por manzana tiene un costo de 3 unidades, mientras que confundir una manzana por pera tiene un costo de 1 unidad (quizás porque la gente esperando en la tienda es más tolerante a obtener una pera cuando pidió manzana, que lo opuesto).

La Regla de Decisión Bayesiana de Mínimo Riesgo modifica la decisión para consideradr estos costos:

ω* = arg min Σⱼ λ(αᵢ|ωⱼ) · P(ωⱼ|x)
      αᵢ

En otras palabras, elegimos la acción que minimiza el riesgo esperado (costo esperado) dado la evidencia observada.

## 2.3 Extensión a Espacios de Alta Dimensión

La teoría que hemos descrito para una característica (color) se extiende naturalmente a múltiples características. Si en lugar de solo observar el color, observamos el peso, el diámetro, la textura y el aroma, entonces nuestro vector de características x se convierte en un vector de d dimensiones: x ∈ Rᵈ.

Matemáticamente, nada cambia fundamentalmente. Todavía aplicamos el Teorema de Bayes:

P(ω|x) = p(x|ω) · P(ω) / p(x)

Y todavía elegimos la clase con mayor probabilidad posterior. La única complicación práctica es que en espacios de alta dimensión, es más difícil estimar las distribuciones p(x|ω) porque necesitamos más datos para capturar la estructura compleja en espacios con muchas dimensiones.

Igualmente, la teoría se extiende fácilmente a problemas multiclase, donde en lugar de dos clases tenemos múltiples clases: W = {ω₁, ω₂, ..., ω|W|}. El procedimiento es idéntico: calcular la probabilidad posterior para cada clase y elegir aquella con la máxima probabilidad posterior.

## 2.4 Estimación de Máxima Verosimilitud

Hemos establecido que la Regla de Decisión de Bayes es óptima, pero requiere que conozcamos las probabilidades posteriores P(ω|x). En la práctica, no conocemos estas probabilidades; deben ser estimadas a partir de datos. Una de las formas más importantes de hacer esto es mediante **Estimación de Máxima Verosimilitud (MLE)**.

El principio detrás de MLE es simple e intuitivo: si tenemos un conjunto de datos observados, los parámetros que mejor describen estos datos son aquellos que hacen que los datos observados sean lo más probables posible. Matemáticamente, si asumimos que nuestros datos siguen una distribución paramétrica p(x|ω, θ), donde θ son los parámetros desconocidos, entonces queremos encontrar θ que maximice la probabilidad de observar exactamente este conjunto de datos.

Supongamos que tenemos un conjunto de datos de n manzanas: D = {x₁, x₂, ..., xₙ}. Asumimos que cada xᵢ fue generado independientemente de la misma distribución p(x|ω=manzana, θ). La probabilidad conjunta de observar todo este conjunto de datos es el producto de las probabilidades individuales (debido a la independencia):

p(D|θ) = ∏ᵢ₌₁ⁿ p(xᵢ|θ)

Esta función p(D|θ) se llama la **verosimilitud** del dataset. Para encontrar el θ que maximiza esta verosimilitud, tomamos la derivada con respecto a θ, la igualamos a cero, y resolvemos. En la práctica, es más conveniente trabajar con el logaritmo natural de la verosimilitud, que es monótonamente creciente:

l(θ) = ln p(D|θ) = Σᵢ₌₁ⁿ ln p(xᵢ|θ)

Encontramos θ̂ que maximiza l(θ), que es equivalente a maximizar p(D|θ).

Un ejemplo importante donde la solución es analítica y cerrada es cuando asumimos que la distribución es gaussiana. Si creemos que las características de las manzanas siguen una distribución gaussiana multivariada con media μ y matriz de covarianza Σ, entonces los estimadores MLE son simplemente:

μ̂ = (1/n) Σᵢ₌₁ⁿ xᵢ  (la media muestral)

Σ̂ = (1/(n-1)) Σᵢ₌₁ⁿ (xᵢ - μ̂)(xᵢ - μ̂)ᵀ  (la matriz de covarianza muestral)

Estos son exactamente los estimadores intuitivos que usaríamos de todos modos: la media y la covarianza de los datos observados.

## 2.5 Problemas Fundamentales en Aprendizaje Automático

A pesar de la elegancia y optimalidad de la teoría bayesiana, cuando aplicamos estos principios en la práctica enfrentamos varios desafíos fundamentales que no pueden ignorarse.

El primero es el problema de la **generalización**. En teoría, nos importa el error que comete nuestro modelo en toda la población de nuevos datos que nunca hemos visto. Esto se llama el **riesgo verdadero**. Sin embargo, en la práctica, solo podemos medir el error en el conjunto de datos finito que tenemos disponible. La pregunta fundamental es: ¿qué tan bien el error que observamos en nuestros datos de prueba predice el error verdadero en toda la población?

Esto nos lleva al concepto del **sesgo-varianza** (bias-variance tradeoff), que es uno de los conceptos más importantes en machine learning. Imagina que entrenamos muchos modelos diferentes, cada uno usando un conjunto de datos de entrenamiento ligeramente diferente muestreado de la misma población. El **sesgo** de un modelo es cuánto, en promedio, la predicción del modelo se desvía del valor verdadero, sin importar qué conjunto de datos de entrenamiento usamos. El **sesgo alto** significa que nuestro modelo es demasiado simple para capturar la complejidad real en los datos: hemos subajustado (underfitting). Por ejemplo, si intentamos predecir precios de casas usando solo el área de la casa, pero el precio también depende crucialmente de la ubicación y la antigüedad, nuestro modelo tendrá alto sesgo.

La **varianza**, por otro lado, mide cuánto cambia la predicción de un modelo cuando usamos diferentes conjuntos de datos de entrenamiento. Alta varianza significa que pequeños cambios en los datos de entrenamiento conducen a cambios grandes en el modelo aprendido. Esto ocurre cuando el modelo es demasiado complejo y ha sobreajustado (overfitting). Por ejemplo, si tenemos un árbol de decisión que crece hasta la profundidad máxima, memorizará características específicas del ruido en los datos de entrenamiento que no generalizan a datos nuevos.

El error total de nuestro modelo se puede descomponer en tres componentes:

Error_total = Sesgo² + Varianza + Ruido_Irreducible

El ruido irreducible es el error inherente que existe porque los datos en sí mismos tienen aleatoriedad o porque hay variables importantes que no estamos midiendo. Podemos pensar que idealmente queremos minimizar tanto el sesgo como la varianza, pero existe un tradeoff fundamental: los modelos simples tienden a tener bajo sesgo pero alta varianza, mientras que los modelos complejos tienden a tener bajo sesgo pero alta varianza. El punto óptimo, donde la suma total de error es mínima, típicamente ocurre en algún punto intermedio.

El segundo desafío fundamental es la **maldición de la dimensionalidad**. Cuando el número de características d crece, ocurren varias cosas problemáticas. Primero, el espacio de características se vuelve exponencialmente más grande. Imagina un espacio donde cada característica puede tomar 10 valores discretos. Con 2 características, hay 10² = 100 posibilidades. Con 10 características, hay 10¹⁰ = 10 mil millones de posibilidades. Si solo tenemos, digamos, 1000 datos de entrenamiento, entonces el espacio está enormemente escaso: la mayoría del espacio de características posibles no está representado en nuestros datos.

Esta escasez tiene consecuencias graves. Segundo, el modelo tiene mucha libertad para ajustarse al ruido específico en nuestro conjunto de entrenamiento particular, porque hay muchas formas diferentes de ajustar los datos en este espacio grande. Esto conduce a overfitting severo. Tercero, la distancia entre puntos se vuelve menos significativa en espacios de alta dimensión: todos los puntos tienden a estar aproximadamente a la misma distancia el uno del otro, lo que hace que los algoritmos basados en distancia sean menos efectivos.

Para manejar la maldición de la dimensionalidad, disponemos de varias estrategias. La **selección de características** implica elegir un subconjunto de características que sean más relevantes para la tarea. La **regularización** implica añadir restricciones al modelo para penalizar la complejidad. La **reducción de dimensionalidad** implica proyectar el espacio de características en un espacio de menor dimensión mientras se retiene la máxima información posible.

---

# TEMA 3: EVALUACIÓN Y VALIDACIÓN DE MODELOS

## 3.1 Conceptos Fundamentales de Evaluación

Después de desarrollar un modelo de machine learning, necesitamos responder una pregunta crítica: ¿qué tan bien funciona realmente? Esta no es una pregunta trivial, y la respuesta depende cuidadosamente de cómo evaluamos el modelo.

Antes de profundizar en métricas específicas, es importante distinguir entre dos conceptos relacionados pero diferentes. La **pérdida (loss)** es una función que usamos durante el entrenamiento del modelo. Guía el proceso de optimización, diciéndole al algoritmo qué dirección ajustar los parámetros. La **métrica (figure of merit)**, por otro lado, es lo que realmente nos importa en el mundo real. Refleja el objetivo de negocio o científico que estamos tratando de lograr.

A menudo, la pérdida y la métrica son diferentes. Por ejemplo, durante el entrenamiento podríamos usar la pérdida de error cuadrático (MSE), que penaliza fuertemente los errores grandes. Pero para evaluar nuestro modelo, podrías estar interesado en la precisión: el porcentaje de predicciones correctas. O podrías estar interesado en métricas más sofisticadas que consideran el costo de diferentes tipos de errores.

Esta distinción es importante porque a veces optimizar directamente la pérdida no conduce al mejor desempeño en la métrica que realmente importa. Por esto es crucial elegir cuidadosamente qué métrica usar para evaluar nuestro modelo.

## 3.2 Partición de Datos para Evaluación

El problema de evaluar un modelo es sutil pero crítico de entender. Si entrenamos un modelo en un conjunto de datos D y luego evaluamos su desempeño en el mismo conjunto D, obtendremos resultados engañosamente optimistas. El modelo ha visto estos datos antes, los ha memorizado, al menos parcialmente. Esto es especialmente problemático si nuestro modelo es complejo y puede sobreje ustarse fácilmente.

La solución es dividir nuestros datos disponibles en subconjuntos disjuntos con propósitos diferentes. El conjunto más grande, típicamente 60-80% de los datos, es el **conjunto de entrenamiento** (training set). Este es donde "enseñamos" al modelo, ajustando sus parámetros basado en estos datos. Un segundo conjunto, típicamente 10-20% de los datos, es el **conjunto de validación** (validation set). Este conjunto se usa para ajustar hiperparámetros (parámetros que controlan cómo se entrena el modelo, como la tasa de aprendizaje) y para hacer decisiones sobre la selección del modelo. Un tercero, tipicamente 10-20%, es el **conjunto de prueba** (test set), que nunca se usa durante el entrenamiento o ajuste. Este conjunto es reservado exclusivamente para evaluar el desempeño final del modelo en datos completamente nuevos.

Es crucial que estos conjuntos sean completamente disjuntos. No puede haber solapamiento. El conjunto de entrenamiento debe ser más grande que los otros dos porque el aprendizaje requiere muchos datos, pero la proporción exacta depende del tamaño total del dataset y de cuánta información tienes sobre hiperparámetros desde el conocimiento previo.

Cuando dividimos el dataset, también debemos considerar la **estratificación**, especialmente cuando el dataset es desbalanceado (tiene muchas más instancias de una clase que de otras). La estratificación asegura que la proporción de clases sea aproximadamente la misma en cada conjunto. Por ejemplo, si 95% de nuestros datos son "normales" y 5% son "anómalos", queremos asegurar que todos nuestros conjuntos mantengan aproximadamente esa proporción.

## 3.3 Validación Cruzada

En muchas situaciones, especialmente cuando el conjunto de datos es relativamente pequeño, dividir los datos una única vez en train/validation/test puede ser ineficiente. Estamos "desperdiciando" datos en el sentido de que cada dato se usa para un propósito específico. La **validación cruzada** es una técnica que permite un uso más eficiente de los datos limitados.

El enfoque más común es la **k-fold cross-validation**. En k-fold CV, dividimos el conjunto de datos en k pliegues (folds) aproximadamente iguales. Luego realizamos k iteraciones. En cada iteración i, usamos el pliegue i como conjunto de prueba y los k-1 pliegues restantes como conjunto de entrenamiento. Entrenamos el modelo, evaluamos su desempeño en el pliegue i, y guardamos el resultado. Después de completar todas las k iteraciones, promediamos los k resultados para obtener una estimación del desempeño general.

La ventaja de este enfoque es que cada dato es usado tanto para entrenamiento como para evaluación, solo en iteraciones diferentes. Esto proporciona una estimación más estable del desempeño que una única división. La desventaja es que es k veces más computacionalmente costoso, porque necesitamos entrenar k modelos.

Un caso extremo es la **validación de dejar-uno-fuera** (LOOCV), donde k = n (el número de datos). Esto significa que en cada iteración, entrenamos en n-1 datos y evaluamos en 1 dato. Esto proporciona una estimación muy baja en sesgo (muy próxima a la verdad), pero tiene varianza muy alta y es computacionalmente costosísimo para datasets grandes.

Una variante importante para problemas con desbalance de clases es la **k-fold cross-validation estratificada**, que mantiene las proporciones de clases en cada pliegue. Esto asegura que no accidentalmente obtenemos un pliegue donde todas las instancias son de una clase.

## 3.4 Evaluación en Clasificación Binaria

Para problemas de clasificación, disponemos de varias métricas que capturan diferentes aspectos del desempeño. Para entender estas métricas, comencemos con la **matriz de confusión**, una herramienta fundamental que nos muestra exactamente qué tipo de errores está cometiendo nuestro modelo.

Para un problema de clasificación binaria donde queremos clasificar instancias como positivas (ω) o negativas (ω̄), la matriz de confusión tiene cuatro entradas. Los **Verdaderos Positivos (TP)** son instancias que verdaderamente son positivas y nuestro modelo las predice como positivas. Los **Verdaderos Negativos (TN)** son instancias que verdaderamente son negativas y nuestro modelo las predice como negativas. Los **Falsos Positivos (FP)** son instancias negativas que nuestro modelo incorrectamente predice como positivas (falsa alarma). Los **Falsos Negativos (FN)** son instancias positivas que nuestro modelo falla en detectar.

Con estas cuatro cantidades, podemos calcular múltiples métricas que enfatizan diferentes aspectos. La **exactitud (accuracy)** es simplemente el porcentaje de predicciones correctas:

Exactitud = (TP + TN) / (TP + FN + TN + FP)

Esta métrica es intuitiva pero tiene un problema grave en presencia de desbalance de clases. Imagina un detector de fraude donde el 99% de las transacciones son legítimas y el 1% es fraude. Un modelo que simplemente predice "legítimo" para todo tendría una exactitud del 99%, pero sería completamente inútil para detectar fraude.

La **precisión (precision)** mide, de todas las instancias que el modelo predice como positivas, cuántas son verdaderamente positivas:

Precisión = TP / (TP + FP)

La precisión es importante cuando los falsos positivos son costosos. Por ejemplo, si enviamos una notificación a un cliente diciendo que se detectó fraude en su cuenta cuando en realidad fue legítimo, es una experiencia negativa. Queremos alta precisión para minimizar falsas alarmas.

El **recall** (también llamado exhaustividad o sensibilidad) mide, de todas las instancias que verdaderamente son positivas, cuántas el modelo detecta:

Recall = TP / (TP + FN)

El recall es importante cuando los falsos negativos son costosos. En detección de fraude, un falso negativo significa que dejamos pasar fraude verdadero, lo cual puede resultar en pérdida de dinero.

La **F-medida (F1-score)** es la media armónica de precisión y recall, proporcionando un balance entre ambas:

F1 = 2 · (Precisión · Recall) / (Precisión + Recall)

La F-medida es útil cuando queremos un balance equilibrado entre precisión y recall.

Para problemas multiclase, estas métricas se generalizan de dos formas. En el promediado **micro**, agregamos todas las predicciones verdaderas/falsas entre todas las clases antes de calcular la métrica, lo que es equivalente a la exactitud global. En el promediado **macro**, calculamos la métrica para cada clase de forma individual y luego promediamos, lo que trata todas las clases igual sin importar cuán frecuentes sean.

## 3.5 Curva ROC y AUC

La **curva ROC (Receiver Operating Characteristic)** es una herramienta visual poderosa para entender el desempeño de un clasificador binario. Es especialmente útil porque es independiente del desbalance de clases.

Para entender la curva ROC, primero necesitamos entender la **Tasa Positiva Verdadera (TPR)** y la **Tasa Falsa Positiva (FPR)**:

TPR = TP / (TP + FN)  [qué fracción de positivos verdaderos detectamos]
FPR = FP / (FP + TN)  [qué fracción de negativos incorrectamente marcamos como positivos]

Ahora, los clasificadores típicamente no producen una predicción binaria directa, sino una puntuación o probabilidad continua. Por ejemplo, un modelo podría producir un valor entre 0 y 1 indicando la probabilidad de que la instancia sea positiva. Para convertir esto en una predicción binaria, establecemos un umbral: si la probabilidad es mayor que el umbral, predecimos positivo; de lo contrario, predicimos negativo.

Aquí está la clave: si variamos este umbral, el TPR y FPR cambiarán. Con un umbral muy bajo (predecimos positivo para casi todo), tanto TPR como FPR serán altos. Con un umbral muy alto (predecimos positivo solo para instancias muy confiantes), ambos serán bajos. La curva ROC grafica FPR en el eje x y TPR en el eje y, mostrando cómo varía el tradeoff entre detectar positivos y falsas alarmas conforme variamos el umbral.

Un clasificador perfecto tendría una curva que va directamente hacia arriba (TPR = 1, FPR = 0) y luego hacia la derecha. Una clasificación aleatoria produciría una línea diagonal de (0,0) a (1,1). Una curva ROC curvada hacia la esquina superior izquierda indica un buen clasificador.

El **área bajo la curva (AUC)** cuantifica este desempeño en un único número entre 0 y 1. Un AUC de 0.5 indica desempeño de clasificación aleatoria. Un AUC de 1.0 indica desempeño perfecto. Un AUC de 0.8 o superior generalmente se considera bueno.

## 3.6 Evaluación en Regresión

Para problemas de regresión donde predecimos valores continuos, usamos métricas diferentes que reflejan cómo el error numérico se distribuye.

El **Error Medio Absoluto (MAE)** es el promedio de las diferencias absolutas entre predicciones y valores verdaderos:

MAE = (1/n) Σ |ŷᵢ - yᵢ|

El MAE es robusto a outliers porque trata todos los errores proporcionalmente.

El **Error Cuadrático Medio (MSE)** es el promedio de las diferencias cuadradas:

MSE = (1/n) Σ (ŷᵢ - yᵢ)²

El MSE penaliza fuertemente los errores grandes (porque los eleva al cuadrado), por lo que es más sensible a outliers que MAE.

La **Raíz del Error Cuadrático Medio (RMSE)** es la raíz cuadrada del MSE:

RMSE = √MSE

La ventaja de RMSE es que está en las mismas unidades que el objetivo, lo que lo hace más interpretable que MSE.

---

# TEMA 4: MÉTODOS NO PARAMÉTRICOS Y BASADOS EN DISTANCIA

## 4.1 Introducto a Métodos No Paramétricos

Hemos aprendido que la Teoría de Decisión Bayesiana proporciona un marco óptimo para clasificación, pero requiere que estimemos las densidades de probabilidad p(x|ω). En el Tema 2, vimos cómo hacerlo bajo el supuesto de que los datos siguen una distribución gaussiana. Sin embargo, ¿qué ocurre cuando los datos no son gaussianos? ¿Qué si la verdadera distribución es multimodal o tiene formas complejas que no se pueden capturar bien con una distribución paramétrica simple?

Los métodos **no paramétricos** responden a esta pregunta: en lugar de asumir una forma paramétrica específica para p(x|ω), estimamos la densidad directamente a partir de los datos, permitiendo que la forma de la densidad se determine completamente por los datos mismos. Esta es una idea poderosa porque ofrece más flexibilidad, pero también viene con desafíos: necesitamos más datos y debemos ser cuidadosos con los parámetros de control.

Hay dos enfoques principales. El primer enfoque busca **estimar la densidad de probabilidad** p(x|ω), normalmente usando técnicas como histogramas o ventanas de Parzen, y luego usar estas estimaciones con el teorema de Bayes para clasificar. El segundo enfoque intenta **estimar directamente la probabilidad posterior** P(ω|x) sin pasar por la estimación de densidad intermedia. Este segundo enfoque es más directo, ya que evita la estimación de algo que solo necesitamos como paso intermedio.

Los métodos basados en distancia como el vecino más cercano pertenecen a esta segunda categoría: estiman la probabilidad posterior implícitamente basándose en la idea de que instancias cercanas probablemente pertenecen a la misma clase.

## 4.2 Estimación de Densidad

### Histogramas

La forma más simple de estimar una densidad es dividir el espacio en regiones y contar cuántos datos caen en cada región. Esto se llama un **histograma**.

Por ejemplo, supongamos que medimos los pesos de 500 personas hombres y queremos estimar la distribución de pesos. Dividimos el rango de pesos posibles en intervalos, digamos [50-55), [55-60), [60-65), etc. Luego contamos cuántos datos caen en cada intervalo. Si el intervalo [90-95) kg contiene 23 muestras, entonces estimamos que la probabilidad de observar un peso en ese rango es aproximadamente 23/500 = 0.046. Para obtener una densidad de probabilidad (que integra a 1), dividimos por el ancho del intervalo. Si cada intervalo tiene ancho 5 kg, entonces la densidad estimada es 0.046/5 = 0.0092 kg⁻¹.

Los histogramas tienen varios problemas. Primero, son muy sensibles a la resolución (ancho de intervalo) que elegimos. Si los intervalos son demasiado estrechos, la estimación es ruidosa y varía mucho debido a fluctuaciones aleatorias en los datos. Si son demasiado anchos, perdemos detalle y la estimación es demasiado suave. Segundo, los histogramas son discontinuos: hay saltos abruptos en los límites de los intervalos, incluso si la densidad verdadera es suave.

### Ventanas de Parzen

Una mejora sobre los histogramas es usar **ventanas de Parzen** (también llamadas kernel density estimation). En lugar de usar cajas duras que son 1 dentro del intervalo y 0 fuera, usamos una función suave llamada kernel.

La idea es: para estimar la densidad en un punto x, miramos todos los puntos de datos y contribuimos suavemente dependiendo de cuán cerca estén del punto x. Matemáticamente:

p̂(x|ω) = (1/|D|·hᵈ) Σᵢ K((x - xᵢ)/h)

Donde K(u) es una función kernel (por ejemplo, gaussiana), h es el ancho de ventana (bandwidth), y d es la dimensionalidad.

El kernel gaussiano es especialmente popular:

K(u) = (1/√(2π)) exp(-u²/2)

Las ventanas de Parzen producen estimaciones suaves y continuas. Sin embargo, tienen un parámetro h que necesita ser ajustado. Si h es demasiado pequeño, la estimación es ruidosa. Si h es demasiado grande, la estimación es demasiado suave. Además, h es global: usamos el mismo ancho en todas partes del espacio, lo que puede no ser óptimo si los datos tienen densidades diferentes en diferentes regiones.

### Estimador k-Vecino Más Cercano

Una solución a la limitación de h global es usar el **estimador k-vecino más cercano**. En lugar de fijar h y dejar que el número de datos en cada región varíe, fijamos el número de datos (k) en cada región y dejamos que el volumen de la región varíe.

La idea es simple: para estimar la densidad en un punto x, encontramos los k puntos de datos más cercanos a x. Estos k puntos ocupan algún volumen V(x) alrededor de x. Entonces estimamos:

p̂(x|ω) = k / (|D| · V(x))

En otras palabras, la densidad es proporcional al número de puntos dividido por el volumen que ocupan. En regiones densas, V(x) será pequeño, resultando en una alta densidad estimada. En regiones escasas, V(x) será grande, resultando en una baja densidad estimada. Esto adapta automáticamente la escala a la densidad local.

La ventaja es que el estimador se adapta localmente. La desventaja es que es más complicado computacionalmente y que necesitamos elegir k.

## 4.3 La Regla del Vecino Más Cercano

Un salto conceptual importante es ir de la estimación de densidad a la **regla del vecino más cercano** para clasificación. Esta regla es sorprendentemente simple y sorprendentemente efectiva.

La idea es: para clasificar una nueva instancia q, encontrar el punto de entrenamiento más similar (por alguna medida de distancia), y asignar q la clase del punto de entrenamiento más cercano. Matemáticamente:

ω̂ = ωᵢ : donde i = arg min D(q, xᵢ)

Donde D es una función de distancia. La hermosura de esta regla es su simplicidad y que no requiere hacer supuestos sobre la forma de las distribuciones. Solo requiere que podamos definir una medida de distancia significativa entre puntos.

La regla del vecino más cercano está conectada a la teoría bayesiana por la siguiente observación: si tenemos infinitos datos de entrenamiento y usamos distancia euclidiana, entonces con probabilidad, el vecino más cercano pertenecerá a la clase con la máxima probabilidad posterior P(ω|x). Por lo tanto, la regla del vecino más cercano implementa implícitamente la regla bayesiana óptima en el límite de infinitos datos.

Cuando no tenemos infinitos datos, la regla del vecino más cercano aún funciona bien, pero la garantía teórica no se mantiene perfectamente. Sin embargo, el análisis teórico muestra que el error de la regla del vecino más cercano está acotado por el doble del error óptimo de Bayes. En otras palabras, es una aproximación razonable al óptimo teórico.

Una decisión importante al usar la regla del vecino más cercano es elegir la métrica de distancia. Las propiedades de una métrica válida son: no-negatividad (D(a,b) ≥ 0), reflexividad (D(a,b) = 0 solo si a = b), simetría (D(a,b) = D(b,a)), y desigualdad triangular (D(a,b) + D(b,c) ≥ D(a,c)).

La métrica de Minkowski es una familia flexible que include varias opciones comunes:

D(a,b) = [Σᵢ |aᵢ - bᵢ|ᵖ]^(1/p)

Cuando p=1, obtenemos la distancia Manhattan (suma de diferencias absolutas). Cuando p=2, obtenemos la distancia euclidiana (raíz cuadrada de suma de cuadrados). Cuando p=∞, obtenemos la distancia de Chebyshev (máxima diferencia).

## 4.4 Regla del k-Vecino Más Cercano

Extendiendo la idea del vecino más cercano, podríamos considerar los k vecinos más cercanos en lugar de solo 1. La **regla del k-vecino más cercano (k-NN)** funciona así:

Para clasificar una instancia q:
1. Encontrar los k puntos de entrenamiento más cercanos a q
2. Contar los votos: cuántos de estos k puntos pertenecen a cada clase
3. Asignar q la clase con más votos

Por ejemplo, con k=5, si 4 de los 5 vecinos más cercanos son de la clase "manzana" y 1 es de la clase "pera", entonces clasificamos q como manzana.

La ventaja de k-NN sobre 1-NN es que es más robusto al ruido. Un solo punto de datos puede ser un outlier o ruido, pero es menos probable que 5 puntos sean todos outliers. Sin embargo, k-NN también tiene una desventaja: necesitamos elegir k. Si k es muy pequeño, el clasificador es ruidoso. Si k es muy grande, el clasificador se vuelve demasiado suave.

## 4.5 Propiedades y Limitaciones de Métodos Basados en Distancia

Los métodos basados en distancia tienen varias propiedades importantes. Primero, son ejemplos de algoritmos **perezosos** (lazy): no construyen un modelo explícito durante el entrenamiento. En su lugar, memorizan simplemente los datos de entrenamiento. Cuando se presenta una instancia de consulta, el algoritmo realiza el trabajo (encontrar vecinos cercanos) en ese momento. Esto contrasta con algoritmos como el perceptrón que construyen un modelo explícito durante el entrenamiento. La ventaja es que el entrenamiento es instantáneo. La desventaja es que la clasificación es lenta porque necesitamos buscar a través de todos los datos de entrenamiento, y los algoritmos se adaptan bien a datos locales pero pueden tener dificultades en espacios de alta dimensión.

Los métodos basados en distancia también sufren de la **maldición de la dimensionalidad** de una manera particular: en espacios de alta dimensión, todos los puntos tienden a estar aproximadamente a la misma distancia el uno del otro. La noción de "cercano" se vuelve menos significativa, por lo que el método pierde efectividad. Por esta razón, a menudo es útil realizar reducción de dimensionalidad antes de aplicar métodos basados en distancia.

---

# TEMA 5: MÉTODOS LINEALES Y REDES NEURONALES

## 5.1 Modelos Lineales para Clasificación

Después de estudiar métodos bayesianos y métodos basados en distancia, ahora consideramos una familia diferente de modelos: los modelos lineales. Los modelos lineales son el punto de partida natural para muchos algoritmos de machine learning porque son simples de entender, rápidos de entrenar, y a menudo proporcionan un desempeño sorprendentemente bueno, incluso en problemas complejos.

La idea fundamental es que la decisión se puede tomar basada en una combinación lineal de las características de entrada. Para un problema de clasificación binaria, la función discriminante lineal más simple es:

g(x) = θᵀx + θ₀

Donde θ es un vector de pesos y θ₀ es un sesgo. El resultado g(x) es un número real. Para clasificar, comparamos este número con cero: si g(x) > 0, asignamos la instancia a la clase positiva; si g(x) < 0, asignamos a la clase negativa.

Geométricamente, la superficie donde g(x) = 0 es un hiperplano que divide el espacio en dos regiones. El vector θ es perpendicular a este hiperplano y define su orientación, mientras que el sesgo θ₀ controla la posición del hiperplano en el espacio. Esta interpretación geométrica es poderosa: claramente, no todos los problemas de clasificación pueden ser resueltos con un único hiperplano. Si las clases están entrelazadas de maneras complejas, ningún hiperplano será capaz de separarlas bien. Pero para problemas donde las clases son aproximadamente linealmente separables, los modelos lineales son excelentes.

Para problemas multiclase con múltiples clases W = {ω₁, ω₂, ..., ω|W|}, extendemos la idea teniendo una función discriminante por cada clase:

gₖ(x) = θₖᵀx + θ₀ₖ    para k = 1, 2, ..., |W|

Luego clasificamos usando la regla del máximo:

ω̂ = arg max gₖ(x)
     k

En otras palabras, asignamos la instancia a la clase cuya función discriminante produce el valor más alto.

## 5.2 Entrenamiento de Modelos Lineales

Ahora que tenemos la forma del modelo, la pregunta es: ¿cómo encontramos los parámetros θ? El enfoque es formular esto como un problema de optimización.

Definimos una función de objetivo J(θ) que mide qué tan bien el modelo con parámetros θ realiza en el conjunto de entrenamiento. La función de objetivo típicamente toma la forma:

J(θ) = (1/|D|) Σᵢ L(g(xᵢ; θ), ωᵢ)

Donde L es una función de pérdida que penaliza predicciones incorrectas. El objetivo es encontrar θ que minimiza esta función de objetivo:

θ* = arg min J(θ)
      θ

Para algunos problemas y funciones de pérdida, existe una solución analítica en forma cerrada. Sin embargo, en general, necesitamos usar métodos de optimización iterativa. El más fundamental de estos es el **descenso por gradiente**.

El descenso por gradiente es basado en una idea simple pero poderosa: el gradiente de una función apunta en la dirección de máxima pendiente ascendente. Si queremos minimizar la función, debemos movernos en la dirección opuesta al gradiente. El algoritmo funciona así:

1. Inicializar θ con valores aleatorios
2. Repetir hasta convergencia:
   - Calcular el gradiente: ∇J(θ)
   - Actualizar: θ ← θ - η∇J(θ)

Donde η es la **tasa de aprendizaje**, un parámetro que controla cuán grandes son los pasos que damos. Si η es muy pequeño, el aprendizaje es lento. Si η es muy grande, podríamos saltar sobre el mínimo y diverger.

La convergencia se determina típicamente por una condición como ||η∇J(θ)|| < δ para algún umbral pequeño δ.

## 5.3 El Perceptrón

El Perceptrón, introduceido por Frank Rosenblatt en 1958, es un ejemplo histórico importante de un modelo lineal para clasificación. Es notablemente simple: toma un modelo lineal y lo envuelve en una función de paso:

ω̂ = sign(θᵀx + θ₀)

Donde la función sign produce +1 si el argumento es positivo y -1 si es negativo. Esta es exactamente la regla de decisión que describrimos antes para modelos lineales.

Lo que distingue al Perceptrón es su **algoritmo de entrenamiento**. El Perceptrón usa una función de pérdida muy simple: penaliza solo los puntos mal clasificados. Si un punto es bien clasificado, su pérdida es cero; si está mal clasificado, su pérdida es positiva. Esta función de pérdida muy simple conduce a un algoritmo de entrenamiento muy simple:

Para cada punto de entrenamiento (xᵢ, ωᵢ):
    Si el punto está mal clasificado (sign(θᵀxᵢ + θ₀) ≠ ωᵢ):
        Actualizar: θ ← θ + ηωᵢxᵢ

Es decir, si clasificamos mal un punto positivo, aumentamos los pesos en la dirección del punto. Si clasificamos mal un punto negativo, disminuimos los pesos en esa dirección.

Una propiedad teórica importante del Perceptrón es que converge garantizado si los datos son **linealmente separables** (si existe un hiperplano que separa perfectamente las dos clases). Sin embargo, si los datos no son linealmente separables, el Perceptrón puede oscilar indefinidamente sin converger. Esto es una limitación seria.

Peor aún, incluso si los datos son linealmente separables, hay infinitos hiperplanos que pueden separarlos. ¿Cuál elige el Perceptrón? Resulta que depende del orden en que procesamos los puntos de entrenamiento y de la inicialización. El Perceptrón no proporciona ninguna garantía sobre cuál de los hiperplanos de separación encontrará.

## 5.4 Limitaciones del Perceptrón y Modelos Lineales

La limitación más fundamental del Perceptrón y otros modelos lineales es que solo pueden aprender fronteras de decisión lineales. Hay clases de problemas que simplemente no son linealmente separables.

El ejemplo más famoso es el **problema XOR**. XOR (exclusive or) es una función booleana simple:

Entrada 1, Entrada 2 → Salida
0, 0 → 0
0, 1 → 1
1, 0 → 1
1, 1 → 0

Si grafiamos estos puntos en un plano 2D, vemos que no existe una línea recta que pueda separarlos. Los puntos (0,0) y (1,1) (que producen 0) están en diagonal opuesta de los puntos (0,1) y (1,0) (que producen 1). Un hiperplano lineal no puede capturar esta relación.

Marvin Minsky y Seymour Papert demostraron esto rigosamente en 1969 en su libro "Perceptrons", que llevó a una disminución significativa en la investigación de redes neuronales durante años. Sin embargo, el análisis de Minsky y Papert también sugería la solución: si usamos múltiples capas de perceptrones, conectados de manera apropiada, entonces podemos resolver problemas como XOR.

## 5.5 Redes Neuronales Multicapa

La idea de que múltiples capas de perceptrones conectados pueden resolver problemas más complejos condujo al desarrollo de las **redes neuronales multicapa (MLP)**.

Una MLP es una colección de unidades de perceptrón organizadas en capas. Típicamente hay una capa de entrada, una o más capas ocultas, y una capa de salida. La información fluye hacia adelante desde la entrada hacia la salida (estas se llaman redes feedforward). Cada unidad en una capa está conectada a cada unidad en la capa siguiente; se dice que la red es completamente conectada.

La capa de entrada tiene d neuronas, una para cada característica. Estas simplemente pasan los valores de entrada sin procesamiento.

Las capas ocultas son donde ocurre la magia. Cada neurona en una capa oculta realiza una transformación no-lineal de sus entradas. La no-linealidad es crítica: sin ella, múltiples capas serían equivalentes a una única capa lineal. Las funciones de activación no-lineales comunes incluyen la función sigmoide σ(x) = 1/(1 + e^(-x)), la tangente hiperbólica tanh(x), y la unidad lineal rectificada ReLU(x) = max(0, x).

La capa de salida produce las predicciones finales. Para problemas de regresión, la capa de salida simplemente produce un valor continuo. Para problemas de clasificación, la capa de salida tiene una neurona por clase, y sus salidas se pueden interpretar como puntuaciones o (usando una función softmax) como probabilidades.

## 5.6 Aprendizaje en Redes Neuronales Multicapa

Entrenar una red neuronal multicapa es más complejo que entrenar un perceptrón porque necesitamos actualizar los pesos en todas las capas, no solo en la última capa. La solución es un algoritmo llamado **retropropagación (backpropagation)**.

El entrenamiento procede en cuatro pasos:

1. **Forward Pass**: Presentamos una instancia de entrada a la red y la procesamos hacia adelante a través de todas las capas, computando las activaciones de cada neurona.

2. **Pérdida Computation**: Comparamos la salida de la red con el objetivo. Para regresión, usamos típicamente error cuadrático medio (MSE). Para clasificación, usamos típicamente entropía cruzada categórica.

3. **Backward Pass (Retropropagación)**: Computamos el gradiente del error con respecto a cada peso usando la regla de la cadena. Comenzamos en la capa de salida, computamos cómo el error cambia con respecto a los pesos de salida, luego propaguemos estos gradientes hacia atrás a través de las capas ocultas.

4. **Weight Update**: Usamos los gradientes para actualizar todos los pesos, típicamente usando descenso por gradiente estocástico o variantes como Momentum o Adam.

El algoritmo de retropropagación es poderoso pero requiere cuidado en la implementación. Un problema común es el **vanishing gradient problem**: conforme los gradientes se propagan hacia atrás a través de muchas capas, se multiplican por las derivadas de las funciones de activación. Si estas derivadas son menores que 1 (como con sigmoid que tiene derivada máxima de 0.25), los gradientes se hacen cada vez más pequeños, y el aprendizaje en las capas tempranas se vuelve muy lento.

Este problema es una razón por la cual las funciones de activación más recientes como ReLU son preferidas: su derivada es 1 para entradas positivas, evitando el vanishing gradient.

Otro desafío es el **overfitting**. Las redes neuronales pueden ser arbitrariamente complejas dependiendo del número de capas ocultas y neuronas en cada capa. Una red muy compleja puede memorizar los datos de entrenamiento incluyendo sus particularidades y ruido. Para mitigar esto, usamos técnicas como **regularización L1/L2** (añadir penalizaciones para pesos grandes), **dropout** (desconectar neuronas aleatoriamente durante entrenamiento), y **early stopping** (parar el entrenamiento cuando el error de validación comienza a aumentar).

## 5.7 Teorema de Aproximación Universal

Un resultado teórico profundo sobre redes neuronales es el **Teorema de Aproximación Universal**. Este teorema dice que una red neuronal feedforward con al menos una capa oculta de un número suficiente de neuronas, usando activaciones no-lineales, puede aproximar cualquier función continua en un espacio compacto con exactitud arbitraria.

Esto es un resultado sorprendente: básicamente dice que, en principio, las redes neuronales son lo suficientemente expresivas para representar cualquier relación razonable entre entradas y salidas. Sin embargo, es importante entender las limitaciones de este teorema. Primero, no dice cuántas neuronas necesitamos; para algunos problemas, podría necesitamos un número imprácticamente grande. Segundo, no garantiza que podamos encontrar los pesos correctos con nuestros algoritmos de entrenamiento; solo dice que existen. Tercero, no aborda la generalización; la red podría aproximar la función en los datos de entrenamiento pero fallar en datos nuevos.

---

# TEMA 6: APRENDIZAJE NO SUPERVISADO

## 6.1 Introducción al Aprendizaje No Supervisado

Hasta ahora hemos enfatizado principalmente problemas de aprendizaje supervisado donde tenemos datos etiquetados que guían el aprendizaje. Sin embargo, en el mundo real, es a menudo más fácil recopilar datos sin etiquetar que datos etiquetados. El aprendizaje no supervisado aborda esta situación: trabajamos con datos sin etiquetas y tratamos de encontrar estructura o patrones ocultos en los datos.

El aprendizaje no supervisado es valioso por varias razones. Primero, como mencionamos, es a menudo la única opción cuando no tenemos datos etiquetados. Segundo, el aprendizaje no supervisado puede ayudar a guiar la exploración de datos y sugerir hipótesis interesantes sobre la estructura de los datos. Tercero, los resultados del aprendizaje no supervisado pueden ser usados como preprocesamiento para tareas supervisadas. Por ejemplo, podríamos usar clustering no supervisado para crear grupos de clientes similares, y luego entrenar modelos supervisados en cada grupo de forma individual.

Las tareas principales en aprendizaje no supervisado incluyen clustering (agrupar datos similares), reducción de dimensionalidad (encontrar representaciones de menor dimensión que capturan lo esencial de los datos), y detección de anomalías (identificar puntos que difieren significativamente del patrón general).

## 6.2 Clustering

### 6.2.1 Concepto Fundamental

El **clustering** o agrupamiento es la tarea de dividir un conjunto de datos en grupos donde elementos dentro del mismo grupo son similares entre sí, y elementos en grupos diferentes son disimilares. La pregunta fundamental es: ¿qué significa "similar"?

En los problemas de clustering que consideraremos, estamos usando la proximidad espacial como medida de similitud. Es decir, dos puntos son similares si están cercanos en el espacio de características. Esta es una definición natural y es lo que la mayoría de algoritmos de clustering implementan, aunque tenga limitaciones. Por ejemplo, podría haber estructura que no está capturada por proximidad espacial, o el significado de "cercano" podría variar a través del espacio.

Un resultado de clustering divide el conjunto de datos D en subconjuntos disjuntos C = {C₁, C₂, ..., C_k} tales que su unión es el conjunto completo. Cada punto pertenece a exactamente un cluster.

### 6.2.2 Taxonomía de Algoritmos de Clustering

Hay varias formas de categorizar algoritmos de clustering. Una distinción importante es entre **clustering particional** y **clustering jerárquico**.

En el clustering particional, el resultado es una simple partición plana: un conjunto de clusters sin estructura jerárquica. El algoritmo k-means es el ejemplo más prominente. Los datos se asignan a uno de k clusters, y eso es todo.

En el clustering jerárquico, el resultado es un árbol llamado dendrograma que muestra cómo se agrupan elementos de forma jerárquica. Hay dos aproximaciones: **aglomerativa** (bottom-up) donde comenzamos con cada punto como su propio cluster y fusionamos clusters progresivamente, y **divisiva** (top-down) donde comenzamos con un cluster conteniendo todos los puntos y dividimos recursivamente.

Dentro del clustering particional, hay también una distinción entre **hard clustering** (cada punto pertenece a exactamente un cluster), **soft clustering** (cada punto tiene un grado de membresía en cada cluster), y **fuzzy clustering** (un caso especial de soft clustering donde los grados de membresía siguen ciertas propiedades matemáticas).

### 6.2.3 El Algoritmo k-means

El algoritmo **k-means** es probablemente el algoritmo de clustering más ampliamente usado. Es simple de entender, rápido de implementar, y a menudo produce resultados prácticos útiles.

La idea central es encontrar k puntos en el espacio (llamados centroides) tales que cuando asignamos cada punto al centroide más cercano, la varianza total dentro de cada cluster sea minimizada. Esta cantidad se llama la **suma de cuadrados intracluster (WCSS)**:

WCSS = Σₖ Σ_{x ∈ Cₖ} ||x - μₖ||²

Donde μₖ es el centroide del cluster k.

El algoritmo funciona iterativamente usando el algoritmo de Lloyd:

1. **Inicialización**: Elegir k puntos iniciales como centroides. Este paso es importante porque la inicialización afecta el resultado final.

2. **Asignación**: Para cada punto x, asignarlo al cluster cuyo centroide está más cercano. Esto particiona los datos en k grupos.

3. **Actualización**: Para cada cluster, recalcular el centroide como el promedio de todos los puntos en ese cluster.

4. **Convergencia**: Repetir los pasos 2 y 3 hasta que los centroides no cambien (o cambien por menos de un umbral).

Cada iteración disminuye (o mantiene igual) el WCSS, por lo que el algoritmo converge. Sin embargo, converge a un mínimo local, no necesariamente al mínimo global. El resultado depende de la inicialización.

Una mejora importante es el algoritmo **k-means++**, que elige iniciales centroides más sabiamente:

1. Elegir el primer centroide aleatoriamente de los datos.
2. Para cada punto x, computar la distancia d(x) al centroide más cercano ya elegido.
3. Elegir el siguiente centroide con probabilidad proporcional a d(x)².
4. Repetir hasta que tengamos k centroides.

La intuición es que queremos que los centroides iniciales estén alejados unos de otros. Al elegir con probabilidad proporcional a d(x)², puntos que están lejos de centroides existentes tienen mayor probabilidad de ser elegidos.

### 6.2.4 Determinación del Número de Clusters

Un desafío fundamental con k-means es que necesitamos especificar k (el número de clusters) antes de ejecutar el algoritmo. Pero en problemas reales, no sabemos cuántos clusters hay realmente. Varias técnicas ayudan con esto.

El **método del codo** grafica k versus WCSS. Conforme k aumenta, WCSS disminuye, como se espera: más clusters significa menos varianza. Sin embargo, después de cierto punto, aumentar k produce disminuciones muy pequeñas en WCSS. El "codo" de la curva, donde el cambio en pendiente es más pronunciado, sugiere el número óptimo de clusters. La intuición es que este es el punto donde hemos encontrado la estructura real en los datos, y aumentar k más allá simplemente está dividiendo clusters reales.

El **método de silueta** es más cuantitativo. Para cada punto, computamos un coeficiente de silueta que mide cuán bien encaja el punto en su cluster comparado con otros clusters. Para un punto x en cluster Cⱼ, la silueta es:

s(x) = (b(x) - a(x)) / max(a(x), b(x))

Donde a(x) es la distancia promedio dentro del cluster (cohesión) y b(x) es la distancia mínima promedio a otros clusters (separación). La silueta está en el rango [-1, 1]. Un valor positivo significa que el punto está mejor en su cluster que en otros clusters. El promedio de silueta sobre todos los puntos da una medida del desempeño del clustering. Elegimos k que maximiza el coeficiente de silueta promedio.

### 6.2.5 Fortalezas y Debilidades de k-means

El algoritmo k-means tiene varias fortalezas. Es simple de entender e implementar. Es computacionalmente eficiente, con complejidad O(nkdI) donde I es el número de iteraciones. Se ha demostrado que funciona bien en muchas aplicaciones prácticas.

Sin embargo, también tiene debilidades importantes. El algoritmo es sensible a la inicialización; diferentes inicializaciones pueden producir resultados muy diferentes. El algoritmo puede quedar atrapado en mínimos locales. El operador de media es sensible a outliers: un único punto muy alejado puede tirar el centroide significativamente.

Una alternativa que es más robusta a outliers es **k-medoids**, donde los centroides se constriñen a ser puntos de datos reales (en lugar de cualquier punto en el espacio). El "centroide" de un cluster es el punto dentro del cluster que minimiza la distancia promedio a otros puntos en el cluster.

## 6.3 Reducción de Dimensionalidad

### 6.3.1 Motivación: Maldición de Dimensionalidad

Hemos mencionado la "maldición de dimensionalidad" varias veces. Vale la pena entender bien este concepto porque es fundamental para muchos problemas de machine learning en el mundo real.

Cuando el número de características d es muy grande, varios problemas emergen. Primero, el espacio de características se vuelve exponencialmente grande. Si cada característica puede tomar 10 valores discretos y tenemos d = 20 características, hay 10²⁰ = 100 quintillones de posibilidades. Si solo tenemos 1 millón de datos de entrenamiento, entonces estamos muestreando menos de 1 en 100 billones de posibilidades. El espacio está enormemente escaso.

Segundo, esta escasez causa problemas prácticos severos. En espacios de alta dimensión, los algoritmos basados en distancia se vuelven inefectivos porque todos los puntos tienden a estar aproximadamente a la misma distancia. Las nociones intuitivas de "cercano" desaparecen. Los algoritmos tienden a sobraje ustarse porque tienen mucha libertad para memorizar particularidades de los datos de entrenamiento.

Tercero, la complejidad computacional aumenta dramáticamente. Muchos algoritmos tienen complejidad que escala con la dimensionalidad, lo que hace que sean impracticales para espacios de alta dimensión.

Hay varias estrategias para mitigar la maldición de la dimensionalidad. La **selección de características** implica elegir un subconjunto de las características originales que son más relevantes para la tarea. La **regularización** implica añadir restricciones al modelo para penalizar la complejidad. La **reducción de dimensionalidad** implica transformar el espacio de características en uno de menor dimensión mientras se retiene la máxima información relevante.

### 6.3.2 Análisis de Componentes Principales (PCA)

El **Análisis de Componentes Principales (PCA)** es uno de los métodos más importantes y ampliamente usados para reducción de dimensionalidad. Es un método lineal que busca direcciones en el espacio de características que capturan la máxima varianza en los datos.

La intuición es simple: si los datos varían mucho en una dirección particular, esa dirección es probablemente importante para distinguir entre diferentes tipos de datos. Direcciones donde los datos varían poco probablemente contienen poco información útil y pueden ser descartadas.

Matemáticamente, el algoritmo funciona así:

1. **Preprocesar**: Centrar los datos restando la media de cada característica. Esto asegura que el promedio es cero.

2. **Matriz de covarianza**: Computar la matriz de covarianza Σ = (1/(n-1)) XᵀX, donde X es la matriz de datos centrados.

3. **Eigenvectores**: Encontrar los eigenvectores de Σ. Los eigenvectores son direcciones especiales donde la matriz solo escala el vector (no lo rota). Los eigenvalores asociados indican cuánta varianza hay en esa dirección.

4. **Ordenar**: Ordenar los eigenvectores por sus eigenvalores, del mayor al menor. El eigenvector con el eigenvalor más grande es la dirección de máxima varianza.

5. **Proyectar**: Para reducir de d dimensiones a d' dimensiones, usar los d' eigenvectores superiores para proyectar los datos:

x_proj = x · V

Donde V es la matriz de d' eigenvectores.

Una medida importante es la **varianza acumulada**:

CumVar(d') = (Σᵈ'ᵢ₌₁ λᵢ) / (Σᵈⱼ₌₁ λⱼ)

Esto mide qué fracción de la varianza total es capturada por las d' primeras componentes principales. Por ejemplo, si CumVar(5) = 0.95, significa que usando solo 5 componentes principales, retenemos 95% de la varianza en los datos, y probablemente podemos descartar las otras d-5 características sin perder mucha información.

Las ventajas de PCA son que es rápido (complejidad O(d² × n) donde d es la dimensionalidad y n es el número de muestras), es teóricamente bien fundamentado, y produce interpretable (los eigenvectores mostrar combinaciones lineales de las características originales).

Las limitaciones son que PCA es un método lineal. Si la estructura en los datos es altamente no-lineal, PCA podría no ser efectivo. Además, PCA intenta preservar varianza global, que podría no ser lo que queremos. En algunos casos, queremos preservar estructura local (datos cercanos permanecen cercanos) en lugar de varianza global.

### 6.3.3 t-SNE (t-Stochastic Neighbor Embedding)

Mientras que PCA es un método lineal que preserva varianza global, **t-SNE** es un método no-lineal que se enfoca en preservar estructura local. Es especialmente popular para visualización.

La idea central es que en espacios de alta dimensión, computamos similitudes pairwise entre todos los puntos (típicamente usando una función gaussiana de distancia). Luego, en el espacio de baja dimensión (típicamente 2D para visualización), buscamos una configuración de puntos que tenga similitudes pairwise lo más cercanas posible a las del espacio original.

Lo que hace que t-SNE sea "estocástico" es que modela las similitudes como probabilidades en lugar de distancias diréctas, y la "t" se refiere a usar la distribución t-Student en el espacio proyectado en lugar de gaussiana.

Una ventaja importante de t-SNE es que produce visualizaciones que a menudo revelan estructura clara y clustering en los datos. Los puntos que son similares en el espacio original tienden a quedar cerca en la visualización. Sin embargo, t-SNE tiene limitaciones. Es computacionalmente costoso, especialmente para datasets grandes. También puede distorsionar la estructura global; solo se enfoca en vecindades locales. Por esto, t-SNE es principalmente útil para visualización, no para preprocesamiento de datos para algoritmos posteriores.

---

# TEMA 7: COMPARACIÓN ESTADÍSTICA DE MODELOS

## 7.1 Introducción a Pruebas Estadísticas para Comparación de Modelos

Después de desarrollar varios modelos de machine learning, inevitablemente surge la pregunta: ¿cuál modelo es mejor? Esta pregunta requiere comparación estadística rigurosa porque las diferencias que observamos en el desempeño podrían simplemente ser debidas al azar en lugar de diferencias verdaderas.

El marco de las pruebas de hipótesis estadísticas proporciona una manera formal de responder esta pregunta. Mientras que el detalle técnico puede ser abrumador, la idea fundamental es simple: asumimos una hipótesis nula (por ejemplo, "no hay diferencia entre los dos modelos") y preguntamos si los datos observados son consistentes con esta hipótesis. Si los datos son muy improbables bajo la hipótesis nula, rechazamos la hipótesis y concluimos que hay una diferencia verdadera.

## 7.2 Comparación de Dos Modelos

### Prueba t-Pareada

Cuando comparamos dos modelos, una pregunta natural es: ¿en promedio, cuál tiene mejor desempeño? La **prueba t-pareada** es una prueba estadística común para responder esto cuando tenemos múltiples datasets de evaluación.

El procedimiento es:

1. Entrenar ambos modelos en cada dataset y computar su desempeño (por ejemplo, precisión).

2. Computar las diferencias: dᵢ = Perf₁(Dᵢ) - Perf₂(Dᵢ) para cada dataset.

3. Computar la media y desviación estándar de las diferencias.

4. Calcular el estadístico t: t = d̄ / (s / √m) donde d̄ es la media de diferencias, s es la desviación estándar, y m es el número de datasets.

5. Comparar con el valor crítico de la distribución t con m-1 grados de libertad.

Si el estadístico t es más grande (en valor absoluto) que el valor crítico, rechazamos la hipótesis nula y concluimos que hay una diferencia significativa entre los modelos.

La prueba t-pareada hace ciertos supuestos: que las diferencias siguen una distribución normal. Si este supuesto es violado, la prueba puede no ser fiable.

### Prueba de Wilcoxon Signed-Rank

La **prueba de Wilcoxon signed-rank** es una alternativa no-paramétrica a la prueba t-pareada que no asume normalidad. En su lugar, usa ranking.

El procedimiento es similar, pero en lugar de trabajar directamente con diferencias, las rangoseamos. Las ventajas son que es más robusto a outliers y no requiere supuestos de distribución. Las desventajas son que puede ser ligeramente menos poderosa (menos probable detectar diferencias verdaderas) si la normalidad se cumple.

## 7.3 Comparación de Múltiples Modelos

Cuando comparamos tres o más modelos, simplemente hacer muchas pruebas pairwise es problemático. Si hacemos 10 pruebas, cada una con nivel de significancia α=0.05, la probabilidad de obtener al menos un "falso positivo" (rechazar incorrectamente la hipótesis nula) es mucho mayor que 0.05.

Tests específicamente diseñados para comparación múltiple abordan este problema.

### Prueba de Friedman

La **prueba de Friedman** es una prueba no-paramétrica para comparar múltiples modelos. Funciona rangeando los modelos en cada dataset, del mejor al peor.

El procedimiento es:

1. Para cada dataset Dᵢ, ordenar los C modelos de mejor a peor y asignar rangos 1, 2, ..., C.

2. Computar el rango promedio para cada modelo: R̄ⱼ = (1/M) Σᵢ Rᵢⱼ

3. Calcular el estadístico de Friedman: χ²_F = [12M / (C(C+1))] · Σⱼ R̄²ⱼ - 3M(C+1)

4. Comparar con el valor crítico de la distribución chi-cuadrada con C-1 grados de libertad.

Si el estadístico es mayor que el valor crítico, rechazamos la hipótesis nula y concluimos que hay diferencias significativas entre los modelos.

### Tests Post-Hoc

Después de encontrar que hay diferencias significativas (usando Friedman o ANOVA), queremos saber CUÁLES pares de modelos difieren significativamente. Esto requiere tests post-hoc.

Un test post-hoc común es el **test de Nemenyi**, que compara todos los pares. La idea es computar una "diferencia crítica" (CD):

CD = qₐ(C) · √[C(C+1) / (6M)]

Donde qₐ(C) es un valor crítico tabulado. Dos modelos i y j se consideran significativamente diferentes si |R̄ᵢ - R̄ⱼ| > CD.

Otro test post-hoc es el **test de Bonferroni-Dunn**, que compara todos los modelos contra un modelo de referencia en lugar de hacer todas las comparaciones pairwise. Esto reduce el número de comparaciones.

## 7.4 Ejemplo Práctico Completo

Para solidificar la comprensión, consideremos un ejemplo concreto. Supongamos que hemos desarrollado 4 clasificadores diferentes y queremos compararlos usando 6 datasets diferentes. Medimos accuracy en cada dataset:

Dataset    Clf1    Clf2    Clf3    Clf4
-----------
D1         70      73      78      82
D2         68      76      75      80
D3         72      74      79      85
D4         69      72      78      81
D5         71      74      77      82
D6         67      70      73      79

Primero, aplicamos la prueba de Friedman para determinar si hay diferencias significativas.

Rangeamos los modelos en cada dataset:

D1: Clf4(1), Clf3(2), Clf2(3), Clf1(4)
D2: Clf4(1), Clf2(2), Clf3(3), Clf1(4)
D3: Clf4(1), Clf3(2), Clf2(3), Clf1(4)
D4: Clf4(1), Clf3(2), Clf2(3), Clf1(4)
D5: Clf4(1), Clf3(2), Clf2(3), Clf1(4)
D6: Clf4(1), Clf3(2), Clf2(3), Clf1(4)

Computamos rangos promedio:
R̄₁ = (4+4+4+4+4+4)/6 = 4
R̄₂ = (3+2+3+3+3+3)/6 = 2.83
R̄₃ = (2+3+2+2+2+2)/6 = 2.17
R̄₄ = (1+1+1+1+1+1)/6 = 1

Calculamos el estadístico de Friedman:
χ²_F = (12·6)/(4·5) · (16 + 8.01 + 4.71 + 1) - 3·6·5
     = 0.6 · 29.72 - 90
     = 17.83 - 1.83 = 17

Comparamos con χ²₀.₀₅,₃ = 7.815. Como 17 > 7.815, rechazamos H₀ y concluimos que hay diferencias significativas entre los modelos.

Luego aplicamos el test de Nemenyi para ver cuáles pares difieren:

CD = 2.403 · √(4·5 / (6·6)) = 2.403 · 0.745 = 1.79

Comparaciones (|R̄ᵢ - R̄ⱼ|):
|R̄₁ - R̄₂| = 1.17 < 1.79 → No significativo
|R̄₁ - R̄₃| = 1.83 > 1.79 → Significativo
|R̄₁ - R̄₄| = 3.00 > 1.79 → Significativo
|R̄₂ - R̄₃| = 0.66 < 1.79 → No significativo
|R̄₂ - R̄₄| = 1.83 > 1.79 → Significativo
|R̄₃ - R̄₄| = 1.17 < 1.79 → No significativo

Conclusión: Clf4 es significativamente mejor que Clf1 y Clf2. Clf1, Clf2, y Clf3 no son significativamente diferentes entre sí.

---

## CONCLUSIONES Y SÍNTESIS FINAL

A lo largo de este libro, hemos viajado a través de los fundamentos del Aprendizaje Automático, desde los principios teóricos de la teoría bayesiana hasta los algoritmos prácticos implementados en el mundo real.

Hemos visto que el Aprendizaje Automático no es una colección de trucos desconectados, sino un conjunto coherente de principios guiados por conceptos fundamentales. El Teorema de Bayes proporciona la base teórica. La teoría de evaluación nos enseña cómo medir realmente si estamos teniendo éxito. El concepto de sesgo-varianza nos muestra los tradeoffs fundamentales entre complejidad del modelo y generalización.

Hemos explorado múltiples familias de algoritmos: métodos bayesianos paramétricos, métodos no-paramétricos basados en distancia, modelos lineales, redes neuronales, algoritmos de clustering, y técnicas de reducción de dimensionalidad. Cada uno tiene fortalezas y debilidades, y el practicante informado entiende cuándo usar cuál.

El tema de evaluación es quizás más importante que cualquier algoritmo específico. La mejor precisión en datos de entrenamiento no significa nada si el modelo no generaliza. Validación cruzada, tests estadísticos, y cuidadosa evaluación son el corazón de la práctica de ML.

Finalmente, entendemos que el Aprendizaje Automático no es un sustituto para el pensamiento; es una herramienta para potenciarlo. Recolectar buenos datos, entender el dominio del problema, elegir métricas significativas, interpretar resultados críticamente: estas habilidades son tan importantes como entender los algoritmos.

El campo del Aprendizaje Automático está evolucionando rápidamente, con nuevos algoritmos y técnicas emergiendo constantemente. Pero los principios fundamentales que hemos cubierto aquí permanecerán vigentes. Armado con estos fundamentos, el estudiante está bien preparado para aprender nuevas técnicas a medida que emergen.

