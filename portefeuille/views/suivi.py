from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
import json

from ..models import Portefeuille, Stock, BaseOF, BaseOperation, BaseNomenclature, StockGobal, CommandeFournisseur

# Passage du dictionnaire stocks PF dans une variable triée par code produit
stocks = Stock.objects.all().order_by('-produit').values()
# Passage du dictionnaire des OF dans une variable triée par code produit
ofs = BaseOF.objects.all().order_by('num_produit', 'nbre_operation', 'num_of').values()
# Passage du dictionnaire des opérations dans une variable avec un trie sur le N° OF et ensuite le numéro de phase
liste_operations = BaseOperation.objects.all().order_by('num_of_operation', 'num_phase_operation').values()
# Passage du dictionnaire des nomenclatures dans une variable avec un trie sur le N° OF
liste_nomenclatures = BaseNomenclature.objects.all().order_by('num_of_nomenclature').values()
# Passage du dictionnaire du stock global dans une variable avec un trie sur le N° de produit
liste_stocks = StockGobal.objects.all().order_by('produit_global').values()
# Passage du dictionnaire des commande HA dans une variable sans trie
liste_cde_ha = CommandeFournisseur.objects.all().values()


@staff_member_required
def suivi_list(request):
    """Fonction pour analyser chaque ligne de commande client

    """
    # Passage du dictionnaire des lignes de commande dans une variable triées par la date de livraison
    suivi_listing = Portefeuille.objects.all().order_by('date_arrivee').values()
    # Passage du dictionnaire stocks PF dans une variable triée par code produit

    # Boucle pour lire chaque ligne de commande
    for suivi_list in suivi_listing:
        # print("passage dans la boucle d'analyse", suivi_list)
        # Création d'un tableau vide afin de mettre les OF nécéssaire à la réalisation d'une ligne de commande
        suivi_list['of'] = []
        # Création d'un tableau vide afin de mettre les nomenclatures nécéssaire à la réalisation d'une ligne de cde
        suivi_list['nomenclatures'] = []
        # Création d'un tableau vide afin de mettre les opérations nécéssaire à la réalisation d'une ligne de commande
        suivi_list['operations'] = []
        # Création d'une variable avec affectation de la qté en commande (sera déduite après consommation d'un OF)
        suivi_list['qte_cde_recalcule'] = suivi_list['quantite_cde']

        # --- Lancement de la fonction 'ligne_cde_en_stock' pour lire chaque ligne de stock afin
        # de déduire les stocks de la quantité à réaliser ---
        stock_cde = ligne_cde_en_stock(suivi_list['produit'], suivi_list['quantite_cde'])
        # Affectation sur la ligne de commande des stocks, livrable, qte manquante pour ligne de commande
        suivi_list['stock'] = stock_cde["stock_pour_cde"]
        suivi_list['livrable'] = stock_cde["livrable"]
        suivi_list['qte_cde_recalcule'] = stock_cde["qte_cde_recalcule"]

        # --- Si la ligne de commande n'a pas assez de stock
        # on lance la fonction 'of_pour_ligne_cde' recherche un OF pour couvrir le besoin ---
        if suivi_list['qte_cde_recalcule'] > 0:
            # Lancement de la fonction
            liste_ofs = of_pour_ligne_cde(suivi_list['produit'], suivi_list['qte_cde_recalcule'])
            # Affectation sur la ligne de commande la qté restant à 0
            suivi_list['qte_cde_recalcule'] = liste_ofs["quantite_a_produire"]
            # boucle pour mettre les N° OF affecté sur la ligne de commande
            for besoin_of in liste_ofs['liste_of']:
                suivi_list['of'].append(besoin_of)

        # --- Si un of est affecté à la ligne de commande
        # on lance la fonction 'operation_pour_of' récupération des opérations de l'OF ---
        if suivi_list['of'] is not None:
            for of in suivi_list['of']:
                listes_operations = operation_pour_of(int(of["of"]))
                suivi_list['operations'].append(listes_operations)

        # --- S'il y a une opération d'OF sur la ligne de commande
        # on lance la fonction 'nomenclature_operation' pour récupérer la liste de nomenclature ---
        if suivi_list['operations'] is not None:
            for of in suivi_list['of']:
                liste_ope = []
                for ope_ofs in suivi_list['operations']:
                    for ope in ope_ofs:
                        if int(ope["num_of_operation"]) == int(of["of"]):
                            liste_ope.append(ope)
                liste_nomenclature = nomenclature_operation(of, liste_ope)
                suivi_list['nomenclatures'].append(liste_nomenclature)

        # --- S'il y a une ligne de nomenclature sur la ligne de commande
        # on lance la fonction 'stock_ligne_nomenclature' pour récupérer les stocks ou les cde HA ---
        if suivi_list['nomenclatures'] is not None:
            for nomenclatures in suivi_list['nomenclatures']:
                for ligne_nomenclature in nomenclatures:
                    if ligne_nomenclature["produit_gp"]:
                        retour_of = stock_so(ligne_nomenclature)
                        if retour_of == "stock":
                            pass
                        else:
                            liste_operations_so = []
                            liste_of_so = []
                            for of_besoin_so in suivi_list['of']:
                                liste_of_so.append(of_besoin_so["of"])
                            for of_so in retour_of["liste_of"]:
                                if of_so["of"] in liste_of_so:
                                    pass
                                else:
                                    suivi_list['of'].append(of_so)
                                    listes_operations = operation_pour_of(of_so["of"])
                                    suivi_list['operations'].append(listes_operations)
                                    liste_operations_so.append(listes_operations)
                            if liste_operations_so is not None:
                                for operations_so in liste_operations_so:
                                    liste_nomenclature = nomenclature_operation(of_so, operations_so)

                                suivi_list['nomenclatures'].append(liste_nomenclature)

                    else:
                        stock_ligne_nomenclature(ligne_nomenclature)

    # Création du fichier JSON suite à l'analyse complète
    data = []
    for data_list in suivi_listing:
        data.append(data_list)
    data_json = json.dumps(data, indent=4, sort_keys=True, default=str)
    file_json = open("data.json", "w")
    file_json.write(data_json)
    file_json.close()

    return render(request, 'portefeuille/maj_suivi.html', context={"suivi_lists": suivi_listing})


def ligne_cde_en_stock(produit, quantite_cde):
    # --- Fonction pour connaitre les stocks de PF et déduire la qté à la commande ---
    for stock in stocks:
        #  si le produit correspond au produit de la ligne de commande
        if produit == stock["produit"]:
            # Affectation de la quantité en stock sur la ligne de commande
            stock_pour_cde = int(stock["stock_recalcule"])

            # condition qui vérifie si la qté en stock est supérieur ou égale à la quantité en commande
            if stock_pour_cde >= quantite_cde:
                # si la quantité est supérieur ou égale alors ajout du Tag livrable = 1
                # et déduction dans le stock de la quantité en commande
                livrable = 1
                stock["stock_recalcule"] = stock_pour_cde - quantite_cde
                qte_cde_recalcule = 0
                break
            # Sinon condition pour vérifier si la quantité est supérieur à 0 et inférieur à la quantité en commande
            elif stock_pour_cde < quantite_cde and quantite_cde > 0:
                # Si la qté est inférieur déduction du stock afin de connaitre la qté à produire
                qte_cde_recalcule = quantite_cde - stock_pour_cde
                # Affectation à la ligne de stock la quantité à 0
                stock["stock_recalcule"] = 0
                # affectation de la ligne livrable à 0
                livrable = 0
                break
    return {"livrable": livrable, "qte_cde_recalcule": qte_cde_recalcule, "stock_pour_cde": stock_pour_cde}


def of_pour_ligne_cde(produit_cde, quantite_cde):
    # print("la qté en commande est de : ", quantite_cde)
    liste_of = []
    quantite_a_produire = quantite_cde
    # --- Boucle pour connaitre les N° OF sur les lignes de commandes
    if quantite_a_produire > 0:
        for of in ofs:
            if of['num_produit'] == produit_cde and of['quantite'] > 0:
                if quantite_a_produire <= of['quantite']:
                    # Affectaion du N° d'OF dans le tableau des OF
                    liste_of.append({"of": of['num_of'],
                                     "qte": quantite_a_produire,
                                     "produit": of['num_produit'],
                                     "qte_base": of["qte_base"],
                                     "statut_of": of["statut_of"]})
                    reste = of['quantite'] - quantite_a_produire
                    # Affection sur la ligne de commande la qté à 0 pour la qté restante à produire
                    of['quantite'] = reste
                    # Affectation sur la ligne d'OF le nombre de pièces restante disponible
                    quantite_a_produire = 0
                    break
                elif quantite_a_produire > of['quantite']:
                    # Calcul du nombre de pièces restante à produire pour la ligne de commande
                    quantite_a_produire = quantite_a_produire - of['quantite']
                    liste_of.append({"of": of['num_of'],
                                     "qte": of['quantite'],
                                     "produit": of['num_produit'],
                                     "qte_base": of["qte_base"],
                                     "statut_of": of["statut_of"]})

                    # Affectation de la quantité 0 sur l'OF afin de ne plus l'utiliser
                    of['quantite'] = 0

    return {"liste_of": liste_of, "quantite_a_produire": quantite_a_produire}


def of_pour_ligne_so(produit_cde, quantite_cde):
    # print("la qté en commande est de : ", quantite_cde)
    liste_of = []
    quantite_a_produire = quantite_cde
    # --- Boucle pour connaitre les N° OF sur les lignes de commandes
    if quantite_a_produire > 0:
        for of in ofs:
            if of['num_produit'] == produit_cde and of['quantite'] > 0:
                if quantite_a_produire <= of['quantite']:
                    # Affectaion du N° d'OF dans le tableau des OF
                    liste_of.append({"of": of['num_of'],
                                     "qte": quantite_a_produire,
                                     "produit": of['num_produit'],
                                     "qte_base": of["qte_base"],
                                     "statut_of": of["statut_of"]})
                    reste = of['quantite'] - quantite_a_produire
                    # Affection sur la ligne de commande la qté à 0 pour la qté restante à produire
                    of['quantite'] = reste
                    # Affectation sur la ligne d'OF le nombre de pièces restante disponible
                    quantite_a_produire = 0
                    break
                elif quantite_a_produire > of['quantite']:
                    # Calcul du nombre de pièces restante à produire pour la ligne de commande
                    quantite_a_produire = quantite_a_produire - of['quantite']
                    liste_of.append({"of": of['num_of'],
                                     "qte": of['quantite'],
                                     "produit": of['num_produit'],
                                     "qte_base": of["qte_base"],
                                     "statut_of": of["statut_of"]})

                    # Affectation de la quantité 0 sur l'OF afin de ne plus l'utiliser
                    of['quantite'] = 0

    return {"liste_of": liste_of, "quantite_a_produire": quantite_a_produire}


def operation_pour_of(of):
    # Boucle pour récupérer les opérations d'un OF et ajouter la liste dans "opérations" de suivi_list
    liste_opes = liste_operations.filter(num_of_operation=of).values()
    # liste_opes = liste_operations.filter(num_of_operation=of).values()
    listes_operations_of = []
    for operation in liste_opes:
        listes_operations_of.append(operation)
    return listes_operations_of


def nomenclature_operation(of, operations_of):
    liste_nomenc = liste_nomenclatures.filter(num_of_nomenclature=of["of"]).values()
    liste_nomenclature = []
    for operations in operations_of:
        for nomenclature in liste_nomenc:
            if nomenclature['num_unique_nomenclature'] == operations['num_unique']:
                if nomenclature['produit_gp']:
                    coef = nomenclature['quantite_besoin'] / of['qte_base']
                    besoin_ligne = of['qte'] * coef
                    nomenclature['quantite_besoin'] = besoin_ligne
                    liste_nomenclature.append(nomenclature)
                else:
                    liste_nomenclature.append(nomenclature)
    return liste_nomenclature


def stock_ligne_nomenclature(ligne_nomenclature):
    # Boucle aller chercher le stock global du produit de nomenclature

    stock_produit_nomen = liste_stocks.get(produit_global=ligne_nomenclature['num_produit'])
    ligne_nomenclature.update({'stock_global': stock_produit_nomen['stock_global']})
    liste_stock_nomenclature = liste_nomenclatures.filter(num_produit=ligne_nomenclature['num_produit'])
    date_besoin = ligne_nomenclature['date_conso']
    qte_besoin_a_date = 0
    for besoin_a_date in liste_stock_nomenclature:
        # Si le stock est supérieur au besoin à date on arrête
        # pas besoin de trouver les lignes de commandes HA
        if besoin_a_date['date_conso'] <= date_besoin:
            qte_besoin_a_date += besoin_a_date['quantite_besoin']
        stock_a_date = ligne_nomenclature['stock_global'] - qte_besoin_a_date
    ligne_nomenclature.update({'stock_a_date': stock_a_date})
    # Si le stock est inférieur au stock à date alors on recherche les lignes de commande HA
    if ligne_nomenclature['stock_a_date'] < 0:
        ligne_cd_ha = liste_cde_ha.all().filter(
            num_produit_achat=ligne_nomenclature['num_produit']).order_by('date_liv_accorde').values()
        liste_cde = []
        for ligne in ligne_cd_ha:
            besoin = abs(ligne_nomenclature['stock_a_date'])
            # Si la première ligne de commande HA couvre le besoin on arrête
            if ligne['quantite_commande'] >= besoin:
                liste_cde.append(ligne)
                break
            # Sinon on affiche toutes les lignes de commande HA
            elif ligne['quantite_commande'] < besoin:
                liste_cde.append(ligne)
        ligne_nomenclature.update({'liste_cde_ha': liste_cde})
    # Ajout
    return 'fait'


def stock_so(ligne_nomenclature):
    # --- Fonction pour connaitre les stocks de SO ---
    for stock_so in liste_stocks:
        if stock_so["produit_global"] == ligne_nomenclature['num_produit']:
            ligne_nomenclature.update({'stock_global': stock_so['stock_recalcule_global']})
            if stock_so['stock_recalcule_global'] >= ligne_nomenclature["quantite_besoin"]:
                stock_so['stock_recalcule_global'] = stock_so['stock_recalcule_global'] - ligne_nomenclature["quantite_besoin"]
                ligne_nomenclature.update({'stock_a_date': stock_so['stock_recalcule_global']})
                return "stock"
            else:
                quantite_manquante_so = stock_so['stock_recalcule_global'] - ligne_nomenclature["quantite_besoin"]
                quantite_manquante_OF = ligne_nomenclature["quantite_besoin"] - stock_so['stock_recalcule_global']
                ligne_nomenclature.update({'stock_a_date': quantite_manquante_so})
                stock_so['stock_recalcule_global'] = 0
                # of_a_realiser = of_pour_ligne_cde(ligne_nomenclature['num_produit'], quantite_manquante_OF)
                of_a_realiser = of_pour_ligne_so(ligne_nomenclature['num_produit'], quantite_manquante_OF)

                return of_a_realiser
