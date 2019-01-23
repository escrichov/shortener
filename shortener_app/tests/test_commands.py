from django.core.management import call_command
from django.test import TestCase
from shortener_app.models import ShortUrl
from datetime import datetime


class UpdateUrlActiveCommandTestCase(TestCase):
    def test_updated_ok(self):
        " Test my custom command."

        now = datetime.utcnow()

        short_url = ShortUrl()
        short_url.url = 'https://google.com'
        short_url.url_active = False
        short_url.save()

        args = []
        opts = {}
        call_command('update_url_active', *args, **opts)

        updated_short_url = ShortUrl.objects.get(id=short_url.id)
        self.assertEqual(updated_short_url.url_active, True)
        self.assertGreater(updated_short_url.url_active_last_checked, now)

    def test_updated_failed(self):
        " Test my custom command."

        now = datetime.utcnow()

        short_url = ShortUrl()
        short_url.url = 'https://fsdafe.com'
        short_url.url_active = False
        short_url.save()

        args = []
        opts = {}
        call_command('update_url_active', *args, **opts)

        updated_short_url = ShortUrl.objects.get(id=short_url.id)
        self.assertEqual(updated_short_url.url_active, False)
        self.assertGreater(updated_short_url.url_active_last_checked, now)