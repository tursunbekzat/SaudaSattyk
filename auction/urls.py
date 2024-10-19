# auction/urls.py
from django.urls import path
from .views import *

app_name = 'auction'

urlpatterns = [
    path('', AuctionListView.as_view(), name='auction_list'),  # Список аукционов
    path('create/', AuctionCreateView.as_view(), name='auction_create'),  # Создание аукциона
    path('category/<slug:slug>/', CategoryDetailView.as_view(), name='category_detail'),  # новый маршрут
    path('<slug:slug>/', AuctionDetailView.as_view(), name='auction_detail'),  # Детали аукциона
    path('<slug:slug>/bid/', place_bid, name='place_bid'),  # Место для ставки на аукцион
    path('take-quiz/', take_quiz, name='take_quiz'),  # Маршрут для прохождения викторины
    path('quiz-result/', quiz_result, name='quiz_result'),  # Маршрут для просмотра результатов викторины
]
