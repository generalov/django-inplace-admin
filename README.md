django-inplace-admin
--------------------

Display inplace editor, based on admin forms.

settings.py :

    INSTALLED_APPS = (
	...,
	'django_inplaceadmin',
    )

    MIDDLEWARE_CLASSES = (
	...,
	'django_inplaceadmin.middleware.InplaceEditorMiddleware',
    )

urls.py :

    (r'^inplace-api/',
        include('django_inplaceadmin.urls', namespace='django_inplaceadmin')),

template.html :

    {% load inplaceadmin_tags %}
    <body>
	<div class="{{ user|editable_field:'username' }}">{{ user.username }}</div>
    </body>
