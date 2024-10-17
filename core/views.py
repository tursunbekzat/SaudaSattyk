from django.shortcuts import render
from auction.models import Auction, Category
from django.utils import timezone


def base(request):
    return render(request, 'core/base.html')


def home(request):
    now = timezone.now()
    try:
        latest_auctions = Auction.objects.filter(end_time__gt=now).order_by('-created_at')[:6]
    except Exception as e:
        print(f"Error fetching auctions: {e}")  # Логирование ошибки
    
    # Получаем последние аукционы (например, последние 6 аукционов)
    latest_auctions = Auction.objects.filter(end_time__gt=now, is_active=True).order_by('-created_at')[:6]
    
    # Получаем все категории
    categories = Category.objects.all()

    context = {
        'latest_auctions': latest_auctions,
        'categories': categories,
    }
    
    return render(request, 'core/home.html', context)