from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.urls import reverse
from django.utils.http import urlencode
from ..forms.recherche import ClientSearchForm
import json


def portefeuille(request):
    """
        Fonction pour afficher les données avec les filtres de la page de suivi
    """
    # Ouverture du fichier JSON
    with open('data.json', 'r') as f:
        data = json.load(f)
    # Vérification des données qui sont envoyer depuis la page
    if request.method == "POST":
        form = ClientSearchForm(request.POST)
        # Si les données sont valide on passe les informations dans l'url
        if form.is_valid():
            base_url = reverse('suivi')
            query_string = urlencode(form.cleaned_data)
            url = '{}?{}'.format(base_url, query_string)
            return redirect(url)
    else:
        # Chargement du formulaire
        form = ClientSearchForm()
        client_form = request.GET.get("client", 0)
        produit_form = request.GET.get("produit", 0)
        commande_form = request.GET.get("commande", 0)
        ref_interne_form = request.GET.get("ref_interne", 0)
        montant_form = request.GET.get("montant", 0)
        if client_form == 0 and produit_form == 0 and commande_form == 0 and montant_form == 0 and \
                ref_interne_form == 0:
            # Chargement des données de recherche dans le formulaire de base avec des valeurs à 0
            form.fields['client'].initial = client_form
            form.fields['produit'].initial = produit_form
            form.fields['commande'].initial = commande_form
            form.fields['ref_interne'].initial = ref_interne_form
            form.fields['montant'].initial = montant_form
            # Envoie des données globale s'il n'y a pas de filtre sur le client et le produit
            data = data
        else:
            # création d'une variable pour récupérer les éléments en fonction du filtre
            liste_filtre = []
            # Chargement des valeurs du filtre dans la page de base
            form.fields['client'].initial = client_form
            form.fields['produit'].initial = produit_form
            form.fields['commande'].initial = commande_form
            form.fields['ref_interne'].initial = ref_interne_form
            form.fields['montant'].initial = montant_form
            # S'il y a un filtre sur le client, le produit, la commande et sur le montant
            if client_form != "0" and \
                    produit_form != "0" and \
                    commande_form != "0" and \
                    ref_interne_form != "0" and \
                    montant_form != "0":

                for client in data:
                    if client["num_client"] == int(client_form) and \
                            client["produit"] == int(produit_form) and \
                            client["num_cde"] == int(commande_form) and \
                            client["ref_interne"] == str(ref_interne_form) and \
                            client["montant_total"] >= float(montant_form):

                        liste_filtre.append(client)

                data = liste_filtre

            # S'il y a un filtre sur le client, le produit, la commande et pas le montant
            elif client_form != "0" and \
                    produit_form != "0" and \
                    commande_form != "0" and \
                    ref_interne_form != "0" and \
                    montant_form == "0":

                for client in data:
                    if str(ref_interne_form) is not None:
                        if client["num_client"] == int(client_form) and \
                                client["produit"] == int(produit_form) and \
                                client["ref_interne"] == str(ref_interne_form) and \
                                client["num_cde"] == int(commande_form):

                            liste_filtre.append(client)

                data = liste_filtre

            # S'il y a un filtre sur le client, le produit, le montant et pas la commande
            elif client_form != "0" and \
                    produit_form != "0" and \
                    commande_form == "0" and \
                    montant_form != "0":

                for client in data:
                    if client["num_client"] == int(client_form) and \
                            client["produit"] == int(produit_form) and \
                            client["montant_total"] >= float(montant_form):

                        liste_filtre.append(client)

                data = liste_filtre

            # S'il y a un filtre sur le client, la commande, le montant et pas sur le produit
            elif client_form != "0" and \
                    produit_form == "0" and \
                    commande_form != "0" and \
                    montant_form != "0":

                for client in data:
                    if client["num_client"] == int(client_form) and \
                            client["num_cde"] == int(commande_form) and \
                            client["montant_total"] >= float(montant_form):

                        liste_filtre.append(client)

                data = liste_filtre

            # S'il y a un filtre sur le produit, la commande, le montant et pas sur le client
            elif client_form == "0" and \
                    produit_form != "0" and \
                    commande_form != "0" and \
                    montant_form != "0":

                for client in data:
                    if client["produit"] == int(produit_form) and \
                            client["num_cde"] == int(commande_form) and \
                            client["montant_total"] >= float(montant_form):

                        liste_filtre.append(client)

                data = liste_filtre

            # S'il y a un filtre sur le client, la commande et pas sur le produit, le montant
            elif client_form != "0" and \
                    produit_form == "0" and \
                    commande_form != "0" and \
                    montant_form == "0":

                for client in data:
                    if client["num_client"] == int(client_form) and \
                            client["num_cde"] == int(commande_form):

                        liste_filtre.append(client)

                data = liste_filtre

            # S'il y a un filtre sur le client, le produit, et pas sur le montant, la commande
            elif client_form != "0" and \
                    produit_form != "0" and \
                    commande_form == "0" and \
                    montant_form == "0":

                for client in data:
                    if client["num_client"] == int(client_form) and \
                            client["produit"] == int(produit_form):

                        liste_filtre.append(client)

                data = liste_filtre

            # S'il y a un filtre sur le client, le montant et pas sur le produit, la commande
            elif client_form != "0" and \
                    produit_form == "0" and \
                    commande_form == "0" and \
                    montant_form != "0":

                for client in data:
                    if client["num_client"] == int(client_form) and \
                            client["montant_total"] >= float(montant_form):

                        liste_filtre.append(client)

                data = liste_filtre

            # S'il y a un filtre sur la commande, le produit, et pas sur le montant, le client
            elif client_form == "0" and \
                    produit_form != "0" and \
                    commande_form != "0" and \
                    montant_form == "0":

                for client in data:
                    if client["produit"] == int(produit_form) and \
                            client["num_cde"] == int(commande_form):

                        liste_filtre.append(client)

                data = liste_filtre

            # S'il y a un filtre sur la commande, le montant et pas sur le client, le produit
            elif client_form == "0" and \
                    produit_form == "0" and \
                    commande_form != "0" and \
                    montant_form != "0":

                for client in data:
                    if client["num_cde"] == int(commande_form) and \
                            client["montant_total"] >= float(montant_form):

                        liste_filtre.append(client)

                data = liste_filtre

            # S'il y a un filtre sur le produit, le montant et pas sur le client, la commande
            elif client_form == "0" and \
                    produit_form != "0" and \
                    commande_form == "0" and \
                    montant_form != "0":

                for client in data:
                    if client["produit"] == int(produit_form) and \
                            client["montant_total"] >= float(montant_form):

                        liste_filtre.append(client)

                data = liste_filtre

            # S'il y a un filtre sur le client seulement
            elif client_form != "0" and \
                    produit_form == "0" and \
                    commande_form == "0" and \
                    montant_form == "0":

                for client in data:
                    if client["num_client"] == int(client_form):

                        liste_filtre.append(client)

                data = liste_filtre

            # S'il y a un filtre sur la commande seulement
            elif client_form == "0" and \
                    produit_form == "0" and \
                    commande_form != "0" and \
                    montant_form == "0":

                for client in data:
                    if client["num_cde"] == int(commande_form):

                        liste_filtre.append(client)

                data = liste_filtre

            # S'il y a un filtre sur le produit seulement
            elif client_form == "0" and \
                    produit_form != "0" and \
                    commande_form == "0" and \
                    montant_form == "0":

                for client in data:
                    if client["produit"] == int(produit_form):

                        liste_filtre.append(client)

                data = liste_filtre

            # S'il y a un filtre sur le montant seulement
            if client_form == "0" and \
                    produit_form == "0" and \
                    commande_form == "0" and \
                    montant_form != "0":

                for client in data:
                    if client["montant_total"] >= float(montant_form):

                        liste_filtre.append(client)

                data = liste_filtre

            # S'il y a un filtre sur la ref interne
            if client_form == "0" and \
                    produit_form == "0" and \
                    commande_form == "0" and \
                    ref_interne_form != "0" and \
                    montant_form == "0":

                for client in data:

                    if client["ref_interne"] is not None:
                        if str(ref_interne_form) in client["ref_interne"]:

                            liste_filtre.append(client)

                data = liste_filtre

    # Gestion de la pagination des pages
    paginator = Paginator(data, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'portefeuille/suivi.html', context={"page_obj": page_obj, "form": form})
