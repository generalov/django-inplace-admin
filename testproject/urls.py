from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

from django.contrib.sites.models import Site

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),

    (r'^inplace-api/',
        include('django_inplaceadmin.urls', namespace='django_inplaceadmin')),

    (r'^$', 'django.views.generic.list_detail.object_list',
             {'queryset': Site.objects.all(), 'template_name': 'index.html'}),
)
