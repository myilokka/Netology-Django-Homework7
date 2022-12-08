from django.conf import settings
from django.db import models


class AdvertisementStatusChoices(models.TextChoices):
    """Статусы объявления."""

    OPEN = "OPEN", "Открыто"
    CLOSED = "CLOSED", "Закрыто"
    DRAFT = "DRAFT", "Черновик"


class Advertisement(models.Model):
    """Объявление."""

    title = models.TextField()
    description = models.TextField(default='')
    status = models.TextField(
        choices=AdvertisementStatusChoices.choices,
        default=AdvertisementStatusChoices.OPEN
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )


class FavoritesStatusChoices(models.TextChoices):

    IN_FAVORITES = "IN FAVORITES", "В избранном"
    NOT_IN_FAVORITES = "NOT IN FAVORITES ", "Не в избранном"


class Favorites(models.Model):
    status = models.TextField(
        choices=FavoritesStatusChoices.choices,
        default=FavoritesStatusChoices.NOT_IN_FAVORITES
    )
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE, related_name='favorites')

    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name='favorites')


