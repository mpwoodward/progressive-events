from .settings import *

import dj_database_url


DEPLOYMENT_ENVIRONMENT = 'heroku'
STATIC_URL = '/static/'

DEBUG = False
ALLOWED_HOSTS = ['dbevents-test.herokuapp.com', ]

DATABASES['default'] = dj_database_url.config()
DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'
