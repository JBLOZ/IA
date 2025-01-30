#!/usr/bin/env bash

# Verificar si awk y diff están instalados
if ! command -v awk &> /dev/null || ! command -v diff &> /dev/null
then
    echo "Error: awk o diff no están instalados. Por favor, instala awk y diff para continuar."
    exit 1
fi

# Función para medir el tiempo en segundos con precisión de microsegundos
function measure_time() {
    local start end
    start=$(date +%s.%N)
    "$@"
    local status=$?
    end=$(date +%s.%N)
    if [ $status -ne 0 ]; then
        echo "Error: El comando '$@' falló con estado $status" >&2
        return $status
    fi
    # Calcular la diferencia de tiempo usando awk
    echo "$(awk -v start="$start" -v end="$end" 'BEGIN { printf "%.6f", end - start }')"
}

# Capturar el tiempo inicial para el tiempo total
GLOBAL_START=$(date +%s.%N)

# Inicializar variables para tiempo total
TOTAL_OK=0
TOTAL_FAIL=0

# Iterar sobre los tests del 01 al 09
for i in {01..09}; do
    INPUT="${i}.entrada.txt"
    EXPECTED="${i}.salida.txt"
    OUTPUT="out.${i}.txt"

    # Verificar si los archivos de entrada y salida esperada existen
    if [[ ! -f "$INPUT" ]]; then
        echo "Error: No se encuentra el fichero de entrada $INPUT"
        echo "-------------------------------------"
        continue
    fi
    if [[ ! -f "$EXPECTED" ]]; then
        echo "Error: No se encuentra el fichero de salida esperada $EXPECTED"
        echo "-------------------------------------"
        continue
    fi

    # Medir el tiempo de ejecución del programa sin agregarlo a la salida
    echo "Ejecutando Test $i..."
    TIME=$(measure_time ./main < "$INPUT" > "$OUTPUT")
    echo "DEBUG: TIME capturado para Test $i: $TIME"
    if [ $? -ne 0 ]; then
        echo "Test $i: Error al ejecutar 'main'"
        echo "-------------------------------------"
        continue
    fi
    echo "Tiempo medido para Test $i: $TIME seg"

    # Comparar los archivos usando diff
    diff_output=$(diff -u "$EXPECTED" "$OUTPUT")
    if [[ -z "$diff_output" ]]; then
        # No hay diferencias
        OK=$(wc -l < "$EXPECTED")
        FAIL=0
        echo "Test $i:"
        echo "numero de oks: $OK"
        echo "fallos: $FAIL"
        echo "tiempo: $TIME seg"
    else
        # Hay diferencias
        FAIL=$(echo "$diff_output" | grep -c '^[-+]')
        OK=$(wc -l < "$EXPECTED")
        echo "Test $i:"
        echo "numero de oks: $OK"
        echo "fallos: $FAIL"
        echo "tiempo: $TIME seg"
        echo "Diferencias encontradas:"
        echo "$diff_output" | grep '^+' | grep -v '^+++' | head -n 10  # Mostrar solo las primeras 10 diferencias de inserción
        if [[ $(echo "$diff_output" | wc -l) -gt 10 ]]; then
            echo "..."
        fi
    fi
    echo "-------------------------------------"

    # Sumar al total
    TOTAL_OK=$((TOTAL_OK + OK))
    TOTAL_FAIL=$((TOTAL_FAIL + FAIL))
done

# Capturar el tiempo final para el tiempo total
GLOBAL_END=$(date +%s.%N)

# Calcular el tiempo total usando awk
TOTAL_TIME=$(awk -v start="$GLOBAL_START" -v end="$GLOBAL_END" 'BEGIN { printf "%.6f", end - start }')

# Mostrar el tiempo total y los totales
echo "Numero total de oks: $TOTAL_OK"
echo "Numero total de fallos: $TOTAL_FAIL"
echo "Tiempo total de todos los tests: $TOTAL_TIME seg"
