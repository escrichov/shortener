from django.core.exceptions import ValidationError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from shortener_app.models import ShortUrl
from shortener_app.serializers import ShortUrlSerializer, ShortUrlCreateSerializer


@api_view(['GET'])
def api_url_list(request):
    """
    List user urls
    """

    urls = ShortUrl.objects.filter(user=request.user).all()
    serializer = ShortUrlSerializer(urls, many=True)

    return Response(serializer.data)


@api_view(['POST'])
def api_url_delete(request, uid):
    """
    Delete user urls
    """

    deleted, _ = ShortUrl.objects.filter(user=request.user, uid=uid).delete()
    if deleted == 0:
        return Response({'error': 'Url does not exist'}, status=status.HTTP_400_BAD_REQUEST)

    return Response({})


@api_view(['POST'])
def api_url_create(request):
    """
    Create user urls
    """

    s_input = ShortUrlCreateSerializer(data=request.data)
    if not s_input.is_valid():
        return Response(s_input.errors, status=status.HTTP_400_BAD_REQUEST)

    try:
        short_url = ShortUrl.create_and_validate(s_input.validated_data.get('url'), request.user)
    except ValidationError:
        return Response({'error': 'Invalid url'}, status=status.HTTP_400_BAD_REQUEST)

    s_output = ShortUrlSerializer(short_url)

    return Response(s_output.data)