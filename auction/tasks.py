# Celery task for ending auctions
from celery import shared_task
from django.core.mail import send_mail
from .models import Auction

@shared_task
def end_auction(auction_id):
    auction = Auction.objects.get(id=auction_id)
    if not auction.is_ended:
        return
    
    winning_bid = auction.bids.first()
    if winning_bid:
        auction.winner = winning_bid.user
        auction.is_active = False
        auction.save()
        
        # Notify winner
        send_mail(
            'You won the auction!',
            f'Congratulations! You won the auction for {auction.name}',
            'from@example.com',
            [winning_bid.user.email],
            fail_silently=True,
        )
        
        # Notify seller
        send_mail(
            'Your auction has ended',
            f'Your auction for {auction.name} has ended. The winning bid was ${winning_bid.amount}',
            'from@example.com',
            [auction.author.email],
            fail_silently=True,
        )