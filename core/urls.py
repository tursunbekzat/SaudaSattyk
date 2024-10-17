from django.urls import path
from .views import *

app_name='core'
urlpatterns = [
    path('', base, name='home'),
    path('home/', home, name='home'),
]
