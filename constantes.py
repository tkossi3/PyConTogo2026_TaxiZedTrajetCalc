# Tarifs plus des infos à propos des prix des courses
TARIFS = {
    "1":{
        "nom": "Zemidjan (Moto)",
        "base": 150,
        "prix_km": 75,
        "majoration": 0.15
    },
    "2":{
        "nom": "Taxis (Voiture)",
        "base": 200,
        "prix_km": 100,
        "majoration": 0.25
    }
}

# Heures de pointes
HEURES_POINTES = [
    (7.0, 8.75),
    (11.75, 13.0),
    (17.0, 19.0)
]

# Fichier json pour le sauvegarde des historiques de courses
FICHIER_HISTORIQUE = "historiqueTrajets.json"