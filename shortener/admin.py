from django.contrib import admin

from . import models

admin.site.register(models.URL)
admin.site.register(models.UrlHistory)
