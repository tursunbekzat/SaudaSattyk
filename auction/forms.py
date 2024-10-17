# auction/forms.py
from django import forms
from .models import Auction, Bid

class AuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ['name', 'description', 'starting_price', 'category', 'end_time', 'photo']
        widgets = {
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['amount']
        widgets = {
            'amount': forms.NumberInput(attrs={'step': '0.01', 'min': '0'})
        }
