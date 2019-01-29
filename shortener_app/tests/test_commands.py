from datetime import datetime
from django.core.management import call_command
from django.test import TestCase

from shortener_app.models import ShortUrl, ShortUrlLog


class UpdateUrlActiveCommandTestCase(TestCase):

    def setUp(self):
        self.now = datetime.utcnow()
        self.short_url = ShortUrl()
        self.short_url.url = 'https://google.com'
        self.short_url.url_active = False
        self.short_url.save()

    def test_updated_ok(self):
        " Test my custom command."

        self.short_url.url = 'https://google.com'
        self.short_url.save()

        args = []
        opts = {}
        call_command('update_url_active', *args, **opts)

        updated_short_url = ShortUrl.objects.get(id=self.short_url.id)
        self.assertEqual(updated_short_url.url_active, True)
        self.assertGreater(updated_short_url.url_active_last_checked, self.now)

    def test_updated_failed(self):
        " Test my custom command."

        self.short_url.url = 'https://fasdf.com'
        self.short_url.save()

        args = []
        opts = {}
        call_command('update_url_active', *args, **opts)

        updated_short_url = ShortUrl.objects.get(id=self.short_url.id)
        self.assertEqual(updated_short_url.url_active, False)
        self.assertGreater(updated_short_url.url_active_last_checked, self.now)


class UpdateLogsGeolocationCommandTestCase(TestCase):

    def test_updated_ok(self):
        " Test my custom command."

        log = ShortUrlLog()
        log.ip = '90.74.206.135'
        log.save()

        args = []
        opts = {}
        call_command('update_logs_geolocation', *args, **opts)

        updated_log = ShortUrlLog.objects.get(id=log.id)
        self.assertEqual(updated_log.country_code, None)
        self.assertEqual(updated_log.latitude, None)
        self.assertEqual(updated_log.longitude, None)

    def test_updated_failed(self):
        " Test my custom command."

        log = ShortUrlLog()
        log.ip = '213.789.478.154'
        log.save()

        args = []
        opts = {}
        call_command('update_logs_geolocation', *args, **opts)

        updated_log = ShortUrlLog.objects.get(id=log.id)
        self.assertEqual(updated_log.country_code, None)
        self.assertEqual(updated_log.latitude, None)
        self.assertEqual(updated_log.longitude, None)
