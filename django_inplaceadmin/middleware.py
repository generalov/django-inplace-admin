"""
Inplace Admin middleware
"""
import os.path

from django.core import urlresolvers
from django.utils.encoding import smart_unicode
from django.views.static import serve

from django_inplaceadmin import settings


_HTML_TYPES = ('text/html', 'application/xhtml+xml')

def replace_insensitive(string, target, replacement):
    no_case = string.lower()
    index = no_case.rfind(target.lower())
    if index != -1:
        result = string[:index] + replacement + string[index + len(target):]
        return result
    # no results so return the original string
    return string

def ssi_view(viewname, request, *args, **kwargs):
    try:
        # resolve 'namespace:action' views
        if isinstance(viewname, basestring) and ':' in viewname and not '/' in viewname:
            viewname = urlresolvers.reverse(viewname, args=args, kwargs=kwargs)
        urlconf = getattr(request, "urlconf", settings.ROOT_URLCONF)
        resolver = urlresolvers.RegexURLResolver(r'^/', urlconf)
        view, args, kwargs = resolver.resolve(viewname)
    except:
        view = urlresolvers.get_callable(viewname)
    if not callable(view):
        raise ValueError, ("%r is not callable" % view)
    response = view(request, *args, **kwargs)
    return response


class InplaceEditorMiddleware(object):
    """
    Middleware to set up Inplace Admin on incoming request and render it
    on outgoing response.
    """
    def _show_toolbar(self, request, response=None):
        if not settings.ENABLED or settings.TEST:
            return False

        if request.path.startswith(settings.MEDIA_URL):
            return False

        if response:
            if response.status_code >= 300 and response.status_code < 400:
                return False
        
        # Allow access if remote ip is in INTERNAL_IPS or
        # the user doing the request is logged in as super user.
        if (not request.META.get('REMOTE_ADDR') in settings.INTERNAL_IPS and 
           (not request.user.is_authenticated() or not request.user.is_superuser)):
            return False
        return True

    def process_request(self, request):
        if request.path.startswith(settings.MEDIA_URL + settings.APP_LABEL):
            return serve(request,
                    request.path[len(settings.MEDIA_URL):],
                    os.path.join(os.path.dirname(__file__), 'media'))

    def process_response(self, request, response):
        if not request.is_ajax() and self._show_toolbar(request, response):
            if response['Content-Type'].split(';')[0] in _HTML_TYPES:
                response.content = replace_insensitive(
                        smart_unicode(response.content),
                        u'</body>',
                        smart_unicode(ssi_view('django_inplaceadmin:widget', request).content) + u'</body>')
        return response
