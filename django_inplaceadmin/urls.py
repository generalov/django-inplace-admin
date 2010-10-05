from django.conf.urls.defaults import *


urlpatterns = patterns('django_inplaceadmin.views',
    url(r'^edit/(?P<addr>[-\w]+)/$', view='field', name='field'),
    url(r'^clam/$', view='clam', name='clam'),
    url(r'^widget/$', view='widget', name='widget'),
    url(r'^$', view='base', name='base'),
)
