import django_filters
from django_filters import rest_framework as filters
from advertisements.models import Advertisement, Favorits


class AdvertisementFilter(filters.FilterSet):
    """Фильтры для объявлений."""
    created_at = filters.DateFromToRangeFilter()
    updated_at = filters.DateFromToRangeFilter()

    creator = django_filters.NumberFilter(field_name='creator__id')
    status = django_filters.CharFilter(field_name='status', lookup_expr='icontains')

    class Meta:
        model = Advertisement
        fields = ['created_at', 'updated_at', 'status', 'creator__id']


class FavoritsFilter(filters.FilterSet):
    users_fk = django_filters.NumberFilter(field_name='users_fk')

    class Meta:
        model = Favorits
        fields = ['users_fk']


