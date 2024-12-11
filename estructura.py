import os

def listar_estructura(ruta, nivel=0, archivo=None):
    # Carpetas a excluir
    carpetas_excluidas = {".vscode", ".git", ".vs"}
    prefijo = "  " * nivel
    for elemento in os.listdir(ruta):
        ruta_completa = os.path.join(ruta, elemento)
        # Excluir carpetas especificadas
        if os.path.basename(ruta_completa) in carpetas_excluidas:
            continue
        if os.path.isdir(ruta_completa):
            linea = f"{prefijo}[Carpeta] {elemento}\n"
            archivo.write(linea)
            listar_estructura(ruta_completa, nivel + 1, archivo)


ruta = r"C:\Users\jordi\Documents\IA\IA"
with open("estructura.txt", "w", encoding="utf-8") as archivo:
    archivo.write(f"Estructura de la carpeta: {ruta}\n")
    listar_estructura(ruta, archivo=archivo)
