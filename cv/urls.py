from django.urls import path
from django.views.generic import RedirectView

from . import views


urlpatterns = [
    path('', RedirectView.as_view(url='preview/')),
    path('preview/', views.PreviewView.as_view(), name='preview'),
    path('edit/<int:pk>/', views.EditView.as_view(), name='edit'),
]
