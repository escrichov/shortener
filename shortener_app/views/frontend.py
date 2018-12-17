from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.db.models import F
from django.conf import settings
from django.shortcuts import render

import requests
from ua_parser import user_agent_parser

from shortener_app.models import ShortUrl, ShortUrlLog
from shortener_app import utils


def index(request):
    return render(request, 'shortener_app/index.html', {})


def pricing(request):
    return render(request, 'shortener_app/pricing.html', {})


def shorten(request):
    url = request.POST.get('url')
    if url is None or url == "":
        return HttpResponse("No url provided", status=404)

    if request.user.is_authenticated:
        user = request.user
    else:
        user = None

    try:
        short_url = ShortUrl.create_and_validate(url, user)
    except ValidationError:
        return HttpResponse("Invalid url", status=404)

    if user is None:
        return redirect(reverse('shortener_app:info', kwargs={'short_url_uid': short_url.uid}))
    else:
        return redirect(reverse('shortener_app:urls'))


def info(request, short_url_uid):
    try:
        short_url = ShortUrl.objects.get(
            uid=short_url_uid,
            user__id=request.user.id
        )
    except ShortUrl.DoesNotExist:
        return HttpResponse("Not found", status=404)

    return render(request, 'shortener_app/info.html', {'urls': [short_url]})


def url_redirect(request, short_url_uid):
    try:
        short_url = ShortUrl.objects.get(
            uid=short_url_uid,
        )
    except ShortUrl.DoesNotExist:
        return HttpResponse("Not found", status=404)

    # Update total clicks
    ShortUrl.objects.filter(id=short_url.id).update(clicks=F('clicks') + 1)

    # Get ip from header if behind proxy, else get ip directly
    ip = utils.get_client_ip(request)

    # Parse user agent into os, user_agent and device
    if 'HTTP_USER_AGENT' in request.META:
        parsed_string = user_agent_parser.Parse(
            request.META.get('HTTP_USER_AGENT'))
        browser_string = parsed_string['user_agent'].get('family')
        os_string = parsed_string['os'].get('family')
    else:
        browser_string = None
        os_string = None

    # Locate visitors by ip address
    r = requests.get('http://api.ipstack.com/{ip}'.format(
        ip=ip), params={'access_key': settings.IPSTACK_APIKEY})
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
    point.os = os_string
    point.browser = browser_string
    point.country_code = response_data.get('country_code')
    point.latitude = response_data.get('latitude')
    point.longitude = response_data.get('longitude')
    point.save()

    return redirect(short_url.url)
