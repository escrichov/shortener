from django.db import models
from django.urls import reverse
from django.conf import settings


class ShortUrl(models.Model):

    url = models.CharField(max_length=1024)

    def short_url(self, request):
        absolute_uri = request.build_absolute_uri(
            reverse(
                'shortener_app:url_redirect',
                kwargs={'short_url_id': self.id}
            )
        )

        absolute_uri = absolute_uri.strip("https:").strip("http:").strip("/")

        return absolute_uri
