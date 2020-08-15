from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate

class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).count():
            raise ValidationError("This email already exists!")
        return email
    
class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(max_length=150, required=True, widget=forms.PasswordInput())

    def clean_password(self):
        password = self.cleaned_data["password"]
        username = self.cleaned_data.get("username")
        user = authenticate(username=username,password=password)
        try:
            if not user:
                username = User.objects.get(email=username).get_username()
                user = authenticate(username=username,password=password)
        except:
            pass
        if not user:
            raise ValidationError("Username or Password is invalid.")
        return password