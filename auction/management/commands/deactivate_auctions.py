from django.core.management.base import BaseCommand
from auction.models import Auction

class Command(BaseCommand):
    help = 'Deactivate auctions that have ended'

    def handle(self, *args, **options):
        auctions = Auction.objects.filter(is_active=True)
        for auction in auctions:
            auction.deactivate_auction()
            if not auction.is_active:
                self.stdout.write(self.style.SUCCESS(f'Deactivated auction: {auction.name}'))
