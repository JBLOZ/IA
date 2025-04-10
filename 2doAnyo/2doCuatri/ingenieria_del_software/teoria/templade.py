from abc import ABC, abstractmethod

# Clase base para generar informes
class GeneradorInforme(ABC):
    def generar(self):
        """Método plantilla que define el esqueleto del algoritmo."""
        datos = self.obtener_datos()
        informe = self.formatear_informe(datos)
        self.exportar_informe(informe)

    @abstractmethod
    def obtener_datos(self):
        """Obtiene los datos necesarios para el informe."""
        pass

    @abstractmethod
    def formatear_informe(self, datos):
        """Formatea los datos en el informe."""
        pass

    @abstractmethod
    def exportar_informe(self, informe):
        """Exporta el informe en el formato deseado."""
        pass

# Clases específicas para cada tipo de informe
class InformePDF(GeneradorInforme):
    def obtener_datos(self):
        print("Obteniendo datos para el informe PDF...")
        return "datos_pdf"

    def formatear_informe(self, datos):
        print("Formateando informe en PDF...")
        return f"<PDF>{datos}</PDF>"

    def exportar_informe(self, informe):
        print("Exportando informe PDF:", informe)

class InformeHTML(GeneradorInforme):
    def obtener_datos(self):
        print("Obteniendo datos para el informe HTML...")
        return "datos_html"

    def formatear_informe(self, datos):
        print("Formateando informe en HTML...")
        return f"<html><body>{datos}</body></html>"

    def exportar_informe(self, informe):
        print("Exportando informe HTML:", informe)

# Ejemplo de uso:
if __name__ == "__main__":
    print("Generando Informe PDF:")
    informe_pdf = InformePDF()
    informe_pdf.generar()

    print("\nGenerando Informe HTML:")
    informe_html = InformeHTML()
    informe_html.generar()
