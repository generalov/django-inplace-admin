# coding: utf-8

from django.contrib import admin
from django.core.urlresolvers import reverse
from django.db.models import get_model
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.views.generic.simple import direct_to_template 
from django.utils import simplejson
from django.utils.translation import ugettext as _

from django_inplaceadmin import settings


def base(request):
    pass

def field(request, addr):
    app_label, model_name, pk, field_name = addr.split('-')
    model = get_model(app_label, model_name)
    opts = model._meta
    change_permission = opts.app_label + '.' + opts.get_change_permission()
    fields = [field_name] if field_name else  None
    instance = model.objects.get(pk=pk)

    # authorize by ``change_permission``
    if not request.user.has_perm(change_permission):
        return HttpResponseForbidden('%s: %s' % (addr, change_permission))
    try:
        # Use admin form then it's exists
        AForm = admin.site._registry[model].get_form(request, instance, fields=fields)

        # HACK: remove superfluous fields from AForm class
        #
        # The django.forms.models.ModelFormMetaclass
        # overrides default model fields with any custom declared ones
        # (plus, include all the other declared fields).
        # Therefore the AForm may to got extra fields. Remove them.
        if fields:
            for key in AForm.base_fields:
                if key not in fields:
                    del AForm.base_fields[key]
    except KeyError:
        # Build custom ModelForm for given model and fields
        from django.forms.models import modelform_factory
        AForm = modelform_factory(model, fields=fields)

    if request.method == 'GET':
        form = AForm(instance=instance)
        response = HttpResponse

    elif request.method == 'PUT':
        # HACK: parse request content into request.POST and request.FILES
        # because they aren't filled for PUT-requests
        request.method = 'POST'
        request._load_post_and_files()
        request.method = 'PUT'

        form = AForm(request.POST, request.FILES, instance=instance)

        if form.is_valid():
            instance = form.save()

            # Return saved value
            value = getattr(instance, field_name)
            try:
                value = getattr(instance, 'get_%s_display' % field_name)();
            except AttributeError:
                pass

            return HttpResponse(value)

        response = HttpResponseBadRequest

    data = {
        'formId': settings.APP_LABEL,
        'formAction': reverse('%s:field' % settings.APP_LABEL, args=[addr]),
        'formMethod': 'post',
        'saveBtnName': 'save',
        'cancelBtnName': 'cancel',
        'saveBtnText': _('save'),
        'cancelBtnText': _('cancel'),
        'addr': addr,
        'form': form,
        }
    return direct_to_template(request,
                              '%s/change_form.html' % settings.APP_LABEL,
                              data)

def clam(request):
    """Filter list of addr with change_permission.
    """
    if request.method == 'POST':
        actions = {} 
        errors = []
        response_dict = {'errors': errors, 'permited': actions}

        addr_list = request.POST.keys()
        for addr in addr_list:
            app_label, cls, pk, field_name = addr.split('-')
            model = get_model(app_label, cls)
            opts = model._meta
            change_permission = '%s.%s' % (
                    opts.app_label, opts.get_change_permission())

            if opts.get_field_by_name(field_name)[0].editable and request.user.has_perm(change_permission):
                actions.update({
                    addr: reverse('%s:field' % settings.APP_LABEL, args=[addr]),
                })
    
    return HttpResponse(simplejson.dumps(response_dict), mimetype='application/json')

def widget(request):
    return direct_to_template(request, '%s/widget.html' % settings.APP_LABEL, dict(
        baseUrl = reverse('%s:base' % settings.APP_LABEL),
        FIELD_CLASS = settings.FIELD_CLASS,
    ))
    
