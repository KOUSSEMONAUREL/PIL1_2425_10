from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=200)
    latitude = models.FloatField()
    longitude = models.FloatField()

    class Meta:
        verbose_name = ("Personne")
        verbose_name_plural = ("Personnes")
        
    def __str__(self):
        return self.titre   