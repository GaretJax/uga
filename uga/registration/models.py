from django.db import models


class Member(models.Model):
    """
    A single member of the association.
    """
    email = models.EmailField(required=True)
    first_name = models.CharField()
    last_name = models.CharField()
