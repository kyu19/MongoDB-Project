import streamlit as st
import pandas as pd
from pymongo import MongoClient
import pprint as pp
import json
import warnings
import matplotlib.pyplot as plt
import seaborn as sns

# # Fonction pour se connecter à MongoDB
# def connect_to_mongodb():
#     # Remplacez les valeurs suivantes par celles de votre configuration MongoDB
#     mongo_url = "votre_url_mongodb"
#     database_name = "votre_nom_de_base_de_donnees"

#     client = MongoClient(mongo_url)
#     return client[database_name]

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://boobacar5252:ZbsNiFG2mvM2MHcl@clusteryanis.iemddda.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

cursor = client['IPSSI']['projetMongo']

#open Videsogames.csv

df = pd.read_csv('C:\\Users\\ACER NITRO\\Desktop\\MongoDB-Project\\Video_Games.csv', index_col='index')


# warnings.filterwarnings('ignore')





def main():
    # Adding a black background color to the entire body and red text color
    custom_styles = """
    <style>
        body {
            background-color: #000000;
            color: white;
        }
        
        h1 {
            color: red;
            text-align: center;
        }
        .st-emotion-cache-18ni7ap, .st-emotion-cache-fg4pbf {
            background: none;
        }
        .graph-selector {
            text-align: center;
            padding-bottom: 20px;
        }
        p {
            color: white;
        }
        .st-emotion-cache-zt5igj:hover a {
            display:none;
        }
        .description {
            margin-top: 25px;
            float: right;
            background: white;
            padding: 10px;
        }
        
    </style>
    """
    st.markdown(custom_styles, unsafe_allow_html=True)

    # Titre centré en haut au milieu de la page
    st.title('Video Games Sales Analysis')
    # st.markdown("<h1 class='centered-title'>Video Games Sales Analysis</h1>", unsafe_allow_html=True)

    # Ajouter un titre avant la selectbox
    st.write("Sélectionnez un graphique dans la liste ci-dessous :")

    # Selectbox en bas pour afficher les graphiques
    graphique = st.selectbox('Sélectionnez une option:', options=['graphique1', 'graphique2', 'graphique3', 'graphique4', 'graphique5', 'graphique6'],
                            key='selectbox')  # Ajoutez un identifiant 'key' pour éviter les problèmes de mise en cache

    # Logique pour afficher les graphiques
    if graphique == 'graphique1':
        total_sales_by_genre = df.groupby('Genre')['Global_Sales'].sum().sort_values(ascending=False)

        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(x=total_sales_by_genre.values, y=total_sales_by_genre.index, palette='viridis', ax=ax)
        plt.title("Total Sales by Genre")
        plt.xlabel("Total Sales (in millions)")
        plt.ylabel("Genre")
        # Instead of plt.show(), use st.pyplot()
        st.pyplot(fig)
        # Add your description
        st.markdown("<div class='description'>Text1 here</div>", unsafe_allow_html=True)

        st.markdown("<div class='description'>Text1 here</div>", unsafe_allow_html=True)
    elif graphique == 'graphique2':
        st.write('On affiche le graphique 2')
        st.markdown("<div class='description'>Text2 here</div>", unsafe_allow_html=True)
    elif graphique == 'graphique3':
        st.write('On affiche le graphique 3')
        st.markdown("<div class='description'>Text3 here</div>", unsafe_allow_html=True)
    elif graphique == 'graphique4':
        st.write('On affiche le graphique 4')
        st.markdown("<div class='description'>Text4 here</div>", unsafe_allow_html=True)
    elif graphique == 'graphique5':
        st.write('On affiche le graphique 5')
        st.markdown("<div class='description'>Text5 here</div>", unsafe_allow_html=True)
    elif graphique == 'graphique6':
        st.write('On affiche le graphique 6')
        st.markdown("<div class='description'>Text6 here</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
