# urls.py
from django.urls import path
from .views import (
    HomeView, RegistroView, CustomLoginView, CustomLogoutView, PerfilView)



app_name = 'security'

urlpatterns = [
    
    path('', HomeView.as_view(), name='home'), 
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', RegistroView.as_view(), name='register'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('perfil/', PerfilView.as_view(), name='perfil'),
]

