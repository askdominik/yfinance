from django.db import models
from django.utils import timezone


class Company(models.Model):
    symbol = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)
    last_updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
