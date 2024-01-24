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
client = MongoClient(uri, tls=True, tlsAllowInvalidCertificates=True, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

cursor = client['IPSSI']['projetMongo']

#open Videsogames.csv

df = pd.read_csv('C:\\Users\\33619\\Desktop\\IPSSI_COURS\\NoSQL\\PROJET_Mongo\\MongoDB-Project\\Video_Games.csv', index_col='index')


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
        .e1nzilvr5 p {
            color: white;
        }
        
    </style>
    """
    st.markdown(custom_styles, unsafe_allow_html=True)

    # Titre centré en haut au milieu de la page
    st.title('Video Games Sales Analysis')
    # st.markdown("<h1 class='centered-title'>Video Games Sales Analysis</h1>", unsafe_allow_html=True)

    # Ajouter un titre avant la selectbox
    # st.write("Sélectionnez un graphique dans la liste ci-dessous :")

    # Selectbox en bas pour afficher les graphiques
    graphique = st.selectbox('Sélectionnez un graphique dans la liste ci-dessous :', options=['Total Sales by Genre', 'Sales by Game Types by Region', 'Sales by region', 'Top 10 Platforms by Global Sales', 'Boxplot of Global Sales by Genre', 'Distribution of Release Years', 'Average Global Sales per Region for each Genre'],
                            key='selectbox')  # Ajoutez un identifiant 'key' pour éviter les problèmes de mise en cache

    # Logique pour afficher les graphiques

    if graphique == 'Total Sales by Genre':
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
        # st.sidebar.text("""Analyse du graphique 1: \
        # Les jeux de divertissement qui \
        # demandent moins d'attention \
        # et de concentration sont beaucoup \
        # plus vendus que les jeux qui \
        # demandent une forte concentration. \
        # Par exemple 3400 millions de jeux d'action et de sport \
        # ont été vendus tandis que seulement 420 millions \
        # de jeux de puzzle et de stratégie ont été vendus.""")

        st.sidebar.markdown("""
        **Analyse du graphique 1:**

        Les jeux de divertissement qui demandent moins d'attention et de concentration sont beaucoup plus vendus que les jeux qui demandent une forte concentration. Par exemple, 3400 millions de jeux d'action et de sport ont été vendus, tandis que seulement 420 millions de jeux de puzzle et de stratégie ont été vendus.
        """)

        
    elif graphique == 'Sales by Game Types by Region':
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

        st.sidebar.markdown("""
        **Analyse du graphique 2:**
        
        Aux Etats-Unis et en Europe, les jeux d'actions, de rôle et de sports sont le plus vendus. Tandis qu'au Japon ce sont les jeux de rôle qui sont de loin les plus vendus.
        """)
        
    elif graphique == 'Sales by region':
        sales_by_region = df[['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']].sum().reset_index()
        sales_by_region.columns = ['Region', 'Sales']

        fig = px.pie(sales_by_region,
                    names='Region',
                    values='Sales',
                    title='Sales by region',
                    template='plotly_dark',
                    hole=0.4)
        st.plotly_chart(fig)


        st.sidebar.markdown("""
        **Analyse du graphique 3:**
        
        L'Amérique du Nord, l'Europe et le Japon représentent 92% des ventes de jeux dans le monde. L'Amérique du Nord représente à elle seule 50% des ventes de jeux.
        """)
        
    elif graphique == 'Top 10 Platforms by Global Sales':
        top_platforms = df.groupby('Platform')['Global_Sales'].sum().nlargest(10).reset_index()

        fig = px.bar(top_platforms,
                    x='Platform',
                    y='Global_Sales',
                    title='Top 10 Platforms by Global Sales',
                    labels={'Global_Sales': 'Global Sales (in millions)', 'Platform': 'Platform'},
                    template='plotly_dark')

        
        st.plotly_chart(fig)
        st.sidebar.markdown("""
        **Analyse du graphique 4:**
        
        Au vu des données il vaut mieux sortir un jeu sur console que sur PC.
        """)
        # st.markdown("<div class='description'>Text4 here</div>", unsafe_allow_html=True)
    elif graphique == 'Boxplot of Global Sales by Genre':
        summary_categorical_dist1(df, 'Genre')
        st.sidebar.markdown("""
        **Analyse du graphique 5:**
        
        Les jeux d'action et de sport représentent la majorité des ventes dans le monde.
        """)
        # st.markdown("<div class='description'>Text5 here</div>", unsafe_allow_html=True)
    elif graphique == 'Distribution of Release Years':
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
        st.sidebar.markdown("""
        **Analyse du graphique 6:**
        
        C'est entre 2008 et 2010 que le plus de jeux sont sortis. Au cours de l'année 2010 les jeux d'action, de sports, de tirs et de rôles représentent beaucoup plus de ventes que les jeux de stratégie et d'aventures.
        """)

        # st.markdown("<div class='description'>Text6 here</div>", unsafe_allow_html=True)

    elif graphique == 'Average Global Sales per Region for each Genre':
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

        st.sidebar.markdown("""
        **Analyse du graphique 7:**
        
        Les jeux de plateformes, de tirs et de rôles représentent le plus de ventes dans le monde. En Amérique du Nord et en Europe c'est les jeux de plateforme et de tirs qui sont le plus vendus. Au Japon c'est principalement les jeux de rôle.
        """)

        # plt.show()
        # st.markdown("<div class='description'>Text7 here</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
