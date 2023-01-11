from django.urls import path, include
from . import views

# Sukuriame marsrutus
urlpatterns = [
    path('', views.index, name='index')
]