import pyodbc
import streamlit as st

def get_connection():
    try:
        # Récupération des secrets à partir de Streamlit
        server = st.secrets["DB_SERVER"]
        database = st.secrets["DB_DATABASE"]
        username = st.secrets["DB_USERNAME"]
        password = st.secrets["DB_PASSWORD"]

        connection = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            f'SERVER={server};'
            f'DATABASE={database};'
            f'UID={username};'
            f'PWD={password};'
            'Encrypt=yes;'
            'TrustServerCertificate=no;'
        )
        print("Connexion réussie à la base de données.")
        return connection
    except pyodbc.Error as e:
        print("Erreur lors de la connexion à la base de données :")
        print(e)
        return None
