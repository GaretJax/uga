from django.db import models
from django.utils.translation import ugettext_lazy as _
from urllib import urlencode
from decimal import Decimal as D

from schedule import models as schedule_models


class Location(models.Model):
    title = models.CharField(max_length=100)

    address = models.CharField(max_length=150)
    zipcode = models.CharField(_("zip code"), max_length=30)
    city = models.CharField(max_length=100)

    description = models.CharField(max_length=255, blank=True, null=True)

    lat = models.DecimalField(_('latitude'), max_digits=10, decimal_places=6, null=True, blank=True,
        help_text=_('Use latitude & longitude to fine tune the map position.'))
    lng = models.DecimalField(_('longitude'), max_digits=10, decimal_places=6, null=True, blank=True)

    def __unicode__(self):
        return self.title

    @property
    def coords(self):
        if self.lat and self.lng:
            return self.lat, self.lng

    @property
    def static_url(self):
        base = 'http://maps.googleapis.com/maps/api/staticmap'
        query = {
            'center': '{},{}'.format(*self.coords),
            'zoom': 14,
            'size': '350x150',
            'maptype': 'roadmap',
            'center': '{},{}'.format(self.lat + D(0.0002) * 14, self.lng),
            'markers': (
                'size:small|{},{}'.format(*self.coords),
            ),
            'style': 'feature:landscape|hue:0x112233',
            'sensor': 'false',
        }

        url = '{}?{}'.format(base, urlencode(query, doseq=True))

        return url


class EventLocation(models.Model):
    event = models.OneToOneField(schedule_models.Event)
    location = models.ForeignKey(Location)

    class Meta:
        app_label = 'schedule'

    def __unicode__(self):
        return u'{} ({}) at {}'.format(self.event.title,
                self.event.start.date(), self.location.title)
