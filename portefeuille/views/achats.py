from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.urls import reverse
from django.utils.http import urlencode
from ..forms.achats import AchatsSearchForm
import json


def achats(request):
    """
        Fonction pour afficher les données avec les filtres de la page de recherche achats
    """
    # Ouverture du fichier JSON
    with open('data.json', 'r') as f:
        data = json.load(f)
    # Vérification des données qui sont envoyer depuis la page

    if request.method == "POST":
        form = AchatsSearchForm(request.POST)
        # Si les données sont valide on passe les informations dans l'url
        if form.is_valid():
            base_url = reverse('achats')
            query_string = urlencode(form.cleaned_data)
            url = '{}?{}'.format(base_url, query_string)
            return redirect(url)

    else:
        # Chargement du formulaire
        form = AchatsSearchForm()
        base_form = request.GET.get("base_forme", 0)
        commande_form = request.GET.get("commande_choix", 0)
        fournisseur_form = request.GET.get("fournisseur", 0)
        num_commande_form = request.GET.get("num_commande", 0)
        date_commande_form = request.GET.get("date_commande", 0)

        if base_form == 0:
            # Chargement des données de recherche dans le formulaire de base avec des valeurs à 0
            form.fields['base_forme'].initial = base_form
            form.fields['commande_choix'].initial = commande_form
            form.fields['fournisseur'].initial = fournisseur_form
            form.fields['num_commande'].initial = num_commande_form
            form.fields['date_commande'].initial = date_commande_form

            # Envoie des données globale avec des besoins d'achats
            data = data
        else:
            # création d'une variable pour récupérer les éléments en fonction du filtre
            liste = []
            # Chargement des valeurs du filtre dans la page de base
            form.fields['base_forme'].initial = base_form
            form.fields['commande_choix'].initial = commande_form
            form.fields['fournisseur'].initial = fournisseur_form
            form.fields['num_commande'].initial = num_commande_form
            form.fields['date_commande'].initial = date_commande_form

            # S'il y a un filtre sur les lignes sans commandes d'achats
            if commande_form == "1":
                for client in data:
                    if client['nomenclatures']:
                        for nomenclature in client['nomenclatures']:
                            for ligne in nomenclature:
                                if ligne["stock_a_date"] < 0 and ligne["produit_gp"] is False:
                                    if ligne["liste_cde_ha"]:
                                        pass
                                    else:
                                        if client in liste:
                                            break
                                        else:
                                            liste.append(client)
                                            break

                data = liste
            # S'il y a un filtre sur le code fournisseur
            elif fournisseur_form != "0":
                for client in data:
                    if client['nomenclatures']:
                        for nomenclature in client['nomenclatures']:
                            for ligne in nomenclature:
                                if ligne["stock_a_date"] < 0 and ligne["produit_gp"] is False:
                                    if ligne["liste_cde_ha"]:
                                        for ligne_cde in ligne["liste_cde_ha"]:
                                            if ligne_cde["num_fournisseur"] == int(fournisseur_form):
                                                if client in liste:
                                                    break
                                                else:
                                                    liste.append(client)
                                                    break

                data = liste
            # S'il y a un filtre sur le numéro de commande
            elif num_commande_form != "0":
                for client in data:
                    if client['nomenclatures']:
                        for nomenclature in client['nomenclatures']:
                            for ligne in nomenclature:
                                if ligne["stock_a_date"] < 0 and ligne["produit_gp"] is False:
                                    if ligne["liste_cde_ha"]:
                                        for ligne_cde in ligne["liste_cde_ha"]:
                                            if ligne_cde["num_commande"] == int(num_commande_form):
                                                if client in liste:
                                                    break
                                                else:
                                                    liste.append(client)
                                                    break

                data = liste
            # S'il y a un filtre sur la date de livraison
            elif date_commande_form != "0":
                for client in data:
                    if client['nomenclatures']:
                        for nomenclature in client['nomenclatures']:
                            for ligne in nomenclature:
                                if ligne["stock_a_date"] < 0 and ligne["produit_gp"] is False:
                                    if ligne["liste_cde_ha"]:
                                        for ligne_cde in ligne["liste_cde_ha"]:
                                            if ligne_cde["date_liv_accorde"] <= date_commande_form:
                                                if client in liste:
                                                    break
                                                else:
                                                    liste.append(client)
                                                    break

                data = liste

    # Gestion de la pagination des pages
    paginator = Paginator(data, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'portefeuille/achats.html', context={"page_obj": page_obj, "form": form})
