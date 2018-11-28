from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from django.urls import reverse
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.db.models import F
from django.contrib.auth.decorators import login_required

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import ShortUrl, APIAccess
from .serializers import ShortUrlSerializer, ShortUrlCreateSerializer


# Throw ValidationError exception if url_target is not incorrect format
def create_short_url(url_target, user):
    if not url_target.startswith('http://') and not url_target.startswith('https://'):
        url_target = 'http://' + url_target

    validate = URLValidator()
    validate(url_target)

    short_url, _ = ShortUrl.objects.get_or_create(
        url=url_target,
        user=user,
    )

    return short_url


def index(request):

    template = loader.get_template('shortener_app/index.html')
    context = {}

    return HttpResponse(template.render(context, request))


def shorten(request):
    url = request.POST['url']
    if url is None or url == "":
        return HttpResponse("No url provided")

    if request.user.is_authenticated:
        user = request.user
    else:
        user = None

    try:
        short_url = create_short_url(url, user)
    except ValidationError:
        return HttpResponse("Invalid url")

    return redirect(reverse('shortener_app:info', kwargs={'short_url_uid': short_url.uid}))


def info(request, short_url_uid):
    try:
        short_url = ShortUrl.objects.get(
            uid=short_url_uid,
        )
    except ShortUrl.DoesNotExist:
        return HttpResponse("Not found", status=404)

    template = loader.get_template('shortener_app/info.html')

    context = {
        'url': short_url,
    }

    return HttpResponse(template.render(context, request))


def url_redirect(request, short_url_uid):
    try:
        short_url = ShortUrl.objects.get(
            uid=short_url_uid,
        )
    except ShortUrl.DoesNotExist:
        return HttpResponse("Not found")

    ShortUrl.objects.filter(id=short_url.id).update(clicks=F('clicks') + 1)

    return redirect(short_url.url)


@login_required
def list_urls(request):
    urls = ShortUrl.objects.filter(user=request.user)

    template = loader.get_template('shortener_app/urls.html')

    context = {
        'urls': urls,
    }

    return HttpResponse(template.render(context, request))


@login_required
def delete(request, short_url_uid):
    ShortUrl.objects.filter(
        uid=short_url_uid,
        user=request.user,
    ).delete()

    return redirect(reverse('shortener_app:urls'))


@login_required
def create_api_access(request):
    api_access = APIAccess()
    api_access.user = request.user
    api_access.save()

    return redirect(reverse('shortener_app:profile'))


@login_required
def delete_api_access(request, api_access_id):
    APIAccess.objects.filter(id=api_access_id, user=request.user).delete()

    return redirect(reverse('shortener_app:profile'))


@login_required
def profile(request):
    template = loader.get_template('shortener_app/profile.html')

    api_accesses = APIAccess.objects.filter(user=request.user)

    context = {
        'api_accesses': api_accesses,
    }

    return HttpResponse(template.render(context, request))


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
        short_url = create_short_url(s_input.validated_data.get('url'), request.user)
    except ValidationError:
        return Response({'error': 'Invalid url'}, status=status.HTTP_400_BAD_REQUEST)

    s_output = ShortUrlSerializer(short_url)

    return Response(s_output.data)
