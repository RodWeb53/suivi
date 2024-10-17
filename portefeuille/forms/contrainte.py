from django import forms


# Modéle pour le formulaire de recherche dans le suivi
class ContrainteSearchForm(forms.Form):
    CHOICES = [
        ('0', 'Complet'),
        ('1', 'Opération restante'),
        ('2', 'Sans opérations'),
    ]
    affichage_choix = forms.ChoiceField(
        label="Choix d'affichage",
        widget=forms.RadioSelect,
        choices=CHOICES,
    )
    contrainte = forms.CharField(label="Contrainte", required=False)
    sem_contrainte = forms.CharField(label="Semaine contrainte", required=False)
