from flask import Flask, request, jsonify
import joblib

# Corregido: Flask en lugar de Flasck
app = Flask(__name__)

# La ruta donde el script user-data descargó el modelo
MODEL_LOCAL_PATH = 'modelo.pkl'
model = None

# Cargamos el modelo directamente al iniciar, ya que user-data lo ha descargado
try:
    print("Cargando modelo desde:", MODEL_LOCAL_PATH)
    model = joblib.load(MODEL_LOCAL_PATH)
    print("Modelo cargado exitosamente.")
except Exception as e:
    print(f"Error al cargar el modelo: {e}")
    # La aplicación se ejecutará, pero el endpoint de predicción devolverá un error.

@app.route('/predict', methods=['POST'])
def predict():
    # Comprobamos si el modelo se cargó correctamente al inicio
    if model is None:
        return jsonify({"error": "Modelo no disponible o no se pudo cargar al inicio."}), 500
    
    try:
        data = request.get_json(force=True)
        # Asumiendo que 'features' es una lista de valores, ej: [5.1, 3.5, 1.4, 0.2]
        features = data['features']
        
        prediction = model.predict([features])
        
        return jsonify({"prediction": prediction.tolist()[0]})
    
    except KeyError:
        return jsonify({"error": "La clave 'features' no se encontró en el JSON."}), 400
    except Exception as e:
        return jsonify({"error": f"Ocurrió un error en la predicción: {str(e)}"}), 400

if __name__ == '__main__':
    # Escucha en todas las interfaces de red en el puerto 5000
    app.run(host='0.0.0.0', port=5000)
