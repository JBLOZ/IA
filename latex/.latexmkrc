# Configuración de Latexmk para usar XeLaTeX
$pdf_mode = 5;  # Usar XeLaTeX para generar PDF
$postscript_mode = 0;
$dvi_mode = 0;

# Configurar XeLaTeX
$xelatex = 'xelatex -synctex=1 -interaction=nonstopmode -file-line-error %O %S';

# Configurar biber para bibliografía
$biber = 'biber %O %S';
$bibtex_use = 2;  # Usar biber en lugar de bibtex

# Archivos a limpiar
@generated_exts = qw(aux bbl bcf blg fdb_latexmk fls log out run.xml synctex.gz toc);

# Previsualización continua (opcional)
# $preview_continuous_mode = 1;
# $pdf_previewer = 'start';
