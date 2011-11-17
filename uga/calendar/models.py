from django.db import models
from cms.models import CMSPlugin
from schedule.models import Calendar


class MonthCalendarPlugin(CMSPlugin):
    calendars_to_display = models.ManyToManyField(Calendar)
    display_details = models.BooleanField(default=True)