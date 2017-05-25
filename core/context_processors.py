from datetime import datetime

from django.conf import settings


def organization_details(request):
    return {
        'ORGANIZATION_SETTINGS': settings.ORGANIZATION_SETTINGS,
        'COPYRIGHT_YEAR': datetime.now().year,
    }
