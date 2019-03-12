from datetime import datetime, timedelta
from dateutil import rrule
from urllib.parse import urlparse


def get_client_ip(request):
    """Extract client ip from request headers

    Retrieves rows pertaining to the given keys from the Table instance
    represented by big_table.  Silly things may happen if
    other_silly_variable is not None.

    Args:
        request: django HttpRequest object.

    Returns:
        IP Address in string format from header HTTP_X_FORWARDED_FOR if exist or
        from header REMOTE_ADDR
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def strip_scheme(url):
    """Remove scheme from url

    Returns url without scheme

    Args:
        url: url string.

    Returns:
        Url without scheme
    """
    parsed = urlparse(url)
    scheme = "%s://" % parsed.scheme
    return parsed.geturl().replace(scheme, '', 1)


def date_range(frequency, begin, end):
    """Generate list of datetimes in a range

    Create a list of datetimes from begin to end.
    The list starts with begin datetime and terminates with end datetime.
    The difference between datetimes in the list is the frequency.

    Args:
        frequency: rrule frequency. Only supports HOURLY, DAILY and MONTHLY
        begin: datetime.datetime object.
        end: datetime.datetime object.

    Returns:
        List of datetimes
    """
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
    """Generate list of datetimes in a hourly range"""
    return date_range(rrule.HOURLY, begin, end)


def daily_range(begin, end):
    """Generate list of datetimes in a daily range"""
    return date_range(rrule.DAILY, begin, end)


def monthly_range(begin, end):
    """Generate list of datetimes in a monthly range"""
    return date_range(rrule.MONTHLY, begin, end)


def convert_to_stats(logs):
    now = datetime.utcnow()
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
