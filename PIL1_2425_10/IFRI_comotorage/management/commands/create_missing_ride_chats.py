from django.core.management.base import BaseCommand
from IFRI_comotorage.models import RideOffer, RideChat

class Command(BaseCommand):
    help = 'Crée des instances de RideChat pour toutes les RideOffer existantes qui n\'en ont pas.'

    def handle(self, *args, **options):
        self.stdout.write("Vérification des RideOffers sans RideChat associé...")
        
        # Récupérer tous les RideOffers
        all_ride_offers = RideOffer.objects.all()
        
        created_count = 0
        for ride_offer in all_ride_offers:
            # Vérifier si un RideChat existe déjà pour ce RideOffer
            if not hasattr(ride_offer, 'chat'):
                # Si non, créer un RideChat pour ce RideOffer
                RideChat.objects.create(ride_offer=ride_offer)
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"RideChat créé pour le trajet ID: {ride_offer.id} ({ride_offer.departure_location} à {ride_offer.arrival_location})"))
            else:
                self.stdout.write(f"RideChat existe déjà pour le trajet ID: {ride_offer.id}")
        
        self.stdout.write(self.style.SUCCESS(f"\nTerminé. {created_count} RideChats ont été créés."))