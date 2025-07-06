────────────────────────────────────────
GUÍA DE EJERCICIOS – SEÑALES Y SISTEMAS EN TIEMPO DISCRETO  
(Tema 6 – Clase de teoría y problemas nº 6)  
────────────────────────────────────────

La colección de problemas puede agruparse en 7 grandes familias.  
Cada familia incluye varias “sub-variantes” y un protocolo de resolución
que sirve incluso si nunca has visto el tema.

============================================================
A. REPRESENTACIÓN DE SECUENCIAS
============================================================
1. “TABLA”  
   • Enunciado típico : se da una lista de valores X[n] para unos cuantos n.  
   • Objetivo : dibujar los palitos, o bien re-escribir la secuencia usando impulsos δ.  
   • Pasos:  
     1. Para cada n donde la secuencia vale algo ≠ 0 coloca un palito.  
     2. Si quieres forma analítica: X[n] = Σ X[n₀] δ[n − n₀].

2. “GRÁFICA”  
   • Se muestra la gráfica y debes leer amplitudes y posiciones.  
   • Convierte la gráfica en tabla y procede como en 1.

3. “EXPRESIÓN ANALÍTICA”  
   • Ej.:  X[n]=cos(0,1π n+π/4) ; 0≤n≤100.  
   • Tareas:  
     – Determinar período, amplitud, fase, número total de muestras.  
     – Generar el vector en Matlab/Python o dibujarla a mano.

4. “COMBINACIÓN DE SECUENCIAS BÁSICAS”  
   • Se usan δ[n], u[n], Π[n/L], senos, exponenciales, etc.  
   • Debes identificar cada bloque y dibujar/puntualizar.

============================================================
B. CÁLCULO DE PARÁMETROS DE UNA SECUENCIA
============================================================
Sub-variantes y algoritmo:

1. Duración (dur{X[n]})  
   dur = n_fin − n_ini +1.

2. Valores extremo y pico-a-pico  
   X_max = max{X[n]}, X_min = min{X[n]}, X_pp = X_max − X_min.

3. Valor medio <X[n]>  
   a) No periódica:  lim_{N→∞} (1/(2N+1)) Σ_{n=−N}^{N} X[n].  
   b) Periódica: promedio sobre un período (1/N₀) Σ_{n=0}^{N₀−1} X[n].

4. Potencia (P_x)  
   Solo para señales de potencia finita:  (1/N₀) Σ_{n=0}^{N₀−1} |X[n]|².

5. Energía (E_x)  
   E_x = Σ_{n=−∞}^{∞} |X[n]|² (se usa cuando P_x=0).

Cómo resolver:  
• Primero identifica si la señal es finita, periódica o aperiodica.  
• Aplica la fórmula correcta.  
• Para series finitas la suma se detiene en los n mostrados.

============================================================
C. CLASIFICACIÓN ENERGÍA / POTENCIA
============================================================
Pregunta típica: “¿Es esta secuencia de energía, de potencia o ninguna?”  
Regla mnemónica:

              ┌──────────────┐
              │ |X[n]| tiende │
              │ a 0 si n→∞ ? │
              └──────┬───────┘
                     │Sí
      ┌──────────────┴───────────────┐
      │ Suma |X[n]|² finita?         │
      ├──────────────────────────────┤
      │  Sí  →  Energía (P=0)        │
      │  No  →  Ninguna              │
      └──────────────────────────────┘
Si la señal es periódica y no decae → Potencia finita, Energía infinita.

============================================================
D. OPERACIONES BÁSICAS CON SECUENCIAS
============================================================
1. Desplazamiento (Shift)  
   • X[n − n₀]   →  retrasa n₀ muestras (se dibuja a la derecha).  
   • X[n + n₀]   →  adelanta n₀ muestras (izquierda).  
   • Procedimiento: sustituye “n” por “n−n₀” en la expresión o re-etiqueta el eje.

2. Inversión (Reflexión)  
   • X[−n].  Dibuja la señal espejada respecto n=0.

3. Inversión + Desplazamiento  
   • X[−n + n₀] (primero invierte → luego retrasa).  
   • X[−n − n₀] (invierte → adelanta).  
   • Regla rápida: haz la tabla “n’ = −n ± n₀”, resuelve n, recoloca impulsos.

4. Escalado temporal  
   • X[M n]  (M>1) → compresión/diezmado (pierdes muestras).  
   • X[n/ M] (M>1) → expansión/interpolación.  
   • Pasos: sustituye n por M n o n/M y ajusta índices enteros.

5. Multiplicación por otra secuencia (ventaneo)  
   • Típico: X[n] · u[n−n₀] o X[n] · δ[n−n₁].  
   • Método: escribe ambas en forma δ; conserva solo los impulsos que coinciden en n.

============================================================
E. EJERCICIOS COMPUESTOS
============================================================
Ej.: Calcular X[−n+2] de una señal dada.  
1. Toma la forma δ del original.  
2. Aplica inversión (cambia el signo en los índices).  
3. Aplica desplazamiento (suma +2).  
4. Redibuja o re-lista valores.

Otro ejemplo: X[n+1] · δ[n−3]  
1. Shift izquierdo (n+1).  
2. δ[n−3] actúa como “filtro extractor”: solo el valor donde n=3 sobrevive.  
3. Resultado final suele ser un único impulso con la amplitud correspondiente.

============================================================
F. CONVOLUCIÓN DISCRETA
============================================================
F-1. Concepto y propiedades  
   • Definición: Z[n]=Σ_{k=−∞}^{∞} X[k] Y[n−k].  
   • Propiedades que ahorran trabajo: conmutativa, asociativa, distributiva, identidad δ[n].

F-2. Duración y límites rápidos  
   • dur{Z} = dur{X} + dur{Y} − 1.  
   • n_ini(Z) = n_ini(X) + n_ini(Y)  
     n_fin(Z) = n_fin(X) + n_fin(Y)

F-3. Métodos de cálculo (sub-variantes)  

a) Superposición de impulsos (método analítico)  
   1. Escribe X y Y solo con δ.  
   2. Usa la propiedad: δ[n−a] * δ[n−b] = δ[n−(a+b)].  
   3. Distribuye y suma.  
   Ventaja: algebraico, rápido con pocas δ.  

b) Tabla de solape (método “matricial”)  
   1. Coloca X[k] en una fila, indexado.  
   2. Espeja Y[−k]; desplázala columna a columna (n).  
   3. Para cada desplazamiento suma productos.  
   4. Lee Z[n] como la lista de sumas.  
   Útil si hay pocas muestras (≤20).

c) Resolución gráfica  
   1. Dibuja X[k].  
   2. Dibuja Y[−k] reflejada.  
   3. Desplázala, calcula el área/peso de solape a mano.  
   4. Repite para todos los n en rango.  
   Educativo pero engorroso; hoy se usa para ilustrar, no para cuentas largas.

============================================================
G. VERIFICACIÓN DE PROPIEDADES DE CONVOLUCIÓN
============================================================
Ejercicios típicos:  
• Comprueba que X*δ = X.  
• Demuestra con números que X*Y = Y*X.  
• Muestra que dur{X*Y} concuerda con la fórmula anterior.

Procedimiento:  
1. Elige secuencias cortas (2-3 impulsos).  
2. Convoluciona manualmente por cualquiera de los tres métodos.  
3. Comprueba igualdad de resultados.

────────────────────────────────────────
RESUMEN VISUAL DE FLUJO PARA CUALQUIER PROBLEMA
────────────────────────────────────────
1. ¿Primero NECESITO representar la señal?  
   → Tablas, δ-expansión o gráfica.

2. ¿Debo CALCULAR parámetros (duración, pico, media…)?  
   → Aplico fórmulas directas.

3. ¿Hay OPERACIONES como shift/inversión/escala?  
   → Sustituye índices con cuidado: observa el signo y la magnitud.  
   → Redibuja antes de continuar.

4. ¿Se pide MULTIPLICAR o VENTANEAR?  
   → Convierte a δ; conserva coincidencias.

5. ¿Se pide CONVOLUCIÓN?  
   → Decide método (δ-expansión, tabla o gráfica).  
   → Calcula rango primero, luego valores.

6. ¿El ejercicio encadena varias de las anteriores?  
   → Resuelve en el mismo orden en que aparecerían si escribieras la expresión paso a paso
     (paréntesis → inversión → desplazamientos → multiplicaciones → suma/convolución).

────────────────────────────────────────
CONSEJO FINAL
────────────────────────────────────────
• Ten siempre una “pizarra auxiliar” con la recta n y marca impulsos; los dibujos evitan errores
  de signo y desplazamiento.  
• Guarda una plantilla de δ[n−k] ↔ “impulso en n=k” pegada en tu libreta.  
• Al comprobar resultados, cuenta el número de muestras no nulas: si excede la
  “duración teórica” algo falló.

¡Con esta guía ya puedes atacar cualquier problema del Tema 6 con método y seguridad!
