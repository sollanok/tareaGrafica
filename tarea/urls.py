from django.urls import path
from .import views

urlpatterns = [
    path('', views.index, name = 'index'),

    path('datos', views.datos, name = 'datos'),

    path('bubblegraph', views.bubblegraph, name = 'bubble graph'),
]