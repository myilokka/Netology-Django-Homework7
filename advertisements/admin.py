from django.contrib import admin
from advertisements.models import Advertisement, Favorits


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    pass

@admin.register(Favorits)
class Favorits(admin.ModelAdmin):
    pass


