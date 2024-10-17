# auction/views.py
from django.forms import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView
from django.contrib import messages
from django.utils import timezone
from .models import Auction, Category
from .forms import AuctionForm, BidForm
from django.contrib.auth.decorators import login_required   


class AuctionListView(ListView):
    model = Auction
    context_object_name = 'auctions'
    template_name = 'auction/auction_list.html'
    paginate_by = 12

    def get_queryset(self):
        queryset = Auction.objects.filter(end_time__gt=timezone.now())
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class AuctionDetailView(DetailView):
    model = Auction
    context_object_name = 'auction'
    template_name = 'auction/auction_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bid_form'] = BidForm()
        context['bids'] = self.object.bids.all()[:10]
        return context

class AuctionCreateView(LoginRequiredMixin, CreateView):
    model = Auction
    form_class = AuctionForm    
    template_name = 'auction/auction_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.current_price = form.instance.starting_price
        return super().form_valid(form)



@login_required
def place_bid(request, slug):
    auction = get_object_or_404(Auction, slug=slug)
    
    if request.method == 'POST':
        form = BidForm(request.POST)
        if form.is_valid():
            bid = form.save(commit=False)
            bid.auction = auction
            bid.user = request.user
            
            try:
                bid.clean()
                bid.save()
                auction.current_price = bid.amount
                auction.save()
                messages.success(request, 'Your bid was placed successfully!')
                return redirect('auction:auction_detail', slug=slug)
            except ValidationError as e:
                # Получаем сообщения об ошибках
                errors = e.messages
                # Передаем ошибки в контекст
                return render(request, 'auction/auction_detail.html', {
                    'auction': auction,
                    'bid_form': form,
                    'bids': auction.bids.all(),
                    'errors': errors,  # Добавляем ошибки в контекст
                })
    
    form = BidForm()
    return render(request, 'auction/auction_detail.html', {
        'auction': auction,
        'bid_form': form,
        'bids': auction.bids.all(),
    })


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'auction/category_detail.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['auctions'] = Auction.objects.filter(category=self.object, is_active=True)
        return context