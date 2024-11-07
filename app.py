import streamlit as st
import pandas as pd
from db_connection import get_connection  # Import de la fonction de connexion

st.title("Analyse et Exportation de Données Étudiantes pour les Cours")


ville_selectionnee = st.sidebar.selectbox(
    "Choisissez une ville ou 'Tous' pour afficher toutes les données",
    ["Tous", "BEAUNE", "BORDEAUX", "CHAMBERY", "LONDON", "LYON", "MARSEILLE", "MONACO", "PARIS", "RENNES", "SANFRANCISCO"]
)


if ville_selectionnee == "Tous":
    requete_sql = """
    SELECT DISTINCT TYPE, LIBELLE_MAT, UID_MAT, NOMPERSO, UID, NOM_DIP, NOMPERSO_DIP, 'BEA' AS code
    FROM STG_HYP.BEAUNE_Cours
    WHERE UID_MAT LIKE '90OM%'
    UNION ALL
    SELECT DISTINCT TYPE, LIBELLE_MAT, UID_MAT, NOMPERSO, UID, NOM_DIP, NOMPERSO_DIP, 'BOR' AS code
    FROM STG_HYP.BORDEAUX_Cours
    WHERE UID_MAT LIKE '90OM%'
    UNION ALL
    SELECT DISTINCT TYPE, LIBELLE_MAT, UID_MAT, NOMPERSO, UID, NOM_DIP, NOMPERSO_DIP, 'CHA' AS code
    FROM STG_HYP.CHAMBERY_Cours
    WHERE UID_MAT LIKE '90OM%'
    UNION ALL
    SELECT DISTINCT TYPE, LIBELLE_MAT, UID_MAT, NOMPERSO, UID, NOM_DIP, NOMPERSO_DIP, 'LON' AS code
    FROM STG_HYP.LONDON_Cours
    WHERE UID_MAT LIKE '90OM%'
    UNION ALL
    SELECT DISTINCT TYPE, LIBELLE_MAT, UID_MAT, NOMPERSO, UID, NOM_DIP, NOMPERSO_DIP, 'LYO' AS code
    FROM STG_HYP.LYON_Cours
    WHERE UID_MAT LIKE '90OM%'
    UNION ALL
    SELECT DISTINCT TYPE, LIBELLE_MAT, UID_MAT, NOMPERSO, UID, NOM_DIP, NOMPERSO_DIP, 'MAR' AS code
    FROM STG_HYP.MARSEILLE_Cours
    WHERE UID_MAT LIKE '90OM%'
    UNION ALL
    SELECT DISTINCT TYPE, LIBELLE_MAT, UID_MAT, NOMPERSO, UID, NOM_DIP, NOMPERSO_DIP, 'MON' AS code
    FROM STG_HYP.MONACO_Cours
    WHERE UID_MAT LIKE '90OM%'
    UNION ALL
    SELECT DISTINCT TYPE, LIBELLE_MAT, UID_MAT, NOMPERSO, UID, NOM_DIP, NOMPERSO_DIP, 'PAR' AS code
    FROM STG_HYP.PARIS_Cours
    WHERE UID_MAT LIKE '90OM%'
    UNION ALL
    SELECT DISTINCT TYPE, LIBELLE_MAT, UID_MAT, NOMPERSO, UID, NOM_DIP, NOMPERSO_DIP, 'REN' AS code
    FROM STG_HYP.RENNES_Cours
    WHERE UID_MAT LIKE '90OM%'
    UNION ALL
    SELECT DISTINCT TYPE, LIBELLE_MAT, UID_MAT, NOMPERSO, UID, NOM_DIP, NOMPERSO_DIP, 'SAN' AS code
    FROM STG_HYP.SANFRANCISCO_Cours
    WHERE UID_MAT LIKE '90OM%'
    """
else:
    requete_sql = f"""
    SELECT DISTINCT TYPE, LIBELLE_MAT, UID_MAT, NOMPERSO, UID, NOM_DIP, NOMPERSO_DIP, '{ville_selectionnee[:3].upper()}' AS code
    FROM STG_HYP.{ville_selectionnee}_Cours
    WHERE UID_MAT LIKE '90OM%'
    """

if st.button("Exécuter la requête et générer le CSV"):
    connection = get_connection()

    if connection:
        try:
            with st.spinner('Exécution de la requête en cours... veuillez patienter'):

                df = pd.read_sql_query(requete_sql, connection)

            df['UID'] = df['UID'].astype(str).str.split(', ')
            df['NOMPERSO'] = df['NOMPERSO'].astype(str).str.split(', ')
            df = df.explode(['UID', 'NOMPERSO'])
            df = df.drop_duplicates()

            connection.close()

            st.write("Aperçu des données :", df.head())

            csv = df.to_csv(index=False).encode('utf-8')

            st.download_button(
                label="Télécharger les données en CSV",
                data=csv,
                file_name='resultats_requete.csv',
                mime='text/csv'
            )
        except Exception as e:
            st.error(f"Erreur lors de l'exécution de la requête : {e}")
    else:
        st.error("Impossible de se connecter à la base de données. Veuillez vérifier les paramètres de connexion.")

