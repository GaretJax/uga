from django.db import models
from django.utils import timezone as tz
from random import choice

from schedule.models import Event


class List(models.Model):
    """
    A list to hold the inscriptions to an event.
    """

    event = models.OneToOneField(Event)
    rate = models.PositiveSmallIntegerField(default=2)
    limit = models.PositiveSmallIntegerField()
    start = models.DateTimeField(default=tz.now)
    end = models.DateTimeField(blank=True, null=True)
    deleting = models.BooleanField(default=False, editable=False)

    def open(self):
        if not self.end:
            return self.start <= tz.now()

        return self.start <= tz.now() <= self.end
    open.boolean = True

    def entries(self):
        return InscriptionEntry.objects.filter(inscription__list=self)

    def count(self):
        return self.entries().count()

    def __unicode__(self):
        return self.event.title


class Inscription(models.Model):
    """
    An editable inscription.
    """

    contact = models.EmailField()
    password = models.CharField(max_length=100, blank=True)
    timestamp = models.DateTimeField(blank=True, auto_now_add=True)
    list = models.ForeignKey(List)

    def save(self, *args, **kwargs):
        if not self.password:
            chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
            self.password = ''.join([choice(chars) for i in range(32)])

        super(Inscription, self).save(*args, **kwargs)

    def names(self):
        return u', '.join(map(unicode, self.inscriptionentry_set.all()))

    def add_name(self, first_name, last_name):
        return InscriptionEntry.objects.create(**{
            'first_name': first_name,
            'last_name': last_name,
            'inscription': self
        })

    @models.permalink
    def get_absolute_url(self):
        return ('inscriptions.manage', (), {
            'inscription_id': self.pk,
            'auth': self.password
        })

    def __unicode__(self):
        return u'%s (%s)' % (self.list, self.contact)

    class Meta:
        unique_together = (('contact', 'list'),)
        ordering = ('timestamp',)

class InscriptionEntry(models.Model):
    """
    A single name held by an inscription.
    """

    inscription = models.ForeignKey(Inscription)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    timestamp = models.DateTimeField(blank=True, auto_now_add=True)
    confirmation_sent = models.BooleanField(default=False, editable=False)

    class Meta:
        ordering = ('timestamp',)

    def enrolled(self, update=False):
        """
        Returns true if this entry enrollment is currently confirmed and the
        participation to the event is granted.
        """
        enrolled = self.rank() <= self.inscription.list.limit

        if update and enrolled and not self.confirmation_sent:
            InscriptionEntry.objects.filter(pk=self.pk).update(
                    confirmation_sent=True)

        return enrolled
    enrolled.boolean = True
    enrolled.admin_order_field = 'timestamp'

    def queue(self):
        return self.rank - self.inscription.list.limit

    def full_name(self):
        return u'%s %s' % (self.first_name, self.last_name)

    def rank(self):
        """
        Returns the current rank of the enrollment entry based of the number
        of enrollments preceding the current one.
        """

        return InscriptionEntry.objects.filter(**{
            'inscription__list': self.inscription.list,
            'timestamp__lt': self.timestamp
        }).count() + 1
    rank.admin_order_field = 'timestamp'

    def __unicode__(self):
        return self.full_name()

#post_delete.connect(signals.delete_enrollment_name, sender=InscriptionEntry)
