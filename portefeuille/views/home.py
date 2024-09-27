from django.shortcuts import render
import datetime
from dateutil.relativedelta import relativedelta
import os.path
import time
import json


def index(request):
    date_fichier = datetime.datetime.strptime(time.ctime(os.path.getmtime("data.json")), "%a %b %d %H:%M:%S %Y")
    date_jour = datetime.datetime.today()
    date_jour_complete = date_jour.strftime("%Y-%m-%d")
    date_mois_plus_un = datetime.date.today() + relativedelta(months=+1)
    date_mois_plus_deux = datetime.date.today() + relativedelta(months=+2)
    date_mois_plus_trois = datetime.date.today() + relativedelta(months=+3)
    mois_recherche = date_jour.strftime("%Y-%m")
    mois_recherche_plus_un = date_mois_plus_un.strftime("%Y-%m")
    mois_recherche_plus_deux = date_mois_plus_deux.strftime("%Y-%m")
    mois_recherche_plus_trois = date_mois_plus_trois.strftime("%Y-%m")

    # Ouverture du fichier JSON
    with open('data.json', 'r') as f:
        data = json.load(f)
        montant_retard = 0
        das_retard = []
        das_mois = []
        date_analyse = ""
        das_mois_suivant = []
        das_mois_suivant_deux = []
        das_mois_suivant_trois = []
        montant_encours = 0
        montant_mois_suivant = 0
        montant_mois_suivant_deux = 0
        montant_mois_suivant_trois = 0
        for ligne in data:
            date_analyse = ligne["date_arrivee"][0:10]
            if ligne["date_arrivee"][0:10] < date_jour_complete:
                montant_retard = montant_retard + int(ligne["montant_total"])
                das_retard.append(ligne)
            elif ligne["date_arrivee"][0:7] == mois_recherche:
                montant_encours = montant_encours + int(ligne["montant_total"])
                das_mois.append(ligne)
            elif ligne["date_arrivee"][0:7] == mois_recherche_plus_un:
                montant_mois_suivant = montant_mois_suivant + int(ligne["montant_total"])
                das_mois_suivant.append(ligne)
            elif ligne["date_arrivee"][0:7] == mois_recherche_plus_deux:
                das_mois_suivant_deux.append(ligne)
                montant_mois_suivant_deux = montant_mois_suivant_deux + int(ligne["montant_total"])
            elif ligne["date_arrivee"][0:7] == mois_recherche_plus_trois:
                montant_mois_suivant_trois = montant_mois_suivant_trois + int(ligne["montant_total"])
                das_mois_suivant_trois.append(ligne)

        montant_das_retard = montant_das(das_retard)
        montant_das_mois = montant_das(das_mois)
        montant_das_mois_suivant = montant_das(das_mois_suivant)
        montant_das_mois_suivant_deux = montant_das(das_mois_suivant_deux)
        montant_das_mois_suivant_trois = montant_das(das_mois_suivant_trois)

    return render(request, "portefeuille/home.html", locals())


def montant_das(liste_cde_das):
    ligne_montant_das = {"fe": 0, "me": 0, "be": 0, "ma": 0, "ae": 0, "de": 0, "en": 0, "div": 0}
    for ligne_das in liste_cde_das:
        if ligne_das['das'] == "FE":
            ligne_montant_das["fe"] = ligne_montant_das["fe"] + int(ligne_das["montant_total"])
        elif ligne_das['das'] == "ME":
            ligne_montant_das["me"] = ligne_montant_das["me"] + int(ligne_das["montant_total"])
        elif ligne_das['das'] == "BE":
            ligne_montant_das["be"] = ligne_montant_das["be"] + int(ligne_das["montant_total"])
        elif ligne_das['das'] == "MA":
            ligne_montant_das["ma"] = ligne_montant_das["ma"] + int(ligne_das["montant_total"])
        elif ligne_das['das'] == "AE":
            ligne_montant_das["ae"] = ligne_montant_das["ae"] + int(ligne_das["montant_total"])
        elif ligne_das['das'] == "DE":
            ligne_montant_das["de"] = ligne_montant_das["de"] + int(ligne_das["montant_total"])
        elif ligne_das['das'] == "EN":
            ligne_montant_das["en"] = ligne_montant_das["en"] + int(ligne_das["montant_total"])
        elif ligne_das['das'] == "DIV":
            ligne_montant_das["div"] = ligne_montant_das["div"] + int(ligne_das["montant_total"])
    return ligne_montant_das
