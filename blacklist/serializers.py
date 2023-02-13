
from rest_framework import serializers

from blacklist.models import PlayerReport, Game


class PlayerSerializer(serializers.ModelSerializer):
    """ Defines API representation for Player """

    class Meta:
        model = PlayerReport
        fields = ['email', 'reason', 'game']


class GameSerializer(serializers.ModelSerializer):
    """ Defines API representation for Player """

    class Meta:
        model = Game
        fields = ['name']
