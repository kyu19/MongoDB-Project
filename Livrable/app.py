import streamlit as st
import pandas as pd
from pymongo import MongoClient
import pprint as pp
import json
import warnings
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

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

def summary_categorical_dist1(df_data, col):
    count = df_data[col].value_counts().sort_index().reset_index()
    count.columns = [col, 'count']

    # Plot Count
    fig_count = px.bar(count, x='count', y=col, orientation='h', title=f"Counts - Distribution of: {col}",
                       labels={'count': 'Counts', col: col},
                       template='plotly_dark')

    # Plot Proportions
    fig_proportions = px.pie(count, names=col, values='count', title=f"Proportions - Distribution of: {col}",
                             labels={col: col, 'count': 'Proportions'},
                             template='plotly_dark')

    # Show the plots
    st.plotly_chart(fig_count)
    st.plotly_chart(fig_proportions)

    # fig_count.show()
    # fig_proportions.show()



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
    graphique = st.selectbox('Sélectionnez une option:', options=['graphique1', 'graphique2', 'graphique3', 'graphique4', 'graphique5', 'graphique6', 'graphique7'],
                            key='selectbox')  # Ajoutez un identifiant 'key' pour éviter les problèmes de mise en cache

    # Logique pour afficher les graphiques

    if graphique == 'graphique1':
        total_sales_by_genre = df.groupby('Genre')['Global_Sales'].sum().sort_values(ascending=False).reset_index()

        fig = px.bar(total_sales_by_genre,
                    x='Global_Sales',
                    y='Genre',
                    orientation='h',
                    title="Total Sales by Genre",
                    labels={'Global_Sales': 'Total Sales (in millions)', 'Genre': 'Genre'},
                    template='plotly_dark',
                    color='Global_Sales',  # Utilisez une colonne numérique pour la coloration
                    color_continuous_scale='viridis')

        fig.update_layout(yaxis=dict(categoryorder='total ascending'))
        # Instead of fig.show(), use st.plotly_chart()
        st.plotly_chart(fig)
        # Add your description
        # st.markdown("<div class='description'>Text1 here</div>", unsafe_allow_html=True)
        st.sidebar.text("Analyse du graphique 1: ...")
        
    elif graphique == 'graphique2':
        sales_by_genre_region = df.groupby('Genre')[['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']].sum()

        most_sold_genre_by_region = sales_by_genre_region.idxmax(axis=0)

        plt.figure(figsize=(12, 12))
        sns.barplot(x='Genre', y='value', hue='variable', data=pd.melt(sales_by_genre_region.reset_index(), id_vars='Genre'))
        plt.title("Sales by Game Types by Region")
        plt.xlabel("Game Genre")
        plt.ylabel("Total Sales Amount (million)")
        plt.legend(title='Region', loc='upper right')
        plt.xticks(rotation=45, ha='right')
        plt.style.use("dark_background")
        st.pyplot(fig=plt)

        st.sidebar.text("Analyse du graphique 2: ...")
        
    elif graphique == 'graphique3':
        sales_by_region = df[['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']].sum().reset_index()
        sales_by_region.columns = ['Region', 'Sales']

        fig = px.pie(sales_by_region,
                    names='Region',
                    values='Sales',
                    title='Répartition des Ventes par Région',
                    template='plotly_dark',
                    hole=0.4)
        st.plotly_chart(fig)


        st.sidebar.text("Analyse du graphique 3: ...")
        
    elif graphique == 'graphique4':
        top_platforms = df.groupby('Platform')['Global_Sales'].sum().nlargest(10).reset_index()

        fig = px.bar(top_platforms,
                    x='Platform',
                    y='Global_Sales',
                    title='Top 10 des Plateformes par Ventes Globales',
                    labels={'Global_Sales': 'Ventes Globales (en millions)', 'Platform': 'Plateforme'},
                    template='plotly_dark')

        
        st.plotly_chart(fig)
        st.markdown("<div class='description'>Text4 here</div>", unsafe_allow_html=True)
    elif graphique == 'graphique5':
        summary_categorical_dist1(df, 'Genre')
        st.markdown("<div class='description'>Text5 here</div>", unsafe_allow_html=True)
    elif graphique == 'graphique6':
        # Create a histogram with Seaborn
        sns.histplot(df['Year_of_Release'].dropna(), bins=30, color='skyblue')
        plt.title("Distribution of Release Years")
        plt.xlabel("Year of Release")
        plt.ylabel("Count")
        #print the histogram with streamlit
        st.pyplot(fig=plt)

        # # Filter data for the year 2010
        games_2010 = df[df['Year_of_Release'] == 2010]

        # Calculate total sales by genre in 2010
        total_sales_by_genre_2010 = games_2010.groupby('Genre')['Global_Sales'].sum().sort_values(ascending=False).reset_index()

        # Create a bar chart with Plotly Express
        fig = px.bar(total_sales_by_genre_2010,
                    x='Global_Sales',
                    y='Genre',
                    title="Total Sales by Genre in 2010",
                    labels={'Global_Sales': 'Total Sales (in millions)', 'Genre': 'Genre'},
                    template='plotly_dark',
                    color='Global_Sales',  # Utilize a numerical column for coloring
                    color_continuous_scale='viridis')

        fig.update_layout(yaxis=dict(categoryorder='total ascending'))

        # Instead of st.plotly_chart(fig), use st.plotly_chart() without arguments
        st.plotly_chart(fig)

        st.markdown("<div class='description'>Text6 here</div>", unsafe_allow_html=True)

    elif graphique == 'graphique7':
        sales_col = df.columns[df.columns.str.contains('Sales')]
        fig, axs = plt.subplots(3, 2, figsize=(15, 15))

        # Choisir une palette de couleurs, par exemple 'Set3'
        color_palette = sns.color_palette("tab10")

        for i, sale in enumerate(sales_col):
            dfi = df.groupby('Genre')[sale].mean().reset_index().sort_values(sale, ascending=False)
            axs = axs.flatten()
            sns.barplot(data=dfi, y='Genre', x=sale, ax=axs[i], palette=color_palette)
            axs[i].set_title(f'Avg {sale} for each Genre')

        plt.tight_layout()
        st.pyplot(fig=plt)

        # plt.show()
        st.markdown("<div class='description'>Text7 here</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
