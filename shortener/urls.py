from django.urls import path, include

from . import views

app_name = "shortener"

urlpatterns = [
    path("", views.Home.as_view(), name='home'),
    path("signup", views.Signup.as_view(), name='signup'),
    path('login', views.Login.as_view() ,name='login'),
    path('logout', views.Logout ,name='logout'),
    path('createUrl', views.CreateShortUrl.as_view(), name="createUrl"),
    # path("a/<slug:short_url>", views.R)
    path("s/<slug:short_url>", views.Redirect, name="redirect"),
]
