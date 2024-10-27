import streamlit as st
import pandas as pd
from utils.data_processing import DataProcessor
from utils.chart_processing import ChartProcessor
import plotly.express as px



# Nous appelons la classe Data pour lui signaler l'emplacement des données 
# Et nous appelons également processor pour les transformer
processor = DataProcessor('data/')
df_final = processor.obtenir_dataframe()

# Pour que les graphiques fonctionnent, nous appelons également ChartProcessor
chart = ChartProcessor(df_final)


# Ajout d'une barre latérale pour naviguer entre les pages, pour cela nous utilisons selectbox (choix unique)
# https://docs.streamlit.io/develop/api-reference/layout/st.sidebar
page = st.sidebar.selectbox(
    "Naviguer vers",
    ("Accueil", "Manipulation des data", "Comparaison par sexe","Performance par participant")
)

def page_accueil():
    st.title("Dashboard Anca, Nassim, Paul-Elie, Yasmine")
    st.write("Nous avons construit cette application dans le but de proposer un dépassement des questions 1, 2 et 3")
    st.write("Nous vous invitons à cliquer sur la barre de navigation disponnible à gauche")
    st.title("Description des différentes pages :")
    st.header("**Manipulation des data**")
    st.write("Cette page permet de créer le dataframe de manière interractive en selectionnant les colonnes souhaitées, pour le transformer en fichier téléchargeable")
    st.header("**Comparaison par sexe**")
    st.write("Cette page permet de créer une comparaison Femme / Homme sur toutes les colonnes ayant des valeurs numériques")
    st.header("**Performance par participant**")
    st.write("Cette page permet de recréer de manière dynamique la performance des participants le long des différents splits")



def page_compare_sexe_means():
    st.title("Comparaison des moyennes entre Hommes et Femmes")

    # Exclusion des données non numériques pour la copmparaison (risque de bug)
    numeric_columns = df_final.select_dtypes(include='number').columns.tolist()

    # Nous utilisons selectbox (l'outil de selection intégré streamlit) pour choisir la colonne utilisée
    selected_column = st.selectbox("Sélectionnez une colonne pour comparer", numeric_columns)

    fig = chart.compare_gender_means(selected_column)
    st.plotly_chart(fig)

def dataframe():
    st.title("Manipulation des data")
    # Ajouter des analyses et des statistiques supplémentaires ici
    st.write("Veuillez selectionner les colonnes qui vous intéresse pour créer votre dataframe")
    # Get all column names from df_final
    all_columns = df_final.columns.tolist()

    # Nous utiliserons ici le multiselect (comme pour le graph de la performance des participants)
    selected_columns = st.multiselect(
        "Sélectionnez les colonnes à afficher", 
        options=all_columns
    )

    # initialisation de df_button pour la boucle plus tard, cela permet d'éviter un emssage d'erreur quand le dataframe est vide
    df_boutton = None 
    
    # Une fonction if pour afficher un message d'erreur cohérent quand auncune colonne selectionnée
    if selected_columns:
        st.write("DataFrame personnalisé avec les colonnes sélectionnées :")
        st.dataframe(df_final[selected_columns])
        df_boutton = df_final[selected_columns]
    else:
        st.write("Aucune colonne sélectionnée. Veuillez choisir au moins une colonne.")

    # Nous avons construit ce boutton en suivant le tutoriel disponnible sur le site de streamlit :
    # https://docs.streamlit.io/knowledge-base/using-streamlit/how-download-pandas-dataframe-csv
    def convert_df(df):
        return df.to_csv(index=False).encode('utf-8')
    
    # Une fonction if pour afficher un message d'erreur cohérent quand auncune colonne selectionnée
    if df_boutton is not None:
        csv = convert_df(df_boutton)
        st.download_button(
        "Press to Download",
        csv,
        "file.csv",
        "text/csv",
        key='download-csv'
        )
    else:
        st.write("Pas de données à télécharger.")


def splitperf():
    st.title("Performance des participants par split")
    st.write("Dans cette page, nous pouvons selectionner les participants souhaités pour afficher une comparaison de leurs performances par splits")
    
    # Prendre tous les participants
    participants = df_final["participant"].unique() 

    # Nous utilisons ici l'outil multiselect de streamlit (comme pour le dataframe), qui contrairement à selectbox accepte plusieurs données, parfait pour cette utilisation
    selected_participants = st.multiselect(
        "Sélectionnez les participants à afficher",
        options=participants,
        default=participants[:3] # Pour éviter de tous les afficher, nous en afficherons uniquement 3
    )
    # grace a la selection nous pouvons créer un nouveau dataframe pour le graphique, voir sa composition dans ChartProcessor 
    filtered_df = df_final[df_final["participant"].isin(selected_participants)]
    chart = ChartProcessor(filtered_df)
    fig = chart.plot_performance_splits()
    st.plotly_chart(fig)

# Logique pour afficher la page choisie
if page == "Accueil":
    page_accueil()
elif page == "Comparaison par sexe":
    page_compare_sexe_means()
elif page == "Manipulation des data":
    dataframe()
elif page == "Performance par participant":
    splitperf()