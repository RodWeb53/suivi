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
    # Ouverture du fichier de données JSON
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
        date_recherche_fin_form = request.GET.get("date_recherche_fin", 0)
        code_produit_form = request.GET.get("code_produit", 0)

        if machine_form == 0:
            # Chargement des données de recherche dans le formulaire de base avec des valeurs à 0
            form.fields['client'].initial = client_form
            form.fields['machine_choix'].initial = machine_form
            form.fields['type_machine'].initial = type_machine_form
            form.fields['lance_choix'].initial = lance_form
            form.fields['date_recherche_fin'].initial = date_recherche_fin_form
            form.fields['code_produit'].initial = code_produit_form
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
            form.fields['date_recherche_fin'].initial = date_recherche_fin_form
            form.fields['code_produit'].initial = code_produit_form

            # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
            # \\\ Fonction pour recherche par le POSTE  Uniquement                          \\\
            # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

            # Statut OF Tout (Suggéré et lancé)
            if machine_form == "1" and client_form == "0" and lance_form == "0" and date_recherche_fin_form == "0" and code_produit_form == "0":

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
            # Statut OF est sur Lancé
            if machine_form == "1" and client_form == "0" and lance_form == "1" and date_recherche_fin_form == "0" and code_produit_form == "0":

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
            # Statut OF est sur Suggéré
            if machine_form == "1" and client_form == "0" and lance_form == "2" and date_recherche_fin_form == "0" and code_produit_form == "0":

                for client in data:
                    if client['operations']:
                        for recherche in client['operations']:
                            for machine in recherche:
                                if machine["phase"] == type_machine_form.upper() and not machine["solder"]:
                                    for of_lancer in client['of']:
                                        if of_lancer['of'] == machine['num_of_operation'] and of_lancer['statut_of'] == 'G':
                                            if client in liste_filtre:
                                                break
                                            else:
                                                liste_filtre.append(client)

                data = liste_filtre

            # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
            # /// Fonction pour recherche par le POSTE  et sur une de fin de recherche                  \\\
            # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

            # Statut OF Tout (Suggéré et lancé)
            if machine_form == "1" and client_form == "0" and lance_form == "0" and date_recherche_fin_form != "0" and code_produit_form == "0":

                for client in data:
                    if client['operations']:
                        for recherche in client['operations']:
                            for machine in recherche:
                                if machine["phase"] == type_machine_form.upper() and not machine["solder"]:
                                    for of_lancer in client['of']:
                                        if of_lancer['of'] == machine['num_of_operation'] and machine['date_fab'] <= date_recherche_fin_form:
                                            if client in liste_filtre:
                                                break
                                            else:
                                                liste_filtre.append(client)

                data = liste_filtre
            # Statut OF est sur Lancé
            if machine_form == "1" and client_form == "0" and lance_form == "1" and date_recherche_fin_form != "0" and code_produit_form == "0":

                for client in data:
                    if client['operations']:
                        for recherche in client['operations']:
                            for machine in recherche:
                                if machine["phase"] == type_machine_form.upper() and not machine["solder"]:
                                    for of_lancer in client['of']:
                                        if of_lancer['of'] == machine['num_of_operation'] and of_lancer['statut_of'] == 'L' and machine['date_fab'] <= date_recherche_fin_form:
                                            if client in liste_filtre:
                                                break
                                            else:
                                                liste_filtre.append(client)

                data = liste_filtre
            # Statut OF est sur Suggéré
            if machine_form == "1" and client_form == "0" and lance_form == "2" and date_recherche_fin_form != "0" and code_produit_form == "0":

                for client in data:
                    if client['operations']:
                        for recherche in client['operations']:
                            for machine in recherche:
                                if machine["phase"] == type_machine_form.upper() and not machine["solder"]:
                                    for of_lancer in client['of']:
                                        if of_lancer['of'] == machine['num_of_operation'] and of_lancer['statut_of'] == 'G' and machine['date_fab'] <= date_recherche_fin_form:
                                            if client in liste_filtre:
                                                break
                                            else:
                                                liste_filtre.append(client)

                data = liste_filtre

            # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
            # \\\ Fonction pour recherche par le POSTE  AVEC le Client                               \\\
            # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

            # Statut OF Tout (Suggéré et lancé)
            elif machine_form == "1" and client_form != "0" and lance_form == "0" and date_recherche_fin_form == "0" and code_produit_form == "0":

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
            # Statut OF sur Lancé
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
            # Statut OF sur suggéré
            elif machine_form == "1" and client_form != "0" and lance_form == "2":

                for client in data:
                    if client["num_client"] == int(client_form):
                        if client['operations']:
                            for recherche in client['operations']:
                                for machine in recherche:
                                    if machine["phase"] == type_machine_form.upper() and not machine["solder"]:
                                        for of_lancer in client['of']:
                                            if of_lancer['of'] == machine['num_of_operation'] and of_lancer['statut_of'] == 'G':
                                                if client in liste_filtre:
                                                    break
                                                else:
                                                    liste_filtre.append(client)

                data = liste_filtre

            # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
            # \\\ Fonction pour recherche par le POSTE et avec un code produit en nomenclature      \\\
            # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

            # Statut OF Tout (Suggéré et lancé)
            if machine_form == "1" and client_form == "0" and lance_form == "0" and date_recherche_fin_form == "0" and code_produit_form != "0":

                for client in data:
                    if client['operations']:
                        for recherche in client['operations']:
                            for machine in recherche:
                                if machine["phase"] == type_machine_form.upper() and not machine["solder"]:
                                    for of_lancer in client['of']:
                                        if of_lancer['of'] == machine['num_of_operation']:
                                            if client['nomenclatures']:
                                                result = composant_nomenclature(code_produit_form, client['nomenclatures'])
                                                if result == "1":
                                                    if client in liste_filtre:
                                                        break
                                                    else:
                                                        liste_filtre.append(client)

                data = liste_filtre
            # Statut OF est sur Lancé
            if machine_form == "1" and client_form == "0" and lance_form == "1" and date_recherche_fin_form == "0" and code_produit_form != "0":

                for client in data:
                    if client['operations']:
                        for recherche in client['operations']:
                            for machine in recherche:
                                if machine["phase"] == type_machine_form.upper() and not machine["solder"]:
                                    for of_lancer in client['of']:
                                        if of_lancer['of'] == machine['num_of_operation'] and of_lancer['statut_of'] == 'L':
                                            if client['nomenclatures']:
                                                result = composant_nomenclature(code_produit_form, client['nomenclatures'])
                                                if result == "1":
                                                    if client in liste_filtre:
                                                        break
                                                    else:
                                                        liste_filtre.append(client)

                data = liste_filtre
            # Statut OF est sur Suggéré
            if machine_form == "1" and client_form == "0" and lance_form == "2" and date_recherche_fin_form == "0" and code_produit_form != "0":

                for client in data:
                    if client['operations']:
                        for recherche in client['operations']:
                            for machine in recherche:
                                if machine["phase"] == type_machine_form.upper() and not machine["solder"]:
                                    for of_lancer in client['of']:
                                        if of_lancer['of'] == machine['num_of_operation'] and of_lancer['statut_of'] == 'G':
                                            if client['nomenclatures']:
                                                result = composant_nomenclature(code_produit_form, client['nomenclatures'])
                                                if result == "1":
                                                    if client in liste_filtre:
                                                        break
                                                    else:
                                                        liste_filtre.append(client)

                data = liste_filtre

            # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
            # \\\ Fonction pour recherche par le POSTE, avec un code produit en nomenclature et date de fin de recherche       \\\
            # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

            # Statut OF Tout (Suggéré et lancé)
            if machine_form == "1" and client_form == "0" and lance_form == "0" and date_recherche_fin_form != "0" and code_produit_form != "0":

                for client in data:
                    if client['operations']:
                        for recherche in client['operations']:
                            for machine in recherche:
                                if machine["phase"] == type_machine_form.upper() and not machine["solder"]:
                                    for of_lancer in client['of']:
                                        if of_lancer['of'] == machine['num_of_operation'] and machine['date_fab'] <= date_recherche_fin_form:
                                            if client['nomenclatures']:
                                                result = composant_nomenclature(code_produit_form, client['nomenclatures'])
                                                if result == "1":
                                                    if client in liste_filtre:
                                                        break
                                                    else:
                                                        liste_filtre.append(client)

                data = liste_filtre
            # Statut OF est sur Lancé
            if machine_form == "1" and client_form == "0" and lance_form == "1" and date_recherche_fin_form != "0" and code_produit_form != "0":

                for client in data:
                    if client['operations']:
                        for recherche in client['operations']:
                            for machine in recherche:
                                if machine["phase"] == type_machine_form.upper() and not machine["solder"]:
                                    for of_lancer in client['of']:
                                        if of_lancer['of'] == machine['num_of_operation'] and of_lancer['statut_of'] == 'L' and machine['date_fab'] <= date_recherche_fin_form:
                                            if client['nomenclatures']:
                                                result = composant_nomenclature(code_produit_form, client['nomenclatures'])
                                                if result == "1":
                                                    if client in liste_filtre:
                                                        break
                                                    else:
                                                        liste_filtre.append(client)

                data = liste_filtre
            # Statut OF est sur Suggéré
            if machine_form == "1" and client_form == "0" and lance_form == "2" and date_recherche_fin_form != "0" and code_produit_form != "0":

                for client in data:
                    if client['operations']:
                        for recherche in client['operations']:
                            for machine in recherche:
                                if machine["phase"] == type_machine_form.upper() and not machine["solder"]:
                                    for of_lancer in client['of']:
                                        if of_lancer['of'] == machine['num_of_operation'] and of_lancer['statut_of'] == 'G' and machine['date_fab'] <= date_recherche_fin_form:
                                            if client['nomenclatures']:
                                                result = composant_nomenclature(code_produit_form, client['nomenclatures'])
                                                if result == "1":
                                                    if client in liste_filtre:
                                                        break
                                                    else:
                                                        liste_filtre.append(client)

                data = liste_filtre

            # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
            # \\\ Fonction pour recherche par la MACHINE UNIQUEMENT                                                            \\\
            # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

            # Statut OF Tout (Suggéré et lancé)
            elif machine_form == "2" and client_form == "0" and lance_form == "0" and date_recherche_fin_form == "0" and code_produit_form == "0":

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
            # Statut OF sur Lancé
            elif machine_form == "2" and client_form == "0" and lance_form == "1" and date_recherche_fin_form == "0" and code_produit_form == "0":

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
            # Statut OF sur Suggéré
            elif machine_form == "2" and client_form == "0" and lance_form == "2" and date_recherche_fin_form == "0" and code_produit_form == "0":

                for client in data:
                    if client['operations']:
                        for recherche in client['operations']:
                            for machine in recherche:
                                if machine["machine"] == type_machine_form.upper() and not machine["solder"]:
                                    for of_lancer in client['of']:
                                        if of_lancer['of'] == machine['num_of_operation'] and of_lancer['statut_of'] == 'G':
                                            if client in liste_filtre:
                                                break
                                            else:
                                                liste_filtre.append(client)

                data = liste_filtre

            # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
            # \\\ Fonction pour recherche par la MACHINE Et par le produit de nomenclature                                     \\\
            # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

            # Statut OF Tout (Suggéré et lancé)
            elif machine_form == "2" and client_form == "0" and lance_form == "0" and date_recherche_fin_form == "0" and code_produit_form != "0":

                for client in data:
                    if client['operations']:
                        for recherche in client['operations']:
                            for machine in recherche:
                                if machine["machine"] == type_machine_form.upper() and not machine["solder"]:
                                    if client['nomenclatures']:
                                        result = composant_nomenclature(code_produit_form, client['nomenclatures'])
                                        if result == "1":
                                            if client in liste_filtre:
                                                break
                                            else:
                                                liste_filtre.append(client)

                data = liste_filtre
            # Statut OF sur Lancé
            elif machine_form == "2" and client_form == "0" and lance_form == "1" and date_recherche_fin_form == "0" and code_produit_form != "0":

                for client in data:
                    if client['operations']:
                        for recherche in client['operations']:
                            for machine in recherche:
                                if machine["machine"] == type_machine_form.upper() and not machine["solder"]:
                                    for of_lancer in client['of']:
                                        if of_lancer['of'] == machine['num_of_operation'] and of_lancer['statut_of'] == 'L':
                                            if client['nomenclatures']:
                                                result = composant_nomenclature(code_produit_form, client['nomenclatures'])
                                                if result == "1":
                                                    if client in liste_filtre:
                                                        break
                                                    else:
                                                        liste_filtre.append(client)

                data = liste_filtre
            # Statut OF sur Suggéré
            elif machine_form == "2" and client_form == "0" and lance_form == "2" and date_recherche_fin_form == "0" and code_produit_form != "0":

                for client in data:
                    if client['operations']:
                        for recherche in client['operations']:
                            for machine in recherche:
                                if machine["machine"] == type_machine_form.upper() and not machine["solder"]:
                                    for of_lancer in client['of']:
                                        if of_lancer['of'] == machine['num_of_operation'] and of_lancer['statut_of'] == 'G':
                                            if client['nomenclatures']:
                                                result = composant_nomenclature(code_produit_form, client['nomenclatures'])
                                                if result == "1":
                                                    if client in liste_filtre:
                                                        break
                                                    else:
                                                        liste_filtre.append(client)

                data = liste_filtre

            # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
            # \\\ Fonction pour recherche par la MACHINE et Date de fin de recherche                                           \\\
            # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

            # Statut OF Tout (Suggéré et lancé)
            elif machine_form == "2" and client_form == "0" and lance_form == "0" and date_recherche_fin_form != "0" and code_produit_form == "0":

                for client in data:
                    if client['operations']:
                        for recherche in client['operations']:
                            for machine in recherche:
                                if machine["machine"] == type_machine_form.upper() and not machine["solder"]:
                                    for of_lancer in client['of']:
                                        if of_lancer['of'] == machine['num_of_operation'] and machine['date_fab'] <= date_recherche_fin_form:
                                            if client in liste_filtre:
                                                break
                                            else:
                                                liste_filtre.append(client)

                data = liste_filtre
            # Statut OF sur Lancé
            elif machine_form == "2" and client_form == "0" and lance_form == "1" and date_recherche_fin_form != "0" and code_produit_form == "0":

                for client in data:
                    if client['operations']:
                        for recherche in client['operations']:
                            for machine in recherche:
                                if machine["machine"] == type_machine_form.upper() and not machine["solder"]:
                                    for of_lancer in client['of']:
                                        if of_lancer['of'] == machine['num_of_operation'] and of_lancer['statut_of'] == 'L' and machine['date_fab'] <= date_recherche_fin_form:
                                            if client in liste_filtre:
                                                break
                                            else:
                                                liste_filtre.append(client)

                data = liste_filtre
            # Statut OF sur Suggéré
            elif machine_form == "2" and client_form == "0" and lance_form == "2" and date_recherche_fin_form != "0" and code_produit_form == "0":

                for client in data:
                    if client['operations']:
                        for recherche in client['operations']:
                            for machine in recherche:
                                if machine["machine"] == type_machine_form.upper() and not machine["solder"]:
                                    for of_lancer in client['of']:
                                        if of_lancer['of'] == machine['num_of_operation'] and of_lancer['statut_of'] == 'G' and machine['date_fab'] <= date_recherche_fin_form:
                                            if client in liste_filtre:
                                                break
                                            else:
                                                liste_filtre.append(client)

                data = liste_filtre

            # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
            # \\\ Fonction pour recherche par la MACHINE, par le produit de nomenclature et une date de fin                    \\\
            # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

            # Statut OF Tout (Suggéré et lancé)
            elif machine_form == "2" and client_form == "0" and lance_form == "0" and date_recherche_fin_form != "0" and code_produit_form != "0":

                for client in data:
                    if client['operations']:
                        for recherche in client['operations']:
                            for machine in recherche:
                                if machine["machine"] == type_machine_form.upper() and not machine["solder"] and machine['date_fab'] <= date_recherche_fin_form:
                                    if client['nomenclatures']:
                                        result = composant_nomenclature(code_produit_form, client['nomenclatures'])
                                        if result == "1":
                                            if client in liste_filtre:
                                                break
                                            else:
                                                liste_filtre.append(client)

                data = liste_filtre
            # Statut OF sur Lancé
            elif machine_form == "2" and client_form == "0" and lance_form == "1" and date_recherche_fin_form != "0" and code_produit_form != "0":

                for client in data:
                    if client['operations']:
                        for recherche in client['operations']:
                            for machine in recherche:
                                if machine["machine"] == type_machine_form.upper() and not machine["solder"]:
                                    for of_lancer in client['of']:
                                        if of_lancer['of'] == machine['num_of_operation'] and of_lancer['statut_of'] == 'L' and machine['date_fab'] <= date_recherche_fin_form:
                                            if client['nomenclatures']:
                                                result = composant_nomenclature(code_produit_form, client['nomenclatures'])
                                                if result == "1":
                                                    if client in liste_filtre:
                                                        break
                                                    else:
                                                        liste_filtre.append(client)

                data = liste_filtre
            # Statut OF sur Suggéré
            elif machine_form == "2" and client_form == "0" and lance_form == "2" and date_recherche_fin_form != "0" and code_produit_form != "0":

                for client in data:
                    if client['operations']:
                        for recherche in client['operations']:
                            for machine in recherche:
                                if machine["machine"] == type_machine_form.upper() and not machine["solder"]:
                                    for of_lancer in client['of']:
                                        if of_lancer['of'] == machine['num_of_operation'] and of_lancer['statut_of'] == 'G' and machine['date_fab'] <= date_recherche_fin_form:
                                            if client['nomenclatures']:
                                                result = composant_nomenclature(code_produit_form, client['nomenclatures'])
                                                if result == "1":
                                                    if client in liste_filtre:
                                                        break
                                                    else:
                                                        liste_filtre.append(client)

                data = liste_filtre

            # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
            # \\\ Fonction pour recherche par la MACHINE et le CLient seulement                                                \\\
            # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

            # Statut OF Tout (Suggéré et lancé)
            elif machine_form == "2" and client_form != "0" and lance_form == "0" and date_recherche_fin_form == "0" and code_produit_form == "0":

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
            # Statut OF Lancé
            elif machine_form == "2" and client_form != "0" and lance_form == "1" and date_recherche_fin_form == "0" and code_produit_form == "0":

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
            # Statut OF Suggéré
            elif machine_form == "2" and client_form != "0" and lance_form == "2" and date_recherche_fin_form == "0" and code_produit_form == "0":

                for client in data:
                    if client["num_client"] == int(client_form):
                        if client['operations']:
                            for recherche in client['operations']:
                                for machine in recherche:
                                    if machine["machine"] == type_machine_form.upper() and not machine["solder"]:
                                        for of_lancer in client['of']:
                                            if of_lancer['of'] == machine['num_of_operation'] and of_lancer['statut_of'] == 'G':
                                                if client in liste_filtre:
                                                    break
                                                else:
                                                    liste_filtre.append(client)

                data = liste_filtre

    # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    # \\\\  Gestion de la pagination des pages                               \\\\
    # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    paginator = Paginator(data, 15)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'portefeuille/recherche_operation.html', context={"page_obj": page_obj, "form": form})

# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# \\\\ Fonction pour lire les composants dans la nomenclature            \\\\
# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


def composant_nomenclature(code_produit_form, donnees_brut):
    """ Permet à partir des données passées à la fonction
    de savoir si le composant de nomenclature est présent par rapport au cde produit demandé
    Fonction appellé dans les recherche avec code produit

    Args:
        code_produit_form (_type_Integer): _récupération de la valeur à chercher_
        donnees_brut (_type_Tableau): _Si une ligne de gamme est trouvé renvoie des données de la ligne_

    Returns:
        _type_Texte: _Si valeur trouvé = 1 Sinon valeur = 0_
    """
    for donnees in donnees_brut:
        if donnees:
            for lignes_nomeclature in donnees:
                if int(lignes_nomeclature["num_produit"]) == int(code_produit_form):
                    return ("1")
                break
    return ("0")


def list_operation(request):
    return render(request, 'portefeuille/operations.html')
