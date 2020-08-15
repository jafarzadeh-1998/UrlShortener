from django.urls import path, include

from . import views

app_name = "shortener"

urlpatterns = [
    path("", views.Home.as_view(), name='home'),
    path("signup", views.Signup.as_view(), name='signup'),
    path('login', views.Login.as_view() ,name='login'),
]
