from django.db import models
from django.db.models import Q


class IncompleteMemberManager(models.Manager):

    def _get_completion_query(self):
        return ~Q(last_name='') & ~Q(first_name='')

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

    def is_complete(self):
        return bool(self.first_name and self.last_name)
    is_complete.boolean = True

