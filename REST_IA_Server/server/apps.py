from django.apps import AppConfig
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, mean_absolute_error
from sklearn import preprocessing
import pickle


class ServerConfig(AppConfig):
    name = 'server'

    def calcul_pertinence(self, row):
        temps_estime = int(row.pge_estimated_time)
        temps_passe = int(row.vst_time)
        pourcentage_pertinence = {
            1: [20, 30, 40],
            2: [20, 30, 40],
            3: [20, 30, 40],
            4: [20, 30, 40]
        }

        ecart = (temps_passe - temps_estime) / temps_estime * 100
        if ecart < 0:
            ecart = ecart * -1

        for i in range(3):
            if ecart <= pourcentage_pertinence[row.pge_type_id][i]:
                return i + 1
        return 3

    def ready(self):
        print("Début du ready()")

        #Récupération des fichiers
        df_dataset = pd.read_csv(r"C:\Users\trist\Desktop\IA\dataset.csv", sep=";")


        #Ajoute de features
        df_dataset['pertinence_computed'] = df_dataset.apply(self.calcul_pertinence, axis=1)

        features = [
            'app_id',
            'vst_time',
            'pge_estimated_time',
            'pge_type_id'
        ]
        # On n'ajoute pas pertinence_computed car c'est ce que l'on cherche à prédire.
        # J'ajoute pas la colonne pge_name car elle n'a pas d'intérêt pour l'apprentissage de l'IA

        train_features = df_dataset[features]  # X_train

        label = ['pertinence_computed']  # ce que l'on cherche à prédire

        train_label = df_dataset[label]  # y_train


        #découpage du jeux en 2
        train, test = train_test_split(df_dataset, test_size=0.3, random_state=42)

        #RandomForrest
        rf = RandomForestClassifier(n_estimators=100,
                                    max_depth=8,
                                    random_state=0)

        rf.fit(train_features, train_label)  # apprentissage


        #sauvegarde
        filename = 'finalized_model.sav'
        pickle.dump(rf, open(filename, 'wb'))

