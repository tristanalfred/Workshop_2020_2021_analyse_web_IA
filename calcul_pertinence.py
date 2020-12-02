import csv

#Variables globales
COLONNE_TPS_ESTIME = 4
COLONNE_TPS_PASSE = 3
COLONNE_PERTINENCE = 6
NOMBRE_CATEGORIES_PERTINENCE = 3
CHEMIN_FICHIER = 'C://Users/trist/Desktop/contenu.csv'

COLONNE_TPS_ESTIME = COLONNE_TPS_ESTIME -1
COLONNE_TPS_PASSE = COLONNE_TPS_PASSE -1
COLONNE_PERTINENCE = COLONNE_PERTINENCE -1


#Contenu
contenu_temps_estime = []
contenu_temps_passe = []
header = []
data = []
nombre_ligne = 1


def calcul_pertinence(temps_estime, temps_passe, type_page):
    """
    En fonction des valeurs de temps et du type de page, renvoie un code situé entre 1 et 3
    :param temps_estime:
    :param temps_passe:
    :param type_page:
    :return: 1, 2 ou 3
    """
    temps_estime = int(temps_estime)
    temps_passe = int(temps_passe)
    pourcentage_pertinence = {
        'accueil' : [20, 30, 40],
        'informatif' : [20, 30, 40],
        'formulaire' : [20, 30, 40],
        'article' : [20, 30, 40]
        }

    ecart = (temps_passe - temps_estime) / temps_estime * 100
    if ecart < 0:
        ecart = ecart * -1

    for i in range(NOMBRE_CATEGORIES_PERTINENCE):
        if ecart <= pourcentage_pertinence[type_page][i]:
            return i+1
    return NOMBRE_CATEGORIES_PERTINENCE



#LECTURE
with open(CHEMIN_FICHIER, newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
    header = next(spamreader, None)

    for row in spamreader:
        contenu_temps_estime.append(row[COLONNE_TPS_ESTIME])
        contenu_temps_passe.append(row[COLONNE_TPS_PASSE])
        data.append(row)
        nombre_ligne += 1

    print(data) #Valeur en entrée


#ECRITURE
for row in range(nombre_ligne-1):
    data[row][COLONNE_PERTINENCE] = calcul_pertinence(data[row][COLONNE_TPS_ESTIME], data[row][COLONNE_TPS_PASSE], 'accueil')

print(data) #Valeurs après traitement

data_header = [header, data]
print(data_header) #Contenu du fichier complet avec les entêtes

#Il reste la variable "data" et à l'ajouter à un fichier


# writer = csv.writer(open('contenu.csv', 'wb'))
# writer.writerows(data_header)
