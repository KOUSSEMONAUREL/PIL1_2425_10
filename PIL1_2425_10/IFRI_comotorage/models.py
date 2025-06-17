from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import time

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
    departure_latitude = models.FloatField(null=True, blank=True)
    departure_longitude = models.FloatField(null=True, blank=True)

    arrival_location = models.CharField(max_length=255)
    arrival_latitude = models.FloatField(null=True, blank=True)
    arrival_longitude = models.FloatField(null=True, blank=True)

    # Champ pour la date du trajet, avec la date du jour comme valeur par défaut
    departure_date = models.DateField(default=timezone.now) 
    departure_time = models.TimeField(default=time(8, 0))
    available_seats = models.PositiveIntegerField(default=1)
    seats_taken = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = ("Offre de Trajet")
        verbose_name_plural = ("Offres de Trajets")
        ordering = ['departure_time']

    def __str__(self):
        return f"Trajet de {self.departure_location} à {self.arrival_location} par {self.driver.username}"

    @property
    def remaining_seats(self):
        """Calcule et retourne le nombre de places restantes."""
        return self.available_seats - self.seats_taken

class RideRequest(models.Model):
    ride_offer = models.ForeignKey(RideOffer, on_delete=models.CASCADE, related_name='requests')
    passenger = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ride_requests')
    
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('accepted', 'Accepté'),
        ('rejected', 'Rejeté'),
        ('cancelled', 'Annulé'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    chat_access_granted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = ("Demande de Trajet")
        verbose_name_plural = ("Demandes de Trajets")
        unique_together = ('ride_offer', 'passenger')

    def __str__(self):
        return f"Demande de {self.passenger.username} pour {self.ride_offer} - Statut: {self.status}"

class RideChat(models.Model):
    ride_offer = models.OneToOneField(RideOffer, on_delete=models.CASCADE, related_name='chat')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = ("Chat de Trajet")
        verbose_name_plural = ("Chats de Trajets")

    def __str__(self):
        return f"Chat pour le trajet: {self.ride_offer}"

class ChatMessage(models.Model):
    chat = models.ForeignKey(RideChat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = ("Message de Chat")
        verbose_name_plural = ("Messages de Chat")
        ordering = ['timestamp']

    def __str__(self):
        return f"[{self.timestamp.strftime('%H:%M')}] {self.sender.username}: {self.message[:50]}..."