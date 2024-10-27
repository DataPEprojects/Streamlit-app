import plotly.express as px
import pandas as pd

# chart_processing.py sert à regrouper en une seule classe les différents graphiques utilisés dans app.py
# Cela permet une main page beaucoup plus épurée 

# Pour des graphiques interractifs nous avons fait le choix de la library plotly

class ChartProcessor:
    def __init__(self, df):
        self.df = df

    def compare_gender_means(self, selected_column):
        
        # Ici nous réutilisons le travail ayant été fait dans le notebook principal pour plot facilement une comparaison par sexe
        
        mean_values = self.df.groupby('sexe')[selected_column].mean().reset_index()
        fig = px.bar(
            mean_values,
            x="sexe",
            y=selected_column,
            title=f"Moyenne de {selected_column} par sexe",
            labels={"sexe": "Sexe", selected_column: f"Moyenne de {selected_column}"},
            color="sexe",
            # cette ligne n'est pas nécessaire mais facilite la compréhension rapide du graph
            color_discrete_map={"Homme": "blue", "Femme": "pink"}
        )

        fig.update_layout(xaxis_title="Sexe", yaxis_title=f"Moyenne de {selected_column}")

        return fig
    

    def plot_performance_splits(self):
        split_columns = [col for col in self.df.columns if "Temps_500m" in col]
        
    # La méthode melt transforme les colonnes 'Temps_500m_X' (une par portion) en une seule colonne 'Temps_500m'
    # et ajoute une nouvelle colonne 'Split' pour indiquer la portion de 500m associée à chaque valeur de temps.
    # Cela permet de simplifier la visualisation en regroupant toutes les portions de temps dans deux colonnes : 'Split' et 'Temps_500m'.

        df_long = self.df.melt(
            id_vars=["participant"],
            value_vars=split_columns,
            var_name="Split",
            value_name="Temps_500m"
        )
        
        # Enfin nous créons le graphique avec Plotly
        fig = px.line(
            df_long,
            x="Split",
            y="Temps_500m",
            color="participant",
            title="Évolution des temps sur chaque portion de 500m",
            labels={"Split": "Portions de 500m", "Temps_500m": "Temps (s)", "participant": "Participant"}
        )
        
        return fig