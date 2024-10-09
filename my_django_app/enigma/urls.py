from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("enigma", views.enigma, name="enigma"),
]
