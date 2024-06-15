from django.urls import path
from .views import home, suivi, update_base, portefeuille

urlpatterns = [
    # url de la page d'accueuil
    path("", home.index, name="home"),
    # Urls suivi
    path("suivi", portefeuille.portefeuille, name="suivi"),
    # urls pour l'administration
    # url pour la mise à jour des fichiers dans la base de données
    path("maj_suivi", suivi.suivi_list, name="maj_suivi"),
    # rl pour lancer l'analyse du portefeuille et créer un fichier Json
    path("mise_a_jour", update_base.mise_a_jour_base, name="mise_a_jour"),
]
