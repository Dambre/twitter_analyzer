from .models import Battle
from rest_framework import serializers

class BattleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Battle
        fields = ('id', 'hashtag1', 'hashtag1_score','hashtag2', 'hashtag2_score', 'score', 'start_time', 'end_time', 'winner')

        