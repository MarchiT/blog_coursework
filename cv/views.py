from django.shortcuts import render
from django.views import generic
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.forms import modelformset_factory, Textarea

from .models import Credentials, Qualification
from .forms import CForm


types = Qualification.QTypes.values


class PreviewView(generic.base.TemplateView):
    template_name = 'cv/preview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['credentials'] = Credentials.objects.first()
        context['qualifications'] = Qualification.objects.all()
        context['q_types'] = types
        return context


def edit_cv(request):
    QFormSet = modelformset_factory(Qualification, fields=('text', ), widgets={"text": Textarea(attrs={'rows': 6})}, can_delete=True, extra=1)

    if request.method == 'POST':
        credentials_form = CForm(request.POST, instance=Credentials.objects.first())
        formsets = [QFormSet(request.POST, prefix=t) for t in types]

        if credentials_form.is_valid() and all([f.is_valid() for f in formsets]):
            credentials_form.save()
            [save_formset(f) for f in formsets]
            return HttpResponseRedirect(reverse('cv:preview'))
    else:
        credentials_form = CForm(instance=Credentials.objects.first())
        formsets = [QFormSet(prefix=t, queryset=Qualification.objects.filter(type=t)) for t in types]

    return render(request, 'cv/edit.html', {'credentials_form': credentials_form, 'formsets': formsets})


def save_formset(f):
    f.save(commit=False)
    for q in f.new_objects:
        q.type = f.prefix
    f.save()
