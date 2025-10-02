import sentiment_analysis

# Inicializa el analizador de sentimiento
analizador = sentiment_analysis.SentimentAnalysisSpanish()

# Analiza una frase
texto_positivo = "Me encanta este producto, es de una calidad excelente."
sentimiento_pos = analizador.sentiment(texto_positivo)
print(f"Texto: '{texto_positivo}'")
print(f"Puntuación de sentimiento: {sentimiento_pos}")

texto_negativo = "El servicio fue terrible, no lo recomiendo para nada."
sentimiento_neg = analizador.sentiment(texto_negativo)
print(f"\nTexto: '{texto_negativo}'")
print(f"Puntuación de sentimiento: {sentimiento_neg}")