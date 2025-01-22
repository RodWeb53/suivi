from django import forms


# Modéle pour le formulaire de recherche dans le suivi
class AchatsSearchForm(forms.Form):
    base_forme = forms.CharField(label="base", required=False)
    fournisseur = forms.CharField(label="fournisseur", required=False)
    num_commande = forms.CharField(label="num_commande", required=False)
    date_commande = forms.CharField(label="date_commande", required=False)
    date_debut_commande = forms.CharField(label="date_debut_commande", required=False)
    produit = forms.CharField(label="produit", required=False)
    famille_produit = forms.CharField(label="famille_produit", required=False)
    CHOICES = [
        ('0', 'Pas de recherche'),
        ('1', 'Pas de commande'),
    ]
    commande_choix = forms.ChoiceField(
        label="Choix de recherche",
        widget=forms.RadioSelect,
        choices=CHOICES,
    )
    CHOICES_FAMILLE = [
        ('0', 'Complet'),
        ('1', 'Sans traitement'),
        ('2', 'Seulement traitement'),
    ]
    famille_choix = forms.ChoiceField(
        label="Choix famille",
        widget=forms.RadioSelect,
        choices=CHOICES_FAMILLE,
    )
