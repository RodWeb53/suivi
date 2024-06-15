from django import forms


# Modéle pour le formulaire de recherche dans le suivi
class ClientSearchForm(forms.Form):
    client = forms.CharField(label="Numéro du client", required=True)
    produit = forms.CharField(label="Numéro du produit", required=True)
    commande = forms.CharField(label="Numéro de commande", required=True)
    montant = forms.CharField(label="Montant sup à", required=True)
