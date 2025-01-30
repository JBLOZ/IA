#! /bin/bash

OUT="entrega.cc"

if [ ! -f "Fecha.h" ]; then
   echo "ERROR: No se encuentra el fichero Fecha.h"
   exit 1
fi

if [ ! -f "Fecha.cc" ]; then
   echo "ERROR: No se encuentra el fichero Fecha.cc"
   exit 1
fi

if [ ! -f "main-incrementaDias.cc" ]; then
   echo "ERROR: No se encuentra el fichero main-incrementaDias.cc. Asegúrate de haber descomprimido correctamente el fichero descargado de Moodle"
   exit 1
fi

cat Fecha.h > $OUT
cat main-incrementaDias.cc >> $OUT
cat Fecha.cc  | grep -v '#include[ ]*"[ ]*Fecha\.h[ ]*"' >> $OUT

echo "Ahora puedes entregar el fichero entrega.cc en jutge.org"
