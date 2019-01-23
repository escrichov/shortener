from django.core.management.base import BaseCommand
from datetime import datetime
from shortener_app.models import ShortUrl
import requests


def check_url_active(url):
    try:
        response = requests.get(url)
    except:
        return False

    return response.ok


class Command(BaseCommand):
    def handle(self, **options):
        now = datetime.utcnow()
        short_urls = ShortUrl.objects.all()
        for short_url in short_urls:
            url_active = check_url_active(short_url.url)
            short_url.url_active = url_active
            short_url.url_active_last_checked = now
            short_url.save()
