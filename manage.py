#!/usr/bin/env python
import os
import sys

import dotenv

from django.conf import settings


if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'progressive_events.settings')
    if settings.DEPLOYMENT_ENVIRONMENT != 'heroku':
        dotenv.read_dotenv()
        os.environ['DJANGO_SETTINGS_MODULE'] = 'progressive_events.settings'
    else:
        os.environ['DJANGO_SETTINGS_MODULE'] = 'progressive_events.settings_heroku'

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
