from django.urls import path
from django.contrib.auth import views
import accounts.views as views1

urlpatterns = []

urlpatterns += [
    path('login', views.LoginView.as_view(), name='login'),
    path('register', views1.register, name='register'),
]

