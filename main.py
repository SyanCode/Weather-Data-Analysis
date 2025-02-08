import csv

# 1. INTRODUCTION
# Ce programme analyse des relevés météorologiques à partir de fichiers CSV.
# Il réalise différentes requêtes statistiques et comparatives sur les données.

# 2. IMPORT DE FICHIER CSV EN PYTHON
def load_data(file_path):
    """Charge les données du fichier CSV en filtrant les valeurs invalides et en effectuant les conversions nécessaires."""
    liste_releves = []
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            if 'mq' in (row['ff'], row['t'], row['u'], row['rr1']):
                continue  # Ignore les enregistrements incomplets
            
            liste_releves.append({
                'id': int(row['numer_sta']),
                'vitesse_vent': float(row['ff']) * 3.6,  # Conversion m/s -> km/h
                'temperature': float(row['t']) - 273.15,  # Conversion Kelvin -> Celsius
                'humidite': int(row['u']),
                'precipitations': float(row['rr1'])
            })
    return liste_releves

# 3. REQUÊTES

## 3.1 - STATISTIQUES
def temperature_min(liste_releves):
    return min(releve['temperature'] for releve in liste_releves)

def station_vitesse_max(liste_releves):
    return max(liste_releves, key=lambda x: x['vitesse_vent'])['id']

def humidite_moyenne(liste_releves):
    return sum(releve['humidite'] for releve in liste_releves) / len(liste_releves)

def precipitation_moyenne(liste_releves):
    stations_filtrees = [r['precipitations'] for r in liste_releves if 60000 <= r['id'] <= 69999]
    return sum(stations_filtrees) / len(stations_filtrees) if stations_filtrees else 0

## 3.2 - RECHERCHE D'UNE STATION
def rechercher_station_logarithmique(liste_releves, id_station):
    id_station = int(id_station)
    liste_releves.sort(key=lambda x: x['id'])
    gauche, droite = 0, len(liste_releves) - 1
    while gauche <= droite:
        milieu = (gauche + droite) // 2
        if liste_releves[milieu]['id'] == id_station:
            return [releve for releve in liste_releves if releve['id'] == id_station]
        elif liste_releves[milieu]['id'] < id_station:
            gauche = milieu + 1
        else:
            droite = milieu - 1
    return []

## 3.3 - FUSION DE TABLES
def fusionner_tables(fichier_2009, fichier_2019):
    data_2009 = load_data(fichier_2009)
    data_2019 = load_data(fichier_2019)
    
    fusion = []
    relevés_2009 = {releve['id']: releve['temperature'] for releve in data_2009}
    relevés_2019 = {releve['id']: releve['temperature'] for releve in data_2019}
    
    for id_station in relevés_2009.keys() & relevés_2019.keys():
        fusion.append({
            'id': id_station,
            't2009': relevés_2009[id_station],
            't2019': relevés_2019[id_station]
        })
    
    return fusion

def mois_plus_chaud(fusion):
    t2009_moy = sum(f['t2009'] for f in fusion) / len(fusion)
    t2019_moy = sum(f['t2019'] for f in fusion) / len(fusion)
    return "Février 2019" if t2019_moy > t2009_moy else "Février 2009"

# Exemple d'utilisation
liste_releves = load_data('meteo_2019.csv')
print("Question 1: Modifications appliquées pour les champs requis.")
print(f"Question 2: Température minimale en février 2019: {temperature_min(liste_releves):.2f}°C")
print(f"Question 3: ID de la station avec la vitesse de vent maximale en février 2019: {station_vitesse_max(liste_releves)}")
print(f"Question 4: Humidité moyenne en février 2019: {humidite_moyenne(liste_releves):.1f}%")
print(f"Question 5: Précipitations moyennes pour les stations entre 60000 et 69999 en février 2019: {precipitation_moyenne(liste_releves)}mm")

fusion = fusionner_tables('meteo_2009.csv', 'meteo_2019.csv')
print(f"Question 9 et 10: Le mois le plus chaud entre février 2009 et 2019: {mois_plus_chaud(fusion)}")
