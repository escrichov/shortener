from django.db import models
from django.urls import reverse
from datetime import datetime


class ShortUrl(models.Model):

    url = models.CharField(max_length=1024)
    clicks = models.IntegerField(default=0)
    created_on = models.DateTimeField(default=datetime.utcnow)

    @property
    def relative_short_url(self):
        relative_uri = reverse(
            'shortener_app:url_redirect',
            kwargs={'short_url_id': self.id}
        )

        return relative_uri

    def full_short_url(self, request):
        absolute_uri = request.build_absolute_uri(self.relative_short_url)
        absolute_uri = absolute_uri.strip("https:").strip("http:").strip("/")

        return absolute_uri
