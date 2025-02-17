# Código para practica3.ipynb

import torch
import time
from torchvision import models, transforms
from torchvision.models import ResNet18_Weights
from PIL import Image
import os
import logging
import warnings



class PracticaCPUvsGPU:
    def __init__(self, debug: bool = True):
        """
        Inicializa la práctica.
        """
        self.debug = debug
        if not self.debug:
            warnings.simplefilter("ignore", UserWarning)
        
        # Configurar logging según la variable debug
        if self.debug:
            logging.basicConfig(level=logging.DEBUG,
                                format='%(asctime)s - %(levelname)s - %(message)s')
        else:
            logging.basicConfig(level=logging.WARNING,
                                format='%(asctime)s - %(levelname)s - %(message)s')
        
        logging.debug("GPU disponible (inicial): %s", torch.cuda.is_available())
        logging.debug("Número de GPUs (inicial): %s", torch.cuda.device_count())
    
        # Definir las resoluciones a comparar
        self.resoluciones = [(224, 224), (512, 512), (1024, 1024)]
        
        # Cargar el modelo ResNet18 para CPU y establecerlo en modo evaluación

        self.model_cpu = models.resnet18(pretrained=True)
        self.model_cpu.eval()
        
        # Verificar GPU y cargar modelo en GPU si aparece disponible
        self.gpu_disponible = torch.cuda.is_available()
        if self.gpu_disponible:
            self.model_gpu = models.resnet18(pretrained=True).to('cuda')
            self.model_gpu.eval()
        else:
            self.model_gpu = None
        
        # Directorio donde se encuentran las imágenes
        self.imagenes_dir = "Fotos ejemplo"
        # Lista de rutas de imagen (Foto facial 1.jpg a Foto facial 5.jpg)
        self.image_paths = [os.path.join(self.imagenes_dir, f"Foto facial {i}.jpg") for i in range(1, 6)]
    
    def run_measurements(self):
        """
        Recorre las imágenes y mide los tiempos de ejecución sobre CPU y GPU (si está disponible),
        registrando los resultados mediante logging.
        """
        for path in self.image_paths:
            try:
                image = Image.open(path)
            except Exception as e:
                logging.error("Error al abrir la imagen %s: %s", path, e)
                continue

            for res in self.resoluciones:
                # Definir la transformación para la resolución actual
                transform_res = transforms.Compose([
                    transforms.Resize(res),
                    transforms.ToTensor()
                ])
    
                # Convertir la imagen a tensor y añadir dimensión batch
                input_tensor = transform_res(image).unsqueeze(0)
    
                # Medición en CPU
                start_cpu = time.time()
                with torch.no_grad():
                    _ = self.model_cpu(input_tensor)
                tiempo_cpu = time.time() - start_cpu
    
                resultado = f"Imagen: {path} | Tamaño: {res[0]}x{res[1]} | Tiempo en CPU: {tiempo_cpu:.4f} segundos"
    
                # Medición en GPU si está disponible
                if self.gpu_disponible:
                    input_tensor_gpu = input_tensor.to('cuda')
                    start_gpu = time.time()
                    with torch.no_grad():
                        _ = self.model_gpu(input_tensor_gpu)
                    torch.cuda.synchronize()  # Asegurarse de que la GPU finalice la operación
                    tiempo_gpu = time.time() - start_gpu
                    resultado += f" | Tiempo en GPU: {tiempo_gpu:.4f} segundos"
                else:
                    resultado += " | GPU no disponible."
    
                logging.info(resultado)
    
    def generar_tabla_markdown(self) -> str:
        """
        Genera una tabla en formato Markdown con los tiempos de ejecución en CPU y GPU.
        
        Returns:
            Una cadena con la tabla Markdown.
        """
        table_lines = []
        # Cabecera de la tabla Markdown
        table_lines.append("| Imagen | Tamaño | Tiempo CPU (s) | Tiempo GPU (s) |")
        table_lines.append("|--------|--------|----------------|----------------|")
    
        for path in self.image_paths:
            try:
                image = Image.open(path)
            except Exception as e:
                table_lines.append(f"| {path} | Error al abrir imagen: {e} | - | - |")
                continue
    
            for res in self.resoluciones:
                transform_res = transforms.Compose([
                    transforms.Resize(res),
                    transforms.ToTensor()
                ])
                input_tensor = transform_res(image).unsqueeze(0)
                start_cpu = time.time()
                with torch.no_grad():
                    _ = self.model_cpu(input_tensor)
                tiempo_cpu = time.time() - start_cpu
    
                if self.gpu_disponible:
                    input_tensor_gpu = input_tensor.to('cuda')
                    start_gpu = time.time()
                    with torch.no_grad():
                        _ = self.model_gpu(input_tensor_gpu)
                    torch.cuda.synchronize()
                    tiempo_gpu = time.time() - start_gpu
                    tiempo_gpu_str = f"{tiempo_gpu:.4f}"
                else:
                    tiempo_gpu_str = "N/A"
    
                table_lines.append(f"| {os.path.basename(path)} | {res[0]}x{res[1]} | {tiempo_cpu:.4f} | {tiempo_gpu_str} |")
    
        return "\n".join(table_lines)

    def run_all(self):
        """
        Ejecuta el análisis (mediciones) y genera la tabla Markdown.
        """
        self.run_measurements()
        md_table = self.generar_tabla_markdown()
        
        return md_table

if __name__ == "__main__":

    practica = PracticaCPUvsGPU()
    tabla = practica.run_all()
    print(tabla)

