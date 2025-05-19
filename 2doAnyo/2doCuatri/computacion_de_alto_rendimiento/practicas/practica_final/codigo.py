"""
detectar_personas.py

Detección de personas en imágenes estáticas usando YOLOv8
"""

import os
import cv2
import time
import argparse
from ultralytics import YOLO

def cargar_imagen(path):
    """
    Carga una imagen desde disco.
    :param path: Ruta al fichero de imagen.
    :return: Imagen en formato BGR (numpy array).
    """
    img = cv2.imread(path)
    if img is None:
        raise FileNotFoundError(f"No se pudo leer la imagen: {path}")
    return img

def detectar_personas(model, img, conf=0.25):
    """
    Ejecuta la inferencia del modelo YOLOv8 sobre una imagen
    y filtra las cajas de clase 'persona' (cls == 0).
    :param model: Objeto YOLO cargado.
    :param img: Imagen sobre la que inferir.
    :param conf: Umbral de confianza.
    :return: Lista de cajas (objetos result.boxes) de personas.
    """
    results = model.predict(source=img, conf=conf)
    boxes = results[0].boxes
    person_boxes = [b for b in boxes if int(b.cls) == 0]
    return person_boxes

def dibujar_cajas(img, boxes):
    """
    Dibuja rectángulos verdes alrededor de las detecciones.
    :param img: Imagen BGR en la que dibujar.
    :param boxes: Lista de cajas detectadas.
    :return: Imagen anotada.
    """
    for box in boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
    return img

def main():
    parser = argparse.ArgumentParser(description='Detección de personas con YOLOv8')
    parser.add_argument('--input',  required=True, help='Ruta de la imagen de entrada')
    parser.add_argument('--output', required=True, help='Carpeta donde guardar resultados')
    parser.add_argument('--conf',   default=0.25, type=float, help='Umbral de confianza (0–1)')
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)

    print(f"[INFO] Cargando imagen: {args.input}")
    img = cargar_imagen(args.input)

    print("[INFO] Cargando modelo YOLOv8 (yolov8n.pt)...")
    model = YOLO('yolov8n.pt')

    print(f"[INFO] Ejecutando detección (conf={args.conf})...")
    t0 = time.time()
    boxes = detectar_personas(model, img, args.conf)
    t1 = time.time()
    elapsed = t1 - t0

    print(f"[RESULT] {len(boxes)} personas detectadas en {elapsed:.3f} segundos")

    img_annot = dibujar_cajas(img.copy(), boxes)
    nombre = os.path.splitext(os.path.basename(args.input))[0]
    salida = os.path.join(args.output, f"resultado_{nombre}.jpg")
    cv2.imwrite(salida, img_annot)
    print(f"[INFO] Imagen anotada guardada en: {salida}")

if __name__ == '__main__':
    main()
