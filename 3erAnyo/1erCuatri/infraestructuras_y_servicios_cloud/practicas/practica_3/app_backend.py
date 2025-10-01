from flask import Flask, request, jsonify
import torch
from transformers import BertTokenizer

# Corregido: Flask en lugar de Flasck
app = Flask(__name__)

# La ruta donde el script user-data descargó el modelo
MODEL_LOCAL_PATH = '40model_amazon.pt'
model = None
tokenizer = None

# Configuración para el modelo BERT
MAX_LEN = 100
PRE_TRAINED_MODEL_NAME = 'bert-base-cased'
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Cargamos el modelo y tokenizer directamente al iniciar
try:
    print("Cargando modelo desde:", MODEL_LOCAL_PATH)
    model = torch.load(MODEL_LOCAL_PATH, map_location=device)
    model.eval()  # Ponemos el modelo en modo evaluación
    print("Modelo cargado exitosamente.")
    
    print("Cargando tokenizer BERT...")
    tokenizer = BertTokenizer.from_pretrained(PRE_TRAINED_MODEL_NAME)
    print("Tokenizer cargado exitosamente.")
except Exception as e:
    print(f"Error al cargar el modelo o tokenizer: {e}")
    # La aplicación se ejecutará, pero el endpoint de predicción devolverá un error.

@app.route('/predict', methods=['POST'])
def predict():
    # Comprobamos si el modelo y tokenizer se cargaron correctamente al inicio
    if model is None or tokenizer is None:
        return jsonify({"error": "Modelo o tokenizer no disponible o no se pudo cargar al inicio."}), 500
    
    try:
        data = request.get_json(force=True)
        # Asumiendo que 'text' es el texto para análisis de sentimientos
        review_text = data['text']
        
        # Tokenizar el texto de entrada
        encoding_review = tokenizer.encode_plus(
            review_text,
            max_length=MAX_LEN,
            truncation=True,
            add_special_tokens=True,
            return_token_type_ids=False,
            padding='max_length',
            return_attention_mask=True,                               
            return_tensors='pt'
        )

        input_ids = encoding_review['input_ids'].to(device)
        attention_mask = encoding_review['attention_mask'].to(device)
        
        # Realizar la predicción
        with torch.no_grad():
            output = model(input_ids, attention_mask)
            _, prediction = torch.max(output, dim=1)
        
        # Convertir la predicción a un resultado interpretable
        sentiment = "positivo" if prediction.item() == 1 else "negativo"
        
        return jsonify({
            "prediction": prediction.item(),
            "sentiment": sentiment,
            "text": review_text
        })
    
    except KeyError:
        return jsonify({"error": "La clave 'text' no se encontró en el JSON."}), 400
    except Exception as e:
        return jsonify({"error": f"Ocurrió un error en la predicción: {str(e)}"}), 400

if __name__ == '__main__':
    # Escucha en todas las interfaces de red en el puerto 5000
    app.run(host='0.0.0.0', port=5000)
