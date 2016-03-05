
from django.core.management.base import BaseCommand, CommandError

from battle_app.models import Battle
from battle_app.twitter import count_hash


class Command(BaseCommand):
    '''
    Class to get hashtags score
    '''
    def handle(self, *args, **kwargs):
        battles = Battle.objects.all()
        for battle in battles:
            hash1 = battle.hashtag1
            hash2 = battle.hashtag2
            count, updated_time = count_hash(
                [hash1, hash2],
                battle.start_time,
                battle.end_time,
                battle.updated_time,
                )
            battle.hashtag1_score += count[hash1]
            battle.hashtag2_score += count[hash2]
            battle.updated_time = updated_time
            battle.save()
            print(battle.score)
        return
if __name__ == '__main__':
    Command.handle()