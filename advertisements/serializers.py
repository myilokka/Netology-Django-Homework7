from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from advertisements.models import Advertisement, Favorits


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)



class FavoritsSerializer(serializers.ModelSerializer):
    users_fk = UserSerializer(
    read_only=True,)

    class Meta:
        model = Favorits
        fields = ('id', 'users_fk', 'advertisements_fk')

    def create(self, validated_data):
        validated_data["users_fk"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        adv_data = data['advertisements_fk']
        if adv_data.creator_id == self.context["request"].user.id:
            raise ValidationError ('Вы не можете добавлять в избранное свои объявления!')
        return data


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
        k = len(Advertisement.objects.filter(status="OPEN"))
        if data.get('status') == 'OPEN':
            k +=1
        if k > 10:
            raise ValidationError ('Вы не можете иметь 10 открытых объявлений одновременно!')
        return data







