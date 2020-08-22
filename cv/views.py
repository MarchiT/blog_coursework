from django.shortcuts import render
from django.views import generic
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.forms import modelformset_factory

from .models import Credentials, Qualification
from .forms import CForm


class PreviewView(generic.base.TemplateView):
    template_name = 'cv/preview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['credentials'] = Credentials.objects.first()
        context['qualifications'] = Qualification.objects.all()
        return context


def edit_cv(request):
    types = Qualification.QTypes
    QFormSet = modelformset_factory(Qualification, fields=('text', ), can_delete=True, extra=1)

    if request.method == 'POST':
        credentials_form = CForm(request.POST, instance=Credentials.objects.first())
        formsets = [QFormSet(request.POST, prefix=t) for t in types.values]

        if credentials_form.is_valid() and all([f.is_valid() for f in formsets]):
            credentials_form.save()
            [save_formset(f) for f in formsets]
            return HttpResponseRedirect(reverse('cv:preview'))
        print(formsets[0].errors)

    context = {t.lower() + '_formset': QFormSet(prefix=t, queryset=Qualification.objects.filter(type=t)) for t in types.values}
    context['credentials_form'] = CForm(instance=Credentials.objects.first())
    return render(request, 'cv/edit.html', context)


def save_formset(f):
    f.save(commit=False)
    for q in f.new_objects:
        q.type = f.prefix
    f.save()
