from django.shortcuts import render
from django.views import generic

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

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

    def form_valid(self, form):
        print("FORM VALIDATED")
        return super().form_valid(form)