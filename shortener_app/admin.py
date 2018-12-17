from django.contrib import admin

from .models import ShortUrl, ShortUrlLog, APIAccess


admin.site.register(ShortUrl)
admin.site.register(ShortUrlLog)
admin.site.register(APIAccess)
