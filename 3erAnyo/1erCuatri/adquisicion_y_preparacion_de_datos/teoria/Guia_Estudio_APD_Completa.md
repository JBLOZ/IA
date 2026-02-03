# Guía Completa de Estudio: Adquisición y Preparación de Datos (APD) 2025

## Tabla de Contenidos
1. [Tema 1: Introducción a Datos y Big Data](#tema-1)
2. [Tema 2: Diseño Conceptual de Almacenes de Datos](#tema-2)
3. [Tema 3: Diseño Lógico de Almacenes de Datos](#tema-3)
4. [Tema 4: Preparación de Datos para IA con ETL](#tema-4)
5. [Tema 5: Introducción a la Integración de Datos mediante ETLs](#tema-5)
6. [Tema 6: Limpieza, Transformación y Normalización de Datos](#tema-6)
7. [Tema 7: Diseño de Flujos ETL con Jobs en Pentaho](#tema-7)
8. [Tema 8: Transformación y Enriquecimiento de Datos en LOD](#tema-8)
9. [Tema 9: Visualización y Reutilización de Datos](#tema-9)
10. [Tema 10: Infraestructuras para Almacenamiento y Procesamiento](#tema-10)
11. [Taller 1: Modelado Conceptual Práctico](#taller-1)

---

## TEMA 1: Introducción a Datos y Big Data {#tema-1}

### 1.1 ¿Qué es la Ciencia de Datos?

La ciencia de datos es un campo multidisciplinario que combina estadística, programación y conocimiento de dominio para extraer información valiosa de datos. No es un proyecto de una única persona, sino que requiere colaboración de múltiples roles:

- **Servidores y Arquitectura**: Infraestructura tecnológica
- **Programación**: Desarrollo de soluciones
- **Diseño**: Interfaz y experiencia
- **Análisis**: Interpretación de datos
- **Dirección**: Coordinación del proyecto

### 1.2 Roles Profesionales en Big Data

#### Ingeniero de Datos
- Lidia con problemas de recolección, gestión, transformación y publicación de datos
- Conocimientos: Modelado, SQL, NoSQL, ETL/ELT, Spark, MapReduce, Kafka, Flume
- Desarrollo y despliegue en la nube

#### Data Scientist
- Integra técnicas de ingeniería de datos con análisis estadístico y machine learning
- Conocimientos: Todo del ingeniero de datos + Estadística, R, Python, SAS, SPSS, Minería de datos, NLP, Machine Learning
- La línea divisoria entre ambas figuras no siempre es clara

### 1.3 Machine Learning y Proyectos de IA

Un proyecto de Machine Learning requiere:
- No solo conocimientos en técnicas de procesamiento de datos y algoritmos
- Sino también conocimiento profundo del dominio
- Fuerte dependencia y necesidad de comunicación entre desarrolladores y stakeholders
- Captura de numerosos requisitos (funcionales y no funcionales)

**Problema común**: Los proyectos de data warehouses, visualizaciones de usuario y proyectos de ML se abordan de manera independiente, ignorando:
- Posibles requerimientos cruzados
- Restricciones colectivas
- Dependencias entre salidas de diferentes sistemas
- Objetivos de negocio comunes

### 1.4 Ciclo de Vida del Dato

El ciclo de vida del dato consta de varias fases:

1. **Adquisición de datos**: Obtener datos de valor de fuentes internas y externas (bases de datos, ficheros Excel, informes, APIs)
2. **Almacenamiento**: Almacenar los datos de forma segura
3. **Procesamiento**: Transformar y procesar los datos
4. **Análisis**: Interpretar los datos
5. **Visualización**: Presentar los resultados
6. **Disposición**: Archivar o eliminar los datos

### 1.5 Introducción a Big Data

#### ¿Qué es Big Data?

"Forma de afrontar el procesamiento o análisis de grandes volúmenes de información que por su naturaleza desestructurada no pueden ser analizados, y en un tiempo aceptable, usando los procesos y herramientas tradicionales de BI" (IBM)

#### Las 5 V's de Big Data

1. **Volumen**: Capacidad para procesar grandes volúmenes de datos
   - 2000: 800.000 Petabytes
   - 2011: 1.8 Zettabytes
   - 2021: 35 Zettabytes
   - 2025: 175 Zettabytes
   - 1 Zettabyte = 10^6 Petabytes = 10^9 Terabytes = 10^12 Gigabytes

2. **Variedad**: Capacidad para soportar el aumento en la heterogeneidad de las fuentes a procesar
   - Datos estructurados (BD), semiestructurados (JSON, XML), no estructurados (imágenes, texto, vídeo)

3. **Velocidad**: Velocidad a la que fluye la información
   - Ejemplo: Telescopio SKA genera 10 petabytes/hora
   - Twitter: 350.000 tweets por minuto

4. **Veracidad**: Calidad y confiabilidad de los datos

5. **Valor**: Capacidad de extraer valor de los datos

#### Data Lakes

Un Data Lake es un almacén centralizado de datos en bruto (raw data):
- Múltiples formatos: estructurados, semiestructurados y no estructurados
- Escalable y flexible, pensado para grandes volúmenes de datos
- Ideal para análisis exploratorio, ciencia de datos e IA
- Bajo coste de almacenamiento, pero requiere buena gobernanza

**Data Swamp**: Data Lake MAL GESTIONADO
- Datos desorganizados, falta de metadatos ni controles de calidad
- Difíciles de explorar, mantener y extraer valor
- Duplicidades, inconsistencias → Pérdida de confianza

### 1.6 Nuevas Necesidades de Gestión de Datos

#### Entornos Económicos Altamente Competitivos

Las empresas necesitan pasar de preguntas simples a preguntas estratégicas:

- **Típica pregunta a SGBDR**: ¿Cuántos zapatos vendimos el último mes?
- **Pregunta estratégica**: ¿Cuántos zapatos del 41 de color rojo se vendieron el último mes en la zona norte, este y sur, comparados con las ventas del mismo mes el año pasado?

#### Requisitos Clave

1. **Gran volumen de datos**: Varios años, clientes, productos, almacenes, etc.
   - Históricos de distintas fuentes

2. **Presentación amigable**: Entorno fácil de usar
   - Entender preguntas "estratégicas"

#### Limitaciones de los Sistemas OLTP

Los sistemas OLTP (OnLine Transaction Processing) no son válidos para análisis estratégicos porque:
- Los datos históricos no están disponibles
- Los datos están normalmente en distintas fuentes de datos
- Los directivos no saben manejar sistemas transaccionales
- Problemas de rendimiento y errores

### 1.7 Almacén de Datos (Data Warehouse)

#### Definición

Un almacén de datos (DW) es un repositorio centralizado de datos integrado, no volátil, orientado a la toma de decisiones, que almacena datos históricos de múltiples fuentes operacionales.

#### Características Principales

- **Integrado**: Datos de múltiples fuentes unificadas
- **No volátil**: Los datos no se eliminan, solo se añaden
- **Orientado a temas**: Organizado por áreas de análisis (ventas, clientes, productos)
- **Histórico**: Datos del pasado para análisis de tendencias
- **Denormalizado**: Estructura optimizada para consultas analíticas

#### Diferencias entre OLTP y OLAP

| Característica | OLTP | OLAP |
|---|---|---|
| **Tipo de operación** | Transacciones cortas | Consultas complejas |
| **Datos** | Actuales | Históricos |
| **Normalización** | Altamente normalizado | Desnormalizado |
| **Usuarios** | Empleados | Analistas/Directivos |
| **Volumen** | Pequeño a medio | Muy grande |
| **Disponibilidad** | 24/7 | Periódica |

### 1.8 Arquitectura de Data Warehouses

#### Esquema Tradicional

```
Fuentes Externas → BD Operacionales → Fuentes de Datos
                                      ↓
                          [PROCESOS ETL]
                                      ↓
Metadatos ← → Almacén de Datos (DW)
                ↓
Servidores OLAP ← Data Marts
                ↓
    Análisis/Consultas/Informes/Minería de Datos
                ↓
        Herramientas de Consulta
```

#### Componentes Principales

1. **Fuentes de Datos**: Internas y externas
   - Bases de datos operacionales
   - Fuentes externas
   - Datos abiertos

2. **Procesos ETL**: Extract, Transform, Load
   - Extracción de datos
   - Transformación según reglas de negocio
   - Carga en el DW

3. **Servidor del Almacén de Datos**: SGBD que gestiona
   - Repositorio propio del DW
   - Procesos ETL
   - Responder consultas

4. **Servidor de Consultas**: Separado del servidor DW (por rendimiento)
   - Tecnologías ROLAP (Relational OLAP)
   - Tecnologías MOLAP (Multidimensional OLAP)

5. **Herramientas de Consultas**:
   - Generación de informes
   - Consultas ad-hoc
   - Entornos de directivos
   - Data Mining

6. **Repositorio de Metadatos**: Datos sobre datos
   - Información de fuentes
   - Esquema DW
   - Vistas y agregados
   - Dimensiones y jerarquías
   - Consultas y informes
   - Data Marts
   - Diseño físico

#### Tipos de Metadatos

- **Administrative**: Información completa del DW (fuentes, esquema, dimensiones, consultas predefinidas, Data Marts, diseño físico)
- **Business**: Términos de negocio, políticas de propiedad, políticas de acceso
- **Operational**: Datos migrados, transformaciones aplicadas, auditoría, informes de error

### 1.9 Arquitecturas de DW

1. **Arquitectura Centralizada**: Un único DW central
2. **Arquitectura Distribuida**: Múltiples Data Marts independientes
3. **Arquitectura Federada**: Data Marts que comparten metadatos
4. **Arquitectura Data Lake**: DW + Data Lake para datos no estructurados

### 1.10 Procesos ETL

#### Extract (Extracción)
- Extraer datos desde las distintas fuentes de origen
- Fusión de datos
- Identificar fuentes
- Identificar conjuntos de datos
- Conectores para la adquisición
- Fuentes: Hadoop, datos abiertos, SQL, NoSQL, repositorios RDF, Wikidata, etc.
- Analizar datos obtenidos (tipos, codificación, semántica)
- Interpretar y comprobar que cumplen con la estructura esperada

#### Transform (Transformación)
- Depurar y ajustar a requisitos
- Selección de datos (columnas, filas), eliminación de ruido
- Modificación del contenido o estructura
- Integración con datos de otras fuentes
- Corrección de errores
- Cálculo de valores derivados o agregados
- Traducción de valores
- Codificación
- Tratamiento de textos
- Validación de datos frente a reglas de calidad

#### Load (Carga)
- Carga y actualización de los datos en el almacén de datos
- Selección de sistema destino (fichero, DW, BD relacional, índice, NoSQL)
- Nuevo o sobrescribir
- Historial de cambios
- Tipos: acumulación simple, rolling para mayor granularidad

---

## TEMA 2: Diseño Conceptual de Almacenes de Datos {#tema-2}

### 2.1 Modelos Utilizados en Bases de Datos

#### Sistemas Operacionales (OLTP)

Utilizan **Normalización**:
- Múltiples tablas relacionadas
- Eliminación de redundancia
- Enfoque en integridad referencial
- Ejemplo: Almacén → Ciudad → Provincia → Estado

#### Sistemas Analíticos (OLAP)

Utilizan **Modelado Multidimensional**:
- Hechos y Dimensiones
- Desnormalización
- Enfoque en rendimiento de consultas
- Cubos de datos

### 2.2 Modelado Multidimensional

#### Perspectiva Estructural

##### Hechos
- **Definición**: Objeto de análisis
- **Ejemplos**: Ventas de productos, compras, alquileres, transportes
- **Características**:
  - Representan eventos o transacciones
  - Contienen medidas (valores numéricos)
  - Se relacionan con dimensiones mediante claves

##### Dimensiones
- **Definición**: Diferentes perspectivas para analizar los hechos
- **Ejemplos**: Productos, almacenes, tiempo, vehículos
- **Características**:
  - Contienen atributos descriptivos
  - Definen contexto para el análisis
  - Pueden tener jerarquías
  - Suelen ser relativamente pequeñas

##### Relaciones

- Hechos representan normalmente relaciones **muchos a muchos** con todas las dimensiones
- Relaciones **muchos a uno** con cada dimensión en particular
- Ejemplo: Ventas de productos (H) por producto (D), almacenes (D) y tiempo (D)
  - Un producto (D) → varias ventas (H)
  - Una venta (H) → un solo producto (D) y almacén (D)

**Excepciones**: A veces hechos son muchos a muchos con dimensiones en particular
- Ejemplo: Tickets emitidos (H) pueden contener muchos productos

#### Atributos

- **Hechos**: Atributos de hecho o **medidas** (valores numéricos)
- **Dimensiones**: Atributos de dimensión (texto, descripciones)

#### Representación Intuitiva

##### Cubos
- Estructura multidimensional con hechos en el centro
- Dimensiones en los ejes
- Medidas en las celdas

Ejemplo simple:
```
        Tiempo
        (Enero-Diciembre)
            |
Almacén ---|--- Producto
(Madrid,   / \ (Bebidas,
Barcelona) (Comida)
            
Ventas: Cantidad en celdas
```

##### Hipercubos
- Cubos sobre cubos
- Extensión del modelo a más dimensiones

##### Tablas Multidimensionales
- Similares a hojas de cálculo
- Representación tabular del cubo

#### Comparación: Cubo vs Tabla Relacional

Para recuperar los datos necesarios:
- **En una SGBDR**: 4 × 3 × 3 = 36 tuplas (filas)
- **En una BD Multidimensional**: 4 + 3 + 3 = 10 valores en los ejes

Ventaja de multidimensional: Mayor eficiencia en recuperación de datos

### 2.3 Dimensiones

#### Atributos de Dimensión

Pueden tener alto grado de categorización:
- Atributos en función de instancias
- Ejemplo: Volumen y porcentaje de alcohol solo para bebidas
- Ejemplo: Tiempo y modo preparación solo para comidas

#### Jerarquías de Clasificación

Los atributos dimensión → jerarquías clasificación
Los niveles de jerarquía serán usados para la agregación de las medidas
- Ejemplo: Ciudad → Comunidad
- Ejemplo: Tipo de producto → Familia → Grupo

##### Términos Clave

- **Instancias de niveles**: Miembros
- **Cardinalidad**: Relación entre niveles

#### Tipos de Cardinalidad

- **Estrictas (1-m)** (por defecto)
  - Una instancia solo se relaciona con una instancia del nivel superior
  - Ejemplo: Un almacén está ubicado en una sola ciudad

- **No estrictas (m-m)**
  - Una instancia puede relacionarse con múltiples instancias del nivel superior
  - Ejemplo: Un almacén pertenece a más de una zona de ventas

#### Caminos en las Jerarquías

- **Simples**: Representación mediante árbol
  - Un solo camino desde la raíz a cada miembro

- **Múltiples**: Representación mediante grafo
  - Múltiples caminos posibles

#### Tipos de Jerarquías Simples

1. **Simétricas**: Todos los niveles obligatorios e instanciados
2. **Asimétricas**: Niveles inferiores pueden no estar instanciados
3. **Generalizadas**: Camino de navegación por categorización de instancias

Ejemplo Asimétrica:
```
        Estado 1
       /        \
   Condado 1   Condado 2
    |            |
  Ciudad 3    Ciudad 4
    |            |
 Almacén 3   Almacén 4
```

#### Jerarquías Múltiples y de Camino Alternativo

- **Representación**: D.A.G. (Grafo Acíclico Dirigido)
- Ejemplo: Ciudad se puede clasificar en comunidad Y en zona de ventas

#### Jerarquías Paralelas

- **Definición**: Más de una jerarquía definida para la misma dimensión
- **Independientes**: Las jerarquías no comparten niveles
- **Dependientes**: Las jerarquías comparten algún nivel

Ejemplo:
```
Dimensión Producto:
Jerarquía 1: Grupo → Familia → Tipo → Nombre → Marca
Jerarquía 2: Grupo → Familia → Tipo → Nombre
```

#### Jerarquías Completas

- Además de estrictas, un miembro de un nivel superior está compuesto únicamente por los del nivel inferior
- Relación fija entre instancias

### 2.4 Hechos

#### Atributos de Hecho o Medidas

- **Atómicos**
  - Ejemplo: Cantidad vendida, precio

- **Derivados**
  - Utilizan una fórmula para calcularlos
  - Ejemplo: Precio_total = precio × cantidad_vendida

#### Aditividad de Medidas

**Definición**: Conjunto de operadores de agregación (SUM, AVG, etc.) que se pueden aplicar para agregar los valores de medidas a lo largo de las jerarquías de clasificación

- **Aditiva**: SUM sobre todas las dimensiones
- **Semi-aditiva**: SUM solo sobre algunas dimensiones
- **No aditiva**: SUM sobre ninguna dimensión
  - Si no aditiva → otros operadores pueden aplicarse (AVG, MIN, etc.)

Ejemplos:
- Inventarios: Aditivos sobre dimensión producto, NO aditivos sobre dimensión tiempo
- Temperatura: NO aditiva sobre todas las dimensiones
- Número de clientes (que cuenta tickets): No aditiva sobre dimensión producto

### 2.5 Transformación del Modelo E-R a Modelo Multidimensional

#### Preguntas Clave

- ¿Hechos?
- ¿Dimensiones?
- ¿Jerarquías?

#### Ejemplo de Transformación

De un modelo E-R:
```
Cliente ← compra → Producto
  ↓
Estudios, Ciudad, Provincia, Comunidad
  ↓
Datos de cliente
```

A un modelo multidimensional:
```
HECHOS: Compra
DIMENSIONES: Cliente, Producto, Tiempo
JERARQUÍAS:
  - Geográfica: Comunidad → Provincia → Ciudad
  - Producto: Grupo → Familia → Tipo
  - Tiempo: Año → Mes → Día
```

### 2.6 Perspectiva Dinámica: Operaciones OLAP

Las operaciones OLAP permiten navegar y analizar el cubo multidimensional:

#### Roll-up (Drill-up)

- **Definición**: Agregar valores de medidas a lo largo de jerarquías de clasificación
- **Dirección**: De detalle a resumen
- **Ejemplo**: De ventas diarias a ventas mensuales a ventas anuales
- **Acción**: Moverse hacia niveles superiores de la jerarquía

#### Drill-down (Roll-down)

- **Definición**: Desagregar valores de medidas a lo largo de jerarquías de clasificación
- **Dirección**: De resumen a detalle
- **Ejemplo**: De ventas mensuales a ventas diarias
- **Acción**: Moverse hacia niveles inferiores de la jerarquía

#### Drill-across

- **Definición**: Consultar medidas de varios hechos en el mismo cubo
- **Ejemplo**: Ratio de ventas respecto de compras
- **Cálculo**: Ventas / Compras

#### Slice-dice

- **Definición**: Definir restricciones sobre niveles de jerarquías
- **Ejemplo**: Analizar datos donde el año sea 1999
- **Acción**: Filtrar el cubo por valores específicos

Ejemplo práctico:
- Cubo original: Producto × Región × Tiempo
- Slice: Fijar Tiempo = 1997
- Dice: Seleccionar solo Productos = Fax, Mobiles y Regiones = Madrid, C.L.M.

#### Pivoting

- **Definición**: Reorientar la vista multidimensional de los datos
- **Acción**: Cambiar la distribución de filas/columnas
- **Ejemplo**: Cambiar de Tiempo × Almacén a Almacén × Producto

### 2.7 Definición de Requerimientos Iniciales

Los requerimientos deben basarse en jerarquías definidas en Dimensiones

Ejemplo:
"Cantidad vendida de productos comestibles agrupados por su familia y tipo, vendidos en la comunidad valenciana y agrupados por la provincia y ciudad donde se vendieron"

---

## TEMA 3: Diseño Lógico de Almacenes de Datos {#tema-3}

### 3.1 Modelado Lógico Multidimensional

El modelado lógico multidimensional depende del tipo de servidor OLAP:

#### MOLAP (Multidimensional OLAP)

- Utiliza vectores o matrices multidimensionales
- Estructura propietaria de almacenamiento
- Generalmente más rápido para consultas pero menos flexible

#### ROLAP (Relational OLAP)

- Utiliza tablas relacionales para representar hechos y dimensiones
- **Esquema estrella de R. Kimball**
- Variantes del esquema estrella:
  - **Constelaciones de hechos**
  - **Copos de nieve**

### 3.2 Esquema Estrella

#### Estructura Básica

```
Dimensión Producto ─┐
Dimensión Almacén  ├─→ Tabla de Hechos (Ventas) ←─ Medidas
Dimensión Cliente  ├─
Dimensión Tiempo   ─┘
```

#### Definición Formal

- **Hechos** → Tablas de hechos
- **Dimensiones** → Tablas de dimensiones
- La tabla de hechos es relación **muchos a muchos** con las tablas de dimensiones
- Técnica utilizada → **Desnormalización**
- Clave primaria tabla de hechos: Compuesta por claves ajenas de tablas de dimensiones

#### Características Principales

1. **Simples de entender**: Estructura intuitiva
2. **Rendimiento**: Búsquedas rápidas
3. **Flexible**: Fácil de ampliar
4. **Denormalizado**: Redundancia controlada

#### Ejemplo Práctico

Tabla de Hechos (Ventas_productos):
- producto_cod (FK)
- almacén_cod (FK)
- cliente_cod (FK)
- tiempo_cod (FK)
- cantidad_vendida (medida)
- precio (medida)
- total_precio (medida)

Tabla de Dimensión Producto:
- producto_cod (PK)
- producto_nombre
- producto_color
- marca_cod
- marca_director
- familia_cod
- familia_des
- tipo_cod
- grupo_cod

Tabla de Dimensión Tiempo:
- tiempo_cod (PK)
- día
- vacaciones (flag)
- mes
- año

Tabla de Dimensión Almacén:
- almacén_cod (PK)
- almacén_nombre
- almacén_dirección
- ciudad
- provincia
- zona_ventas
- comunidad

Tabla de Dimensión Cliente:
- cliente_cod (PK)
- cliente_nombre
- ciudad
- comunidad

#### Granularidad

**Definición**: Nivel de detalle de los datos

Afecta al Almacén de datos en:
- Tamaño del repositorio
- Grado de análisis
- Flexibilidad

Niveles posibles:
- Transacciones individuales (nivel alto/fine grain)
- Resúmenes diarios
- Resúmenes mensuales
- Resúmenes anuales
- Cualquier otro período de tiempo (nivel bajo/coarse grain)

**Decisión**: Define el nivel en función de las necesidades del negocio

### 3.3 Tablas de Dimensiones

#### Características

- Describen el contexto para analizar los hechos
- Datos "textuales" (Alfanuméricos)
- Datos **desnormalizados** → redundancia
- Cada fila contiene:
  - Su clave primaria
  - Atributos descriptores de todos los niveles de jerarquía
- Tablas más pequeñas que las tablas de hechos
- Cambios lentos (Slowly Changing Dimensions)

#### Ejemplo de Tabla de Dimensión Producto

| Producto_cod | Producto_nombre | Family_Desc |
|---|---|---|
| 1 | Puleva Milk ½ L | Productos lácteos |
| 2 | Puleva Milk 1L | Productos lácteos |
| 3 | Yogourt Pascual | Productos lácteos |
| 4 | Mr. Proper | Productos limpieza |
| 5 | Ajax | Productos limpieza |

### 3.4 Tablas de Hechos

#### Definición

- Representan actividades básicas de empresa
- Cada fila se compone de:
  - **Clave primaria**: Compuesta por claves ajenas de las dimensiones
  - **Medidas**: Datos numéricos
- Generalmente relación m-n con dimensiones
- Relación m-1 en particular con cada dimensión

#### Ejemplo de Tabla de Hecho "Ventas"

| CliKey | ProductoKey | AlmacénKey | Tiempo_key | Sale Amount |
|---|---|---|---|---|
| 1 | 1 | 1 | 1 | 100€ |
| 1 | 2 | 1 | 2 | 120€ |
| 1 | 3 | 1 | 3 | 200€ |

#### Consulta SQL sobre Esquema Estrella

```sql
SELECT District, Brand,
    SUM(DollarsSold) TotalDollars,
    SUM(Cost) TotalCost,
    SUM(DollarsSold) - SUM(Cost) GrossProfit
FROM Sales, Store, Product
WHERE Sales.store_key = Store.store_key
  AND Sales.product_key = Product.product_key
GROUP BY District, Brand
ORDER BY District, Brand
```

### 3.5 Particularidades del Esquema Estrella

#### Dimensiones Degeneradas

- Las tablas de hechos contienen información sobre una dimensión que no existe físicamente
- Este atributo puede/suele formar parte de la clave primaria de la tabla de hechos
- Suelen referirse a dimensiones físicas en mundo real
- Ejemplos: Número de ticket, cod_factura, cod_albarán

Ejemplo:
```
Tabla Ventas_productos:
producto_cod (FK)
almacén_cod (FK)
cliente_cod (FK)
tiempo_cod (FK)
Número_ticket (dimensión degenerada)
cantidad_vendida
precio
total_precio
```

Normalmente indica una relación muchos a muchos en particular con una dimensión.
A estos esquemas se les denomina "Multi Star Schema"

#### Tablas de Hechos que no son Hechos (Factless Fact Tables)

- No contienen medidas o atributos de análisis
- Recogen la ocurrencia de un evento

Ejemplo:
```
Tabla Impartir_clase:
Profesor_dni (FK)
Asignatura_cod (FK)
Alumno_dni (FK)
(Sin medidas numéricas)
```

#### Claves Primarias de las Tablas de Dimensiones

**Opción 1: Autogeneradas**
- Mejor rendimiento
- Incluso en la dimensión Tiempo
- Más fáciles de manejar para procesos ETL

**Opción 2: Con significado semántico**
- Mantiene la información de negocio
- Puede ser más complicada para ETL

### 3.6 Razones para Desnormalizar

1. **Rendimiento**
   - Eliminar el número de uniones entre tablas
   - Elevado número de filas
   - Unión es la operación más cara

2. **Intuición**
   - Más fácil para consultar por parte del usuario no experto

### 3.7 Dimensiones que Cambian Lentamente (SCD: Slowly Changing Dimensions)

#### Problema

Las instancias de dimensiones se pueden considerar fijas a lo largo del tiempo.
Sin embargo, a veces deseamos registrar cambios que puedan suceder en algunas dimensiones para seguir analizando datos históricos.

Normalmente cambios en descripción de productos o de clientes.

Kimball propone tres soluciones básicas y dos híbridas.

#### Solución 1: Sobreescribir el Valor Antiguo

- La fila registra el último valor válido
- Perdemos la habilidad de analizar "la historia"
- Se suele utilizar cuando el valor antiguo deja de tener significado
- Se suele utilizar cuando se corrigen errores
- Aproximación simple

Ejemplos: descripción productos, nombres nuevos

**Ejemplo**:
```
ANTES:
001 | 965650000

DESPUÉS (cambio de teléfono):
001 | 965651111
```

#### Solución 2: Añadir una Fila Nueva

- Utilizar un nuevo valor de clave autogenerada
- Permite registrar el cambio del valor de un atributo
- Representa un cambio físico real en la dimensión
- **Imprescindible utilizar claves autogeneradas**
- Añadir un campo que identifique al valor actual (flag)
- Añadir campos para registrar fecha de comienzo y fin de validez

**Ventajas**:
- Permite analizar "la historia"
- Segmenta la historia
- Particiona la tabla de hechos
- Dos "productos" distintos con claves generadas distintas estarán registrados en las ventas

**Inconvenientes**:
- Necesita almacenamiento extra
- Realizar test para excluir versiones antiguas

**Ejemplos de cambios**: Dirección, Región, etc.

**Queries complejas**: Definir restricciones sobre atributo que ha cambiado el valor
- Si queremos mismo producto, actuaremos sobre clave primaria original
- Si queremos la historia, usaremos la clave autogenerada

Suele ser la más utilizada para las verdaderamente "Dimensiones que cambian lentamente"

#### Solución 3: Añadir una Columna Nueva (No detallada)

- Guardar el valor anterior en una columna adicional
- Permite comparaciones rápidas

#### Soluciones Híbridas

Combinación de las anteriores según necesidades del negocio.

### 3.8 La Dimensión Tiempo

#### Características Especiales

- Dimensión muy especial en DW
- Normalmente se crea con claves autogeneradas
- Debe ser muy desnormalizada
- Incluyendo muchos campos derivados

#### Estructura Típica

| Cod | Dia | Día | CodMes | Mes | CodSemestre | Semestre | CodAño | Año |
|---|---|---|---|---|---|---|---|---|
| 1300 | 2 | 500 | Sept | 200 | S3 | 50 | 1999 | 1 |
| 1301 | 3 | 500 | Sept | 200 | S3 | 50 | 1999 | P |
| ... | ... | ... | ... | ... | ... | ... | ... | ... |

Incluye información de:
- Día de la semana
- Semana del año
- Mes
- Trimestre
- Semestre
- Año
- Información de vacaciones/festivos

### 3.9 Otras Consideraciones de Diseño

#### Many-to-Many Dimensions

**Problema**: Cuando entre la tabla de hechos y una tabla de dimensión existe una relación m-n

Ejemplo: Health Care System
- Un paciente puede tener varios diagnósticos
- Una factura puede ser para varios diagnósticos

**Desafíos**:
- Solo se podría visualizar uno de forma sencilla
- Para visualizar todos, la generación del informe es más compleja
- Necesidad de más uniones entre tablas

**Solución**: Tablas Puente (Bridge Tables)

Estructura:
```
Diagnóstico ←→ Tabla puente de Grupo de diagnósticos ←→ Factura_paciente
                (con weighting factors)
```

Los weighting factors permiten ponderar la contribución de cada diagnóstico.

#### The Data Warehouse Bus Architecture

- Arquitectura detallada de cómo construir todo el DW corporativo
- Cada Data Mart debería estar basado en la mínima granularidad del proceso de negocio
- Dos aproximaciones:
  1. Crear una arquitectura que defina todo el DW
  2. Supervisar la construcción de cada Data Mart en particular
- Utilizar las **dimensiones y hechos comunes (conformed)**

#### Dimensiones Comunes (Conformed Dimensions)

- Es una misma dimensión que existe en todos los Data Marts
- Ejemplo: Tabla maestro de clientes o productos
- Se mantienen de forma independiente a los Data Marts

**Cuando se definen dimensiones comunes**:
- No obviarlas ni menospreciarlas
- Definir el mínimo nivel de granularidad posible
- Utilizar claves autogeneradas (surrogate keys)
- Este tipo de dimensiones puede ocupar el 80% del esfuerzo del desarrollo total

**Ventajas**:
- Una misma dimensión se puede utilizar contra varios hechos
- Interfaces de usuario y datos son consistentes
- Permite navegar entre Data Marts

#### Hechos Comunes (Conformed Facts)

- Medidas utilizadas en más de un Data Mart
- Ejemplos: beneficio, coste, precio

### 3.10 Esquema Constelaciones de Hechos

**Definición**: Múltiples tablas de hechos que comparten dimensiones comunes

**Ventajas**:
- Representa múltiples procesos relacionados
- Permite análisis entre procesos
- Mantiene consistencia dimensional

**Estructura**:
```
        Dimensión Producto
        /    |    \
Hechos Compras  Hechos Ventas  Hechos Inventario
        \    |    /
        Dimensión Tiempo
```

### 3.11 Esquema Copos de Nieve

**Definición**: Normalización parcial de dimensiones

**Características**:
- Las dimensiones se normalizan en múltiples tablas
- Reduce redundancia de datos
- Aumenta complejidad de las consultas
- Más uniones necesarias

**Comparación con Estrella**:

| Aspecto | Estrella | Copo de Nieve |
|---|---|---|
| **Desnormalización** | Total | Parcial |
| **Redundancia** | Alta | Baja |
| **Uniones en queries** | Pocas | Muchas |
| **Velocidad** | Más rápida | Más lenta |
| **Tamaño** | Mayor | Menor |
| **Complejidad** | Simple | Compleja |

### 3.12 El Proceso de Diseño de un DW

#### Análisis de Requisitos

A partir de análisis de requisitos:
- Objeto de análisis → **hechos**
- Contexto de análisis → **dimensiones**
- Jerarquías, etc.

**Nota**: A veces no es intuitivo y se adoptarán decisiones sobre si considerar un elemento como dimensión o como hecho.

#### Decisión: ¿Hechos o Dimensiones?

Criterio:
- **Dimensión**: Si el atributo se percibe como un valor estático o constante
  - Ejemplo: Descripción, Localización, Color, Tamaño

- **Hecho**: Si el atributo varía continuamente
  - Ejemplo: Balance, Unidades vendidas, Llamadas por mes, Color (si varía)

#### Proceso Típico

1. **Diseño Conceptual** (opcional pero recomendado)
   - Para documentación
   - Facilita comprensión del negocio

2. **Diseño Lógico a partir del modelo corporativo/transaccional**
   - Extraer de la documentación o modelo → esquema estrella
   - Identificar tablas de hechos
   - Identificar tablas de dimensiones
   - Identificar jerarquías de clasificación
   - Identificar atributos
   - En función de los requisitos:
     - Normalizar algunas dimensiones → copos de nieve
     - Estudiar qué agregados definir → constelaciones de hechos

3. **Validación con usuarios**
   - Asegurar que el diseño responde a los requisitos del negocio

---

## TEMA 4: Preparación de Datos para IA con ETL {#tema-4}

### 4.1 Ciclo de Vida del Proyecto IA

El ciclo de vida completo incluye:

1. **Definición del Proyecto**
   - Objetivos del modelo
   - Casos de uso

2. **Adquisición y Evaluación de Datos**
   - Analizar y evaluar necesidades de datos
   - Recolectar datos
   - Limpiar datos
   - Estructurar datos
   - Enriquecer datos

3. **Modelado**
   - Selección del modelo
   - Entrenamiento
   - Pruebas, ejecución y optimización

4. **Validación**
   - Métricas clave
   - Validar fiabilidad
   - Alineación con objetivos

### 4.2 Desafíos en la Preparación de Datos

#### Fuentes Heterogéneas

- Formatos diferentes: SQL, archivos CSV, XML, RDF, JSON
- Acceso a APIs
- Múltiples plataformas
- Datos estructurados, semiestructurados y no estructurados

#### Calidad de Datos

- Los datos de diferentes fuentes pueden tener errores
- Pueden estar incompletos
- Pueden ser inconsistentes
- Duplicados

#### Gestión de Volumen

- Grandes volúmenes de datos que se generan a gran velocidad
- Requiere procesamiento paralelo
- Necesidad de herramientas especializadas

#### Seguridad y Privacidad

- Garantizar que la información se maneje de forma segura
- Especialmente si contiene datos sensibles
- Cumplimiento normativo (GDPR, CCPA, etc.)

### 4.3 Procesos ETL en el Contexto de IA

#### Importancia

El ETL es el paso crítico en la preparación de datos para IA:
- Calidad de datos → Calidad del modelo
- Datos limpios y bien preparados → Mejor rendimiento del modelo

#### Enfoque Diferenciado

Para IA, el ETL se enfoca en:
- **Extracción exhaustiva**: Capturar todos los datos necesarios
- **Transformación inteligente**: Crear características relevantes (feature engineering)
- **Carga flexible**: Permitir múltiples formatos y destinos

---

## TEMA 5: Introducción a la Integración de Datos mediante ETLs {#tema-5}

### 5.1 Integración de Datos

#### Definición

"Conjunto de aplicaciones, productos, técnicas y tecnologías que permiten una visión única consistente de los datos" (Josep Curto Díaz)

#### Diagrama de Integración

```
APIs Abiertas ⟶ ⟮ ETL ⟯ ⟵ Bases de Datos
Datos Abiertos ⟶ ⟮    ⟯
Archivos de Datos ⟶ ⟮    ⟯
```

#### ¿Por Qué es Importante?

Los datos pueden estar almacenados en diversas fuentes:
- **Plataformas internas**: Sistemas de información propios, OLTP, OLAP, cloud privado
- **Externas**: IoT, cloud público, dispositivos móviles, datos abiertos, sensores

**Potencial emergen cuando se combinan**:
- Facilita análisis completo con visión total de datos
- Mejora la toma de decisiones en base a datos completos y fiables
- Reduce la duplicidad y mantiene la consistencia

### 5.2 Técnicas de Integración de Datos

#### Propagación de Datos

**Concepto**: Se copian los datos de la fuente al destino (sincronización de datos)

**Características**:
- Los cambios se propagan de forma síncrona o asíncrona
- Se puede activar por eventos o actualizaciones específicas
- Busca asegurar la consistencia
- Facilita datos en tiempo real o con mínima latencia
- Útil cuando es necesario distribuir datos entre sistemas y ubicaciones

**Proceso**:
1. Se realiza un cambio en la fuente
2. Se detecta el cambio (técnica CDC)
3. Se transfiere solo el cambio detectado
4. El sistema destino aplica el cambio

#### Consolidación de Datos

**Concepto**: Agregación de datos de múltiples fuentes a un repositorio central

**Estructura**:
```
BD Fuente 1 ─┐
BD Fuente 2 ─┼─ [ETL] ─→ Data Warehouse
BD Fuente 3 ─┘
                   └─ Meta datos
                   └─ Raw data
                   └─ Summary data
```

**Ventajas**:
- Se puede acceder a todos los datos de forma rápida y sencilla
- No necesidad de consultar manualmente cada fuente origen

**Latencia**:
- **Baja latencia**: Identificar cambios en origen para transmitir solo esos cambios (CDC)
- **Alta latencia**: Procesos batch en intervalos prefijados

#### Federación de Datos

**Concepto**: Capa virtual que proporciona una vista unificada de los datos

**Características**:
- Facilita el acceso y consulta en tiempo real
- Sin necesidad de mover ni replicar datos físicamente
- Crea un modelo lógico con:
  - Información de la estructura
  - Localización de los datos
  - Cómo se relacionan los datos de distintas fuentes
- Optimiza la fragmentación de la consulta original
- Selecciona el camino de acceso más eficiente

**Funcionamiento de una consulta**:
1. La consulta se descompone en consultas individuales
2. Se envía a cada una de las fuente de datos (MySQL, Oracle, APIs, etc.)
3. Los sistemas de origen ejecutan las consultas individuales
4. La capa recopila las respuestas
5. Las integra creando un resultado único

**Diagrama**:
```
      Consulta de usuario
            ↓
    [Capa de Virtualización]
     /     |      \
   Sub    Sub     Sub
  Query1 Query2  Query3
   ↓      ↓       ↓
  BD1    BD2     API
   ↓      ↓       ↓
  Res1   Res2    Res3
     \     |      /
   Resultado Integrado
```

**Ventajas**:
- Proporciona datos actualizados (acceso directo a fuente)
- Reduce costes de almacenamiento (sin DW grande)
- Datos sensibles permanecen en ubicación original
- Integración rápida de nuevas fuentes

#### CDC (Change Data Capture)

**Concepto**: Identifica y captura cambios en el origen y los propaga a entornos destino

**Objetivo**: Mantener sincronizados y consistentes los sistemas

**Técnicas de CDC**:
1. **Aplicación**: La aplicación genera el cambio y actualiza en destino
2. **Timestamp**: Rastrea cambios con timestamp
3. **Triggers**: Se activan tras operación (INSERT, UPDATE, DELETE) y registran detalles en tabla de auditoría
4. **Log**: Se auditan ficheros de logs en busca de cambios

**Ventajas**:
- Integración en tiempo real
- Facilita migración y replicación
- Eficiencia: captura y mueve solo cambios
- Reduce sobrecarga en sistema origen
- Minimiza uso de recursos de red y cómputo

#### Técnicas Híbridas

En la práctica se suelen emplear varias técnicas, dependiendo de:
- Requisitos de negocio para la integración
- Requisitos tecnológicos y restricciones presupuestarias

### 5.3 Tecnologías de Integración de Datos

#### ETL (Extract Transform Load)

**Características**:
- Simplifican y automatizan el proceso de extracción, transformación y carga
- Exigen datos de las fuentes
- Transforman raw data siguiendo reglas de negocio
- Cargan en destino
- Documentan las transformaciones (logs, estadísticas)

**Tipos**:
- ETL basados en motor
- ETL de generación de código
- ETL integrado en la base de datos

**Se centran en**:
- **Calidad**: La transformación garantiza precisión y confiabilidad
- **Organización**: Datos bien estructurados y listos para usar

**Facilita**:
- Adquisición y gestión de datos
- Extracción de datos
- Transformación de datos
- Gestión y administración de servicios
- Validación y auditoría: facilita auditar transformaciones y garantizar aplicación de reglas de negocio

#### ELT (Extract Load Transform)

**Diferencia clave**: Los datos se cargan antes de cualquier transformación

**Características**:
- Prioriza la velocidad de la ingesta
- Útil cuando necesita volcar rápidamente grandes cantidades de datos
- Escalable: aprovecha computación en la nube
- Flexible: almacena datos en formato original
- Permite crear diferentes modelos sin re-extraer

**Dependencias**:
- Depende del coste y eficiencia del almacenamiento y computación en la nube

#### EII (Enterprise Information Integration)

**Concepto**: Crea vista unificada de sistemas heterogéneos

**Características**:
- Basada en federación de datos
- Proporciona acceso en tiempo real y consistente
- Facilita interoperabilidad
- Reduce latencia (datos tal como están en momento de consulta)
- No incurre en costes y complejidad de consolidación física

#### EDR (Enterprise Data Replication)

**Concepto**: Réplica de datos en grandes volúmenes a varias ubicaciones

**Características**:
- Soporta técnicas CDC y propagación de datos
- Utiliza CDC para identificar cambios incrementales
- Sincroniza con destino
- Asegura disponibilidad y consistencia

**Operaciones**:
- Consolida datos en tiempo real, regular o esporádicamente
- Mantiene copias de seguridad

#### Integración Basada en APIs

**Concepto**: Proporciona capa de abstracción entre sistemas

**Características**:
- Conexión mediante API REST o SOAP
- Facilita intercambio de datos en tiempo real
- Reduce dependencias de ETL tradicionales en arquitecturas distribuidas
- Utilizadas por: Google Cloud, AWS, Azure, etc.

### 5.4 Flujos de Trabajo

#### Definición

Diseño y desarrollo de flujos de trabajo:
- Utilizando pasos o entradas
- Unidas por saltos
- Que pasan datos de un elemento al siguiente
- Facilitan análisis de grandes volúmenes de datos

#### Tipos de Archivos

1. **Transformaciones**: Realizan tareas ETL
2. **Trabajos (Jobs)**: Organizan actividades ETL
   - Definición del flujo
   - Dependencias
   - Ejecución

### 5.5 Pentaho Data Integration

#### Introducción

**Pentaho Data Integration (Kettle)**:
- Suite Business Intelligence para gestión de datos
- Open source multiplataforma
- Creada en 2004
- Plataforma Java
- Disponible en dos ediciones:
  - Community Edition (CE)
  - Enterprise Edition (EE)
- Múltiples plugins creados por comunidad open source

#### Componentes Clave

1. **Spoon**: Entorno gráfico para creación de flujos de trabajo
   - Crear transformaciones y trabajos
   - Realizar data warehouse
   - Operaciones: conexiones, transformaciones, fórmulas
   - Múltiples funcionalidades de ejecución, transformación y carga

2. **Pan**: Creación de líneas de comandos para ejecutar transformaciones

3. **Kitchen**: Ejecución de trabajos por línea de comandos

4. **Carte**: Servidor web para ejecutar transformaciones y trabajos

#### Uso de Pentaho Data Integration

- Migración de datos entre diferentes sistemas
- Carga de grandes volúmenes de datos
- Limpieza de datos mediante transformaciones
- Integración de datos en tiempo real

### 5.6 Extracción de Datos: Tipos de Fuentes

#### Extracción Basada en Bases de Datos

**Conexión a BD**:
- Database Connection utilizada por transformations y jobs
- Se establece en tiempo de ejecución
- Definir conexiones no abre conexión real
- Se abre cuando se necesita

**Tipos de BD soportadas**:
- MySQL, PostgreSQL, Oracle, SQLite, SQL Server, Snowflake, etc.

**Gestión de Conexiones**:
- En un job: cada entrada abre y cierra conexiones independientemente
- En una transformación: cada paso abre conexión independiente
- Opción: "Make transformation database transactional" para una única conexión

#### Extracción Basada en Archivos

**Virtual File Systems (VFS)**:
- Gestión flexible y uniforme de archivos
- Especifica archivos como URL
- Utiliza backend VFS de Apache Commons
- Procesa archivos .zip igual que carpetas locales

**Ejemplos de VFS**:
- `/data/input/clientes.dat`: Método clásico
- `file:///data/input/clientes.dat`: Mediante Apache VFS
- `http://servidor.be/GenerateRows.kjb`: Desde servidor web
- `zip:file:///C:/entrada/datos.zip|.*\.txt$`: Archivos en .zip

**Tipos de Archivos**:
- **Delimited (CSV)**: Recomendado, con separador configurable
- **Fixed**: Cada campo tiene ancho designado

**Pasos Clave**:
- **CSV file input**: Básico, especificar delimitador
- **Text file input**: Más potente y completo
  - Obtener nombre de archivo del paso anterior
  - Leer varios archivos en una ejecución
  - Leer desde archivos comprimidos
  - Mostrar contenido sin especificar estructura
  - Especificar carácter de escape
  - Gestionar errores

**Configuración importante**:
- Codificación correcta (UTF-8 es estándar)
- Formato de fecha
- Delimitador correcto

#### Extracción Basada en Web

**Opciones**:
1. **Text-Based Web Extraction**: Via Text file input con URL
2. **HTTP Client**: Recupera datos estructurados
3. **Web Services**:
   - REST client
   - Web services lookup - SOAP

**HTTP Client**:
- Realiza llamada a URL específica
- Retorna datos como String
- Resultado se procesa según formato (CSV, XML, JSON)
- Es un paso de búsqueda (necesita entrada previa)

**Web Services - REST Client**:
- Realiza llamadas a servicios REST
- Retorna JSON o XML
- Ideal para APIs modernas

**Web Services - SOAP**:
- Utiliza WSDL para cargar operaciones
- Mapea campos automáticamente
- URL apunta al WSDL
- Puede necesitar autenticación

---

## TEMA 6: Limpieza, Transformación y Normalización de Datos {#tema-6}

### 6.1 Procesos ETL - Revisión Detallada

#### Extract (Extracción)

**Objetivos**:
- Extraer datos desde distintas fuentes de origen
- Fusión de datos

**Actividades**:
1. Identificar fuentes
2. Identificar conjunto de datos
3. Conectores para la adquisición
4. Fuentes: Hadoop, datos abiertos, SQL, NoSQL, RDF, Wikidata, etc.
5. Analizar datos obtenidos:
   - Tipos de datos
   - Codificación origen
   - Semántica
6. Interpretar y comprobar que cumplen con estructura esperada

#### Transform (Transformación)

**Objetivos**:
- Depurar y ajustar a requisitos
- Aplicar reglas que guíen transformaciones

**Actividades**:
1. Selección de datos (columnas, filas), eliminación de ruido
2. Modificación del contenido o estructura
3. Integración con datos de otras fuentes
4. Corrección de errores
5. Cálculo de valores derivados o agregados
6. Traducción de valores
7. Codificación
8. Tratamiento de textos
9. Validación de datos frente a reglas de calidad

#### Load (Carga)

**Objetivos**:
- Carga y actualización en almacén de datos

**Decisiones**:
1. Selección de sistema destino (fichero, DW, BD, índice, NoSQL)
2. Nuevo o sobrescribir
3. Historial de cambios

**Tipos de carga**:
- Acumulación simple
- Rolling para mayor granularidad

### 6.2 Limpieza de Datos

#### Definición

Los datos sin procesar suelen ser imperfectos y contienen:
- Errores
- Valores faltantes
- Duplicados
- Valores atípicos (outliers)

**Objetivo**: Eliminar anomalías para garantizar calidad y fiabilidad

#### Actividades de Limpieza

1. Corregir errores
2. Eliminar duplicados
3. Gestionar valores que faltan: reemplazo, interpolación o eliminación
4. Gestionar valores atípicos
5. Unificar tipos de datos
6. Reducción de datos:
   - Filtrar campos no necesarios
   - Eliminar valores fuera del rango
   - Gestionar redundancia

#### Mecanismos de Limpieza

1. **Expresiones Regulares**
2. **Otros mecanismos**

### 6.3 Expresiones Regulares

#### Definición

**Mecanismo eficiente y flexible** que facilita el procesamiento de datos

Secuencia de caracteres que forman un patrón para:
- Filtrar
- Encontrar
- Validar
- Tratar un texto

#### Componentes Principales

1. **Literales**: Caracteres que conforman palabras
2. **Clases de caracteres**: Definidas en corchetes
3. **Metacaracteres**: Elementos especiales que permiten delimitar, iterar, alternar

#### Metacaracteres Más Utilizados

| Símbolo | Significado |
|---------|------------|
| `\` | Carácter especial como literal |
| `^` | Principio de cadena |
| `$` | Final de cadena |
| `.` | Cualquier carácter salvo salto de línea |
| `(...)` | Agrupación lógica |
| `[...]` | Conjunto de caracteres |
| `[xyz]` | Coincidencia con cualquiera de los caracteres |
| `[^xyz]` | Cualquier carácter NOT en la lista |
| `[a-z]` | Rango de caracteres |
| `{...}` | Número o intervalo de longitud |
| `{n}` | Repetición n veces |
| `{n,}` | Repetición mínimo n veces |
| `{n,m}` | Repetición entre n y m veces |
| `?` | 0-1 ocurrencias |
| `+` | 1-n ocurrencias |
| `*` | 0-n ocurrencias |
| `\|` | Disyunción lógica (o) |

#### Clases de Caracteres

| Símbolo | Significado |
|---------|------------|
| `\w` | Cualquier carácter alfanumérico o _ |
| `\W` | Cualquier carácter NO alfanumérico |
| `\s` | Espacio en blanco |
| `\S` | NO espacio en blanco |
| `\d` | Dígito decimal [0-9] |
| `\D` | NO dígito |
| `\x` | Dígito hexadecimal |
| `\p{name}` | Carácter Unicode específico |
| `\P{name}` | NOT carácter Unicode |
| `\b` | Límite de palabra |
| `\B` | NO límite de palabra |

#### Flags (Modificadores)

| Flag | Significado |
|------|------------|
| `g` | Encuentra todas las coincidencias |
| `i` | Case insensitive |
| `m` | Múltiples líneas |
| `s` | Modo "dotall" |
| `y` | Búsqueda en posición exacta |
| `u` | Soporte Unicode completo |

#### Ejemplos Prácticos

**Ejemplo 1: Validar fecha YYYY-MM-DD**

```javascript
const pRE = /(20\d{2}|2100)-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])/;
// (20\d{2}|2100): Años 2000-2100
// (0[1-9]|1[0-2]): Meses 01-12
// (0[1-9]|[12]\d|3[01]): Días 01-31
```

**Ejemplo 2: Buscar palabras completas**

```javascript
s1 = "Edición digital Vol II";
const pRE = /\bVol\b/;
pRE.test(s1); // true
s1.replace(pRE, 'Volumen'); // "Edición digital Volumen II"
```

**Ejemplo 3: Validar contraseña**

```javascript
function isValid(pass) {
  // Entre 8-16 caracteres, al menos una minúscula, mayúscula y número
  const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,16}$/;
  return regex.test(pass);
}
```

**Ejemplo 4: Limpiar espacios múltiples**

```javascript
const s1 = "Texto  con   espacios múltiples";
const limpio = s1.replace(/\s+/g, ' ');
// "Texto con espacios múltiples"
```

### 6.4 Transformación y Normalización

#### Normalización de Datos

**Objetivo**: Escalar características a un rango común, asegurando que ninguna variable domine por su magnitud

**Importancia**:
- Mejora la equidad
- Mejora el rendimiento de los modelos

#### Métodos de Normalización

**1. Min-Max Scaling**

```
valor_normalizado = (valor - min) / (max - min)
```

Escala los datos al rango [0,1]

Ejemplo:
```python
import numpy as np
edad = np.array([5, 16, 18, 15, 25, 35, 50])
normalizado = (edad - edad.min()) / (edad.max() - edad.min())
# [0.   0.24 0.29 0.22 0.44 0.67 1.  ]
```

**2. Z-score (Standard Scaler)**

```
valor_estandarizado = (valor - media) / desviación_estándar
```

Ajusta los datos para media=0 y desviación estándar=1

Ejemplo:
```python
import numpy as np
edad = np.array([5, 16, 18, 15, 25, 35, 50])
estandarizado = (edad - edad.mean()) / edad.std()
# [-1.333 -0.537 -0.393 -0.61   0.114  0.837  1.922]
```

### 6.5 Gestión de Valores Atípicos (Outliers)

#### Definición

Un valor atípico (outlier) es una observación que se desvía significativamente de la mayoría de los datos

#### Origen

- Errores en recolección de datos
- Errores de entrada o codificación
- Eventos extraordinarios
- Datos con explicación desconocida

#### Impacto

1. Distorsionan resultados estadísticos
   - La media es sensible a outliers
2. Afectan el rendimiento de modelos
   - Pueden sesgar el modelo

#### Estrategias

1. **Error en recolección**: Filtrado de datos, eliminar o marcar como NULL
2. **Evento extraordinario**: Eliminar (si no representativo)
3. **Sin explicación**: Experimentar con y sin para analizar influencia
4. **Patrón distinto**: Analizar cómo influyen

#### Método: Rango Intercuartílico (IQR)

**Fórmula**:
- Q1 = Percentil 25%
- Q3 = Percentil 75%
- IQR = Q3 - Q1
- Límite inferior = Q1 - 1.5 × IQR
- Límite superior = Q3 + 1.5 × IQR

Outliers están fuera de estos límites

**Ejemplo Python**:
```python
q3 = data['fare'].quantile(0.75)
q1 = data['fare'].quantile(0.25)
iqr = q3 - q1

limitSup = q3 + (1.5 * iqr)
limitInf = q1 - (1.5 * iqr)

outliers = data[(data['fare'] < limitInf) | (data['fare'] > limitSup)]
```

### 6.6 Estrategias y Técnicas de Limpieza

1. **Expresiones regulares**: Encontrar y reemplazar formatos específicos
2. **Limpieza**: Eliminar espacios, caracteres especiales, puntuación
3. **String Matching**: Identificar errores tipográficos y duplicados
4. **Validación con datos del dominio**: Mapear a vocabularios controlados
5. **Estandarización**: Aplicar formato único

### 6.7 Operaciones en Pentaho Data Integration

#### Pasos Frecuentes para Limpieza

1. **Replace in string**: Reemplazar patrones
2. **Split fields**: Dividir campos
3. **Split field to rows**: Dividir campo en múltiples filas
4. **Strings cut**: Cortar cadenas
5. **String operations**: Operaciones con strings
6. **Value mapper**: Mapear valores
7. **Calculator**: Cálculos
8. **Fuzzy match**: Coincidencias aproximadas

#### Expresiones Regulares en Pentaho

**Replace string**:
- Usa expresiones regulares para encontrar y reemplazar

**Regex evaluation**:
- Extrae datos usando patrones

Ejemplo:
```
Paso "Replace string": Buscar /\s+/ Reemplazar por " "
Elimina espacios múltiples
```

### 6.8 String Matching Algorithms

Algoritmos para comparar cadenas y encontrar similitudes:

#### 1. Levenshtein y Damerau-Levenshtein

- Calcula distancia entre dos strings
- Función del número de cambios necesarios

Ejemplo: CASTERS → CASTRO = 2 cambios

#### 2. Needleman-Wunsch

- Calcula similitud de secuencias
- Con penalización por espacio

#### 3. Jaro y Jaro-Winkler

- Calcula índice de similitud (0 a 1)
- 0 = sin similitud
- 1 = coincidencia idéntica

#### 4. Pair Letters Similarity

- Corta cadenas en pares
- Compara conjuntos de pares

#### 5. Fonéticas (Metaphone, Soundex, etc.)

- Hacen coincidir strings basándose en pronunciación
- Algoritmos fonéticos

### 6.9 Tablas de Referencia

#### Conforming Data Using Lookup Tables

**Concepto**: Crear tabla de referencia como tabla maestra de comprobación

**Requisitos**:
1. Cada valor posible del sistema fuente necesita correspondencia
2. La correspondencia debe conducir a conjunto único de valores

**Ejemplo**: Tabla de códigos ISO de idiomas
- ISO 639-2: Código internacional (más restrictivo)
- ISO 639-3: Idioma individual (cobertura amplia)
- ISO 639-1: Más restrictivo

### 6.10 Validación de Datos

#### Applying Validation Rules

**Ejemplo de reglas**:
- Ningún campo puede contener NULL
- Fechas no pueden ser anteriores a 2001-01-01
- Solo nombres de productos en catálogo
- Número de artículos entre 1 y 100
- Precio no puede exceder 1000€

**Pasos en Pentaho**:
- Usar "Validation" steps
- Definir reglas para cada campo
- Rechazar registros inválidos

### 6.11 Gestión de Datos Duplicados

#### Definición

Redundancia de datos que reduce calidad

#### Causas

1. Diversas fuentes de datos no sincronizadas
2. Errores en entrada de datos
3. Fusión de bases de datos sin deduplicación

#### Problemas Derivados

1. Baja calidad de datos
2. Inconsistencia
3. Espacio innecesario
4. Impacto en rendimiento de modelos

#### Proceso de Resolución

**Paso 1: Identificar**
- Duplicados exactos: Usando identificadores únicos
- Duplicados no exactos: Fuzzy matching (Jaro-Winkler, Levenshtein)

**Paso 2: Estandarizar**
- Normalizar datos para facilitar comparación
- Mayúsculas/minúsculas
- Limpieza de datos
- Ejemplo: "calle Mayor", "C/ Mayor", "C. Mayor" → "Calle Mayor"

**Paso 3: Fusionar o Eliminar**
- **Fusionar (Merge)**: Combinar registros duplicados
  - Conservar datos más completos y actualizados
- **Eliminar (Delete)**: Si no se puede fusionar
  - Eliminar duplicado menos relevante

#### Herramientas

- Herramientas ETL comerciales
- Librerías open source: Python (Pandas, Dask, Dedupe)
- SQL: GROUP BY, DISTINCT

---

## TEMA 7: Diseño de Flujos ETL con Jobs en Pentaho {#tema-7}

### 7.1 Ciclo de Vida del Proyecto IA

El ciclo completo incluye:

**Fase de Definición**:
- Objetivos del modelo
- Casos de uso

**Fase de Datos**:
- Analizar y evaluar necesidades
- Recolectar
- Limpiar
- Estructurar
- Enriquecer datos

**Fase de Modelo**:
- Seleccionar modelo
- Entrenar
- Probar, ejecutar, optimizar
- Métricas clave
- Validar fiabilidad
- Alineación con objetivos

### 7.2 Flujos de Trabajo

#### Definición

Diseño y desarrollo de flujos de trabajo:
- Usando pasos o entradas
- Unidas por saltos
- Que pasan datos de un elemento al siguiente
- Facilitan análisis de grandes volúmenes

#### Tipos de Archivos

1. **Transformations**: Realizan tareas ETL
   - Input: Adquisición de datos
   - Transform: Operaciones con datos
   - Output: Carga de datos

2. **Jobs**: Organizan actividades ETL
   - Definen el flujo
   - Especifican dependencias
   - Controlan ejecución

### 7.3 Diseño de Jobs en Pentaho

#### Categorías de Pasos para Jobs

**1. General**
- Pasos de inicio de trabajo
- Ejecución de transformaciones o trabajos
- Otras operaciones

**2. Mail**
- Envío de correos
- Recuperación y validación de cuentas

**3. File Management**
- Gestión de operaciones sobre ficheros y carpetas
- HTTP, FTP

**4. Conditions**
- Comprobaciones sobre conexiones
- Comprobaciones sobre bases de datos
- Comprobaciones sobre ficheros

**5. Scripting**
- Scripts en JavaScript
- Scripts en Shell
- Scripts en SQL

**6. Bulk Loading**
- Cargas a MySQL y MSSQL

**7. XML**
- Validaciones XML (DTD, XSD, XSL)

**8. Utility**
- Ejecución de transformaciones
- Ping, syslog, Nagios

**9. Repository**
- Operaciones con repositorio
- De transformaciones y trabajos

**10. File Transfer**
- Gestión ficheros FTP, FTPS, SFTP

**11. File Encryption**
- Sistema PGP (Pretty Good Privacy)
- Envío y recepción de ficheros

### 7.4 Variables y Parámetros

#### Uso de Variables en Procesos ETL

**Configuración**:
- A nivel de sistema
- Dinámicamente en un trabajo

**Ámbito**:
- Específico que permite ejecución en paralelo
- Mismo trabajo/transformación con diferentes variables
- Mismo sistema a nivel de:
  - JVM
  - Job actual
  - Sesión

**Tipos**:
- Variables de sistema
- Variables definidas por el usuario

#### Ventajas

1. **Flexibilidad**: Misma transformación con distintos parámetros
2. **Reutilización**: Código genérico
3. **Configuración Externa**: Parámetros sin cambiar código
4. **Ejecución Paralela**: Diferentes variables en paralelo

---

## TEMA 8: Transformación y Enriquecimiento de Datos en LOD {#tema-8}

### 8.1 Web Semántica y Linked Open Data

#### Semántica Web

**Definición**: Extensión de la Web tradicional para dotarla de significado, que pueda ser entendida por máquinas y humanos

**Visión**: Convertir toda la información del mundo en una gran base de datos interconectada

#### RDF (Resource Description Framework)

**Concepto**: Proporciona un modelo simple de conveying meaning usando **tripletas**

**Estructura**: Sujeto - Predicado - Objeto

Ejemplo:
```
Sujeto: Miguel de Cervantes
Predicado: es_autor_de
Objeto: El Quijote
```

#### Stack Semántico

Capas de la Web Semántica (de abajo a arriba):

1. **Capa Base**:
   - XML: Sintaxis
   - Unicode: Character Set
   - URI: Identifiers

2. **Capa de Datos**:
   - RDF: Data interchange
   - RDFS: Taxonomies

3. **Capa de Esquema**:
   - OWL: Ontologies

4. **Capa de Consulta**:
   - SPARQL: Querying

5. **Capa de Reglas**:
   - RIF/SWRL: Rules

6. **Capas Superiores**:
   - Proof
   - Trust
   - Unified Logic
   - User Interface & Applications
   - Cryptography

### 8.2 Ontologías y Vocabularios

#### ¿Qué es una Ontología?

**Definición lingüística**: Parte de la metafísica que trata del ser

**En IA**: Red o sistema de datos que define las relaciones existentes entre conceptos de un dominio

**Propósito**: Clases y propiedades para describir recursos

#### Ontologías para Modelar Información

Ejemplos ampliamente usadas:
- **BIBFRAME**: Library of Congress
- **Schema.org**: Google, Bing, Yahoo
- **RDA Registry**: Descripción de recursos bibliográficos
- **CIDOC-CRM**: Patrimonio cultural
- **DCAT**: Catálogos de datos

#### ¿Qué es una Taxonomía o Vocabulario?

**Definición**: Clasificación sistemática y jerárquica con nombres

**En datos**: Términos para describir y clasificar recursos

**Diferencia con Ontología**: Las taxonomías son menos complejas, solo jerarquías de clasificación

#### Vocabularios Promovidos

Instituciones como IFLA, W3C, DARIAH mantienen vocabularios estándar

### 8.3 Wikidata

#### Características

- **Datos estructurados**
- **Dominio público**
- **Editado por la comunidad**
- **Basado en estándares**
- **Multilingüe**

#### Identificadores Únicos

Cada entidad tiene un identificador único:
- Ejemplo: Q5682 = Miguel de Cervantes
- Ejemplo: P569 = Fecha de nacimiento (propiedad)

#### Representación

**En Tripletas**:
```
wd:Q5682 wdt:P569 1547
```

**En Grafo**:
```
wd:Q5682 
  ├─ wdt:P569 → 1547
  ├─ wdt:P31 → wd:Q5 (ser humano)
  ├─ wdt:P21 → wd:Q6581097 (masculino)
  └─ wdt:P18 → [imagen]
```

#### Espacios de Nombre

Para simplificar, se usan prefijos:
- `wd:` = `http://www.wikidata.org/entity/`
- `wdt:` = `http://www.wikidata.org/prop/direct/`

Ejemplo:
- `wd:Q5682` en lugar de `http://www.wikidata.org/entity/Q5682`

### 8.4 SPARQL: Consultas a Datos RDF

#### Estructura Básica

```sparql
PREFIX ex: <example.org>
SELECT *
WHERE { 
    ?s ?p ?o 
}
```

**Componentes**:
- **PREFIX**: Espacios de nombre a usar
- **SELECT**: Columnas a devolver (* = todas)
- **WHERE**: Tripletas para restricciones
- Variables comienzan con `?`

#### Ejemplo Simple

```sparql
SELECT ?autor ?idbvmc
WHERE {
  ?autor wdt:P2799 ?idbvmc
}
LIMIT 10
```

Explicación:
- `?autor`: Variable para el recurso (identificador en Wikidata)
- `wdt:P2799`: Propiedad que enlaza a otros recursos
- `?idbvmc`: Variable para el resultado

#### Labels Automáticos

```sparql
SELECT ?autor ?autorLabel ?idbvmc
WHERE {
  ?autor wdt:P2799 ?idbvmc .
  SERVICE wikibase:label {
    bd:serviceParam wikibase:language "[AUTO_LANGUAGE],es"
  }
}
LIMIT 10
```

Si añadimos "Label" al nombre de la variable, automáticamente recupera la etiqueta.

#### Filtros

```sparql
SELECT ?autor ?autorLabel ?idbvmc ?fechaNacimiento
WHERE {
  ?autor wdt:P2799 ?idbvmc .
  ?autor wdt:P569 ?fechaNacimiento
  FILTER("1500-01-01"^^xsd:dateTime <= ?fechaNacimiento 
    && ?fechaNacimiento < "1550-01-01"^^xsd:dateTime)
  SERVICE wikibase:label {
    bd:serviceParam wikibase:language "[AUTO_LANGUAGE],es"
  }
}
LIMIT 10
```

#### Uso Avanzado

**Values y Bind**:
- Asignar valores específicos a variables
- Asignar resultado de expresión a variable

**Service**:
- Consultas federadas entre repositorios SPARQL

**Visualizaciones**:
- `#defaultView:Map`
- `#defaultView:Graph`

**Expresiones Regulares**:
- `FILTER regex(?x, "pattern" [, "flags"])`
- Ejemplo: `FILTER regex(?nombre, "g", "i")` → contiene "g" o "G"

**Paginación**:
- `LIMIT`: Número máximo de resultados
- `OFFSET`: Número de resultados a saltar

### 8.5 Transformación de Datos a RDF

#### Procesos

1. **Data Extraction**: Extraer datos de ficheros (biblio.json → CSV)
2. **Data Exploration**: Explorar estructura de datos originales
3. **Transformation to LOD**: Convertir a RDF usando vocabularios (Schema.org, EDM)
4. **Data Exploration with SPARQL**: Explorar datos RDF
5. **Data Quality**: Validación usando ShEx (Shape Expressions)

#### Herramientas

- **Jupyter Notebooks**: Para procesos reproducibles
- **OpenRefine**: Limpieza y transformación visual
- **Jena**: Herramientas para RDF
- **RDFLib**: Librería Python para RDF

#### Ejemplo: Moving Image Archive

Datos de metadatos disponibles como MARCXML y Dublin Core
Se transforman a RDF y se enriquecen con repositorios externos

### 8.6 Enriquecimiento con Propiedades Semánticas

#### owl:sameAs

Conecta recursos que representan la misma entidad en diferentes bases de datos

Ejemplo:
```rdf
<https://data.cervantesvirtual.com/person/40>
  owl:sameAs <https://www.wikidata.org/entity/Q5682>
```

#### skos:exactMatch

Conexión más débil que owl:sameAs

#### wdt:P2799

Propiedades específicas de Wikidata que enlazan datos

### 8.7 Linked Open Data Cloud

#### Concepto

Red de repositorios de datos abiertos conectados

#### Estadísticas

- Noviembre 2025: 1678 repositorios
- Dominios: Cross Domain, Geography, Government, Life Sciences, Linguistics, Media, Publications, Social Networking, User Generated

#### Ejemplos de Instituciones

- Library of Congress (id.loc.gov)
- National Library of Sweden (libris.kb.se/sparql)
- Europeana
- British Library
- Deutsche Nationalbibliothek
- Biblioteca Nacional de España (datos.bne.es)
- Biblioteca Virtual Miguel de Cervantes

### 8.8 Calidad de Datos en LOD

#### Validación con ShEx

Shape Expressions (ShEx) para validar estructura RDF

#### Metricas de Calidad

- Completitud
- Exactitud
- Consistencia
- Uniformidad
- Integridad referencial

---

## TEMA 9: Visualización y Reutilización de Datos {#tema-9}

### 9.1 Transformación de Datos

#### Ejemplo: Moving Image Archive (Scotland)

**Datos origen**:
- Formato: MARCXML y Dublin Core
- Fuente: National Library of Scotland metadata collections

**Proceso**:
1. Lectura de CSV
2. Generación de fichero TTL con tripletas RDF
3. Transformación a RDF
4. Exploración con SPARQL
5. Validación de calidad

### 9.2 Reutilización de Datos

#### Preguntas Clave

- ¿Qué datos tenemos? ¿Formato? ¿Enriquecidos?
- ¿Es necesario realizar limpieza?
- ¿Qué quiero analizar? ¿Cuál es el objetivo?
- ¿Quién es mi audiencia? (Estudiantes, Investigadores, etc.)
- ¿Qué infraestructura tengo? ¿Límites de memoria/espacio?
- ¿Qué licencia tienen los datos?

#### Comunidades y Recursos

- GLAM Labs (galleries, libraries, archives, museums)
- Comunidades de humanidades digitales

### 9.3 Visión por Computador

#### Problemas Comunes

1. **Classification**: Asignar categoría a imagen
2. **Detection**: Localizar objetos en imagen
3. **Segmentation**: Delimitar áreas de la imagen

### 9.4 Visualización de Datos

#### Herramientas

- **Jupyter Notebooks**: Análisis interactivo
- **Folium**: Visualización geográfica
- **Wikidata Query Service**: Visualizaciones integradas

#### Proyectos Ejemplares

**Ejemplo: ATRIUM Project**

Enfoque reproducible para publicar y reutilizar colecciones como datos:
1. Extracción de datos
2. Exploración de datos
3. Transformación a LOD
4. Exploración con SPARQL
5. Validación de calidad (ShEx)

**Ejemplo: Humanidades Digitales**

- Wikidata como plataforma para facilitar acceso y enriquecimiento
- SPARQL para recuperar información
- Edición de recursos
- Visualización en mapas y grafos

---

## TEMA 10: Infraestructuras para Almacenamiento y Procesamiento de Datos {#tema-10}

### 10.1 Ciencia Abierta y Datos

#### Ciencia Abierta (Open Science)

**Movimiento internacional** para facilitar:
- Acceso a datos abiertos
- Software con licencias open source
- Métodos
- Resultados
- Colaboración

#### Digital Commons

"Bienes comunes digitales": Recursos digitales compartidos
- Software
- Conocimiento
- Datos

**Características**:
- Acceso abierto
- Gestión participativa
- Licencias que preservan reutilización
- Infraestructura y plataformas para implementar Open Science

### 10.2 Economía del Dato

#### Proyecciones Europeas

- **2025**: Fuerte aumento del valor de la economía del dato
- Aumento del impacto en términos de PIB: +1 punto porcentual
- **2030**: Economía del dato (UE27 + Reino Unido) superará 1 billón de euros
- Tasa de crecimiento anual: 5.6% entre 2025-2030

#### Inversiones

Next Generation EU y fondos de recuperación financian:
- Tecnología cloud
- 5G
- IoT
- Dispositivos inteligentes
- Inteligencia artificial
- Infraestructura digital

### 10.3 Datos en Europa

#### Importancia Estratégica

Los datos son recurso esencial para:
- Crecimiento económico
- Competitividad
- Innovación
- Creación de empleo
- Progreso social

#### Beneficios Esperados

- Mejorar la salud
- Crear sistemas de transporte seguros y limpios
- Generar nuevos productos y servicios
- Reducir coste de servicios públicos
- Mejorar sostenibilidad y eficiencia energética

### 10.4 Infraestructuras Actuales

#### Problema Actual

La mayoría de datos almacenados por grandes corporaciones:
- Amazon Web Services (AWS)
- Google Cloud Platform (GCP)
- Microsoft Azure

**Problemas**:
- Falta de transparencia
- Reuso de datos para entrenar modelos IA privados
- Instituciones restringen acceso a colecciones

#### Solución Europea: Espacios de Datos (Dataspaces)

**Concepto**: Modelo federado de compartición de datos

**Definición**: Lugar de generación de valor alrededor del dato mediante compartición voluntaria en entorno de **soberanía, confianza y seguridad**

**Actores**:
- **Promotor**: Responsable de gobierno y gestión
- **Proveedores**: Conjuntos y servicios de datos
- **Consumidores**: Conjuntos y servicios de datos
- **Proveedor tecnológico**: Desplegar espacio de datos

### 10.5 Enlaces Permanentes

#### ¿Qué es?

Permite a usuario encontrar contenido mediante URL **siempre accesible**

**Ejemplos**: ORCID, DOI

**Ventajas**:
- Acceso permanente
- Información sobre tipo de recurso
- Facilita gestión de información
- Adopción de tecnologías avanzadas

#### Estrategias y Iniciativas

- FAIR principles
- Políticas de instituciones (British Library, Europeana, etc.)
- Nacionales: Australia, España, etc.
- Código4lib

#### Beneficios

| Beneficio | Descripción |
|-----------|------------|
| Conexión | Vinculación de recursos |
| Descubrimiento | Facilita búsqueda |
| Calidad | Consistencia de datos |
| Visibilidad | Mayor exposición |
| Medición | Impacto cuantificable |
| Sostenibilidad | Permanencia en tiempo |
| Deduplicación | Gestión de duplicados |
| SEO | Mejora posicionamiento |
| Reutilización | Facilita reuso |
| Enriquecimiento | Posibilidades nuevas |

#### Ejemplos de Enlaces Permanentes

- `https://data.cervantesvirtual.com/person/40`
- `https://datos.bne.es/persona/XX1718747.html`
- `https://data.bnf.fr/11928669/voltaire/`
- `https://id.loc.gov/resources/works/10118761.html`
- `http://www.wikidata.org/entity/Q5682`

**Estructura**:
- Dominio
- Tipo de entidad
- Identificador

### 10.6 Colecciones como Datos

#### Concepto

Tratar colecciones digitales como datos estructurados y accesibles

#### Plataformas

- **Zenodo**: Repositorio de datos abiertos
- **GitHub**: Control de versiones y datos
- **Wikibase Cloud**: Bases de datos tipo wiki
- **EOSC**: European Open Science Cloud
- **ECCCH**: European Centre for Cultural Heritage

### 10.7 Principios FAIR y CARE

#### FAIR (Findable, Accessible, Interoperable, Reusable)

1. **Findable** (Encontrable)
   - Metadatos descriptivos
   - Identificadores únicos (PID)
   - Indexable

2. **Accessible** (Accesible)
   - Acceso mediante protocolo estándar
   - Autenticación si necesario
   - Metadatos accesibles aunque datos no lo sean

3. **Interoperable** (Interoperable)
   - Usa lenguajes y formatos estándar
   - Vocabularios controlados
   - Referencias calificadas

4. **Reusable** (Reutilizable)
   - Metadatos descriptivos
   - Licencia clara
   - Documentación

#### CARE (Collective Benefit, Authority to Decide, Responsibility, Ethics)

Complementa FAIR enfocándose en derechos indígenas:

1. **Collective Benefit** (Beneficio Colectivo)
   - Datos para beneficio colectivo

2. **Authority to Decide** (Autoridad para Decidir)
   - Pueblos indígenas deciden sobre sus datos

3. **Responsibility** (Responsabilidad)
   - Responsabilidad hacia comunidades

4. **Ethics** (Ética)
   - Uso ético de datos

### 10.8 Documentación de Datos (Datasheets)

#### Concepto

Documento que describe características y limitaciones de un dataset

#### Elementos

- Motivación: Por qué se creó
- Composición: Qué contiene
- Colección: Cómo se recopiló
- Pre-procesamiento: Transformaciones
- Distribución: Cómo se comparte
- Mantenimiento: Actualizaciones futuras

### 10.9 Infraestructuras Específicas

#### Zenodo

- Repositorio de datos abiertos
- Asigna DOI a datasets
- Acceso permanente
- Respeta principios FAIR

#### GitHub

- Control de versiones
- Colaboración en código y datos
- Licencias open source

#### Wikibase Cloud

- Bases de datos tipo Wikidata
- Creación de wikibases propias
- Consultas SPARQL
- Edición colaborativa

#### EOSC (European Open Science Cloud)

- Infraestructura cloud europea
- Acceso a servicios de cómputo y almacenamiento
- Para investigación abierta

#### ECCCH (European Centre for Cultural Heritage)

- Infraestructura para patrimonio cultural
- Integración de colecciones

### 10.10 Espacios de Datos Europeos

#### Concepto

Ecosistema federado de compartición de datos voluntaria

#### Componentes

```
Metadatos
    ↓
Conector ← → Datos
    ↓
Proveedor de datos
    ↓
[Servicios de CH Data Space]
├─ Data Marketplace
├─ Identity Provider
├─ Data App Store
├─ Vocabulary Provider
├─ Clearing House

Consumidor ← Conector ← Datos
                ↓
        [En la nube: Gaia-X]
```

#### Ejemplo: Common European Data Space for Cultural Heritage

- Acceso a datos de patrimonio cultural de Europa
- Integración de colecciones de museos, bibliotecas, archivos
- Búsqueda unificada
- Preservación de soberanía de datos

---

## TALLER 1: Modelado Conceptual Práctico {#taller-1}

### T1.1 Caso de Estudio: Pedidos de Compañía Tecnológica

#### Requisitos

La compañía tecnológica captura datos a nivel de pedidos. Un pedido incluye:

**Del Pedido**:
- Número de unidades
- Valor de venta del producto
- Descuento
- Beneficio de la venta
- Puntos que acumula cliente
- Gastos de envío

**Timing**:
- Fecha de recepción del producto
- Almacén que lo dispensa
- Fecha cuando paquete se deja en mensajería
- Tipo de envío (elegido por cliente)
- Prioridad del pedido

**Del Cliente**:
- Nombre
- Número de cliente
- Tipo de cliente
- Código postal
- Ciudad
- Estado
- País
- Región
- Mercado al que pertenece
- Permite analizar mercados potenciales y clientes clave

**Del Producto**:
- Nombre del producto
- Tipo de producto

**Devoluciones**:
- Cuáles productos se devolvieron
- Motivo principal de devolución

### T1.2 Proceso Kimball (4 Etapas)

#### Paso 1: Seleccionar el Proceso de Negocio a Modelar

**Selección**: Gestión de pedidos realizados por clientes

**Exclusiones**: No incluimos pedidos cancelados antes de procesar cobro, ni carritos de compra sin completar

### T1.3 Paso 2: Seleccionar la Granularidad

**Decisión**: Granularidad fina (high/fine grain)

**Justificación**: 
- Cada fila = información de un artículo del pedido
- Permite análisis detallado
- Soporta agregaciones hacia arriba

**Información de cada fila**:
- Número de unidades
- Valor de venta
- Descuento
- Beneficio
- Puntos
- Gastos de envío

**Timing**:
- Fecha recepción producto
- Almacén dispensador
- Fecha entrega a mensajería

### T1.4 Paso 3: Dimensiones

**Dimensiones identificadas**:

1. **Tiempo (2 aspectos)**:
   - Fecha del pedido
   - Fecha de envío

2. **Almacén**: Que dispensa

3. **Compañía de Mensajería**: (Implícita en tipo de envío)

4. **Cliente**:
   - Nombre
   - Número de cliente
   - Tipo de cliente
   - Código postal
   - Ciudad
   - Estado
   - País
   - Región
   - Mercado

5. **Tipo de Envío**

6. **Prioridad**

7. **Producto**:
   - Nombre
   - Tipo

8. **Devoluciones**: Motivo de devolución

### T1.5 Paso 4: Medidas

**Medidas de la Tabla de Hechos**:

1. **Número de unidades**
2. **Valor de venta**
3. **Descuento**
4. **Beneficio**
5. **Puntos** (acumulados por cliente)
6. **Gastos de envío**

#### Tipos de Medidas

- **Aditivas**: Todas las medidas son aditivas sobre todas las dimensiones (excepto posiblemente algunas restricciones semánticas)
- **Semi-aditivas**: Puntos (acumulativo por cliente, no por producto)

### T1.6 Estructura del Esquema Estrella Resultante

```
            Dimensión Tiempo
            (Fecha Pedido/Envío)
                    ↓
Dimensión Producto ← Tabla Hechos Pedidos → Dimensión Cliente
                    (con medidas)
                    ↑
        Dimensión Almacén
            Dimensión Envío
       Dimensión Prioridad
      Dimensión Devoluciones
```

#### Tabla de Hechos: Detalle Pedidos

```
- pedido_id (FK)
- producto_id (FK)
- cliente_id (FK)
- almacen_id (FK)
- tiempo_id (FK)
- tipo_envio_id (FK)
- prioridad_id (FK)
- num_unidades (medida)
- valor_venta (medida)
- descuento (medida)
- beneficio (medida)
- puntos (medida)
- gastos_envio (medida)
```

#### Dimensiones

**Dimensión Producto**:
- producto_id (PK)
- nombre_producto
- tipo_producto

**Dimensión Cliente**:
- cliente_id (PK)
- numero_cliente
- nombre_cliente
- tipo_cliente
- codigo_postal
- ciudad
- estado
- pais
- region
- mercado

**Dimensión Almacén**:
- almacen_id (PK)
- nombre_almacen
- ubicacion

**Dimensión Tiempo**:
- tiempo_id (PK)
- fecha
- dia
- mes
- año
- trimestre
- semana

**Dimensión Tipo de Envío**:
- tipo_envio_id (PK)
- descripcion_envio

**Dimensión Prioridad**:
- prioridad_id (PK)
- nivel_prioridad

**Dimensión Devoluciones**:
- devolucion_id (PK)
- motivo_devolucion
- fecha_devolucion

---

## RESUMEN FINAL: Conceptos Clave

### Conceptos Fundamentales

1. **Big Data**: Volumen, Variedad, Velocidad, Veracidad, Valor
2. **OLTP vs OLAP**: Transaccionales vs Analíticos
3. **Data Warehouse**: Repositorio central de datos históricos
4. **Modelado Multidimensional**: Hechos, Dimensiones, Jerarquías
5. **Esquema Estrella**: Tabla de hechos rodeada de dimensiones
6. **ETL**: Extract, Transform, Load
7. **Expresiones Regulares**: Patrones para limpiar datos
8. **Datos Abiertos Enlazados (LOD)**: RDF, SPARQL, Wikidata
9. **FAIR**: Findable, Accessible, Interoperable, Reusable
10. **Espacios de Datos**: Ecosistema federado de compartición

### Herramientas Principales

1. **Pentaho Data Integration (Kettle)**:
   - Spoon: Entorno gráfico
   - Pan: Transformations por línea de comandos
   - Kitchen: Jobs por línea de comandos
   - Carte: Servidor web

2. **Wikidata**: Base de datos colaborativa
3. **SPARQL**: Lenguaje de consulta para RDF
4. **OpenRefine**: Limpieza y transformación
5. **Jupyter**: Análisis interactivo

### Metodología de Diseño

1. **Requisitos del Negocio**
2. **Identificación de Hechos y Dimensiones**
3. **Definición de Granularidad**
4. **Selección de Jerarquías**
5. **Normalización vs Desnormalización**
6. **Implementación del Esquema Estrella**
7. **Diseño e Implementación de ETL**
8. **Validación y Testing**

---

**Este documento comprende todo el contenido de los 10 temas principales más el taller práctico de la asignatura APD 2025.**

**Buena suerte en el examen!**

