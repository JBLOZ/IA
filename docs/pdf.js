<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Visor PDF con PDF.js</title>
  <!-- Incluye PDF.js vía CDN -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.8.162/pdf.min.js"></script>
</head>
<body>
  <!-- Elemento canvas donde se renderizará el PDF -->
  <canvas id="pdf-canvas"></canvas>

  <script>
    // Función para cargar y renderizar el PDF
    function renderPDF(url, canvasId, scale = 1.5) {
      // Configurar el worker de PDF.js
      pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.8.162/pdf.worker.min.js';

      // Referencia al canvas y su contexto 2D
      const canvas = document.getElementById(canvasId);
      const context = canvas.getContext('2d');

      // Cargar el documento PDF
      pdfjsLib.getDocument(url).promise.then(pdf => {
        // Obtener la primera página del PDF
        return pdf.getPage(1);
      }).then(page => {
        // Configurar la escala y obtener el viewport
        const viewport = page.getViewport({ scale: scale });

        // Ajustar dimensiones del canvas
        canvas.width = viewport.width;
        canvas.height = viewport.height;

        // Configurar el contexto de renderizado
        const renderContext = {
          canvasContext: context,
          viewport: viewport
        };

        // Renderizar la página en el canvas
        return page.render(renderContext);
      }).catch(err => {
        console.error('Error al cargar el PDF: ', err);
      });
    }

    // Ruta del PDF que deseas mostrar (asegúrate de que esté accesible)
    const url = 'ruta_al_pdf.pdf';

    // Llamar a la función para renderizar el PDF
    renderPDF(url, 'pdf-canvas');
  </script>
</body>
</html>
