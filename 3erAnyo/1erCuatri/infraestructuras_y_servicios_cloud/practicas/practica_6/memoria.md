# Informe: Módulo 3 - Implementación de una canalización de aprendizaje automático con Amazon SageMaker

**Jordi Blasco Lozano**  
**Fundamentos de Machine Learning - AWS Academy**  
**Universidad de Alicante**  
**Diciembre de 2025**

## Resumen

Este informe documenta el módulo 3 del curso AWS Machine Learning Foundations, centrado en la implementación de canalizaciones completas de aprendizaje automático utilizando Amazon SageMaker. Se describe el ciclo de vida completo del aprendizaje automático, desde la formulación del problema hasta el despliegue en producción, pasando por la recolección, preparación, entrenamiento y evaluación de modelos.


## 1. Formulación del Problema de Machine Learning

### 1.1. Definición del Tipo de Problema

La formulación correcta del problema es el paso inicial y más crítico en cualquier proyecto de aprendizaje automático. En esta fase se determina si estamos ante un problema de clasificación, regresión, clustering o una tarea más compleja como procesamiento de lenguaje natural o visión por computadora. La formulación del problema establece el marco sobre el cual se construirá toda la arquitectura de datos y el modelo correspondiente.

Durante la formulación, debemos identificar claramente cuál es el objetivo empresarial que queremos alcanzar. No se trata simplemente de "predecir algo", sino de entender qué decisiones empresariales se tomarán basándose en las predicciones del modelo, cuál es el impacto económico de las predicciones incorrectas y cuáles son las restricciones técnicas o regulatorias que debemos cumplir. Este análisis determinará tanto la métrica de éxito del modelo como los requisitos de datos.

### 1.2. Identificación de Variables y Objetivos

Una vez formulado el problema, se deben identificar las variables (features) que utilizaremos para realizar predicciones. Estas variables pueden ser numéricas, categóricas, temporales o de texto. Es fundamental comprender la relación entre estas variables y el objetivo que queremos predecir. Durante esta fase, realizamos un análisis exploratorio inicial para entender la distribución de las variables, identificar valores faltantes, detectar outliers y comprender correlaciones.

El objetivo o target es la variable que queremos predecir. Este puede ser numérico (en regresión), categórico (en clasificación) o una estructura más compleja. La selección del objetivo debe estar siempre alineada con el problema empresarial identificado en la fase anterior.

## 2. Recolección y Aseguramiento de Datos

### 2.1. Fuentes de Datos

Los datos pueden provenir de múltiples fuentes: bases de datos relaciones, data lakes, APIs externas, sistemas IoT, archivos CSV, databases no relacionales como DynamoDB, y muchas otras. AWS proporciona múltiples servicios para conectarse a estas fuentes: AWS Glue para descubrir y catalogar datos, Amazon RDS para bases de datos relacionales, Amazon DynamoDB para datos no estructurados, y Amazon S3 como almacenamiento centralizado.

En un proyecto típico, los datos se centralizan en Amazon S3, que actúa como el repositorio principal. Desde aquí, servicios como AWS Glue Crawlers pueden analizar automáticamente la estructura de los datos y crear un catálogo de metadatos accesible a otros servicios. Esta estructura permite que múltiples herramientas (Athena, SageMaker, Glue ETL) trabajen sobre los mismos datos sin duplicación.

### 2.2. Estrategias de Seguridad

La seguridad de los datos es una responsabilidad compartida entre AWS y el usuario (Shared Responsibility Model). AWS es responsable de la seguridad de la infraestructura cloud, mientras que el usuario es responsable de la seguridad de sus datos dentro de esa infraestructura. Para proteger datos sensibles, debemos implementar varias capas:

- **Cifrado en reposo**: Los datos almacenados en S3 deben cifrarse usando AWS KMS (Key Management Service) o cifrado gestionado por AWS.
- **Cifrado en tránsito**: Las conexiones entre servicios deben usar TLS/SSL. Al igual que lo hicimos en la práctica anterior con IoT Core, utilizamos certificados para autenticar las conexiones.
- **Control de acceso**: Mediante IAM (Identity and Access Management) definimos qué usuarios, roles y servicios pueden acceder a qué datos. El principio de menor privilegio es fundamental: cada servicio debe tener solo los permisos necesarios para realizar su función.
- **Auditoría y monitoreo**: CloudTrail registra todas las acciones sobre los datos, permitiendo identificar accesos no autorizados o actividades sospechosas.

## 3. Preparación de Datos: Extracción, Transformación y Carga (ETL)

### 3.1. Datos Crudos al Feature Store

La preparación de datos es frecuentemente la fase que consume más tiempo en un proyecto de machine learning, a menudo entre el 60-80% del tiempo total. Los datos crudos raramente están listos para entrenar modelos directamente; contienen valores faltantes, formatos inconsistentes, escalas diferentes y ruido que debe limpiarse.

El proceso comienza con la exploración y validación de datos. Utilizamos herramientas como SageMaker Data Wrangler para cargar datos desde múltiples fuentes, visualizar distribuciones, identificar valores anómalos y aplicar transformaciones interactivamente. Data Wrangler proporciona una interfaz visual que genera código Python automáticamente, permitiendo a los analistas sin experiencia en programación realizar transformaciones complejas.

### 3.2. Procesamiento de Datos con SageMaker Processing

Para transformaciones más complejas o que deben ejecutarse de forma recurrente, utilizamos SageMaker Processing. Este servicio permite ejecutar scripts de procesamiento (Python, PySpark, etc.) en instancias gestionadas sin necesidad de configurar clusters manualmente.

Un Processing Job típico consta de los siguientes pasos:

1. **Cargar datos**: Leer datos desde S3 u otras fuentes
2. **Procesar**: Aplicar transformaciones, limpieza, validación
3. **Guardar**: Escribir datos procesados nuevamente a S3

La estructura típica es crear un objeto `ScriptProcessor` que especifica qué imagen Docker ejecutar, cuántas instancias necesitamos, el tamaño de cada instancia y el rol IAM con permisos para acceder a S3. Luego creamos un `ProcessingJob` que especifica qué script ejecutar, dónde están los datos de entrada y dónde guardar los resultados.

### 3.3. Feature Engineering y Feature Store

El Feature Store de SageMaker es un repositorio centralizado que almacena features (características) procesadas reutilizables. En lugar de duplicar lógica de transformación en múltiples proyectos, definimos features una vez, las almacenamos en el Feature Store, y múltiples modelos pueden acceder a ellas de forma consistente.

El Feature Store proporciona:

- **Almacenamiento Online**: Para consultas en tiempo real con baja latencia, ideal para inferencia en tiempo real
- **Almacenamiento Offline**: Para procesamiento batch, ideal para entrenamiento e inferencia batch
- **Versionado**: Rastrear cambios en los features a lo largo del tiempo
- **Consistencia**: Los mismos features se utilizan en entrenamiento e inferencia, evitando la "skew" entre entrenamiento e inferencia

Los features se organizan en `Feature Groups`, cada uno representando un conjunto lógico de características relacionadas (por ejemplo, features de usuario, features de transacción). El Feature Store automáticamente sincroniza entre almacenamiento online y offline.

## 4. Entrenamiento del Modelo

### 4.1. Configuración del Trabajo de Entrenamiento

Una vez tenemos datos preparados, el siguiente paso es entrenar un modelo. SageMaker proporciona algoritmos integrados optimizados para AWS (XGBoost, Linear Learner, Image Classification, etc.) así como la capacidad de entrenar modelos personalizados usando frameworks como TensorFlow, PyTorch o scikit-learn.

Un Training Job se configura especificando:

- **Datos de entrada**: Ubicación en S3 de datos de entrenamiento y validación
- **Algoritmo o contenedor**: Qué algoritmo ejecutar o qué imagen Docker personalizada usar
- **Recursos de computación**: Tipo y número de instancias
- **Hiperparámetros**: Parámetros que controlan el comportamiento del algoritmo
- **Ubicación de salida**: Dónde guardar el modelo entrenado en S3

SageMaker maneja automáticamente la infraestructura: inicia instancias, descarga el código y datos, ejecuta el entrenamiento, y guarda el artefacto del modelo. El usuario solo paga por el tiempo de computación utilizado, sin necesidad de mantener servidores.

### 4.2. Ajuste Automático de Hiperparámetros (HPO)

Los hiperparámetros son parámetros que no se aprenden durante el entrenamiento, sino que se especifican antes de comenzar. Estos incluyen la tasa de aprendizaje, profundidad del árbol, número de épocas, etc. Encontrar los mejores hiperparámetros es un proceso iterativo que puede ser muy tedioso si se hace manualmente.

SageMaker Automatic Model Tuning automatiza este proceso. Define un rango de valores para cada hiperparámetro, especifica una métrica a optimizar (por ejemplo, AUC, RMSE, accuracy), y SageMaker ejecutará múltiples trabajos de entrenamiento con diferentes combinaciones de hiperparámetros, buscando la combinación que maximiza la métrica elegida.

El proceso utiliza estrategias inteligentes (búsqueda de rejilla, búsqueda aleatoria, o búsqueda bayesiana) para explorar el espacio de hiperparámetros de forma eficiente, evitando probar todas las combinaciones posibles. Es similar a una búsqueda guiada que aprende del historial de intentos anteriores.

### 4.3. SageMaker Studio y Jupyter Notebooks

SageMaker Studio es el entorno integrado de desarrollo para machine learning. Proporciona Jupyter Notebooks integrados con acceso directo a datos en S3, poder de computación escalable, y acceso a todos los servicios de SageMaker.

Los notebooks permiten el desarrollo iterativo: escribir código Python, ejecutarlo, visualizar resultados, ajustar parámetros, y volver a ejecutar. Esta interactividad es crucial durante las fases de exploración y experimentación. Los notebooks se ejecutan en instancias de computación gestionadas, cuyo tipo podemos cambiar según necesidades (desde instancias pequeñas para exploración hasta GPU para entrenamiento de modelos profundos).

## 5. Evaluación del Modelo

### 5.1. Métricas de Rendimiento

Una vez entrenado el modelo, debemos evaluar su desempeño en datos no utilizados durante el entrenamiento (datos de prueba). No evaluar con datos nuevos daría una visión demasiado optimista del rendimiento real.

Las métricas dependen del tipo de problema:

- **Clasificación binaria**: Accuracy, Precision, Recall, F1-Score, AUC-ROC, ROC Curve
- **Clasificación multiclase**: Macro/Micro Accuracy, Macro/Micro F1-Score
- **Regresión**: RMSE (Root Mean Squared Error), MAE (Mean Absolute Error), R² (Coefficient of Determination)

Cada métrica captura un aspecto diferente del rendimiento. Por ejemplo, en un problema de detección de fraude con clases desbalanceadas, la accuracy global puede ser engañosa; es más importante el recall (detectar la mayoría de los fraudes) aunque haya más falsos positivos.

### 5.2. Análisis de Resultados

Más allá de números, debemos entender por qué el modelo funciona de cierta forma. SageMaker proporciona herramientas para interpretabilidad:

- **Confusion Matrix**: Visualizar qué clases confunde el modelo
- **Residual Plots**: Para regresión, visualizar errores de predicción
- **SHAP Values**: Entender la contribución de cada feature a la predicción
- **Feature Importance**: Identificar qué features son más relevantes

Este análisis puede revelar sesgos en los datos, problemas de calidad de datos, o características que no son realmente predictivas. En lugar de aceptar el modelo con mejor métrica, realizamos análisis de error para entender sus limitaciones.

## 6. Registro y Gestión de Modelos

### 6.1. SageMaker Model Registry

No todos los modelos entrenados deben ir a producción. SageMaker Model Registry proporciona un repositorio centralizado donde registramos modelos que han pasado criterios de calidad específicos.

El Model Registry permite:

- **Almacenar modelos**: Versiones de modelos junto con metadatos (fecha de creación, autor, parámetros usados)
- **Comparar versiones**: Visualizar métricas lado a lado para diferentes versiones
- **Gestionar estados**: Un modelo puede estar en estados como "PendingManualApproval", "Approved", "Rejected" o "Archived"
- **Rastrear linaje**: Qué datos, código y parámetros produjo cada versión

### 6.2. Versionado y Seguimiento

Al registrar un modelo, almacenamos no solo el artefacto del modelo (los pesos entrenados), sino también metadatos críticos: qué versión del código lo entrenó, qué datos usamos, qué métricas obtuvo en validación. Este historial es invaluable cuando meses después necesitamos entender por qué un modelo antiguo funcionaba mejor, o cuando un modelo en producción comienza a degradarse.

Los metadatos incluyen:

- Métricas de evaluación (accuracy, RMSE, etc.)
- Fecha y hora de entrenamiento
- Autor/responsable
- Dataset versión utilizada
- Hiperparámetros
- Información de linaje: qué procesamiento y features se usaron

## 7. Despliegue en Producción

### 7.1. Creación de Endpoints

Una vez aprobado un modelo, lo desplegamos para hacer predicciones en datos nuevos. Un **Endpoint** es un servidor REST que sirve predicciones del modelo con baja latencia.

Para crear un endpoint:

1. Crear una **Model Config** especificando el modelo y la instancia donde ejecutarlo
2. Crear un **Endpoint Config** especificando configuración avanzada (variantes, número de instancias, etc.)
3. Crear el **Endpoint** que activa el servicio

El endpoint puede recibir solicitudes HTTP con datos y devuelve predicciones en tiempo real. SageMaker gestiona automáticamente el auto-scaling: si la carga aumenta, despliega más instancias; si disminuye, las retira.

### 7.2. Batch Transform

Para escenarios donde no necesitamos predicciones en tiempo real sino procesamiento de grandes volúmenes de datos, utilizamos **Batch Transform**. Este servicio toma un archivo de datos en S3, lo procesa en paralelo usando instancias de computación, y escribe predicciones nuevamente a S3.

Batch Transform es más económico que endpoints para grandes volúmenes porque inicia instancias solo durante el tiempo que tarda el procesamiento, sin mantenerlas constantemente disponibles.

## 8. Orquestación de Canalizaciones

### 8.1. SageMaker Pipelines

En proyectos reales, todo lo anterior (procesamiento, entrenamiento, evaluación, despliegue) ocurre múltiples veces. Nuevos datos llegan regularmente, modelos antiguos necesitan reciclarse, hiperparámetros se ajustan, etc. Orquestar todo esto manualmente es error-prone y laborioso.

SageMaker Pipelines automatiza estos flujos. Una pipeline define una serie de pasos:

- **ProcessingStep**: Ejecuta Processing Jobs para preparar datos
- **TrainingStep**: Entrena un modelo
- **EvaluationStep**: Evalúa el modelo y genera métricas
- **ConditionStep**: Toma decisiones (por ejemplo, "¿el nuevo modelo es mejor que el anterior?")
- **RegisterModelStep**: Registra modelos aprobados en Model Registry
- **TransformStep**: Ejecuta Batch Transform para predicciones masivas

Los pasos se encadenan definiendo dependencias: si el paso A debe ejecutarse antes del paso B, especificamos esa relación. SageMaker ejecuta pasos en paralelo cuando no hay dependencias, optimizando el tiempo total.

Las pipelines se definen en código Python usando la SDK de SageMaker, permitiendo versionarlas en Git junto con el resto del código. Esto es práctica recomendada: el código de producción debe estar bajo control de versiones.

### 8.2. CI/CD para Machine Learning

Las Pipelines de SageMaker son la base del CI/CD (Continuous Integration/Continuous Deployment) para machine learning. Combinadas con servicios como CodePipeline, CodeBuild y CodeCommit, podemos crear flujos completamente automatizados:

1. Un científico de datos hace commit de cambios a un repositorio Git
2. CodePipeline detecta el cambio y desencadena un flujo:
   - CodeBuild construye una imagen Docker con el código actualizado
   - La imagen se sube a Amazon ECR (Elastic Container Registry)
   - Se invoca una SageMaker Pipeline que:
     - Prepara datos
     - Entrena el modelo
     - Evalúa y compara con modelos anteriores
     - Si es mejor, lo registra automáticamente
     - Despliegua a un endpoint de prueba
   - Un aprobador humano verifica el modelo
   - Si aprueba, se despliega a producción

Este flujo es mucho más robusto que los scripts manuales: cambios de código desencadenan automáticamente nuevos entrenamientos, se evitan errores humanos, y hay un registro completo de qué código produjo qué modelo.

## 9. Conclusiones

El módulo 3 proporciona una visión completa del ciclo de vida del aprendizaje automático en la nube. Contrario a lo que muchos piensan, construir un modelo que funciona bien es solo una pequeña parte. El verdadero reto está en:

- Comprender el problema empresarial profundamente
- Obtener y preparar datos de calidad consistentemente
- Validar que los datos son seguros y cumplen regulaciones
- Entrenar modelos de forma reproducible
- Evaluar honestamente si un modelo es mejor que el anterior
- Desplegar de forma segura a producción
- Monitorear y actualizar cuando el rendimiento se degrada

SageMaker como plataforma intenta simplificar cada uno de estos aspectos. El Feature Store centraliza características; Pipelines automatiza flujos; Model Registry rastrea versiones; los Endpoints sirven predicciones en tiempo real con auto-scaling.

Lo que queda claro es que la infraestructura cloud no es solo computación: es orquestación, automatización, seguridad y observabilidad integradas. Un proyecto bien estructurado en SageMaker no solo es técnicamente superior, sino que es también operacionalmente más sostenible a largo plazo, permitiendo a equipos pequeños gestionar sistemas complejos de machine learning en producción.

---

**Fecha de finalización**: Diciembre de 2025