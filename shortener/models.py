from django.db import models
from django.contrib.auth.models import User

class URL(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    full_url = models.CharField(max_length=255)
    short_url = models.CharField(max_length=127)
    suggested_url = models.CharField(max_length=127)
    create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.creator) + " - " + self.short_url

class UrlHistory(models.Model):
    url = models.ForeignKey(URL, on_delete=models.CASCADE)
    AGENTS = (
        ("mobile", "mobile"),
        ('pc', "pc"),
        ('tablet', 'tablet'),
        ('touch_capable', 'touch_capable'),
        ('bot', 'bot'),
    )
    user_agent = models.CharField(max_length=13, choices=AGENTS)
    browser = models.CharField(max_length=50)
    browser_version = models.CharField(max_length=15, null=True)
    hashcode = models.CharField(max_length=32, null=True, blank=True)
    pub_date = models.DateField(auto_now_add=True, null=True, blank=True)

    def recognizeAgent(self, request):
        if request.user_agent.is_mobile:
            return "mobile"
        if request.user_agent.is_pc:
            return "pc"
        if request.user_agent.is_tablet:
            return "tablet"
        if request.user_agent.is_touch_capable:
            return "touch_capable"
        if request.user_agent.is_bot:
            return "bot"


    def create(self, url, request):
        return UrlHistory(url=url,
                          user_agent=self.recognizeAgent(self, request=request),
                          browser=request.user_agent.browser.family ,
                          browser_version=request.user_agent.browser.version_string,
                          hashcode=request.session['hashcode']
                          )


    def __str__(self):
        return self.url.short_url + " " + self.user_agent