from django.apps import AppConfig
from django.conf import settings
import analytics


class ShortenerAppConfig(AppConfig):
    name = 'shortener_app'

    def ready(self):
        analytics.write_key = settings.SEGMENT_ANALYTICS_WRITE_KEY
        analytics.debug = settings.SEGMENT_ANALYTICS_DEBUG
        analytics.send = True
