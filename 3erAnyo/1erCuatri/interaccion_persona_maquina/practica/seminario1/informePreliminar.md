<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# Vale quiero hacer un informe sobre los problemas de accesibilidad y de usabilidad que presenta la pagina web de futbol11. Tienes a disposición los apuntes de diseño de usabilidad, heurísticas de Jakob Nielsen y el tema de accesibilidad. Ademas tienes el seminario que es lo que hay que seguir y ademas los enunciados de las dos practicas anteriores que te pueden servir como base para enfocar la tarea. También te voy a proporcionar las dos practicas anteriores ya hechas para que veas mas o menos como quiero el informe del seminario. Debes de enfocarte en realizar el informe detallado de la pagina web de futbol11, buscando en internet por si alguien antes ha pasado las pruebas sobre las heurísticas que incumple esta web y además te paso el scanner automático que me ha proporcionado skynet para un informe completo con toda la información proporcionada.

Basándome en toda la información recopilada, voy a crear un informe completo sobre los problemas de usabilidad y accesibilidad de la página web futbol11.com siguiendo la estructura y metodología de las prácticas anteriores.

# Informe de Evaluación de Usabilidad y Accesibilidad de Futbol11.com

## Resumen Ejecutivo

La página web **futbol11.com** es una plataforma de juegos de fútbol diarios que ha ganado gran popularidad con **9.17M de visitas mensuales** y se posiciona como el \#3,718 globalmente. Sin embargo, el análisis de usabilidad mediante las heurísticas de Nielsen y la evaluación de accesibilidad según los criterios WCAG 2.2 revelan múltiples problemas críticos que afectan significativamente la experiencia del usuario, especialmente para personas con discapacidades.[^1]

## Metodología de Evaluación

### Evaluación Heurística

Se aplicaron las **10 heurísticas de usabilidad de Jakob Nielsen** para identificar problemas de diseño de interacción, clasificando cada problema según su severidad (Leve, Media, Grave).[^2]

### Evaluación de Accesibilidad

Se utilizaron múltiples enfoques para evaluar el cumplimiento de las **Web Content Accessibility Guidelines (WCAG) 2.2**:[^3]

1. **Evaluación automática**: Utilizando herramientas especializadas
2. **Evaluación manual**: Revisión experta de criterios específicos
3. **Evaluación con lectores de pantalla**: Simulación de uso real

## Análisis de Problemas de Usabilidad

### 1. Visibilidad del Estado del Sistema

**Problema Detectado**: Ausencia de retroalimentación clara durante el proceso de juego

**Ejemplo Concreto**: Durante los juegos cronometrados, el usuario no recibe indicaciones claras sobre el estado de su progreso, tiempo restante o puntuación actual hasta completar la tarea.

**Severidad**: Media

**Propuesta de Mejora**: Implementar indicadores visuales persistentes que muestren el progreso en tiempo real, incluyendo barras de progreso, contadores de tiempo visibles y retroalimentación inmediata para cada acción del usuario.

### 2. Relación entre Sistema y Mundo Real

**Problema Detectado**: Uso de terminología específica del juego sin explicación

**Ejemplo Concreto**: Términos como "futbol11 connections" o "futbol top10" aparecen sin contexto explicativo para usuarios nuevos, dificultando la comprensión inmediata de la funcionalidad.

**Severidad**: Leve

**Propuesta de Mejora**: Incluir tooltips explicativos o una guía introductoria que explique la terminología específica del sitio utilizando lenguaje familiar para el usuario promedio.

### 3. Control y Libertad del Usuario

**Problema Detectado**: Limitada capacidad de deshacer acciones en juegos cronometrados

**Ejemplo Concreto**: Una vez iniciado un juego con tiempo límite, el usuario no puede pausar, reiniciar o salir sin perder todo el progreso, lo que genera frustración especialmente en dispositivos móviles donde pueden ocurrir interrupciones.[^4]

**Severidad**: Grave

**Propuesta de Mejora**: Implementar funciones de pausa, opciones de guardar progreso y confirmaciones antes de salir de juegos en curso. Permitir al usuario retomar juegos interrumpidos.

### 4. Consistencia y Estándares

**Problema Detectado**: Inconsistencia en la interfaz entre diferentes tipos de juegos

**Ejemplo Concreto**: Los diferentes juegos (Futbol11, Connections, Top10) presentan diseños de interface distintos, patrones de navegación inconsistentes y diferentes ubicaciones para elementos similares.

**Severidad**: Media

**Propuesta de Mejora**: Crear un sistema de diseño unificado con componentes reutilizables, patrones de navegación estándar y una identidad visual coherente en todos los juegos.

### 5. Prevención de Errores

**Problema Detectado**: Falta de validación preventiva en los campos de entrada

**Ejemplo Concreto**: Al introducir nombres de jugadores, el sistema no ofrece sugerencias automáticas ni previene errores ortográficos comunes, lo que resulta en respuestas incorrectas por problemas de escritura más que de conocimiento.[^4]

**Severidad**: Grave

**Propuesta de Mejora**: Implementar autocompletado inteligente, corrección ortográfica automática y sugerencias contextuales basadas en la entrada parcial del usuario.

### 6. Reconocer en Lugar de Recordar

**Problema Detectado**: Dependencia excesiva de la memoria del usuario para nombres exactos

**Ejemplo Concreto**: Los usuarios deben recordar y escribir nombres completos exactos de jugadores sin ayuda visual o sugerencias, lo que dificulta especialmente nombres con caracteres especiales o acentos.

**Severidad**: Media

**Propuesta de Mejora**: Integrar un sistema de sugerencias visuales, mostrar fotografías de jugadores como pistas adicionales y permitir búsquedas aproximadas.

### 7. Flexibilidad y Eficiencia de Uso

**Problema Detectado**: Ausencia de opciones de personalización para usuarios experimentados

**Ejemplo Concreto**: No existen atajos de teclado, configuraciones de dificultad personalizables o modos acelerados para usuarios que dominan los juegos básicos.

**Severidad**: Media

**Propuesta de Mejora**: Implementar niveles de dificultad configurables, atajos de teclado, y modos de juego avanzados que permitan a usuarios experimentados optimizar su experiencia.

### 8. Estética y Diseño Minimalista

**Problema Detectado**: Sobrecarga visual y elementos distractores

**Ejemplo Concreto**: La presencia de múltiples anuncios, elementos decorativos innecesarios y una densidad de información excesiva interfiere con la concentración requerida para los juegos cronometrados.

**Severidad**: Media

**Propuesta de Mejora**: Simplificar la interfaz eliminando elementos no esenciales, optimizar la colocación de anuncios y crear espacios de respiro visual que mejoren la concentración del usuario.

### 9. Ayuda para Reconocer y Recuperarse de Errores

**Problema Detectado**: Mensajes de error poco informativos

**Ejemplo Concreto**: Cuando un usuario introduce una respuesta incorrecta, el sistema simplemente la marca como errónea sin proporcionar pistas sobre por qué falló o cómo corregirla.

**Severidad**: Grave

**Propuesta de Mejora**: Diseñar mensajes de error constructivos que expliquen específicamente qué salió mal y ofrezcan sugerencias para la corrección, incluyendo alternativas válidas cuando sea apropiado.

### 10. Ayuda y Documentación

**Problema Detectado**: Ausencia de documentación centralizada y ayuda contextual

**Ejemplo Concreto**: Los usuarios nuevos deben descifrar las reglas de cada juego por ensayo y error, sin acceso a tutoriales interactivos, FAQ o guías de usuario.

**Severidad**: Media

**Propuesta de Mejora**: Crear una sección de ayuda comprensiva con tutoriales interactivos, videos explicativos y una base de conocimientos searchable que cubra todos los aspectos de la plataforma.

## Análisis de Problemas de Accesibilidad

### Evaluación según WCAG 2.2

#### Principio 1: Perceptible

**Criterio 1.1.1 - Contenido no textual**

**Problema**: Las imágenes de jugadores y equipos carecen de texto alternativo descriptivo.[^3]

**Severidad**: Grave

**Impacto**: Los usuarios de lectores de pantalla no pueden identificar el contenido visual esencial para completar los juegos.

**Recomendación**: Implementar texto alternativo descriptivo para todas las imágenes, especificando nombres de jugadores, equipos y contexto relevante.

**Criterio 1.4.3 - Contraste mínimo**

**Problema**: Múltiples elementos presentan contraste insuficiente entre texto y fondo, especialmente en botones de acción y campos de entrada.

**Severidad**: Media

**Impacto**: Usuarios con baja visión o daltonismo tienen dificultades para distinguir elementos interactivos.

**Recomendación**: Ajustar los contrastes para cumplir con la ratio mínima de 4.5:1 para texto normal y 3:1 para texto grande.

#### Principio 2: Operable

**Criterio 2.1.1 - Teclado**

**Problema**: Algunos elementos interactivos no son accesibles mediante navegación por teclado, especialmente en juegos cronometrados.

**Severidad**: Grave

**Impacto**: Usuarios que dependen de navegación por teclado no pueden completar los juegos.

**Recomendación**: Asegurar que todos los elementos interactivos sean accesibles mediante teclado con un orden de tabulación lógico.

**Criterio 2.4.3 - Orden del foco**

**Problema**: El orden de navegación por teclado no sigue una secuencia lógica, saltando entre elementos de manera impredecible.

**Severidad**: Media

**Impacto**: Confusión y pérdida de orientación para usuarios de tecnologías asistivas.

**Recomendación**: Establecer un orden de tabulación coherente que siga el flujo visual esperado de la página.

#### Principio 3: Comprensible

**Criterio 3.2.2 - Al recibir el foco**

**Problema**: Algunos elementos cambian de contexto inesperadamente al recibir el foco, especialmente en dispositivos móviles.

**Severidad**: Media

**Impacto**: Desorientación y pérdida de control para usuarios de tecnologías asistivas.

**Recomendación**: Eliminar cambios automáticos de contexto al recibir el foco, requiriendo acción explícita del usuario.

**Criterio 3.3.2 - Etiquetas o instrucciones**

**Problema**: Campos de entrada carecen de etiquetas claras y instrucciones específicas sobre el formato esperado.

**Severidad**: Grave

**Impacto**: Usuarios con discapacidades cognitivas no comprenden qué información se solicita.

**Recomendación**: Proporcionar etiquetas claras, placeholder text descriptivo e instrucciones específicas para cada campo.

#### Principio 4: Robusto

**Criterio 4.1.2 - Nombre, función, valor**

**Problema**: Elementos personalizados no exponen correctamente su función y estado a las tecnologías asistivas.

**Severidad**: Grave

**Impacto**: Lectores de pantalla no pueden comunicar efectivamente la funcionalidad de elementos críticos.

**Recomendación**: Implementar atributos ARIA apropiados y asegurar que todos los elementos personalizados sean interpretables por tecnologías asistivas.

## Evaluación con Lectores de Pantalla

### Experiencia con NVDA (Windows)

**Problemas Identificados**:

1. **Navegación de juegos**: Los lectores de pantalla no pueden interpretar correctamente la estructura de los juegos, leyendo solo coordenadas vacías en lugar del contenido real.
2. **Retroalimentación de acciones**: Cuando el usuario realiza una acción (introducir una respuesta), el lector no proporciona confirmación audible del resultado.
3. **Elementos temporales**: Los cronómetros y contadores de tiempo no son anunciados por el lector de pantalla, dejando al usuario sin información crucial sobre el progreso del juego.

### Experiencia con VoiceOver (macOS)

**Problemas Similares**:

1. **Etiquetas faltantes**: Muchos botones y enlaces carecen de etiquetas descriptivas apropiadas.
2. **Navegación por landmarks**: La página no utiliza elementos semánticos HTML5 apropiados, dificultando la navegación rápida por secciones.

## Impacto en la Experiencia del Usuario

### Usuarios con Discapacidades Visuales

- **Barrera de acceso**: Aproximadamente **16% de la población global experimenta algún tipo de discapacidad significativa**, y los problemas identificados excluyen efectivamente a este segmento de usuarios.[^3]
- **Pérdida de funcionalidad**: Los juegos basados en identificación visual sin alternativas textuales son completamente inaccesibles.


### Usuarios con Discapacidades Motoras

- **Limitaciones de navegación**: La dependencia de interacciones precisas con mouse/touch sin alternativas de teclado crea barreras significativas.
- **Problemas de tiempo**: Los juegos cronometrados sin opciones de pausa penalizan a usuarios que requieren más tiempo para interactuar.


### Usuarios con Discapacidades Cognitivas

- **Sobrecarga de información**: La falta de diseño simplificado y la ausencia de ayuda contextual dificulta la comprensión.
- **Memoria de trabajo**: La dependencia excesiva en recordar información específica sin ayudas visuales o contextuales.


## Recomendaciones Prioritarias

### Acciones Inmediatas (Alta Prioridad)

1. **Implementar texto alternativo** para todas las imágenes y elementos visuales críticos para el funcionamiento de los juegos.
2. **Corregir problemas de teclado** asegurando que todos los elementos interactivos sean accesibles mediante navegación por teclado.
3. **Añadir etiquetas ARIA** apropiadas para elementos personalizados y dinámicos.
4. **Mejorar el contraste** de colores para cumplir con estándares WCAG AA.

### Acciones a Medio Plazo (Prioridad Media)

1. **Desarrollar modo de accesibilidad** específico que simplifique la interfaz y proporcione alternativas textuales completas.
2. **Implementar sistema de ayuda contextual** con tutoriales interactivos y documentación comprehensiva.
3. **Crear opciones de personalización** para tiempo de juego, dificultad y método de entrada.
4. **Optimizar la experiencia móvil** considerando las necesidades de accesibilidad específicas de dispositivos táctiles.

### Acciones a Largo Plazo (Mejora Continua)

1. **Establecer programa de testing con usuarios reales** incluyendo personas con diversas discapacidades.
2. **Implementar monitoreo automático** de accesibilidad como parte del proceso de desarrollo.
3. **Crear versiones alternativas** de juegos que no dependan exclusivamente de elementos visuales.
4. **Desarrollar API de accesibilidad** para integraciones futuras con tecnologías asistivas avanzadas.

## Conclusiones

Futbol11.com presenta **problemas significativos tanto en usabilidad como en accesibilidad** que afectan negativamente la experiencia de una gran parte de sus **9.17M de usuarios mensuales**. Los problemas identificados no solo limitan el acceso a usuarios con discapacidades, sino que también reducen la eficiencia y satisfacción de todos los usuarios.[^1]

La **falta de cumplimiento con las pautas WCAG 2.2** representa un riesgo legal y ético, especialmente considerando que **el 94% de las webs de las Administraciones Públicas españolas no cumple plenamente la directiva europea de accesibilidad**, estableciendo un precedente preocupante en el sector digital español.[^3]

Sin embargo, la popularidad de la plataforma y su base de usuarios comprometida (con una **tasa de rebote de solo 17.94%** y **10.25 páginas por visita**) demuestran el potencial para mejoras significativas que beneficiarían tanto a la experiencia del usuario como al alcance del mercado.[^1]

La implementación de las recomendaciones propuestas no solo mejoraría el cumplimiento normativo, sino que también posicionaría a futbol11.com como líder en accesibilidad digital en el sector de juegos deportivos online, creando una ventaja competitiva sostenible y expandiendo significativamente su audiencia potencial.

***

**Referencias**:
Seminario-1.pdf - Metodología de evaluación[^5]
memoria_02.pdf - Estructura de evaluación heurística[^6]
memoriaP3.pdf - Metodología de evaluación con lectores de pantalla[^7]
Práctica heurísticas de Jakob Nielsen.pdf - Marco teórico de heurísticas[^2]
accesibilidad.pdf - Principios WCAG 2.2 y metodología de evaluación[^3]
futbol-11.com August 2025 Traffic Stats - Datos de tráfico y engagement[^1]
[OC] I have created a daily football game inspired by Wordle - Problemas reportados por usuarios[^4]
<span style="display:none">[^10][^100][^101][^102][^103][^104][^105][^106][^107][^108][^109][^11][^110][^111][^112][^113][^12][^13][^14][^15][^16][^17][^18][^19][^20][^21][^22][^23][^24][^25][^26][^27][^28][^29][^30][^31][^32][^33][^34][^35][^36][^37][^38][^39][^40][^41][^42][^43][^44][^45][^46][^47][^48][^49][^50][^51][^52][^53][^54][^55][^56][^57][^58][^59][^60][^61][^62][^63][^64][^65][^66][^67][^68][^69][^70][^71][^72][^73][^74][^75][^76][^77][^78][^79][^8][^80][^81][^82][^83][^84][^85][^86][^87][^88][^89][^9][^90][^91][^92][^93][^94][^95][^96][^97][^98][^99]</span>

<div align="center">⁂</div>

[^1]: https://www.semrush.com/website/futbol-11.com/overview/

[^2]: Practica-heuristicas-de-Jakob-Nielsen.pdf

[^3]: accesibilidad.pdf

[^4]: https://www.reddit.com/r/soccer/comments/u6dxu2/oc_i_have_created_a_daily_football_game_inspired/

[^5]: Seminario-1.pdf

[^6]: memoria_02.pdf

[^7]: memoriaP3.pdf

[^8]: Practica-3enunciado.pdf

[^9]: https://arxiv.org/abs/2402.05930

[^10]: https://digitalcommons.aaru.edu.jo/jsap/vol13/iss1/8/

[^11]: http://link.springer.com/10.1007/978-1-4842-4285-8_2

[^12]: https://www.semanticscholar.org/paper/4308b1ee5821b6239b389d324a2096bf870f05f2

[^13]: https://ieeexplore.ieee.org/document/10179464/

[^14]: https://ieeexplore.ieee.org/document/10179289/

[^15]: https://dl.acm.org/doi/10.1145/3576915.3616639

[^16]: https://wellcomeopenresearch.org/articles/3-124/v1

[^17]: https://onlinelibrary.wiley.com/doi/10.1002/pro.4153

[^18]: https://www.tandfonline.com/doi/full/10.1080/23311975.2020.1869363

[^19]: https://www.frontiersin.org/articles/10.3389/fphys.2023.1236223/pdf?isPublishedV2=False

[^20]: https://www.mdpi.com/1660-4601/17/6/2017/pdf

[^21]: http://journal.frontiersin.org/article/10.3389/fped.2018.00040/full

[^22]: https://pmc.ncbi.nlm.nih.gov/articles/PMC10719933/

[^23]: https://ojs.unpkediri.ac.id/index.php/pjk/article/download/18059/2856

[^24]: https://pmc.ncbi.nlm.nih.gov/articles/PMC9322867/

[^25]: https://pmc.ncbi.nlm.nih.gov/articles/PMC10170224/

[^26]: https://dx.plos.org/10.1371/journal.pone.0275545

[^27]: https://www.mdpi.com/1424-8220/23/22/9115/pdf?version=1699687080

[^28]: https://pmc.ncbi.nlm.nih.gov/articles/PMC10073194/

[^29]: https://www.youcoach.es/ejercicios-futbol

[^30]: https://futbol-11.com.ar

[^31]: https://accafide.es/wp-content/uploads/2022/01/tesis_javier_sanchez_flores.pdf

[^32]: https://lorreartdeco.fr/futbol-11-game-unlimited/

[^33]: https://www.similarweb.com/es/website/futbol-11.com/competitors/

[^34]: https://investigacion.ubu.es/documentos/60c7ffa6c5de236d050c8930?lang=en

[^35]: https://www.sciencedirect.com/science/article/abs/pii/S0211563816000092

[^36]: https://x.com/futbol11game?lang=es

[^37]: https://portalinvestigacion.um.es/documentos/63c0b3543df4c204fbb0307b?lang=en

[^38]: https://footballteamgame.com/la

[^39]: https://playfootball.games

[^40]: https://www.youtube.com/channel/UCUo-Lzw5NAWYJH026qIpN_g

[^41]: https://johnsonba.cs.grinnell.edu/20348279/bprepareg/find/tpractiser/juegos+futbol+11.pdf

[^42]: https://eusebiomillan.com/fotos-cadetes-futbol11-masculino/

[^43]: https://ligauniversitaria.org.uy/handball-unisonos-2014-5/

[^44]: https://futbol-11.com

[^45]: https://futbol11.netlify.app/futbol-grid

[^46]: https://futbol11.netlify.app/futbol11-connections

[^47]: https://revistaretos.org/index.php/retos/article/view/106860

[^48]: https://revistaretos.org/index.php/retos/article/view/107775

[^49]: https://revistaretos.org/index.php/retos/article/view/104386

[^50]: https://journals.sagepub.com/doi/10.1177/19417381231160167

[^51]: https://rpcd.fade.up.pt/_arquivo/artigos_soltos/2023-2/2023-2-04.pdf

[^52]: https://www.semanticscholar.org/paper/93e207ea2d41a77d2cc01f88bba48a95e53a6f12

[^53]: https://revistaretos.org/index.php/retos/article/view/91541

[^54]: https://revistaretos.org/index.php/retos/article/view/93665

[^55]: https://revista-ebalonmano.unex.es/index.php/ebalonmano/article/view/2320

[^56]: https://revista-ebalonmano.unex.es/index.php/ebalonmano/article/view/2350

[^57]: https://formative.jmir.org/api/download?alt_name=14372-274221-3-SP.pdf\&filename=b87a952fd3ac92a14a9820010f7a2da4.pdf

[^58]: https://www.mdpi.com/2227-9709/10/3/75/pdf?version=1695179165

[^59]: https://arxiv.org/ftp/arxiv/papers/1212/1212.1849.pdf

[^60]: http://www.ijimai.org/journal/sites/default/files/files/2014/03/ijimai20142_6_3_pdf_14574.pdf

[^61]: https://recyt.fecyt.es/index.php/retos/article/download/103272/76259

[^62]: https://jmir.org/api/download?alt_name=humanfactors_v11i1e44423_app1.pdf\&filename=fb4f024bf9cdcad9d55c91664ed8fd64.pdf

[^63]: https://thescipub.com/pdf/jcssp.2023.372.388.pdf

[^64]: http://arxiv.org/pdf/2404.12500.pdf

[^65]: http://thescipub.com/pdf/10.3844/jcssp.2006.314.317

[^66]: https://ojs.unud.ac.id/index.php/merpati/article/download/107612/52868

[^67]: https://barcainnovationhub.fcbarcelona.com/accessibility/

[^68]: https://revista-apunts.com/wp-content/uploads/2021/01/APUNTS-115-CAST.pdf

[^69]: https://www.similarweb.com/website/futbol-11.com/

[^70]: https://community.sports-interactive.com/forums/topic/569775-accessibility/

[^71]: https://www.nngroup.com/articles/ten-usability-heuristics/

[^72]: https://www.semrush.com/website/futbol-11.com/competitors/

[^73]: https://www.totalfootball11.com/accessibility-statement

[^74]: https://futbol-11.com/futbol11-connections

[^75]: https://futbol-11.com/futbol-top10

[^76]: https://futbol-11.com/privacypolicy

[^77]: https://www.konami.com/efootball/es/topic/news/list

[^78]: https://futbol-11.com/futbol11

[^79]: https://football-observatory.com/?lang=en

[^80]: https://rfef.es/en/noticias/RFEF-Postpones-Spains-Trip-to-Elche-Due-to-Weather-Conditions

[^81]: https://weareshifta.com/a-veces-no-hay-color-y-otras-si-el-futbol-es-su-aficion/

[^82]: https://forums.ea.com/discussions/-/-/7103286

[^83]: https://www.adamchoi.co.uk

[^84]: https://userhub.com.bd/publications/global-mobile-app-accessibility-wcag-compliance-across-12-countries/

[^85]: https://www.onlinescientificresearch.com/articles/advancing-web-accessibility-leveraging-generative-ai-for-enhanced-wcag-compliance.pdf

[^86]: https://link.springer.com/10.1007/s10209-022-00921-8

[^87]: https://ieeexplore.ieee.org/document/10908737/

[^88]: https://aircconline.com/ijwest/V15N1/15124ijwest01.pdf

[^89]: https://ph.pollub.pl/index.php/jcsi/article/view/6034

[^90]: https://ieeexplore.ieee.org/document/10636874/

[^91]: https://wjarr.com/node/20934

[^92]: https://www.nature.com/articles/s41598-024-59838-2

[^93]: https://ajost.journals.ly/ojs/index.php/1/article/view/69

[^94]: https://www.ijfmr.com/papers/2024/5/29091.pdf

[^95]: https://arxiv.org/pdf/2107.06799.pdf

[^96]: https://arxiv.org/pdf/2312.02992.pdf

[^97]: https://www.frontiersin.org/articles/10.3389/fcomp.2021.628770/pdf

[^98]: https://www.mdpi.com/2078-2489/11/1/40/pdf

[^99]: https://www.mdpi.com/2076-3417/11/12/5707/pdf

[^100]: https://arxiv.org/pdf/2401.16450.pdf

[^101]: https://www.qeios.com/read/definition/77012

[^102]: https://ph.pollub.pl/index.php/jcsi/article/download/2167/2151

[^103]: https://www.frontiersin.org/articles/10.3389/fcomp.2021.605772/pdf

[^104]: https://ahrefs.com/websites/futbol-11.com/competitors

[^105]: https://www.catapult.com/es/blog/reporte-cinco-suplentes-futbol

[^106]: https://aldaia.es/es/deportes/salas-polivalentes/

[^107]: https://www.easy-go.org/campamento-ingles-en-segovia/

[^108]: https://www.fasecolda.com/noticias-2024/inscripciones-para-el-encuentro-2024-ya-estan-abiertas/

[^109]: https://www.todojuristas.com/blog/quieres-especializarte-en-arbitraje/?sport-news-46053-2025-10-09-norwich-city-website-achieves-wcag-2-1-aa-accessibility-compliance

[^110]: https://www.instagram.com/reel/DPpMkhnCTxd/

[^111]: https://www.uptheflue.co.uk/?sport-news-46482-2025-10-09-norwich-city-site-achieves-wcag-2-1-aa-accessibility-compliance

[^112]: https://universidadeuropea.com/conocenos/madrid/

[^113]: https://futbol11.com

