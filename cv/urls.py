from django.urls import path
from django.views.generic import RedirectView

from . import views

app_name = 'cv'

urlpatterns = [
    path('', RedirectView.as_view(url='preview/')),
    path('preview/', views.PreviewView.as_view(), name='preview'),
    path('edit/', views.edit_cv, name='edit'),
]
