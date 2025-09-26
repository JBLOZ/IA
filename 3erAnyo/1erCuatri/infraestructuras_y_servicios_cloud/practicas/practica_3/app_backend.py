from flask import Flask, request, jsonify
import joblib
import os
import boto3
app = Flasck(__name__)
S3_BUCKET = 'tu-nombre-de-bucket-unico' # ¡Cambia esto!
S3_MODEL_KEY = 'backend/modelo.pkl'
MODEL_LOCAL_PATH = 'modelo.pkl'


def download_model_from_s3():
    try:
        s3 = boto3.client('s3')
        s3.download_file(S3_BUCKET, S3_MODEL_KEY, MODEL_LOCAL_PATH)
        return True
    except Exception as e:
        print(f"Error descargando el modelo: {e}")
        return False
    

model_downloaded = download_model_from_s3()
model = None
if model_downloaded:
    model = joblib.load(MODEL_LOCAL_PATH)




@app.route('/predict', methods=['POST'])
def predict():

    if not model:
        return jsonify({"error": "Modelo no disponible"}), 500
    
    try:
        data = request.get_json(force=True)
        features = data['features']
        prediction = model.predict([features])
        return jsonify({"prediction": prediction.tolist()[0]})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)