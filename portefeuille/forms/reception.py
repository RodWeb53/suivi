from django import forms


# Modéle pour le formulaire de recherche dans le suivi
class ReceptionSearchForm(forms.Form):
    base_forme = forms.CharField(label="base", required=False)
    fournisseur = forms.CharField(label="fournisseur", required=False)
    num_commande = forms.CharField(label="num_commande", required=False)
    num_produit = forms.CharField(label="num_produit", required=False)
    date_commande = forms.CharField(label="date_commande", required=False)
    date_today = forms.CharField(label="date_today", required=False)
    CHOICES = [
        ('0', 'Lignes en attentes'),
    ]
    commande_choix = forms.ChoiceField(
        label="Choix de recherche",
        widget=forms.RadioSelect,
        choices=CHOICES,
    )
