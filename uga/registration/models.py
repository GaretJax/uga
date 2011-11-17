import operator

from django.db import models
from django.db.models import Q



class IncompleteMemberManager(models.Manager):

    def _get_completion_status(self, member):
        required = 'first_name', 'last_name', 'street', 'zip_code', 'city'
        values = (bool(getattr(member, attr)) for attr in required)
        return all(values)

    def _get_completion_query(self):
        required = {
            'first_name': '',
            'last_name': '',
            'street': '',
            'zip_code__isnull': True,
            'city': '',
        }

        query = (~Q(**{attr: val}) for attr, val in required.iteritems())
        return reduce(operator.__and__, query)

    def incomplete(self):
        return self.filter(self._get_completion_query())

    def complete(self):
        return self.filter(~self._get_completion_query())



class Member(models.Model):
    """
    A single member of the association.
    """
    objects = IncompleteMemberManager()

    email = models.EmailField(blank=False, unique=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    street = models.CharField(max_length=255, blank=True, null=True)
    street_number = models.PositiveSmallIntegerField(blank=True, null=True)
    zip_code = models.PositiveSmallIntegerField(blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)

    def get_full_name(self):
        return u'{0} {1}'.format(self.first_name, self.last_name)

    def __unicode__(self):
        return u'{0} {1} <{2}>'.format(self.first_name, self.last_name,
                self.email)

    def address(self):
        city = u'{0} {1}'.format(self.zip_code, self.city)

        if self.street:
            if self.street_number:
                street = u'{0} {1}'.format(self.street, self.street_number)
            else:
                street = self.street
            return u'{0}, {1}'.format(street, city)
        else:
            return city

    def is_complete(self):
        return self.__class__.objects._get_completion_status(self)
    is_complete.boolean = True

    class Meta:
        permissions = (
            ("enroll_member", "Can enroll a new member"),
        )
        ordering = 'first_name', 'last_name'



class SubscriptionYear(models.Model):
    start = models.DateField()
    end = models.DateField()
    members = models.ManyToManyField(Member, through='Membership')

    def __unicode__(self):
        return u'Anno sociale {0.year}-{1.year}'.format(self.start, self.end)



class Membership(models.Model):
    date_joined = models.DateTimeField(auto_now_add=True)
    person = models.ForeignKey(Member)
    year = models.ForeignKey(SubscriptionYear)

    def __unicode__(self):
        return u'Iscrizione di {0!s} a {1!s} (iscritto il {2!s})'.format(
                self.person, self.year, self.date_joined)

    class Meta:
        unique_together = (
            ('person', 'year'),
        )
