from django.db import models
from django.urls import reverse
from datetime import datetime
from django.contrib.auth import get_user_model
from django.conf import settings


class ShortUrl(models.Model):

    url = models.CharField(max_length=1024)
    clicks = models.IntegerField(default=0)
    created_on = models.DateTimeField(default=datetime.utcnow)

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True)

    @property
    def relative_short_url(self):
        relative_uri = reverse(
            'shortener_app:url_redirect',
            kwargs={'short_url_id': self.id}
        )

        return relative_uri.rstrip('/')

    def full_short_url(self):
        return settings.HOSTNAME + self.relative_short_url
