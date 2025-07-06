# Práctica Semana 9 - Introducción a MPI: Investigación y Preparación del Entorno (Parte 1 de 2)

## Objetivo de la práctica

Esta práctica introductoria tiene como finalidad que el alumnado conozca los fundamentos de MPI (Message Passing Interface), identifique su origen y desarrollo, comprenda sus aplicaciones y elabore un informe detallado sobre cómo se prepararía un entorno de desarrollo para programar en MPI utilizando diferentes sistemas operativos y lenguajes de programación.

La práctica es individual y corresponde a la primera parte de un trabajo dividido en dos. La entrega final se realizará conjuntamente con la segunda parte de la práctica, en la Semana 10.

**Duración estimada para la realización en aula:** 2 horas

## Parte 1: Investigación Guiada sobre MPI (Tiempo estimado en aula: 1 hora)

### Tareas de Investigación

Cada estudiante deberá investigar y responder de forma individual a las siguientes cuestiones. El contenido se integrará en un informe o presentación que formará parte de la entrega conjunta en la siguiente práctica.

#### 1. ¿Qué es MPI?

- Definir MPI.
- Propósito principal en la computación paralela y distribuida.
- Relevancia de MPI en entornos de alto rendimiento.

#### 2. ¿MPI es un lenguaje de programación o una biblioteca?

- Aclarar si MPI es un lenguaje de programación o una biblioteca.
- Explicar con qué lenguajes de programación es compatible, destacando C y C++.
- Incluir otras opciones (Fortran, Python, Java) y cómo se integran estas bibliotecas en cada caso.

#### 3. ¿Quién desarrolla y mantiene MPI?

- El papel del MPI Forum en la estandarización y evolución de MPI.
- Organismos, empresas y universidades que participan.
- Ejemplos de colaboración de centros de supercomputación y multinacionales tecnológicas.

#### 4. Versiones de MPI

- Descripción de la evolución: MPI-1, MPI-2, MPI-3, MPI-4.
- Resaltar mejoras clave en cada versión.
- Estado actual del estándar y su adopción.

#### 5. Principales usos de MPI

Cada estudiante deberá investigar y documentar:

- Al menos tres áreas de aplicación donde se utilice MPI, explicando cómo MPI contribuye a resolver problemas complejos en esas áreas.
  - Ejemplos de ámbitos:
    - Supercomputación y simulaciones científicas.
    - Inteligencia artificial y machine learning distribuido.
    - Análisis de datos a gran escala o modelado de fluidos.
- Al menos tres organizaciones o instituciones relevantes que utilicen MPI en sus sistemas de computación de alto rendimiento.
  - Ejemplos de entidades:
    - NASA: simulaciones aeroespaciales.
    - CERN: procesamiento de datos del Gran Colisionador de Hadrones.
    - Barcelona Supercomputing Center: simulaciones climáticas.

En el informe deben incluir:

- Una breve descripción del caso de uso o aplicación concreta de cada organización.
- Una explicación sobre por qué MPI es la tecnología adecuada en ese caso (ventajas frente a otros modelos o paradigmas).

## Parte 2: Elaboración del Informe sobre Preparación de Entornos (Tiempo estimado: 1 hora)

Cada alumno deberá elaborar un informe técnico que describa:

1. Una introducción breve sobre cómo se realizaría la instalación y preparación de un entorno MPI en cada uno de los tres sistemas operativos principales (Windows, Linux y MacOS) para su uso en C o C++. Además, deberá mencionar qué otras opciones existen para lenguajes como Python, Fortran o Java en esos sistemas.
2. A continuación, elegirá uno de los tres sistemas operativos y desarrollará de forma detallada cómo se haría la instalación y configuración del entorno en ese caso concreto. Deberá justificar por qué ha elegido ese sistema operativo (por ejemplo, facilidad de instalación, familiaridad con el entorno, soporte de herramientas, etc.).

### Estructura mínima del informe:

- Resumen breve (una tabla o esquema) de las opciones disponibles en Windows, Linux y MacOS.
- Desarrollo detallado de la instalación y preparación en el sistema operativo elegido, incluyendo:
  - Recursos necesarios (compiladores, bibliotecas MPI, entornos de desarrollo).
  - Pasos de instalación.
  - Configuración del entorno para trabajar en C o C++.
  - Opcionalmente, inclusión de herramientas adicionales para otros lenguajes.

## Relación con los Resultados de Aprendizaje de la Asignatura

Esta práctica contribuye a alcanzar los siguientes Resultados de Aprendizaje del módulo de Computación de Alto Rendimiento:

1. Comprender los principios básicos de la computación paralela y distribuida, así como los estándares actuales de comunicación entre procesos en sistemas de memoria distribuida (RA 1).
2. Conocer y documentar los estándares de comunicación entre procesos, valorando las opciones disponibles para diferentes plataformas y lenguajes de programación (RA 2).
3. Planificar la instalación y configuración de entornos de ejecución para la programación paralela, elaborando documentación técnica adecuada (RA 3).

## Entrega y Rúbrica Orientativa

- El documento resultante de esta práctica será entregado conjuntamente con la segunda parte de la práctica (Semana 10).

### Rúbrica Orientativa para la Parte 1 (Semana 9)

| Criterio                                      | Puntos | Descripción                                                                 |
|----------------------------------------------|--------|-----------------------------------------------------------------------------|
| Investigación sobre MPI                      | 4      | Claridad y profundidad en la definición, evolución, mantenimiento y aplicaciones de MPI. |
| Documentación de áreas de aplicación y ejemplos reales | 2    | Calidad de los ejemplos y justificación de su relevancia.                   |
| Análisis de opciones de instalación en los 3 sistemas OS | 2    | Precisión y claridad en la descripción de las alternativas para Windows, Linux y MacOS. |
| Desarrollo detallado de un caso específico    | 2      | Exhaustividad en el sistema operativo elegido y justificación clara de la elección. |

**Total orientativo:** 10 puntos.
Esta rúbrica es orientativa y puede ser revisada para la evaluación conjunta de las dos partes en la Semana 10.
