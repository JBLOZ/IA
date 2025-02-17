## Requisitos
- Python 3.8 o superior.
- Librería necesaria: numpy, pyvista

Para instalar las librerías necesarias, ejecutar:

pip install numpy pyvista

## Estructura de Archivos

Asegúrate de que la carpeta `Datos` este en el mismo directorio que los archivos .py
La carpeta `Datos` debe contener los todos archivos `.pcd` de la lista de ficheros siguiente ["ciencias000", "ciencias001","scan000", "museo000", "poli000", "poli001"] 

## Ejecuciones

### 1. Análisis de Datos

python main.py

### 2. Visualización 3D

python visualizador.py

## Parametros

Cada archivo main.py y visualizador.py contiene al principio una serie de parametros para la generacion de la rejilla o/y para la generacion del Oc-Tree, estos parametros son modificables


## Documentación

-- En memoria.pdf se encuentra la documentación pertinente a los tipos de Mapas métricos (características, métricas, etc)

-- En el código se encuentra la documentación pertinente a la lógica del mismo código 