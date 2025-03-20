import pytest
import django
import os
from django.conf import settings
from django.test.utils import setup_test_environment
import django_stubs_ext

django_stubs_ext.monkeypatch()

@pytest.fixture(scope='session', autouse=True)
def django_test_environment():
    if not settings.configured:
        # Configure Django settings
        settings.configure(
            INSTALLED_APPS=[
                'django.contrib.admin',
                'django.contrib.auth',
                'django.contrib.contenttypes',
                'django.contrib.sessions',
                'django.contrib.messages',
                'django.contrib.staticfiles',
                'djangofoundry',
            ],
            DATABASES = {
                'default': {
                    'ENGINE': 'psqlextra.backend',
                    'NAME': os.getenv('DJANGOFOUNDRY_DB_NAME','test_djangofoundry'),
                    'USER': os.getenv('DJANGOFOUNDRY_DB_USER','postgres'),
                    'PASSWORD': os.getenv('DJANGOFOUNDRY_DB_PASSWORD','postgres'),
                    'HOST': os.getenv('DJANGOFOUNDRY_DB_HOST','localhost'),
                    'PORT': os.getenv('DJANGOFOUNDRY_DB_PORT','5432'),
                }
            }
        )
        django.setup()
    setup_test_environment()
