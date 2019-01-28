from django.core.management.base import BaseCommand
from django.conf import settings
from datetime import datetime
from shortener_app.models import ShortUrlLog
import requests


def get_geolocation_data(ip):
    # Locate visitors by ip address
    r = requests.get(
        'http://api.ipstack.com/{ip}'.format(ip=ip),
        params={'access_key': settings.IPSTACK_APIKEY})
    if r.status_code == 200:
        response_data = r.json()
    else:
        response_data = {}

    return response_data


class Command(BaseCommand):

    def handle(self, **options):
        now = datetime.utcnow()
        logs = ShortUrlLog.objects.filter(
            country_code=None, latitude=None, longitude=None)

        for log in logs:
            geolocation_data = get_geolocation_data(log.ip)
            if geolocation_data != {}:
                log.country_code = geolocation_data.get('country_code')
                log.latitude = geolocation_data.get('latitude')
                log.longitude = geolocation_data.get('longitude')
