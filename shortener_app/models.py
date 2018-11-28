import string
from django.db import models
from django.urls import reverse
from datetime import datetime
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils.crypto import get_random_string


def generate_random_uid():
    s = get_random_string(length=6, allowed_chars=string.ascii_letters)
    return s


def generate_random_apikey():
    s = get_random_string(length=64, allowed_chars=string.ascii_letters+string.digits)
    return s


class ShortUrl(models.Model):

    uid = models.CharField(default=generate_random_uid, max_length=6, unique=True)
    url = models.CharField(max_length=1024)
    clicks = models.IntegerField(default=0)
    created_on = models.DateTimeField(default=datetime.utcnow)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True)

    @property
    def relative_short_url(self):
        relative_uri = reverse(
            'shortener_app:url_redirect',
            kwargs={'short_url_uid': self.uid}
        )

        return relative_uri.rstrip('/')

    def full_short_url(self):
        return settings.HOSTNAME + self.relative_short_url


class ShortUrlStats(models.Model):

    clicks = models.IntegerField(default=0)
    aggregated_datetime = models.DateTimeField(default=datetime.utcnow)
    short_url = models.ForeignKey(ShortUrl, on_delete=models.CASCADE, null=True, blank=True)


class APIAccess(models.Model):

    apikey = models.CharField(default=generate_random_apikey, max_length=64, unique=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
