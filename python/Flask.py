from flask import Flask, request, jsonify
from sqlalchemy import create_engine
import pandas as pd
from joblib import load
from datetime import datetime

app = Flask(__name__)

# Database credentials and connection setup
dbname = 'lastberasmiNchalah'
user = ''  # Replace with the correct username
password = '********'  # Replace with the correct password
host = 'DESKTOP-FDCR8VU'
port = '1433'
driver = 'ODBC Driver 17 for SQL Server'

# Creating SQLAlchemy engine
connection_string = f'mssql+pyodbc://{user}:{password}@{host}:{port}/{dbname}?driver={driver}'
engine = create_engine(connection_string)

# Load the trained model
model = load('model_Clients_classifier.pkl')  # Update with the path to your model

@app.route('/predict', methods=['GET'])
def predict():
    try:
        # SQL query to load the data
        query = """
        SELECT dd.FullDate, dc.Clients, fs.Nbre_sacs
        FROM Fact_Stpa_Sboula fs
        JOIN Date_Dim dd ON fs.DateFK = dd.DateID
        JOIN DimClient dc ON fs.Client_FK = dc.Client_Id
        """
        print(query)
        df = pd.read_sql_query(query, engine)
        print(df)
        # Data preprocessing
        df['FullDate'] = pd.to_datetime(df['FullDate'])
        df['Nbre_sacs'] = pd.to_numeric(df['Nbre_sacs'], errors='coerce')
        df.sort_values(by=['Clients', 'FullDate'], inplace=True)
        df['Somme_Nbre_sacs_10j'] = df.groupby('Clients')['Nbre_sacs'].rolling(window=10, min_periods=1).sum().reset_index(level=0, drop=True)
        df['Fidele'] = df['Somme_Nbre_sacs_10j'].apply(lambda x: 1 if x > 500 else 0)

        # Prediction
        X = df[['Somme_Nbre_sacs_10j']]  # Features for prediction
        df['Predicted Fidelity'] = model.predict(X)

        # Returning JSON response
        return jsonify(df.to_dict(orient='records'))
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
