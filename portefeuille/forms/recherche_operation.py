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
    type_machine = forms.CharField(label="Code Poste / Machine", required=False)
