from flask import Flask, request, jsonify
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder, StandardScaler
import pandas as pd
from sqlalchemy import create_engine
from flask_cors import CORS  # Import CORS class

app = Flask(__name__)
CORS(app)  # Add this line to enable CORS for all routes

# Database credentials and connection
dbname = 'lastberasmiNchalah'
user = ''  # Remplacez par votre nom d'utilisateur
password = '********'  # Remplacez par votre mot de passe
host = 'DESKTOP-FDCR8VU'
port = '1433'
driver = 'ODBC Driver 17 for SQL Server'  # Assurez-vous que ce pilote est installé
connection_string = f'mssql+pyodbc://{user}:{password}@{host}:{port}/{dbname}?driver={driver}'
engine = create_engine(connection_string)

# Load data
query = """
SELECT * FROM DimClient 
"""
df = pd.read_sql_query(query, engine)

# Encode and scale data
df['Destination'] = df['Destination'].astype(str)
df['Clients'] = df['Clients'].astype(str)

le_destination = LabelEncoder()
le_clients = LabelEncoder()

df['Destination_Encoded'] = le_destination.fit_transform(df['Destination'])
df['Clients_Encoded'] = le_clients.fit_transform(df['Clients'])

# Province determination logic
provinces = {
    1: ["Bizerte", "Beja", "Jendouba", "Le Kef"],
    2: ["Tunis", "Ariana", "Ben Arous", "Zaghouan", "Mannouba", "Nabeul", "Kelibia"],
    3: ["Seliana", "Sousse", "Kairouan", "Monastir", "Mahdia", "El Jem"],
    4: ["Sidi Bouzid", "Sfax", "Gafsa", "El Hencha", "Skhira","Tozeur","El Hamma"],
    5: ["Tataouine", "Gabes", "Kebili", "Medenine", "Djerba", "Zarzis"]
}

def trouver_province(destination):
    for num_province, villes in provinces.items():
        if destination in villes:
            return num_province
    return "Non classée"

df['Province'] = df['Destination'].apply(trouver_province)

# Clustering
kmeans = KMeans(n_clusters=len(provinces), random_state=0)
features_for_clustering = ['Destination_Encoded', 'Clients_Encoded']
df['Cluster'] = kmeans.fit_predict(df[features_for_clustering])

# Define a route to return the cluster number
@app.route('/get_cluster', methods=['POST'])
def get_cluster():
    data = request.get_json()
    destination = data['destination']
    client = data['client']
    
    dest_encoded = le_destination.transform([destination])[0]
    client_encoded = le_clients.transform([client])[0]
    
    cluster_number = kmeans.predict([[dest_encoded, client_encoded]])[0]
    return jsonify({'cluster': int(cluster_number)})

if __name__ == '__main__':
    app.run(debug=True)
