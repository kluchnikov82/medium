from django.urls import path

from . import views

urlpatterns = []

urlpatterns += [
    path('guess', views.GetGuess, name='guess'),
    path('guess_medium', views.GetGuessesMedium, name='guesses-medium'),
]

