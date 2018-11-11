from django.db import models
from django.urls import reverse
from django.conf import settings


class ShortUrl(models.Model):

    url = models.CharField(max_length=1024)

    def short_url(self, request):
        return request.build_absolute_uri(
            reverse(
                'shortener_app:url_redirect',
                kwargs={'short_url_id': self.id}
            )
        )
