from django.contrib.auth.models import Group
from rest_framework import serializers
from apps.account.models import User

class AccountGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id',
                  'name')


class AccountTokenSerializer(serializers.ModelSerializer):
    groups = AccountGroupSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('uuid',
                  'first_name',
                  'last_name',
                  'groups')