from constantes import HEURES_POINTES, TARIFS, FICHIER_HISTORIQUE
import os
import json

# 
def convertirHeureEnDecimal(heureStr):
    try:
        heures, minutes = map(int, heureStr.split(":"))
        if 0 <= heures < 24 and 0 <= minutes < 60:
            return heures + (minutes / 60.0)
        return None
    except ValueError:
        return None


# 
def estHeurePointe(heureDecimale):
    for debut, fin in HEURES_POINTES:
        if debut <= heureDecimale <= fin:
            return True
    return False


# 
def arrondirPrix(montant):
    return round(montant / 25.0) * 25


# 
def calculerPrixTrajet(typeDeplacement, distance, heureDecimale, dateStr):
    info = TARIFS[typeDeplacement]
    
    prixBrut = info["base"] + (info["prix_km"] * distance)
    
    # 
    heurePointe = estHeurePointe(heureDecimale)
    if heurePointe:
        tauxMajoration = info["majoration"]
        prixTotal = prixBrut * (1 + tauxMajoration)
    else:
        prixTotal = prixBrut
    
    prixArrondi = arrondirPrix(prixTotal)
    
    return {
        "moyen": info["nom"],
        "distance": distance,
        "dateStr" : dateStr,
        "heureDecimale": heureDecimale,
        "estPointe": heurePointe,
        "prixBrute": prixBrut,
        "prixTotal": prixTotal,
        "prixArrondi": prixArrondi
    }


# 
def afficherFacture(resultat):
    heureEntiere = int(resultat["heureDecimale"])
    minuteEntiere = int(round((resultat["heureDecimale"] - heureEntiere) * 60))
    heureFomatee = f"{heureEntiere:02d}h{minuteEntiere:02d}"
    
    statutPointe = "OUI (20%)" if resultat['moyen'] == "Taxi" else "OUI (15%)" if resultat["estPointe"] else "NON (00%)"
    
    print("\n" + "<"*20 + ">"*20)
    print("|         FACTURE DU TRAJET            |")
    print("<"*20 + ">"*20)
    print(f"| Moyen de transport :  {resultat['moyen']}|")
    print(f"| Distance           :  {resultat['distance']} km         |")
    print(f"| Date du trajet     :  {resultat['dateStr']}     |")
    print(f"| Heure départ       :  {heureFomatee}          |")
    print(f"| Heure pointe       :  {statutPointe}      |")
    print(f"| Prix exact         :  {resultat['prixTotal']:.2f} FCFA    |")
    print("-" * 40)
    print(f"| Prix à payer       :  {int(resultat['prixArrondi'])} FCFA       |")
    print("<"*20 + ">"*20)

def chargerHistorique(nomFichier = FICHIER_HISTORIQUE):
    if not os.path.exists(nomFichier):
        return []

    try:
        with open(nomFichier, "r", encoding="utf-8") as fush:
            return json.load(fush)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Impossible de lire l'historique ({e}).")
        return []


def sauvergarderHistorique(historique, nomFichier = FICHIER_HISTORIQUE):
    try:
        with open(nomFichier, "w", encoding="utf-8") as fush:
            json.dump(historique, fush, ensure_ascii=False, indent=4)
    except IOError as e:
        print(f"Echec de la sauvegarde dans le fichoer json : {e}")
        

def afficherHistorique(historique):
    if not historique:
        return
    
    print("\n" + "#"*80)
    print(f"|               HISTORIQUES DES TRAJETS ({len(historique)} enregistrement(s))                  |")
    print("#"*80)
    for idx, t in enumerate(historique, 1):
        heureEntiere = int(t["heureDecimale"])
        minuteEntiere = int(round((t["heureDecimale"] - heureEntiere) * 60))
        heureStr = f"{heureEntiere:02d}h{minuteEntiere:02d}"
        
        print(f"| {idx:02d}. [{t['dateStr']}] - {t['moyen']} | {t['distance']} km | Heure: {heureStr} | Total: {int(t['prixArrondi'])} FCFA |")
    print("#"*80 + "\n")