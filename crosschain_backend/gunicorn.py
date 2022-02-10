from multiprocessing import cpu_count
from os import environ


def max_workers():
    return cpu_count()


bind = '{}:{}'.format(
    environ.get('BACKEND_HOST'),
    environ.get('BACKEND_PORT')
)
max_requests = 1000
workers = max_workers() + 1

env = {
    'DJANGO_SETTINGS_MODULE': 'crosschain_backend.settings.{}'.format(
        environ.get('BACKEND_SETTINGS_MODE')
    )
}

reload = True
name = 'crosschain_backend'
