import pandas as pd

# --- Datos del Problema ---

# 1. Probabilidades a priori (Priors)
priors = {
    'manzana': 0.70,
    'pera': 0.30
}

# 2. Probabilidades condicionales (Likelihoods) - p(color | fruta)
likelihoods = {
    'manzana': {'Azul': 0.05, 'Verde': 0.25, 'Amarillo': 0.15, 'Naranja': 0.10, 'Rojo': 0.45},
    'pera':    {'Azul': 0.05, 'Verde': 0.60, 'Amarillo': 0.25, 'Naranja': 0.05, 'Rojo': 0.05}
}

colors = ['Azul', 'Verde', 'Amarillo', 'Naranja', 'Rojo']

# --- Cálculos ---

# Q1: Probabilidad conjunta de manzana amarilla y pera amarilla
p_amarillo_manzana = likelihoods['manzana']['Amarillo'] * priors['manzana']
p_amarillo_pera = likelihoods['pera']['Amarillo'] * priors['pera']

print("--- Respuesta a Q1 ---")
print(f"La probabilidad de obtener una manzana amarilla es: {p_amarillo_manzana:.3f} ({p_amarillo_manzana:.1%})")
print(f"La probabilidad de obtener una pera amarilla es: {p_amarillo_pera:.3f} ({p_amarillo_pera:.1%})")
print("\n" + "="*30 + "\n")


# Q2: Todas las probabilidades posteriores P(fruta | color)
posterior_probabilities = []

for color in colors:
    # Calcular la evidencia P(color)
    p_color_manzana = likelihoods['manzana'][color] * priors['manzana']
    p_color_pera = likelihoods['pera'][color] * priors['pera']
    p_color_evidence = p_color_manzana + p_color_pera

    # Calcular la probabilidad posterior usando el Teorema de Bayes
    # P(fruta | color) = P(color, fruta) / P(color)
    p_manzana_dado_color = p_color_manzana / p_color_evidence
    p_pera_dado_color = p_color_pera / p_color_evidence
    
    posterior_probabilities.append({
        'Color': color,
        'P(manzana | color)': f"{p_manzana_dado_color:.2%}",
        'P(pera | color)': f"{p_pera_dado_color:.2%}"
    })

# Mostrar los resultados en una tabla con la ayuda de la librería pandas
df_posterior = pd.DataFrame(posterior_probabilities)

print("--- Respuesta a Q2 ---")
print("Tabla de probabilidades posteriores P(fruta | color):")
print(df_posterior.to_string(index=False))