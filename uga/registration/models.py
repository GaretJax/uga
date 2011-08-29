from django.db import models


class Member(models.Model):
    """
    A single member of the association.
    """
    email = models.EmailField(blank=False, unique=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
