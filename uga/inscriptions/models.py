from django.db import models
from django.db.models.signals import pre_delete, post_delete, post_save
import datetime
import signals
from random import choice


class List(models.Model):
    """
    A list to hold the inscriptions to an event.
    """
    
    name = models.CharField(max_length=100)
    rate = models.PositiveSmallIntegerField(default=2)
    limit = models.PositiveSmallIntegerField()
    start = models.DateTimeField(default=datetime.datetime.now)
    end = models.DateTimeField(blank=True, null=True)
    deleting = models.BooleanField(default=False, editable=False)
    
    def open(self):
        if not self.end:
            return self.start <= datetime.datetime.now()
        
        return self.start <= datetime.datetime.now() <= self.end
    open.boolean = True
    
    def entries(self):
        return InscriptionEntry.objects.filter(inscription__list=self)
    
    def count(self):
        return self.entries().count()
    
    def __unicode__(self):
        return self.name


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
        InscriptionEntry.objects.create(**{
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
    
    class Meta:
        ordering = ('timestamp',)
    
    def enrolled(self):
        """
        Returns true if this entry enrollment is currently confirmed and the
        participation to the event is granted.
        """
        
        return self.rank() <= self.inscription.list.limit
    enrolled.boolean = True
    enrolled.admin_order_field = 'timestamp'
    
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

post_delete.connect(signals.delete_enrollment_name, sender=InscriptionEntry)