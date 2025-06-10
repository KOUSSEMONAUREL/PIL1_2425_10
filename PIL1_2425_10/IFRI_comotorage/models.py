from django.db import models
from django.contrib.auth.models import AbstractUser

class Location(models.Model):
    name = models.CharField(max_length=200)
    latitude = models.FloatField()
    longitude = models.FloatField()

    class Meta:
        verbose_name = ("Lieu")
        verbose_name_plural = ("Lieux")
        
    def __str__(self):
        return self.name  