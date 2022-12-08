from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from advertisements.models import Advertisement, Favorites


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)



class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at')

    def create(self, validated_data):

        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        k = len(Advertisement.objects.filter(status="OPEN", creator=self.context["request"].user).all())

        if data.get('status') != 'CLOSED' and k >= 10:
            raise ValidationError ('Вы не можете иметь 10 открытых объявлений одновременно!')
        return data


class FavoritesSerializer(serializers.ModelSerializer):

    owner = UserSerializer(read_only=True)
    advertisement = AdvertisementSerializer(read_only=True)

    class Meta:
        model = Favorites
        fields = ('id', 'owner', 'advertisement')

    def create(self, validated_data):
        return super().create(validated_data)

    def validate(self, data):
        advertisement = Advertisement.objects.get(id=self.initial_data["advertisement"].creator_id)
        creator = advertisement.creator_id
        owner = self.initial_data["owner"].id
        if creator == owner:
            raise ValidationError ('Вы не можете добавлять в избранное свои объявления!')
        return self.initial_data

    def advertisement_validate(self, data):
        all_user_fav = Favorites.objects.filter(owner=self.initial_data["owner"])
        for fav in all_user_fav:
            if self.initial_data["advertisement"] == fav.advertisement:
                raise ValidationError ('Это объявление уже есть в избранном!')
        return self.initial_data






