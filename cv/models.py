from django.db import models
from django.utils.translation import gettext_lazy as _


class Credentials(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=500)
    phone = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Qualification(models.Model):
    class QTypes(models.TextChoices):
        SKILLS = 'Skills', _('Skills')
        EDUCATION = 'Education', _('Education')
        CAREER = 'Career', _('Career')

    type = models.CharField(max_length=200, choices=QTypes.choices)
    text = models.TextField()

    def __str__(self):
        return self.type + ' ' + str(self.id)
