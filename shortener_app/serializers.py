from rest_framework import serializers
from .models import ShortUrl


class ShortUrlSerializer(serializers.ModelSerializer):
    short_url = serializers.CharField(source='full_short_url')
    target = serializers.CharField(source='url')

    class Meta:
        model = ShortUrl
        fields = ('created_on', 'clicks', 'target', 'short_url')
