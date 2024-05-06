from flask import Flask, request, jsonify
import pandas as pd
from sqlalchemy import create_engine
import pickle
from flask_cors import CORS  # Import CORS class    
app = Flask(__name__)
CORS(app)  # Add this line to enable CORS for all routes

# Connexion à la base de données
def create_engine_db():
    dbname = 'lastberasmiNchalah'
    user = ''  # Remplacez par votre nom d'utilisateur
    password = '********'  # Remplacez par votre mot de passe
    host = 'DESKTOP-FDCR8VU'
    port = '1433'
    driver = 'ODBC Driver 17 for SQL Server'  # Assurez-vous que ce pilote est installé
    connection_string = f'mssql+pyodbc://{user}:{password}@{host}:{port}/{dbname}?driver={driver}'
    engine = create_engine(connection_string)
    return engine

# Charger les données et préparer les recommandations
def load_data():
    engine = create_engine_db()
    query = "SELECT * FROM DimClient"
    df = pd.read_sql_query(query, engine)
    return df

# Dictionnaire des provinces et leurs villes
provinces = {
    1: ["Bizerte", "Beja", "Jendouba", "Le Kef"],
    2: ["Tunis", "Ariana", "Ben Arous", "Zaghouan", "Mannouba", "Nabeul", "Kelibia"],
    3: ["Seliana", "Sousse", "Kairouan", "Monastir", "Mahdia", "El Jem"],
    4: ["Sidi Bouzid", "Sfax", "Gafsa", "El Hencha", "Skhira", "Tozeur", "El Hamma"],
    5: ["Tataouine", "Gabes", "Kebili", "Medenine", "Djerba", "Zarzis"]
}

# Déterminer la province à partir de la destination
def trouver_province(destination):
    for num_province, villes in provinces.items():
        if destination in villes:
            return num_province
    return "Non classée"

# Préparation des données et recommandations
def prepare_data():
    df = load_data()
    df['Province'] = df['Destination'].apply(trouver_province)
    return df

# Fonction pour recommander des destinations
def recommend_destinations(user_id, df):
    user_profiles = df.groupby('Client_Id')['Province'].apply(set).reset_index(name='Visited_Provinces')
    most_popular_destinations = df.groupby(['Province', 'Destination']).size().reset_index(name='Counts').sort_values(['Province', 'Counts'], ascending=[True, False])
    most_popular_destinations = most_popular_destinations.groupby('Province').head(1)

    visited_provinces = user_profiles.loc[user_profiles['Client_Id'] == user_id, 'Visited_Provinces'].values[0]
    unvisited_provinces = set(provinces.keys()) - visited_provinces
    recommendations = most_popular_destinations[most_popular_destinations['Province'].isin(unvisited_provinces)]
    return recommendations['Destination'].tolist()

# Route pour obtenir des recommandations
@app.route('/recommendations/<int:user_id>', methods=['GET'])
def get_recommendations(user_id):
    df = prepare_data()
    recommendations = recommend_destinations(user_id, df)
    return jsonify({'user_id': user_id, 'recommendations': recommendations})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
