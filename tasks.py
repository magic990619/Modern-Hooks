import os
import time

from invoke import task, run, exceptions

DUMP_PATH = 'data/dump.sql'


def local(command, **kwargs):
    kwargs.update({'pty': True})
    return run(command, **kwargs)


def recreate_db():
    from django.conf import settings
    db_name = settings.DATABASES.get('default').get('NAME')
    local('dropdb -U postgres -h db --if-exists {0}'.format(db_name))
    local('createdb -U postgres -h db {0}'.format(db_name))
    local('cat {0} | psql -h db -U postgres {1}'.format(DUMP_PATH, db_name))


@task
def run_it(ctx):
    """
    Set env PGPASSWORD and DJANGO_SETTINGS_MODULE.
    """
    # Wait till postgres is up
    while True:
        try:
            if os.getenv('RECREATE_DB') and os.path.isfile('./{0}'.format(DUMP_PATH)):
                recreate_db()
            local('python3 manage.py migrate')
            time.sleep(1)
            break
        except exceptions.Failure:
            pass
    local('python3 manage.py collectstatic --noinput')
    # local('python3 manage.py makemessages')
    # local('python3 manage.py compilemessages')
    cmd = (
        'uwsgi --http 0.0.0.0:9000 --master '
        '--module "django.core.wsgi:get_wsgi_application()" '
        '--processes 3 '
    )
    if os.getenv('PY_AUTORELOAD'):
        cmd += ' --py-autoreload 1'
    local(cmd)
