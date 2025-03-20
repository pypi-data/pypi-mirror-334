import os

import django
from conexao.config import get_config
from conexao.ssh import start_forward


def configure(profile_name: str):
    '''Configures a Django project to use its ORM.'''
    profile = get_config()['profiles'][profile_name]

    if ssh := profile.get('ssh'):
        start_forward(ssh['host'], ssh['forwards'])

    if settings := profile['django'].get('settings'):
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings)
        django.setup()
