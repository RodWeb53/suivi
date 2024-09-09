from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.urls import reverse
from django.utils.http import urlencode
from ..forms.contrainte import ContrainteSearchForm
import json


def contrainte(request):
    """
        Fonction pour afficher les données avec les filtres de la page de recherche opération
    """
    # Ouverture du fichier JSON
    with open('data.json', 'r') as f:
        data = json.load(f)
    # Vérification des données qui sont envoyer depuis la page
    if request.method == "POST":
        form = ContrainteSearchForm(request.POST)
        # Si les données sont valide on passe les informations dans l'url
        if form.is_valid():
            base_url = reverse('contrainte')
            query_string = urlencode(form.cleaned_data)
            url = '{}?{}'.format(base_url, query_string)
            return redirect(url)
    else:
        # Chargement du formulaire
        form = ContrainteSearchForm()
        contrainte_form = request.GET.get("contrainte", 0)
        sem_contrainte_form = request.GET.get("sem_contrainte", 0)

        if contrainte_form == 0:
            # Chargement des données de recherche dans le formulaire de base avec des valeurs à 0
            form.fields['contrainte'].initial = contrainte_form
            form.fields['sem_contrainte'].initial = sem_contrainte_form
            # Envoie des données globale
            data = data
        else:
            # création d'une variable pour récupérer les éléments en fonction du filtre
            liste_filtre = []
            # Chargement des valeurs du filtre dans la page de base
            form.fields['contrainte'].initial = contrainte_form
            form.fields['sem_contrainte'].initial = sem_contrainte_form
            # S'il y a un filtre sur la contrainte
            if contrainte_form != "0" and sem_contrainte_form == "0":

                for client in data:
                    if client['of']:
                        for recherche in client['of']:
                            if recherche["contrainte"] == contrainte_form.upper():
                                liste_filtre.append(client)

                data = liste_filtre
            # S'il y a un filtre sur la semaine
            elif contrainte_form == "0" and int(sem_contrainte_form) != 0:

                for client in data:
                    if client['of']:
                        for recherche in client['of']:
                            if int(recherche["sem_contrainte"]) == int(sem_contrainte_form):
                                liste_filtre.append(client)

                data = liste_filtre
            # S'il y a un filtre sur la semaine et la contrainte
            elif contrainte_form != "0" and int(sem_contrainte_form) != 0:

                for client in data:
                    if client['of']:
                        for recherche in client['of']:
                            if int(recherche["sem_contrainte"]) == int(sem_contrainte_form) and \
                                    recherche["contrainte"] == contrainte_form.upper():
                                liste_filtre.append(client)

                data = liste_filtre

    # Gestion de la pagination des pages
    paginator = Paginator(data, 15)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'portefeuille/contrainte.html', context={"page_obj": page_obj, "form": form})


def list_operation(request):
    return render(request, 'portefeuille/operations.html')
