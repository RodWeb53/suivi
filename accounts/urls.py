from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('liste_users/', views.get_users, name='liste_users'),
    path('update/<int:id>', views.update_user, name='update'),
    path('delete/<int:id>', views.delete_user, name='delete'),
]
