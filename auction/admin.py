from django.contrib import admin
from .models import *

class SlugAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, SlugAdmin)
admin.site.register(Auction, SlugAdmin)
admin.site.register(Bid)