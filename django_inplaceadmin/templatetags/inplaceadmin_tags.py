from django import template
from django.utils.encoding import force_unicode

from django_inplaceadmin import settings


register = template.Library()

@register.filter
def editable_field(model, field_name):
    opts = model._meta
    return '%s %s-%s-%s %s' % (
            settings.FIELD_CLASS,
            opts.app_label,
            model.__class__.__name__.lower(),
            force_unicode(model.pk),
            field_name,
    )
