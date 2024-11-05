from typing import List
from rest_framework import serializers
from apps.account.models.user import User
from apps.point.services.expired_points_service import ExpiredPointsService


class StatusPointSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name',)

class WidgetSerializer(serializers.ModelSerializer):
    points_to_expire = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id',
                  'points',
                  'points_to_expire',)
