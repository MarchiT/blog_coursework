from django.contrib import admin

from .models import CV, Credentials, Qualifications, Qualification

admin.site.register(CV)
admin.site.register(Credentials)
admin.site.register(Qualifications)
admin.site.register(Qualification)
