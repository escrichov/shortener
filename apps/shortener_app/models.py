from django.db import models
from django.urls import reverse
from datetime import datetime
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils.crypto import get_random_string
from django.core.validators import URLValidator
from shortener_app import utils

import string


def generate_random_uid():
    s = get_random_string(length=6, allowed_chars=string.ascii_letters)
    return s


def generate_random_apikey():
    s = get_random_string(
        length=64, allowed_chars=string.ascii_letters + string.digits)
    return s


class ShortUrl(models.Model):

    uid = models.CharField(
        default=generate_random_uid, max_length=6, unique=True)
    url = models.CharField(max_length=1024)
    clicks = models.IntegerField(default=0)
    created_on = models.DateTimeField(default=datetime.utcnow)
    url_active = models.BooleanField(default=True)
    url_active_last_checked = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, null=True, blank=True)

    @classmethod
    def create_and_validate(cls, url_target, user):
        if not url_target.startswith('http://') and not url_target.startswith(
                'https://'):
            url_target = 'http://' + url_target

        # Throw ValidationError exception if url_target is not incorrect format
        validate = URLValidator()
        validate(url_target)

        short_url, _ = ShortUrl.objects.get_or_create(
            url=url_target,
            user=user,
        )

        return short_url

    @property
    def relative_short_url(self):
        relative_uri = reverse(
            'shortener_app:url_redirect', kwargs={'short_url_uid': self.uid})

        return relative_uri.rstrip('/')

    @property
    def full_short_url_without_scheme(self):
        return utils.strip_scheme(self.full_short_url_with_scheme)

    @property
    def full_short_url_with_scheme(self):
        return settings.HOSTNAME + self.relative_short_url


class ShortUrlLog(models.Model):

    created_on = models.DateTimeField(default=datetime.utcnow)
    ip = models.GenericIPAddressField(null=True, blank=True)
    browser = models.CharField(max_length=16, null=True, blank=True)
    os = models.CharField(max_length=16, null=True, blank=True)
    country_code = models.CharField(max_length=4, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    referer = models.CharField(max_length=256, null=True, blank=True)
    user_agent = models.CharField(max_length=256, null=True, blank=True)
    short_url = models.ForeignKey(
        ShortUrl, on_delete=models.CASCADE, null=True, blank=True)


class APIAccess(models.Model):

    apikey = models.CharField(
        default=generate_random_apikey, max_length=64, unique=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
