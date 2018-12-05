from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from django.urls import reverse
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.db.models import F, Count, DateTimeField
from django.db.models.functions import Trunc
from django.conf import settings
from django.contrib.auth.decorators import login_required

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

import requests
from ua_parser import user_agent_parser
from datetime import datetime, timedelta

from .models import ShortUrl, ShortUrlLog, APIAccess
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


def utcnow_current_hour():
    return datetime.utcnow().replace(minute=0, second=0, microsecond=0)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


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


def stats(request, short_url_uid):
    try:
        short_url = ShortUrl.objects.get(
            uid=short_url_uid,
        )
    except ShortUrl.DoesNotExist:
        return HttpResponse("Not found", status=404)

    # Get click stats of last 24 hours
    time_threshold = datetime.utcnow() - timedelta(days=1)
    click_stats = ShortUrlLog.objects.filter(
        created_on__gt=time_threshold,
    ).annotate(
        name=Trunc('created_on', 'hour', output_field=DateTimeField())
    ).values('name').annotate(count=Count('id'))

    # Get country stats of last 24 hours
    country_stats = ShortUrlLog.objects.filter(
        created_on__gt=time_threshold,
        country_code__isnull=False,
    ).extra({
        'name': 'country_code'
    }).order_by().values('name').annotate(count=Count('id'))

    # Get referal stats of last 24 hours
    referal_stats = ShortUrlLog.objects.filter(
        created_on__gt=time_threshold,
        referer__isnull=False,
    ).extra({
        'name': 'referer'
    }).order_by().values('name').annotate(count=Count('id'))

    # Get os stats of last 24 hours
    os_stats = ShortUrlLog.objects.filter(
        created_on__gt=time_threshold,
        os__isnull=False,
    ).extra({
        'name': 'os'
    }).order_by().values('name').annotate(count=Count('id'))

    # Get browser stats of last 24 hours
    browser_stats = ShortUrlLog.objects.filter(
        created_on__gt=time_threshold,
        browser__isnull=False,
    ).extra({
        'name': 'browser'
    }).order_by().values('name').annotate(count=Count('id'))

    template = loader.get_template('shortener_app/stats.html')

    context = {
        'url': short_url,
        'click_stats': click_stats,
        'country_stats': country_stats,
        'os_stats': os_stats,
        'referal_stats': referal_stats,
        'browser_stats': browser_stats,
    }

    return HttpResponse(template.render(context, request))


def url_redirect(request, short_url_uid):
    try:
        short_url = ShortUrl.objects.get(
            uid=short_url_uid,
        )
    except ShortUrl.DoesNotExist:
        return HttpResponse("Not found")

    # Update total clicks
    ShortUrl.objects.filter(id=short_url.id).update(clicks=F('clicks') + 1)

    # Get ip from header if behind proxy, else get ip directly
    ip = get_client_ip(request)

    # Parse user agent into os, user_agent and device
    parsed_string = user_agent_parser.Parse(request.META.get('HTTP_USER_AGENT'))

    # Locate visitors by ip address 
    r = requests.get('http://api.ipstack.com/{ip}'.format(ip=ip), params={'access_key': settings.IPSTACK_APIKEY})
    if r.status_code == 200:
        response_data = r.json()
    else:
        response_data = {}

    # Create log
    point = ShortUrlLog()
    point.ip = ip
    point.referer = request.META.get('HTTP_REFERER')
    point.user_agent = request.META.get('HTTP_USER_AGENT')
    point.short_url = short_url
    point.os = parsed_string['os'].get('family')
    point.browser = parsed_string['user_agent'].get('family')
    point.country_code = response_data.get('country_code')
    point.latitude = response_data.get('latitude')
    point.longitude = response_data.get('longitude')
    point.save()

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
