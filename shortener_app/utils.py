from datetime import datetime, timedelta
from dateutil import rrule
from urllib.parse import urlparse


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def strip_scheme(url):
    parsed = urlparse(url)
    scheme = "%s://" % parsed.scheme
    return parsed.geturl().replace(scheme, '', 1)


def date_range(frequency, begin, end):
    datetimes = []
    for dt in rrule.rrule(frequency, dtstart=begin, until=end):
        if frequency == rrule.HOURLY:
            dt = dt.replace(minute=0, second=0, microsecond=0)
        elif frequency == rrule.DAILY:
            dt = dt.replace(hour=0, minute=0, second=0, microsecond=0)
        elif frequency == rrule.MONTHLY:
            dt = dt.replace(day=0, hour=0, minute=0, second=0, microsecond=0)
        datetimes.append(dt)

    return datetimes


def hourly_range(begin, end):
    return date_range(rrule.HOURLY, begin, end)


def daily_range(begin, end):
    return date_range(rrule.DAILY, begin, end)


def monthly_range(begin, end):
    return date_range(rrule.MONTHLY, begin, end)


def convert_to_stats(logs):
    now = datetime.utcnow()
    hourly_list = hourly_range(now-timedelta(days=1), now)
    hourly_list = hourly_range(now - timedelta(days=1), now)

    stats = {'labels': [], 'values': []}
    i = 0
    for hour in hourly_list:
        stats['labels'].append(hour.strftime("%H:00"))
        if i < len(logs) and logs[i]['name'] == hour:
            stats['values'].append(logs[i]['count'])
            i += 1
        else:
            stats['values'].append(0)

    return stats
