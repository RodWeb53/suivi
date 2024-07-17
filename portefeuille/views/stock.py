from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.urls import reverse
from django.utils.http import urlencode
from ..forms.recherche_stock import StockSearchForm
import json


def stock(request):
    """
        Fonction pour afficher les données avec les filtres de la page de suivi
    """
    # Ouverture du fichier JSON
    with open('data.json', 'r') as f:
        data = json.load(f)
    # Vérification des données qui sont envoyer depuis la page
    if request.method == "POST":
        form = StockSearchForm(request.POST)
        # Si les données sont valide on passe les informations dans l'url
        if form.is_valid():
            base_url = reverse('stock')
            query_string = urlencode(form.cleaned_data)
            url = '{}?{}'.format(base_url, query_string)
            return redirect(url)
    else:
        # Chargement du formulaire
        form = StockSearchForm()
        client_form = request.GET.get("client", 0)
        commande_form = request.GET.get("commande", 0)
        date_choix_form = request.GET.get("date_choix", 0)
        date_demande_form = request.GET.get("date_demande", 0)
        ferme_form = request.GET.get("ferme", "")

        if client_form == 0 and commande_form == 0 and date_demande_form == 0 and date_choix_form == 0 and ferme_form == "":
            print("passage dans le if")
            # Chargement des données de recherche dans le formulaire de base avec des valeurs à 0
            liste_filtre_base = []
            form.fields['client'].initial = client_form
            form.fields['commande'].initial = commande_form
            form.fields['date_choix'].initial = date_choix_form
            form.fields['date_demande'].initial = date_demande_form
            form.fields['ferme'].initial = ferme_form

            # Envoie des données globale s'il n'y a pas de filtre sur le client et le produit
            for client in data:
                if client["livrable"] == 1:
                    liste_filtre_base.append(client)
            data = liste_filtre_base
        else:
            print("Passage dans le else")
            # création d'une variable pour récupérer les éléments en fonction du filtre
            liste_filtre = []
            # Chargement des valeurs du filtre dans la page de base
            form.fields['client'].initial = client_form
            form.fields['commande'].initial = commande_form
            form.fields['date_choix'].initial = date_choix_form
            form.fields['date_demande'].initial = date_demande_form
            form.fields['ferme'].initial = ferme_form
            # S'il y a aucun filtre pour un rechargement
            if client_form == "0" and \
                    commande_form == "0" and \
                    date_choix_form == "0" and \
                    ferme_form == "":

                for client in data:
                    if client["livrable"] == 1:

                        liste_filtre.append(client)

                data = liste_filtre
            # S'il y a un filtre seulement sur ferme
            elif client_form == "0" and \
                    commande_form == "0" and \
                    date_choix_form == "0" and \
                    ferme_form != "":

                for client in data:
                    if client["livrable"] == 1 and client["ferme_prev"] == ferme_form.upper():

                        liste_filtre.append(client)

                data = liste_filtre

            # S'il y a un filtre sur ferme et sur le client
            elif client_form != "0" and \
                    commande_form == "0" and \
                    date_choix_form == "0" and \
                    ferme_form != "":

                for client in data:
                    if client["livrable"] == 1 and \
                            client["ferme_prev"] == ferme_form.upper() and \
                            client["num_client"] == int(client_form):

                        liste_filtre.append(client)

                data = liste_filtre

            # S'il y a un filtre sur le client seulement
            elif client_form != "0" and \
                    commande_form == "0" and \
                    date_choix_form == "0" and \
                    ferme_form == "":

                for client in data:
                    if client["livrable"] == 1 and \
                            client["num_client"] == int(client_form):

                        liste_filtre.append(client)

                data = liste_filtre

            # S'il y a un filtre sur ferme, sur le client, le numero de cde
            elif client_form != "0" and \
                    commande_form != "0" and \
                    date_choix_form == "0" and \
                    ferme_form != "":

                for client in data:
                    if client["livrable"] == 1 and \
                            client["ferme_prev"] == ferme_form.upper() and \
                            client["num_cde"] == int(commande_form) and \
                            client["num_client"] == int(client_form):

                        liste_filtre.append(client)

                data = liste_filtre

            # S'il y a un filtre sur le client, le numero de cde
            elif client_form != "0" and \
                    commande_form != "0" and \
                    date_choix_form == "0" and \
                    ferme_form == "":

                for client in data:
                    if client["livrable"] == 1 and \
                            client["num_cde"] == int(commande_form) and \
                            client["num_client"] == int(client_form):

                        liste_filtre.append(client)

                data = liste_filtre

            # S'il y a un filtre sur ferme, sur le client, le numero de cde, la date départ
            elif client_form != "0" and \
                    commande_form != "0" and \
                    date_choix_form == "1" and \
                    ferme_form != "" and \
                    date_demande_form != "0":

                for client in data:
                    if client["livrable"] == 1 and \
                            client["ferme_prev"] == ferme_form.upper() and \
                            client["num_cde"] == int(commande_form) and \
                            client["date_depart"] <= date_demande_form and \
                            client["num_client"] == int(client_form):

                        liste_filtre.append(client)

                data = liste_filtre

            # S'il y a un filtre sur le client, le numero de cde, la date départ
            elif client_form != "0" and \
                    commande_form != "0" and \
                    date_choix_form == "1" and \
                    ferme_form == "" and \
                    date_demande_form != "0":

                for client in data:
                    if client["livrable"] == 1 and \
                            client["num_cde"] == int(commande_form) and \
                            client["date_depart"] <= date_demande_form and \
                            client["num_client"] == int(client_form):

                        liste_filtre.append(client)

                data = liste_filtre

            # S'il y a un filtre sur le client, la date départ
            elif client_form != "0" and \
                    commande_form == "0" and \
                    date_choix_form == "1" and \
                    ferme_form == "" and \
                    date_demande_form != "0":

                for client in data:
                    if client["livrable"] == 1 and \
                            client["date_depart"] <= date_demande_form and \
                            client["num_client"] == int(client_form):

                        liste_filtre.append(client)

                data = liste_filtre

            # S'il y a un filtre sur le client, la date départ ferme
            elif client_form != "0" and \
                    commande_form == "0" and \
                    date_choix_form == "1" and \
                    ferme_form != "" and \
                    date_demande_form != "0":

                for client in data:
                    if client["livrable"] == 1 and \
                            client["date_depart"] <= date_demande_form and \
                            client["ferme_prev"] == ferme_form.upper() and \
                            client["num_client"] == int(client_form):

                        liste_filtre.append(client)

                data = liste_filtre

            # S'il y a un filtre sur ferme, sur le client, le numero de cde, la date arrivé
            elif client_form != "0" and \
                    commande_form != "0" and \
                    date_choix_form == "2" and \
                    ferme_form != "" and \
                    date_demande_form != "0":

                for client in data:
                    if client["livrable"] == 1 and \
                            client["ferme_prev"] == ferme_form.upper() and \
                            client["num_cde"] == int(commande_form) and \
                            client["date_arrivee"] <= date_demande_form and \
                            client["num_client"] == int(client_form):

                        liste_filtre.append(client)

                data = liste_filtre

            # S'il y a un filtre sur le client, le numero de cde, la date arrivée
            elif client_form != "0" and \
                    commande_form != "0" and \
                    date_choix_form == "2" and \
                    ferme_form == "" and \
                    date_demande_form != "0":
                print("passage dans la boucle")

                for client in data:
                    if client["livrable"] == 1 and \
                            client["num_cde"] == int(commande_form) and \
                            client["date_arrivee"] <= date_demande_form and \
                            client["num_client"] == int(client_form):

                        liste_filtre.append(client)

                data = liste_filtre

            # S'il y a un filtre sur le client, la date arrivée
            elif client_form != "0" and \
                    commande_form == "0" and \
                    date_choix_form == "2" and \
                    ferme_form == "" and \
                    date_demande_form != "0":

                for client in data:
                    if client["livrable"] == 1 and \
                            client["date_arrivee"] <= date_demande_form and \
                            client["num_client"] == int(client_form):

                        liste_filtre.append(client)

                data = liste_filtre

            # S'il y a un filtre sur le client, la date arrivée, ferme
            elif client_form != "0" and \
                    commande_form == "0" and \
                    date_choix_form == "2" and \
                    ferme_form != "" and \
                    date_demande_form != "0":

                for client in data:
                    if client["livrable"] == 1 and \
                            client["ferme_prev"] == ferme_form.upper() and \
                            client["date_arrivee"] <= date_demande_form and \
                            client["num_client"] == int(client_form):

                        liste_filtre.append(client)

                data = liste_filtre

            # S'il y a un filtre sur la date arrivée, ferme et cde
            elif client_form == "0" and \
                    commande_form != "0" and \
                    date_choix_form == "2" and \
                    ferme_form != "" and \
                    date_demande_form != "0":

                for client in data:
                    if client["livrable"] == 1 and \
                            client["ferme_prev"] == ferme_form.upper() and \
                            client["num_cde"] == int(commande_form) and \
                            client["date_arrivee"] <= date_demande_form:

                        liste_filtre.append(client)

                data = liste_filtre

            # S'il y a un filtre sur la date depart, ferme et cde
            elif client_form == "0" and \
                    commande_form != "0" and \
                    date_choix_form == "1" and \
                    ferme_form != "" and \
                    date_demande_form != "0":

                for client in data:
                    if client["livrable"] == 1 and \
                            client["ferme_prev"] == ferme_form.upper() and \
                            client["num_cde"] == int(commande_form) and \
                            client["date_depart"] <= date_demande_form:

                        liste_filtre.append(client)

                data = liste_filtre

            # S'il y a un filtre sur la date arrivée et cde
            elif client_form == "0" and \
                    commande_form != "0" and \
                    date_choix_form == "2" and \
                    ferme_form == "" and \
                    date_demande_form != "0":

                for client in data:
                    if client["livrable"] == 1 and \
                            client["num_cde"] == int(commande_form) and \
                            client["date_arrivee"] <= date_demande_form:

                        liste_filtre.append(client)

                data = liste_filtre

            # S'il y a un filtre sur la date départ et cde
            elif client_form == "0" and \
                    commande_form != "0" and \
                    date_choix_form == "1" and \
                    ferme_form == "" and \
                    date_demande_form != "0":

                for client in data:
                    if client["livrable"] == 1 and \
                            client["num_cde"] == int(commande_form) and \
                            client["date_depart"] <= date_demande_form:

                        liste_filtre.append(client)

                data = liste_filtre

            # S'il y a un filtre sur la date départ
            elif client_form == "0" and \
                    commande_form == "0" and \
                    date_choix_form == "1" and \
                    ferme_form == "" and \
                    date_demande_form != "0":

                for client in data:
                    if client["livrable"] == 1 and \
                            client["date_depart"] <= date_demande_form:

                        liste_filtre.append(client)

                data = liste_filtre

            # S'il y a un filtre sur la date départ et ferme
            elif client_form == "0" and \
                    commande_form == "0" and \
                    date_choix_form == "1" and \
                    ferme_form != "" and \
                    date_demande_form != "0":

                for client in data:
                    if client["livrable"] == 1 and \
                            client["ferme_prev"] == ferme_form.upper() and \
                            client["date_depart"] <= date_demande_form:

                        liste_filtre.append(client)

                data = liste_filtre

            # S'il y a un filtre sur la date arrivée
            elif client_form == "0" and \
                    commande_form == "0" and \
                    date_choix_form == "2" and \
                    ferme_form == "" and \
                    date_demande_form != "0":

                for client in data:
                    if client["livrable"] == 1 and \
                            client["date_arrivee"] <= date_demande_form:

                        liste_filtre.append(client)

                data = liste_filtre

            # S'il y a un filtre sur la date arrivée et ferme
            elif client_form == "0" and \
                    commande_form == "0" and \
                    date_choix_form == "2" and \
                    ferme_form != "" and \
                    date_demande_form != "0":

                for client in data:
                    if client["livrable"] == 1 and \
                            client["ferme_prev"] == ferme_form.upper() and \
                            client["date_arrivee"] <= date_demande_form:

                        liste_filtre.append(client)

                data = liste_filtre

    # Gestion de la pagination des pages
    paginator = Paginator(data, 30)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'portefeuille/stock.html', context={"page_obj": page_obj, "form": form})
