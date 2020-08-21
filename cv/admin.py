from django.contrib import admin

from .models import Credentials, Qualification

admin.site.register(Credentials)
admin.site.register(Qualification)
