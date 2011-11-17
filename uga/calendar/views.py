from django.shortcuts import render_to_response
from django.template import RequestContext

import datetime
from schedule.periods import weekday_names


def month(request, year=0, month=0):
    year = int(year)
    month = int(month)

    if not year:
        year = datetime.datetime.today().year

    if not month:
        month = datetime.datetime.today().month

    date = datetime.datetime(year, month, 1)

    return render_to_response('left-sidebar.html', {
        'date': date,
        'weekday_names': weekday_names,
        'managed': True,
    }, context_instance = RequestContext(request))

