from django import forms


# Modéle pour le formulaire de recherche dans le suivi
class ContrainteSearchForm(forms.Form):
    contrainte = forms.CharField(label="Contrainte", required=False)
    sem_contrainte = forms.CharField(label="Semaine contrainte", required=False)
