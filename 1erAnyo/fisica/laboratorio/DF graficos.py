import pandas as pd
import matplotlib.pyplot as plt

# Datos proporcionados en la tabla A2
data = {
    'R': [99.8, 148.5, 324, 671, 982, 1487, 2140, 2630, 3210],
    'R_error': [0.1, 0.1, 1, 1, 1, 1, 10, 10, 10],
    '(R + ri)_inv': [9950, 6710, 3080, 1490, 1020, 670, 470, 380, 310],  # Valores en µΩ^{-1}
    '(R + ri)_inv_error': [10, 10, 10, 10, 10, 10, 10, 10, 10],  # Errores en µΩ^{-1}
    'I': [501, 339, 155, 75, 50, 33, 22, 17, 14],  # Corriente en mA
    'I_error': [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]  # Errores en mA
}

# Convertir la corriente a amperios
data['I'] = [i / 1000 for i in data['I']]
data['I_error'] = [i / 1000 for i in data['I_error']]

# Convertir valores de µΩ^{-1} a Ω^{-1} para la gráfica
data['(R + ri)_inv'] = [x * 1e-6 for x in data['(R + ri)_inv']]
data['(R + ri)_inv_error'] = [x * 1e-6 for x in data['(R + ri)_inv_error']]

# Crear un DataFrame
df = pd.DataFrame(data)

# Crear la gráfica
plt.figure(figsize=(10, 6))
plt.errorbar(df['(R + ri)_inv'], df['I'], xerr=df['(R + ri)_inv_error'], yerr=df['I_error'], fmt='o', ecolor='r', capsize=5, label='Datos experimentales')

# Ajustar etiquetas y título
plt.xlabel('$(R + r_i)^{-1}$ (Ω$^{-1}$)')
plt.ylabel('Intensidad $I$ (A)')
plt.title('Gráfica de I vs $(R + r_i)^{-1}$')
plt.legend()
plt.grid(True)

# Mostrar la gráfica
plt.show()
