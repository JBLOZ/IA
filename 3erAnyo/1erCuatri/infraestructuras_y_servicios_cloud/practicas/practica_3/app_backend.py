from flask import Flask, request, jsonify
import re
import bz2
import _pickle as cPickle
import os
import warnings

# Suprimir warnings de versiones de sklearn
warnings.filterwarnings("ignore", category=UserWarning)

# Corregido: Flask en lugar de Flasck
app = Flask(__name__)

# Expresiones regulares para limpieza de texto
REPLACE_BY_SPACE_RE = re.compile(r'[/(){}\[\]\|@,;]')
BAD_SYMBOLS_RE = re.compile(r'[^\w\s]')

def compressed_pickle(title, data):
    with bz2.BZ2File(title + '.pbz2', 'w') as f:
        cPickle.dump(data, f)

def decompress_pickle(file):
    data = bz2.BZ2File(file, 'rb')
    data = cPickle.load(data)
    return data

class SentimentAnalysisSpanish:
    def __init__(self):
        try:
            # Rutas a los modelos comprimidos
            vectorizer_path = 'saved_model/ngram_vectorized_compressed.pbz2'
            classifier_path = 'saved_model/classifier_naive_bayes_compressed.pbz2'
            
            # Verificar que los archivos existen
            if not os.path.exists(vectorizer_path):
                raise FileNotFoundError(f"No se encontró el archivo: {vectorizer_path}")
            if not os.path.exists(classifier_path):
                raise FileNotFoundError(f"No se encontró el archivo: {classifier_path}")
            
            print("Cargando vectorizador desde:", vectorizer_path)
            self.vectorizer = decompress_pickle(vectorizer_path)
            print("Vectorizador cargado exitosamente.")
            
            print("Cargando clasificador desde:", classifier_path)
            self.classifier = decompress_pickle(classifier_path)
            print("Clasificador cargado exitosamente.")
            
        except Exception as e:
            print(f"Error al inicializar SentimentAnalysisSpanish: {e}")
            raise

    def clean_text(self, text):
        """Limpia el texto eliminando caracteres especiales y normalizando"""
        text = text.lower()
        text = REPLACE_BY_SPACE_RE.sub(' ', text)
        text = BAD_SYMBOLS_RE.sub('', text)
        return text

    def sentiment(self, text: str):
        """
        Devuelve la puntuación de sentimiento de un texto.
        Valores cercanos a 1 = sentimiento positivo
        Valores cercanos a 0 = sentimiento negativo
        """
        try:
            # Limpiar el texto
            cleaned_text = self.clean_text(text)
            
            # Vectorizar el texto
            vals = self.vectorizer.transform([cleaned_text])
            
            # Obtener la probabilidad de sentimiento positivo
            sentiment_score = self.classifier.predict_proba(vals)[0][1]
            
            return sentiment_score
            
        except Exception as e:
            print(f"Error en análisis de sentimiento: {e}")
            raise

# Inicializar el analizador de sentimientos
sentiment_analyzer = None

try:
    print("Inicializando analizador de sentimientos...")
    sentiment_analyzer = SentimentAnalysisSpanish()
    print("Analizador de sentimientos inicializado exitosamente.")
except Exception as e:
    print(f"Error al inicializar el analizador de sentimientos: {e}")
    sentiment_analyzer = None

@app.route('/predict', methods=['POST'])
def predict():
    # Verificar si el analizador se cargó correctamente
    if sentiment_analyzer is None:
        return jsonify({"error": "Analizador de sentimientos no disponible o no se pudo cargar al inicio."}), 500
    
    try:
        data = request.get_json(force=True)
        
        # Verificar que se envió texto
        if 'text' not in data:
            return jsonify({"error": "La clave 'text' no se encontró en el JSON. Envía el texto a analizar."}), 400
        
        text = data['text']
        
        # Validar que el texto no esté vacío
        if not text or not text.strip():
            return jsonify({"error": "El texto no puede estar vacío."}), 400
        
        # Realizar análisis de sentimientos
        sentiment_score = sentiment_analyzer.sentiment(text)
        
        # Determinar si es positivo o negativo (umbral en 0.5)
        is_positive = sentiment_score > 0.5
        sentiment_label = 1 if is_positive else 0  # 1 = positivo, 0 = negativo
        
        # Preparar respuesta
        response = {
            "sentiment": sentiment_label,
            "sentiment_score": float(sentiment_score),
            "sentiment_label": "positive" if is_positive else "negative",
            "text_analyzed": text[:100] + "..." if len(text) > 100 else text  # Mostrar solo los primeros 100 caracteres
        }
        
        print(f"Análisis completado - Texto: '{text[:50]}...', Puntuación: {sentiment_score:.3f}, Sentimiento: {sentiment_label}")
        
        return jsonify(response)
    
    except KeyError as e:
        return jsonify({"error": f"Clave faltante en el JSON: {str(e)}"}), 400
    except Exception as e:
        print(f"Error en predicción: {e}")
        return jsonify({"error": f"Ocurrió un error en el análisis de sentimientos: {str(e)}"}), 500

if __name__ == '__main__':
    print("Iniciando servidor de análisis de sentimientos...")
    print("Endpoint disponible:")
    print("  POST /predict - Análisis de sentimientos")
    
    # Escucha en todas las interfaces de red en el puerto 5000
    app.run(host='0.0.0.0', port=5000, debug=False)
