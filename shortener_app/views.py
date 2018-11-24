from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from django.urls import reverse
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.db.models import F
from .models import ShortUrl




def index(request):

    template = loader.get_template('shortener_app/index.html')
    context = {}

    return HttpResponse(template.render(context, request))


def shorten(request):
    url = request.POST['url']
    if url is None or url == "":
        return HttpResponse("No url provided")

    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'http://' + url

    validate = URLValidator()
    try:
        validate(url)
    except ValidationError:
        return HttpResponse("Invalid url")

    short_url, _ = ShortUrl.objects.get_or_create(
        url=url,
    )

    return redirect(reverse('shortener_app:info', kwargs={'short_url_id': short_url.id}))


def info(request, short_url_id):
    try:
        short_url = ShortUrl.objects.get(
            id=short_url_id,
        )
    except ShortUrl.DoesNotExist:
        return HttpResponse("Not found", status=404)

    template = loader.get_template('shortener_app/info.html')

    context = {
        'url': short_url.url,
        'full_short_url': short_url.full_short_url(request),
        'relative_short_url': short_url.relative_short_url,
        'clicks': short_url.clicks,
        'created_on': short_url.created_on,
    }

    return HttpResponse(template.render(context, request))


def url_redirect(request, short_url_id):
    try:
        short_url = ShortUrl.objects.get(
            id=short_url_id,
        )
    except ShortUrl.DoesNotExist:
        return HttpResponse("Not found")

    ShortUrl.objects.filter(id=short_url.id).update(clicks=F('clicks') + 1)

    return redirect(short_url.url)
