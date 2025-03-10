from django import forms


# Modéle pour le formulaire de recherche dans le suivi
class OperationkSearchForm(forms.Form):
    client = forms.CharField(label="Numéro du client", required=True)
    CHOICES = [
        ('1', 'Poste'),
        ('2', 'Machine'),
    ]
    machine_choix = forms.ChoiceField(
        label="Choix de recherche",
        widget=forms.RadioSelect,
        choices=CHOICES,
    )
    CHOICES_LANCE = [
        ('0', 'Tout'),
        ('1', 'Lancé'),
        ('2', 'Suggéré'),
    ]
    lance_choix = forms.ChoiceField(
        label="Choix de recherche",
        widget=forms.RadioSelect,
        choices=CHOICES_LANCE,
    )
    type_machine = forms.CharField(label="Code Poste / Machine", required=False)
    date_recherche_fin = forms.CharField(label="date recherche fin", required=False)
    code_produit = forms.CharField(label="Code produit", required=False)
