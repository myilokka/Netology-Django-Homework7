from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from advertisements.models import Advertisement, Favorits
from advertisements.serializers import AdvertisementSerializer, FavoritsSerializer
from advertisements.filters import AdvertisementFilter, FavoritsFilter
from advertisements.permissions import IsOwnerOrAdminOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filterset_class = AdvertisementFilter
    filter_backends = [DjangoFilterBackend]

    def get_permissions(self):
        """Получение прав для действий."""
        return [IsAuthenticated(), IsOwnerOrAdminOrReadOnly()]


class FavoritsViewSet(ModelViewSet):
    queryset = Favorits.objects.all()
    serializer_class = FavoritsSerializer
    filterset_class = FavoritsFilter
    filter_backends = [DjangoFilterBackend]

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsOwnerOrAdminOrReadOnly()]
        return []
