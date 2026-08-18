from fonction import *
import datetime

historique = chargerHistorique()
print("Bienvenue dans le Calculateur de Trajet Lomé (Zemidjan/Taxi)")

while True:
    print("\n <<< NOUVEAU TRAJET >>>")
    print("1. Zemidjan (Taxi-moto)")
    print("2. Taxi (Voiture)")
    print("3. Historiques")
    print("4. Quitter")
    
    choix = input("Choisissez le moyen de transport : ").strip()
    
    if choix == "4":
        break
    if choix == "3":
        afficherHistorique(historique)
        continue
    if choix not in TARIFS:
        print("[Erreur] Choix invalide. Veuillez saisir 1 ou 2.")
        continue
    
    while True:
        try:
            distance = float(input("Entrez la distance du trajet en km : "))
            if distance > 0:
                break
            print("[Erreur] La distance doit etre supérieure à 0.")
        except ValueError:
            print("[Erreur] Veuillez entrer une valeur numérique valide.")
    
    # 
    print("\n\tOption Heure :")
    print("1. Utiliser l'heure actuelle du système")
    print("2. Entrer l'heure manuellement")
    heureChoix = input("Entrer votre choix : ").strip()
    
    dateStr = None
    heureDecimale = None
    if heureChoix == "1":
        maintenant = datetime.datetime.now()
        heureDecimale = maintenant.hour + (maintenant.minute / 60.0)
        dateStr = maintenant.strftime("%d/%m/%Y")
        print(f"# Heure du système détectée : {maintenant.strftime('%H:%M')}")
    else:
        dateStr = input("Entrez la date (JJ/MM/AAAA) [Entrée pour aujourd'hui] : ").strip()
        if not dateStr:
            dateStr = datetime.date.today().strftime("%d/%m/%Y")
        while heureDecimale is None:
            heureView = input("Enntrez l'heure au format HH:MM (ex: 07:30) : ").strip()
            heureDecimale = convertirHeureEnDecimal(heureView)
            if heureDecimale is None:
                print("[Erreur] Format d'heure invalide. Utilisez le format HH:MM.")
        
    resultat = calculerPrixTrajet(choix, distance, heureDecimale, dateStr)
    afficherFacture(resultat)
    
    # Ajout du trajet à l'historique
    historique.append(resultat)
    
    # 
    sauvergarderHistorique(historique)
    


print("\nMerci d'avoir utilisé notre Apk ! À bientôt.")