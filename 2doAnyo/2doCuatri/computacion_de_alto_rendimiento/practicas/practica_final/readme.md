Asignatura: Computación de Alto Rendimiento (CAR) 
Profesor: Ricardo Moreno Rodríguez 
 
Práctica  0:  Introducción  Guiada  a  la 
Detección de Personas con HPC e IA 
1. Introducción 
La Computación de Alto Rendimiento (HPC) y la Inteligencia Artificial (IA) forman 
una combinación poderosa que permite abordar problemas complejos de forma eficiente. 
En  particular,  la  detección  de  personas  en  imágenes  es  un  ejemplo  representativo: 
requiere modelos de IA avanzados y puede beneficiarse enormemente de los recursos de 
HPC  (por  ejemplo,  GPUs  o  clusters)  para  procesar  gran  cantidad  de  datos  en  poco 
tiempo.  Esta  práctica  introductoria  tiene  como  objetivo  principal  familiarizar  al 
estudiante con las herramientas y conceptos básicos para detectar personas en imágenes 
utilizando  técnicas  modernas  de  visión  por  computador,  todo  ello  sirviéndose  de  la 
infraestructura de computación de alto rendimiento disponible. 
 
Figura  1.  Ejemplo  de  un  cruce  urbano 
concurrido captado en imagen. La detección 
de peatones en entornos reales, como el que 
se ilustra, es un desafío donde las  técnicas 
actuales  de  IA  (p.  ej.  el  modelo  YOLO) 
permiten identificar automáticamente a cada 
persona en la escena. 
 
En esta práctica 0 (de carácter obligatorio) realizarás una introducción guiada paso a 
paso. A lo largo de la misma aprenderás a descargar imágenes de cámaras urbanas o de 
fuentes abiertas, a procesar esas imágenes con Python, y a aplicar un modelo pre-entrenado 
de detección de personas (You Only Look Once – YOLO, en su versión más reciente YOLOv8). 
La práctica está diseñada para ser asequible y comprensible, sirviendo de preparación 
técnica y conceptual para la Práctica 1. Siguiendo las indicaciones, podrás completar las 
tareas con autonomía creciente, sentando las bases para afrontar la práctica voluntaria 
siguiente con más confianza. 
   
 
Asignatura: Computación de Alto Rendimiento (CAR) 
Profesor: Ricardo Moreno Rodríguez 
 
Nota sobre el uso responsable de la IA: Durante  el  desarrollo de  esta  práctica  es 
importante  recordar  que  el  análisis  de  imágenes  que  contienen  personas  conlleva 
responsabilidades éticas. Asegúrate de respetar la privacidad de las personas que puedan 
aparecer en las fotografías y de cumplir con la normativa de protección de datos vigente. 
Los sistemas de IA deben usarse de forma transparente y segura; en un contexto urbano 
real, la detección automatizada de personas no debe derivar en un uso indebido (por 
ejemplo, vigilancia no autorizada). Esta práctica educativa se realiza con fines académicos y 
de investigación, fomentando siempre un uso responsable de la IA. 
2. Objetivos 
Los objetivos de esta Práctica 0 son: 
  Familiarizarse  con  la  adquisición  de  datos  visuales  urbanos:  aprender  a 
acceder a imágenes provenientes de cámaras de tráfico u otras fuentes públicas 
que muestran entornos con peatones. 
  Manipular  y  preprocesar  imágenes  con  Python:  utilizar  librerías  como 
OpenCV  o  PIL  para  cargar,  visualizar  y  realizar  operaciones  básicas  sobre 
imágenes, preparando los datos para su análisis. 
  Aplicar  un  modelo  de  detección  de  personas  pre-entrenado:  entender  el 
funcionamiento  general  de  un  detector  como  YOLOv8,  usarlo  para  identificar 
personas  en  una  imagen  dada  (sin  requerir  entrenar  el  modelo  desde  cero)  y 
obtener resultados interpretables (p. ej. imágenes con recuadros alrededor de cada 
persona detectada). 
  Introducir conceptos de HPC en visión por computador: reconocer cómo los 
recursos  de  computación  de  alto  rendimiento  (por  ejemplo,  la  aceleración  por 
GPU)  pueden  acelerar  el  procesamiento  de  imágenes  y la  detección  en tiempo 
real, sentando bases para experimentos más complejos. 
  Preparar  al  estudiante  para  la  Práctica  1:  tras  completar  esta  práctica 
introductoria,  el  alumno  contará  con  la  base  técnica  necesaria  (manejo  de 
imágenes,  uso  de  modelos  IA  pre-entrenados,  consideraciones  de  rendimiento) 
para afrontar con mayor autonomía la práctica voluntaria 1, que profundizará en 
un caso más complejo de HPC e IA. 
3. Tareas a Realizar 
A continuación se detallan las tareas guiadas que debes completar para llevar a cabo la 
práctica. Sigue el orden propuesto y las indicaciones en cada paso. Aunque se ofrecen 
ayudas y ejemplos, procura interpretar los resultados y entender cada acción, ya que esto 
te preparará para trabajos posteriores más abiertos. 
 
Asignatura: Computación de Alto Rendimiento (CAR) 
Profesor: Ricardo Moreno Rodríguez 
1. Preparación del entorno de trabajo: Asegúrate de tener un entorno Python funcional 
con las librerías necesarias. Es recomendable usar Jupyter Notebook o un entorno similar 
donde puedas ejecutar código y visualizar resultados cómodamente. Deberás contar con: 
  Python 3 instalado (idealmente en un entorno virtual o conda para la asignatura). 
  Librerías  básicas  de  procesamiento  de  imágenes  como  OpenCV  (cv2)  o 
PIL/Pillow para cargar y manipular imágenes. OpenCV será especialmente útil 
para dibujar detecciones sobre las imágenes. 
  La  biblioteca  o  script  para  YOLOv8  pre-entrenado.  Para  simplificar,  puedes 
usar la implementación de Ultralytics: pip install ultralytics. Esta librería 
proporciona una interfaz sencilla para cargar modelos YOLO pre-entrenados (por 
ejemplo,  yolov8n.pt  o  yolov8s.pt,  que  son  versiones  pequeñas  del  modelo 
entrenadas en el conjunto COCO). Nota: Si no puedes instalar nuevas librerías en 
local, considera usar Google Colab o los recursos HPC de la universidad, donde 
podrás acceder a GPUs y ya hay entornos preparados con estas herramientas. 
Asegúrate de tener acceso a Internet si vas a descargar librerías o pesos pre-entrenados la 
primera vez. Consulta con el profesor o los técnicos de laboratorio si necesitas ayuda para 
configurar el entorno HPC con los paquetes necesarios. 
2.  Obtención  de  imágenes  desde  cámaras  urbanas:  El  primer  paso  práctico  es 
conseguir  una  o  varias  imágenes  donde  haya  personas  en  un  entorno  urbano  (calles, 
plazas, transporte, etc.). Se sugieren dos opciones principales: 
  a. Imágenes de cámaras de tráfico en tiempo real: Muchas ciudades ofrecen 
acceso público a imágenes actualizadas de sus cámaras de tráfico. Por ejemplo, el 
Ayuntamiento  de  Madrid  y  la DGT disponen de portales  donde se pueden ver 
fotografías actualizadas  cada  pocos  minutos  de  distintas  ubicaciones.  Busca en 
Internet si tu ciudad local o alguna ciudad de interés tiene un portal de “cámaras 
de tráfico” o “tráfico en directo”. Suelen ser imágenes JPEG accesibles vía URL. 
Consejo: Si encuentras la URL directa de la imagen (por ejemplo, terminada en 
.jpg), puedes descargarla programáticamente con Python (usando requests.get 
o urllib) para incorporarla a tu entorno de trabajo. En esta práctica no necesitas 
automatizar una descarga continua, basta con obtener una instantánea estática 
para analizar. 
  b. Imágenes abiertas o de ejemplo: Si no logras obtener una imagen de cámara 
de tráfico real, puedes usar imágenes de repositorios abiertos. Por ejemplo, sitios 
como  Pixabay,  Unsplash  u  OpenImageDataset  ofrecen  fotografías  urbanas  con 
transeúntes  bajo  licencias  abiertas.  También  puedes  tomar  una  fotografía  tú 
mismo en la vía pública (asegurándote de respetar la privacidad y de que sea un 
lugar público).  Lo  importante  es  que  en  la  imagen  haya  personas claramente 
visibles (de cuerpo completo o al menos de la cintura para arriba) para que el 
detector las pueda encontrar. Idealmente, elige imágenes de día y relativamente 
nítidas, para no complicar en exceso la detección en este primer intento. 
