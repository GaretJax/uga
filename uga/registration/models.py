from django.db import models


class Member(models.Model):
    """
    A single member of the association.
    """
    email = models.EmailField(blank=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
