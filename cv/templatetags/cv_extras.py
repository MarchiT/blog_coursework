from django import template
from django.template.defaultfilters import stringfilter

import markdown as md

register = template.Library()


@register.filter()
@stringfilter
def markdown(value):
    return md.markdown(value, extensions=['markdown.extensions.fenced_code'])


@register.filter
def get(qs, arg):
    return [q.text for q in qs.filter(type=arg)]


@register.filter
def prefix(formset):
    return formset.prefix
