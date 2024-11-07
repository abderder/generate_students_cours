import os
import pyodbc

def get_connection():
    try:
        server = os.getenv('DB_SERVER', 'default_server')
        database = os.getenv('DB_DATABASE', 'default_database')
        username = os.getenv('DB_USERNAME', 'default_username')
        password = os.getenv('DB_PASSWORD', 'default_password')

        connection = pyodbc.connect(
            f'DRIVER={{SQL Server}};'
            f'SERVER={server};'
            f'DATABASE={database};'
            f'UID={username};'
            f'PWD={password};'
        )
        print("Connexion réussie à la base de données.")
        return connection
    except pyodbc.Error as e:
        print("Erreur lors de la connexion à la base de données :")
        print(e)
        return None