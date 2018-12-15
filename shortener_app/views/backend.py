from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.db.models.functions import Trunc
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Count, DateTimeField
from payments.models import Subscription
from datetime import datetime, timedelta
import json

from shortener_app.models import ShortUrl, ShortUrlLog, APIAccess


@login_required
def upgrade_to_premium(request):
    try:
        subscription = Subscription.objects.get(user=request.user)
    except Subscription.DoesNotExist:
        subscription = None

    if subscription and subscription.state == Subscription.STATE_ACTIVE:
        subscription_active = True
    else:
        subscription_active = False

    context = {
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        'payment_amount': 100,
        'subscription_active': subscription_active,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
    }
    return render(request, 'shortener_app/upgrade_to_premium.html', context)


@login_required
def list_urls(request):
    urls = ShortUrl.objects.filter(user=request.user)

    context = {
        'urls': urls,
    }

    return render(request, 'shortener_app/list_urls.html', context)


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
    api_accesses = APIAccess.objects.filter(user=request.user)
    try:
        subscription = Subscription.objects.get(user=request.user)
    except Subscription.DoesNotExist:
        subscription = None

    if subscription and subscription.state == Subscription.STATE_ACTIVE:
        subscription_active = True
    else:
        subscription_active = False

    context = {
        'api_accesses': api_accesses,
        'payment_amount': 100,
        'subscription_active': subscription_active,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
    }

    return render(request, 'shortener_app/profile.html', context)


@login_required
def stats(request, short_url_uid):
    try:
        short_url = ShortUrl.objects.get(
            uid=short_url_uid,
            user=request.user,
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

    click_stats_javascript = {'labels': [], 'values': []}
    for stat in click_stats:
        click_stats_javascript['labels'].append(str(stat['name']))
        click_stats_javascript['values'].append(stat['count'])

    referal_stats_javascript = {'labels': [], 'values': []}
    for stat in referal_stats:
        referal_stats_javascript['labels'].append(stat['name'])
        referal_stats_javascript['values'].append(stat['count'])

    country_stats_javascript = {'labels': [], 'values': []}
    for stat in country_stats:
        country_stats_javascript['labels'].append(stat['name'])
        country_stats_javascript['values'].append(stat['count'])

    browser_stats_javascript = {'labels': [], 'values': []}
    for stat in browser_stats:
        browser_stats_javascript['labels'].append(stat['name'])
        browser_stats_javascript['values'].append(stat['count'])

    os_stats_javascript = {'labels': [], 'values': []}
    for stat in os_stats:
        os_stats_javascript['labels'].append(stat['name'])
        os_stats_javascript['values'].append(stat['count'])

    context = {
        'url': short_url,
        'click_stats': click_stats,
        'country_stats': country_stats,
        'os_stats': os_stats,
        'referal_stats': referal_stats,
        'browser_stats': browser_stats,
        'country_stats_javascript': json.dumps(country_stats_javascript),
        'referal_stats_javascript': json.dumps(referal_stats_javascript),
        'browser_stats_javascript': json.dumps(browser_stats_javascript),
        'os_stats_javascript': json.dumps(os_stats_javascript),
        'click_stats_javascript': json.dumps(click_stats_javascript),
    }

    return render(request, 'shortener_app/stats.html', context)
