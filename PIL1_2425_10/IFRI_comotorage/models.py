from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
import os

class Location(models.Model):
    name = models.CharField(max_length=200)
    latitude = models.FloatField()
    longitude = models.FloatField()

    class Meta:
        verbose_name = ("Lieu")
        verbose_name_plural = ("Lieux")
        
    def __str__(self):
        return self.name  
    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    adresse_depart = models.CharField(max_length=255, blank=True, null=True)
    horaire_debut = models.TimeField(blank=True, null=True)
    horaire_fin = models.TimeField(blank=True, null=True)
    nombre_places = models.PositiveIntegerField(default=1)
    photo_profil = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    type_utilisateur = models.CharField(
        max_length=20, 
        choices=[('conducteur', 'Conducteur'), ('passager', 'Passager')],
        default='conducteur'
    )
    telephone = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profil de {self.user.username}"

# Signal pour créer automatiquement un profil quand un utilisateur est créé
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


class RideOffer(models.Model):
    driver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='published_rides')
    departure_location = models.CharField(max_length=255)
    arrival_location = models.CharField(max_length=255)
    departure_time = models.TimeField()
    available_seats = models.PositiveIntegerField(default=1)
    # You might want to add a date field if rides are for specific dates
    # ride_date = models.DateField(default=timezone.now) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = ("Offre de Trajet")
        verbose_name_plural = ("Offres de Trajets")
        ordering = ['departure_time'] # Order by departure time by default

    def __str__(self):
        return f"Trajet de {self.departure_location} à {self.arrival_location} par {self.driver.username}"