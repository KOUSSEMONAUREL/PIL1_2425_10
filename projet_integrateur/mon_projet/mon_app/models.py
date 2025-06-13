

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    role = models.CharField(max_length=10, choices=[('conducteur', 'Conducteur'), ('passager', 'Passager')])
    photo = models.ImageField(upload_to='photos/', null=True, blank=True)
    departure_point = models.CharField(max_length=255, null=True, blank=True)
    arrival_time = models.TimeField(null=True, blank=True)
    departure_time = models.TimeField(null=True, blank=True)
    car_model = models.CharField(max_length=50, null=True, blank=True)
    car_brand = models.CharField(max_length=50, null=True, blank=True)
    available_seats = models.PositiveIntegerField(null=True, blank=True)
    address = models.CharField("Adresse de départ", max_length=255, null=True, blank=True)
    return_time = models.TimeField("Heure de retour", null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

class RideOffer(models.Model):
    driver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='offers')
    departure = models.CharField(max_length=255)
    arrival = models.CharField(max_length=255)
    departure_time = models.TimeField(null=True, blank=True)
    seats_available = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

class RideRequest(models.Model):
    passenger = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='requests')
    departure = models.CharField(max_length=255)
    arrival = models.CharField(max_length=255)
    desired_departure_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

class Match(models.Model):
    offer = models.ForeignKey(RideOffer, on_delete=models.CASCADE)
    request = models.ForeignKey(RideRequest, on_delete=models.CASCADE)
    matched_on = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)
from django.conf import settings

class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.sender} → {self.receiver}: {self.content[:30]}"
from django.db import models
from django.conf import settings

class Offre(models.Model):
    utilisateur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='offres'
    )
    depart = models.CharField(max_length=100)
    arrivee = models.CharField(max_length=100)
    date = models.DateField()
    heure = models.TimeField()
    vehicule = models.CharField(max_length=100)
    places_disponibles = models.PositiveIntegerField()

    def _str_(self):
        return f"{self.depart} → {self.arrivee} ({self.date})"
