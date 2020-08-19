from django.db import models
from django.utils.translation import gettext_lazy as _


class Credentials(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=500)
    phone = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.name


class CV(models.Model):
    credentials = models.OneToOneField(Credentials, on_delete=models.CASCADE)

    def __str__(self):
        return self.credentials.name + "'s CV"

    def is_phone_valid(self):
        # can start with +
        # should be numeric
        n = self.credentials.phone
        return n[1:].isnumeric() if n[0] == '+' else n.isnumeric()


class Qualifications(models.Model):
    class QTypes(models.TextChoices):
        SKILLS = 'Skills', _('Skills')
        EDUCATION = 'Education', _('Education')
        CAREER = 'Career', _('Career')

    on_cv = models.ForeignKey(CV, on_delete=models.CASCADE)
    type = models.CharField(max_length=200, choices=QTypes.choices)

    def __str__(self):
        return self.type + ' #' + str(self.qualification_set.count())


class Qualification(models.Model):
    qualifications = models.ForeignKey(Qualifications, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return self.text
