from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm
from django.contrib.auth.models import User


# Modèle pour le formulaire de creation User
class NewUserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "username",
            "password1",
            "last_name",
            "first_name",
            "is_active",
            "is_staff",
        ]


class ChangeUserForm(UserChangeForm):
    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "last_name",
            "first_name",
            "is_active",
            "is_staff",
        ]


class ViewUserForm(ModelForm):
    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "last_name",
            "first_name",
            "is_active",
            "is_staff",
        ]
