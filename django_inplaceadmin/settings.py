
from django.conf import settings


APP_LABEL = 'django_inplaceadmin'
FIELD_CLASS = 'field-value'
INTERNAL_IPS = settings.INTERNAL_IPS
MEDIA_URL = settings.MEDIA_URL
ROOT_URLCONF = settings.ROOT_URLCONF
TEST = getattr(settings, 'TEST', False)
ENABLED = getattr(settings, '%s_ENABLED' % APP_LABEL.upper(), False)
