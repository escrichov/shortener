from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from django.urls import reverse
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.db.models import F
from django.contrib.auth.decorators import login_required
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

    if request.user.is_authenticated:
        user = request.user
    else:
        user = None

    short_url, _ = ShortUrl.objects.get_or_create(
        url=url,
        user=user,
    )

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
    if request.user.is_authenticated:
        urls = ShortUrl.objects.filter(user=request.user)
    else:
        urls = []

    template = loader.get_template('shortener_app/urls.html')

    context = {
        'urls': urls,
    }

    return HttpResponse(template.render(context, request))
