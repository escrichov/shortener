from django.contrib import admin

from .models import ShortUrl, ShortUrlStats, APIAccess


admin.site.register(ShortUrl)
admin.site.register(ShortUrlStats)
admin.site.register(APIAccess)

