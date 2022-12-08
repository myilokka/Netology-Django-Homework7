from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.db.models import Q

from .filters import AdvertisementFilter
from .models import Advertisement, Favorites
from .permissions import IsOwnerOrAdminOrReadOnly
from .serializers import AdvertisementSerializer, FavoritesSerializer


class AdvertisementViewSet(ModelViewSet):

    serializer_class = AdvertisementSerializer
    filterset_class = AdvertisementFilter
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        user = self.request.user.id
        queryset = Advertisement.objects.exclude(Q(status='DRAFT') & ~Q(creator=user)).all()
        return queryset

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsOwnerOrAdminOrReadOnly()]
        return []

    @action(detail=True, methods=["post"], url_path=r'favorites')
    def add_favorites(self, request, pk):
        request.data['advertisement'] = self.get_object()
        request.data['owner'] = self.request.user
        serializer = FavoritesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.advertisement_validate(request.data)
            serializer.create(request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, url_path=r'all_favorites')
    def view_favorites(self, request):
        favorites = Favorites.objects.filter(Q(status="IN FAVORITES") & Q(owner=self.request.user)).all()
        serializer = FavoritesSerializer(data=favorites, many=True)
        serializer.is_valid()
        return Response(serializer.data, status=status.HTTP_200_OK)
