// Configurar el worker de PDF.js
pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.8.162/pdf.worker.min.js';

// Función para cargar y renderizar el PDF
function renderPDF(url, canvasId, scale = 1.5) {
  // Referencia al canvas y su contexto 2D
  const canvas = document.getElementById(canvasId);
  const context = canvas.getContext('2d');

  // Cargar el documento PDF
  pdfjsLib.getDocument(url).promise.then(pdf => {
    console.log(`PDF cargado con ${pdf.numPages} páginas`);
    
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

// Inicializar el visor cuando el documento esté listo
document.addEventListener('DOMContentLoaded', function() {
  const pdfUrl = 'certificaciones/CV_JBLOZ_EN.pdf';
  renderPDF(pdfUrl, 'pdf-canvas');
});