from django.contrib import admin
from advertisements.models import Advertisement, Favorites


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    pass


@admin.register(Favorites)
class Favorites(admin.ModelAdmin):
    pass


