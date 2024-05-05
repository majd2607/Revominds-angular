from flask import Flask, request, jsonify
import pandas as pd
from joblib import load
from datetime import datetime

app = Flask(__name__)

# Load the trained model
with open("model_Clients_classifier.pkl", 'rb') as f:
    model = load(f)

@app.route('/predict', methods=['POST'])
def predict():
    # Check if file is present in the request
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    # Check if the file is an Excel file
    if file.filename == '':
        return jsonify({'error': 'No file selected'})
    if not file.filename.endswith('.xlsx'):
        return jsonify({'error': 'Only Excel files (.xlsx) are supported'})

    # Load the Excel file into a DataFrame
    try:
        df = pd.read_excel(file)

        # Ensure 'FullDate' is a datetime type and 'Nbre_sacs' is numeric
        df['FullDate'] = pd.to_datetime(df['FullDate'])
        df['Nbre_sacs'] = pd.to_numeric(df['Nbre_sacs'], errors='coerce')

        # Calculate the sum of 'Nbre_sacs' for each client over a 10-day rolling period
        df['Somme_Nbre_sacs_10j'] = df.groupby('Clients')['Nbre_sacs'].rolling(window=10, min_periods=1).sum().reset_index(level=0, drop=True)

        # Prepare features for prediction
        X_pred = df[['Somme_Nbre_sacs_10j']]
        df['Predicted Fidelity'] = model.predict(X_pred)
    except Exception as e:
        return jsonify({'error': f'Error processing Excel file: {str(e)}'})

    # Convert DataFrame to JSON and return
    return df.to_json(orient='records')

if __name__ == '__main__':
    app.run(debug=True)
