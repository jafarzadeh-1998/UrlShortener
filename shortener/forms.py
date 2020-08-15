from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate

from . import models

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
        self.cleaned_data['user'] = user
        return password

class UrlForm(forms.ModelForm):

    class Meta:
        model = models.URL
        fields = ('full_url', 'suggested_url')
    
    def spaceCounter(self, string):
        count = 0
        for a in string: 
            if (a.isspace()) == True: 
                count+=1
        return count

    def removeSpace(self, data):
        dataWithUnderScore = data.replace(' ', '_')
        dataWithDash = data.replace(' ', '-')
        spaceCount = self.spaceCounter(data)
        dataMixDashUnder = dataWithUnderScore.replace(" ", '-', spaceCount//2)
        dataMixUnderDash = dataWithDash.replace(" ", '_', spaceCount//2)

        if not models.URL.objects.filter(short_url=dataWithDash).count():
            return dataWithDash, True
        if not models.URL.objects.filter(short_url=dataWithUnderScore).count():
            return dataWithUnderScore, True
        if not models.URL.objects.filter(short_url=dataMixDashUnder).count():
            return dataMixDashUnder, True
        if not models.URL.objects.filter(short_url=dataMixUnderDash).count():
            return dataMixUnderDash, True

        return dataWithDash, False
        

    def checkDataCapital(self, data):
        normalizeDataList = []
        for i in range(len(data)):
            if data[i].isupper():
                data[i] = data[i].lower()
                if i != 0 and data[i-1] != "-":
                    normalizeDataList.append("-")
            normalizeDataList.append(data[i])
        data = "".join(normalizeDataList)
        if not models.URL.objects.filter(short_url=data).count():
                return data, True

        if data.isupper():
            if not models.URL.objects.filter(short_url=data.lower()).count():
                return data.lower(), True
        if data.islower():
            if not models.URL.objects.filter(short_url=data.upper()).count():
                return data.upper(), True
        return data, False

    def clean_suggested_url(self):
        suggested_url = self.cleaned_data["suggested_url"]
        data = suggested_url
        okay = False
        if self.spaceCounter(data):
            data, okay = self.removeSpace(data)
        if not okay:
            data, okay = self.checkDataCapital(data)
        if not okay:
            raise  ValidationError("This suggested Url is not Okay anyway:/")
        self.cleaned_data['short_url'] = data
        return suggested_url

    