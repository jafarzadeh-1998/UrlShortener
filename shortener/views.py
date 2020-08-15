from django.shortcuts import render, HttpResponseRedirect, reverse
from django.views import generic
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin

from . import forms, models

class Home(generic.TemplateView):
    template_name = "shortener/home.html"

class Signup(generic.FormView):
    template_name = "shortener/signup.html"
    form_class = forms.SignupForm
    success_url = "/"

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
    success_url = "/"

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

class CreateShortUrl(LoginRequiredMixin, generic.FormView):
    login_url = '/login'
    template_name = "shortener/createUrl.html"
    form_class = forms.UrlForm
    success_url = "/"

    def form_valid(self, form):
        url = models.URL(creator=self.request.user,
                         full_url=form.cleaned_data['full_url'],
                         short_url=form.cleaned_data['short_url'],
                         suggested_url=form.cleaned_data['suggested_url'])
        url.save()
        return super().form_valid(form)

def Redirect(request, short_url):
    try:
        service = models.URL.objects.get(short_url=short_url)
        url = service.full_url
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'http://{}'.format(url)
        return HttpResponseRedirect(url)
    except Exception as e:
        return HttpResponseRedirect('/')