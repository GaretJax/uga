from django.shortcuts import render
from django.utils.timezone import now, utc
import datetime
from schedule.periods import weekday_names


def month(request, year=0, month=0):
    year = int(year)
    month = int(month)

    if not year:
        year = now().year

    if not month:
        month = now().month

    date = datetime.datetime(year, month, 1, tzinfo=utc)

    return render(request, 'left-sidebar.html', {
        'date': date,
        'weekday_names': weekday_names,
        'managed': True,
    })
