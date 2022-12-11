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
    favorites = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Favorites', related_name='favorites_adv')


class Favorites(models.Model):

    class Meta:
        constraints = [models.UniqueConstraint(fields=('owner', 'advertisement'), name = 'unique_favorite_adv')]

    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE, related_name='favorites_adv_inner')

    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name='favorites_user_inner')


