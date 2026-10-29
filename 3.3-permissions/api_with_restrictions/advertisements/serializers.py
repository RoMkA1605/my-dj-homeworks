from django.contrib.auth.models import User
from rest_framework import serializers

from advertisements.models import Advertisement


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', )

    def create(self, validated_data):

        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        user = self.context["request"].user
        new_status = data.get('status', getattr(self.instance, 'status', 'OPEN'))
        if new_status == 'OPEN':
            open_count = Advertisement.objects.filter(
                creator=user,
                status='OPEN'
            ).count()

            is_becoming_open = True
            if self.instance and self.instance.status == 'OPEN':
                is_becoming_open = False

            if is_becoming_open and open_count >= 10:
                raise serializers.ValidationError(
                    "У вас не может быть больше 10 открытых объявлений."
                )

        return data
