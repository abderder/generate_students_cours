import pyodbc
import streamlit as st

def get_connection():
    try:
        # Récupération des secrets à partir de Streamlit
        server = st.secrets["DB_SERVER"]
        database = st.secrets["DB_DATABASE"]
        username = st.secrets["DB_USERNAME"]
        password = st.secrets["DB_PASSWORD"]

        # Debug: Affichage des informations de connexion (sauf le mot de passe)
        st.write(f"Essai de connexion avec les paramètres : SERVER={server}, DATABASE={database}, USERNAME={username}")

        connection = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            f'SERVER={server};'
            f'DATABASE={database};'
            f'UID={username};'
            f'PWD={password};'
        )
        st.write("Connexion réussie à la base de données.")
        return connection
    except pyodbc.InterfaceError as e:
        st.write("Erreur d'interface (connexion au pilote) :")
        st.write(e)
        st.error(f"Erreur d'interface : {e}")
    except pyodbc.DatabaseError as e:
        st.write("Erreur liée à la base de données :")
        st.write(e)
        st.error(f"Erreur de base de données : {e}")
    except Exception as e:
        st.write("Erreur générale lors de la connexion :")
        st.write(e)
        st.error(f"Erreur générale : {e}")
    return None
