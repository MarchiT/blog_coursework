from django.shortcuts import render
from django.views import generic

from .models import CV


class PreviewView(generic.base.TemplateView):
    template_name = 'cv/preview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cv'] = CV.objects.all().first()
        return context


class EditView(generic.edit.UpdateView):
    model = CV
    fields = ['credentials']
    template_name_suffix = '_update_form'


def submit_changes(request):
    pass
