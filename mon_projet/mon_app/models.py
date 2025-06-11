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


# mon_app/models.py
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.sender} → {self.receiver}"


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
    date_depart = models.DateTimeField(null=True, blank=True)
    vehicule = models.CharField(max_length=100)
    places_disponibles = models.PositiveIntegerField()
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        # Format : 10/06/2025 à 14:30
        date_str = self.date.strftime("%d/%m/%Y")
        return f"{self.depart} → {self.arrivee} ({date_str} à {heure_str})"
