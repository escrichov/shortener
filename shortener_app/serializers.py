from rest_framework import serializers
from .models import ShortUrl


class ShortUrlSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source="uid")
    short_url = serializers.CharField(source="full_short_url")
    target = serializers.CharField(source="url")

    class Meta:
        model = ShortUrl
        fields = ("id", "created_on", "clicks", "target", "short_url")


class ShortUrlCreateSerializer(serializers.ModelSerializer):
    target = serializers.CharField(source="url", write_only=True, required=True)

    class Meta:
        model = ShortUrl
        fields = ("target",)
