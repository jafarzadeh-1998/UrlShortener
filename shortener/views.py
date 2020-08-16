from django.shortcuts import render, HttpResponseRedirect, reverse
from django.views import generic
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.middleware import cache

import datetime

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
        url = models.URL.objects.get(short_url=short_url)
        full_url = url.full_url
        if not full_url.startswith('http://') and not full_url.startswith('https://'):
            full_url = 'http://{}'.format(full_url)
        history = models.UrlHistory.create(models.UrlHistory, url=url, request=request)
        history.save()
        return HttpResponseRedirect(full_url)
    except Exception as e:
        return HttpResponseRedirect('/')
    
class Analyse( generic.FormView):
    template_name = "shortener/showAnalyse.html"
    form_class = forms.ShowResultForm
    login_url = "/login"

    def get_form_kwargs(self):
        kwargs = super(Analyse, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

    def history(self, short_url, duration):
        query = models.UrlHistory.objects.filter(url__short_url=short_url)
        startDate = None        
        today = datetime.date.today()
        if duration == "today":
            return query.filter(pub_date=today)
        elif duration == "day":
            startDate = today - datetime.timedelta(days=1)
        elif duration == "week":
            startDate = today - datetime.timedelta(weeks=1)
        elif duration == "month":
            startDate = today - datetime.timedelta(days=30)
        
        return query.filter(pub_date__gte=startDate).exclude(pub_date=today)

    def getSubQueryWithHashcode(self, query, col):
        result = []
        for q in query.values(col, 'hashcode').distinct():            
            check = False
            for r in result:
                if q[col] == r[col]:
                    r['count'] += 1
                    check = True
                    break
            if not check:
                result.append({col:q[col], 'count':1})
        return result

    def form_valid(self, form):
        self.success_url = self.request.path_info
        query = self.history(form.cleaned_data['short_url'], form.cleaned_data['duration'])
        context = self.get_context_data()
        context["url_total"]  = query.count()
        context["url_agents"]  = query.values('user_agent').annotate(count=Count('user_agent'))
        context["url_browsers"] = query.values('browser').annotate(count=Count('browser'))
                
        context['user_total'] = query.values('hashcode').count()
        context['user_agents'] = self.getSubQueryWithHashcode(query, 'user_agent')
        context['user_browsers'] = self.getSubQueryWithHashcode(query, 'browser')
        return render(request=self.request, template_name=self.template_name, context=context)
