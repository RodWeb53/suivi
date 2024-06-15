from django.contrib.auth.forms import AuthenticationForm
from .forms.user_creation import NewUserCreateForm, ChangeUserForm, ViewUserForm

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User


def login_user(request):
    """ Méthodes pour la gestion du login"""
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.info(request, "Identifiant ou mot de passe incorrect")

    form = AuthenticationForm()
    return render(request, "accounts/login.html", {"form": form})


def logout_user(request):
    """ Méthodes pour la déconnexion"""
    logout(request)
    return redirect("home")


def register_user(request):
    """ Methodes pour la création d'un utilisateur"""
    if request.method == 'POST':
        form = NewUserCreateForm(request.POST)

        if form.is_valid():
            print("formaulaire non valide")
            form.save()
            return redirect("home")

    else:
        form = NewUserCreateForm()
        print("formaulaire non valide base")

    return render(request, "accounts/register.html", {"form": form})


def get_users(request):
    """ Méthodes pour le chargement des utilisateurs"""
    liste_users = User.objects.all()
    return render(request, "accounts/liste_users.html", {"liste_users": liste_users})


def update_user(request, id):
    """ Méthodes pour la mise à jour d'un user"""
    if request.method == "POST":
        user_updated = User.objects.get(pk=id)
        form = ChangeUserForm(request.POST, instance=user_updated)
        if form.is_valid():
            form.save()
            return redirect("accounts:liste_users")
    else:
        user_updated = User.objects.get(pk=id)
        form = ChangeUserForm(instance=user_updated)

    return render(request, "accounts/update.html", {"form": form})


def delete_user(request, id):
    """ Méthodes pour la suppression d'un utilisateur"""
    """ Méthodes pour la mise à jour d'un user"""
    if request.method == "POST":
        user_updated = User.objects.get(pk=id)
        user_updated.delete()
        return redirect("accounts:liste_users")
    else:
        user_updated = User.objects.get(pk=id)
        form = ViewUserForm(instance=user_updated)

    return render(request, "accounts/delete.html", {"form": form})
