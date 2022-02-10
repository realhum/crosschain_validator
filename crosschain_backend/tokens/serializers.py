from rest_framework.fields import CharField, IntegerField
from rest_framework.serializers import ModelSerializer

from .models import Token


class TokenSerializer(ModelSerializer):
    network = CharField(source='network.title')

    class Meta:
        model = Token
        fields = (
            'address',
            'name',
            'symbol',
            'decimals',
            'network',
        )
