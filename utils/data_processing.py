import os
import json
import pandas as pd

# Cette partie du projet est un prétexte pour approfondir notre compréhension de la programmation orientée objet, car nous aurions pu importer directement un dataframe complet
# Nous récupérons simplement la récupération de fichier du projet pour en faire une classe nomée DataProcessor que nous appelerons dans app.py

# Catégorisation des sexes (arbitraire)
sexe_participants = {
    'Maxime': 'Homme', 'Célestin': 'Homme', 'Julien': 'Homme', 'Neve': 'Femme',
    'Merle': 'Femme', 'Léonore': 'Femme', 'Valérie': 'Femme', 'Amaury': 'Homme',
    'Thomas': 'Homme', 'Jerome': 'Homme', 'Corentin': 'Homme', 'Dominique': 'Femme',
    'Usama': 'Homme', 'Noé': 'Homme', 'Jacqueline': 'Femme', 'Emilien': 'Homme',
    'Eric': 'Homme', 'Edouard': 'Homme', 'Baptiste': 'Homme', 'Loïs': 'Homme',
    'Alice': 'Femme', 'Ivan': 'Homme', 'Lison': 'Femme', 'Charlotte': 'Femme',
    'Nancy': 'Femme', 'Eloïse': 'Femme', 'Julie': 'Femme', 'Hervé': 'Homme'
}

class DataProcessor:
    def __init__(self, dossier_json):
        self.dossier_json = dossier_json
        self.dataframes = []

    def charger_donnees(self):
        for fichier in os.listdir(self.dossier_json):
            path_fichier = os.path.join(self.dossier_json, fichier)
            
            with open(path_fichier, 'r', encoding='utf-8') as f:
                data = json.loads(f.read())
            
            df = pd.json_normalize(
                data, 
                record_path=['results', 'participants']
            )
            
            for i, row in enumerate(df['splits']):
                for j, split in enumerate(row, 1):
                    
                    # A la différence du dataframe original, ici nous appelons toutes les colonnes du JSON pour avoir le document complet

                    df.loc[i, f'Temps_500m_{j}'] = split['split_time']
                    df.loc[i, f'Cadence_500m_{j}'] = split['split_stroke_rate']
                    df.loc[i, f'Nombre_coups_500m_{j}'] = split['split_stroke_count']
                    df.loc[i, f'Pace_moyen_500m_{j}'] = split['split_avg_pace']
                    df.loc[i, f'Calories_500m_{j}'] = split['split_calories']
                    df.loc[i, f'Distance_500m_{j}'] = split['split_distance']
                    df.loc[i, f'Drag_factor_500m_{j}'] = split['split_drag_factor']
                    df.loc[i, f'Calories_cumulees_500m_{j}'] = split['split_running_calories']
                    df.loc[i, f'Distance_cumulee_500m_{j}'] = split['split_running_distance']
                    df.loc[i, f'Temps_cumule_500m_{j}'] = split['split_running_time']
                    df.loc[i, f'Type_split_500m_{j}'] = split['split_type']
            

            self.dataframes.append(df)


    def add_gender_column(self, df):
        # Pour ajouter la colonne "sexe" nous réutilisons le code du notebook principal
        df['sexe'] = df['participant'].map(sexe_participants)
        return df

    def concatener_donnees(self):
        # la boucle retourne un DataFrame vide si aucun fichier n'est chargé, utile pendant le développement
        if self.dataframes:

            df_final = pd.concat(self.dataframes, ignore_index=True)
            
            # ici une autre différence majeure avec le dataframe des questions, 
            # nous supprimons toutes les colonnes vides ainsi que la colonne de splits (qui ne consiste qu'en une suite de strings illisibles)

            df_final = df_final.dropna(axis=1, how='all')
            df_final = df_final.drop(columns=['splits'])
            df_final = df_final.loc[:, df_final.notna().any(axis=0)]
            return df_final
        else:
            return pd.DataFrame()  

    # enfin cette dernière fonction nous permet d'appeler le dataframe en une seule ligne (pratique dans app.py)

    def obtenir_dataframe(self):
        self.charger_donnees()
        df_final = self.concatener_donnees()
        df_final = self.add_gender_column(df_final)
        
        return df_final