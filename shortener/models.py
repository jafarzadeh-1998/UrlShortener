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
