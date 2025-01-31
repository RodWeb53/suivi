from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.urls import reverse
from django.utils.http import urlencode
from ..forms.recherche_operation import OperationkSearchForm
import json


def recherche_operation(request):
    """
        Fonction pour afficher les données avec les filtres de la page de recherche opération
    """
    # Ouverture du fichier JSON
    with open('data.json', 'r') as f:
        data = json.load(f)
    # Vérification des données qui sont envoyer depuis la page
    if request.method == "POST":
        form = OperationkSearchForm(request.POST)
        # Si les données sont valide on passe les informations dans l'url
        if form.is_valid():
            base_url = reverse('recherche_operation')
            query_string = urlencode(form.cleaned_data)
            url = '{}?{}'.format(base_url, query_string)
            return redirect(url)
    else:
        # Chargement du formulaire
        form = OperationkSearchForm()
        machine_form = request.GET.get("machine_choix", 0)
        type_machine_form = request.GET.get("type_machine", 0)
        client_form = request.GET.get("client", 0)
        lance_form = request.GET.get("lance_choix", 0)

        if machine_form == 0:
            # Chargement des données de recherche dans le formulaire de base avec des valeurs à 0
            form.fields['client'].initial = client_form
            form.fields['machine_choix'].initial = machine_form
            form.fields['type_machine'].initial = type_machine_form
            form.fields['lance_choix'].initial = lance_form
            # Envoie des données globale
            data = data
        else:
            # création d'une variable pour récupérer les éléments en fonction du filtre
            liste_filtre = []
            # Chargement des valeurs du filtre dans la page de base
            form.fields['client'].initial = client_form
            form.fields['machine_choix'].initial = machine_form
            form.fields['type_machine'].initial = type_machine_form
            form.fields['lance_choix'].initial = lance_form

            # S'il y a un filtre sur le poste et pas sur le client et tout statut OF
            if machine_form == "1" and client_form == "0" and lance_form == "0":

                for client in data:
                    if client['operations']:
                        for recherche in client['operations']:
                            for machine in recherche:
                                if machine["phase"] == type_machine_form.upper() and not machine["solder"]:
                                    if client in liste_filtre:
                                        break
                                    else:
                                        liste_filtre.append(client)

                data = liste_filtre
            # S'il y a un filtre sur le poste et pas sur le client et statut OF est sur Lancé
            if machine_form == "1" and client_form == "0" and lance_form == "1":

                for client in data:
                    if client['operations']:
                        for recherche in client['operations']:
                            for machine in recherche:
                                if machine["phase"] == type_machine_form.upper() and not machine["solder"]:
                                    for of_lancer in client['of']:
                                        if of_lancer['of'] == machine['num_of_operation'] and of_lancer['statut_of'] == 'L':
                                            if client in liste_filtre:
                                                break
                                            else:
                                                liste_filtre.append(client)

                data = liste_filtre
            # S'il y a un filtre sur le poste et le client et tout statut OF
            elif machine_form == "1" and client_form != "0" and lance_form == "0":

                for client in data:
                    if client["num_client"] == int(client_form):
                        if client['operations']:
                            for recherche in client['operations']:
                                for machine in recherche:
                                    if machine["phase"] == type_machine_form.upper() and not machine["solder"]:
                                        if client in liste_filtre:
                                            break
                                        else:
                                            liste_filtre.append(client)

                data = liste_filtre
            # S'il y a un filtre sur le poste et le client et statut OF sur Lancé
            elif machine_form == "1" and client_form != "0" and lance_form == "1":

                for client in data:
                    if client["num_client"] == int(client_form):
                        if client['operations']:
                            for recherche in client['operations']:
                                for machine in recherche:
                                    if machine["phase"] == type_machine_form.upper() and not machine["solder"]:
                                        for of_lancer in client['of']:
                                            if of_lancer['of'] == machine['num_of_operation'] and of_lancer['statut_of'] == 'L':
                                                if client in liste_filtre:
                                                    break
                                                else:
                                                    liste_filtre.append(client)

                data = liste_filtre
            # S'il y a un filtre sur la machine et pas sur le client et tout statut OF
            elif machine_form == "2" and client_form == "0" and lance_form == "0":

                for client in data:
                    if client['operations']:
                        for recherche in client['operations']:
                            for machine in recherche:
                                if machine["machine"] == type_machine_form.upper() and not machine["solder"]:
                                    if client in liste_filtre:
                                        break
                                    else:
                                        liste_filtre.append(client)

                data = liste_filtre
            # S'il y a un filtre sur la machine et pas sur le client et statut OF sur Lancé
            elif machine_form == "2" and client_form == "0" and lance_form == "1":

                for client in data:
                    if client['operations']:
                        for recherche in client['operations']:
                            for machine in recherche:
                                if machine["machine"] == type_machine_form.upper() and not machine["solder"]:
                                    for of_lancer in client['of']:
                                        if of_lancer['of'] == machine['num_of_operation'] and of_lancer['statut_of'] == 'L':
                                            if client in liste_filtre:
                                                break
                                            else:
                                                liste_filtre.append(client)

                data = liste_filtre
            # S'il y a un filtre sur la machine et sur le client et tout statut OF
            elif machine_form == "2" and client_form != "0" and lance_form == "0":

                for client in data:
                    if client["num_client"] == int(client_form):
                        if client['operations']:
                            for recherche in client['operations']:
                                for machine in recherche:
                                    if machine["machine"] == type_machine_form.upper() and not machine["solder"]:
                                        if client in liste_filtre:
                                            break
                                        else:
                                            liste_filtre.append(client)

                data = liste_filtre
            # S'il y a un filtre sur la machine et sur le client et statut OF Lancé
            elif machine_form == "2" and client_form != "0" and lance_form == "1":

                for client in data:
                    if client["num_client"] == int(client_form):
                        if client['operations']:
                            for recherche in client['operations']:
                                for machine in recherche:
                                    if machine["machine"] == type_machine_form.upper() and not machine["solder"]:
                                        for of_lancer in client['of']:
                                            if of_lancer['of'] == machine['num_of_operation'] and of_lancer['statut_of'] == 'L':
                                                if client in liste_filtre:
                                                    break
                                                else:
                                                    liste_filtre.append(client)

                data = liste_filtre

    # Gestion de la pagination des pages
    paginator = Paginator(data, 15)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'portefeuille/recherche_operation.html', context={"page_obj": page_obj, "form": form})


def list_operation(request):
    return render(request, 'portefeuille/operations.html')
