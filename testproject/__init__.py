
from django.db.backends import signals
from django.db.backends import sqlite3

def syncdb_callback(sender, connection, *args, **kwargs):
    from django.core import management
    from django.conf import settings
    username, email = settings.ADMINS[0]
    management.call_command('syncdb', interactive=False)
    management.call_command('createsuperuser', username=username,
                                               email=email,
                                               interactive=False,
                                               noinput=True)
    from django.contrib.auth.models import User
    admin = User.objects.get(username=username)
    admin.set_password(username)
    admin.save()

signals.connection_created.connect(
        syncdb_callback, 
        sender=sqlite3.base.DatabaseWrapper)
