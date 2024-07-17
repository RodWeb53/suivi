from django import forms


# Modéle pour le formulaire de recherche dans le suivi
class StockSearchForm(forms.Form):
    client = forms.CharField(label="Numéro du client", required=True)
    commande = forms.CharField(label="Numéro de commande", required=True)
    CHOICES = [
        ('0', 'Toutes dates'),
        ('1', 'Date départ'),
        ('2', 'Date arrivée'),
    ]
    date_choix = forms.ChoiceField(
        label="Choix du type de départ",
        widget=forms.RadioSelect,
        choices=CHOICES,
    )
    date_demande = forms.CharField(label="Date de fin", required=False)
    ferme = forms.CharField(label="Ferme", required=False)
