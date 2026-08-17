from constantes import HEURES_POINTES, TARIFS


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
def calculerPrixTrajet(typeDeplacement, distance, heureDecimale):
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
    
    print("\n" + "<"*19 + ">"*19)
    print("|         FACTURE DU TRAJET          |")
    print("<"*19 + ">"*19)
    print(f"| Moyen de transport :   {resultat['moyen']}    |")
    print(f"| Distance           :   {resultat['distance']} km     |")
    print(f"| Heure départ       :   {heureFomatee}       |")
    print(f"| Heure pointe       :   {statutPointe}   |")
    print(f"| Prix exact         :   {resultat['prixTotal']:.2f} FCFA|")
    print("-" * 38)
    print(f"| Prix à payer       :   {int(resultat['prixArrondi'])} FCFA   |")
    print("<"*19 + ">"*19)

