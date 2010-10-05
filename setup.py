# -*- coding:utf-8 -*-
from distutils.core import setup


setup(
    name = 'django-inplace-admin',
    version = '0.1',
    author = 'Evgeny V. Generalov',
    author_email = 'e.generalov@gmail.com',
    packages = ['django_inplaceadmin', 'django_inplaceadmin.templatetags'],
    description = 'Django Admin Forms for inplace edit',
    long_description = open('README.md').read(),
    classifiers = ['Development Status :: 5 - Production/Stable',
                   'Environment :: Web Environment',
                   'Framework :: Django',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Software Development :: Libraries :: Python Modules',
                   ],

)
