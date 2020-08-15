from django.shortcuts import render, HttpResponseRedirect, reverse
from django.views import generic
from django.contrib.auth import login, logout

from . import forms, models

class Home(generic.TemplateView):
    template_name = "shortener/home.html"

class Signup(generic.FormView):
    template_name = "shortener/signup.html"
    form_class = forms.SignupForm
    success_url = "/shortener"

    def form_invalid(self, form):
        return super().form_invalid(form)
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.email = form.cleaned_data['email']
        user.save()
        return super().form_valid(form)

class Login(generic.FormView):
    template_name = "shortener/login.html"
    form_class = forms.LoginForm
    success_url = "/shortener"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("shortener:home"))
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.cleaned_data['user'])
        return super().form_valid(form)

def Logout(request):
    if request.user.is_authenticated:
        logout(request)
    return HttpResponseRedirect(reverse('shortener:login'))