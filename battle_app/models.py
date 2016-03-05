
import uuid
import pytz

from datetime import datetime
from django.db import models


class Battle(models.Model):
    id = models.UUIDField(primary_key=True, 
        default=uuid.uuid4, editable=False)
    hashtag1 = models.CharField(max_length=200)
    hashtag2 = models.CharField(max_length=200)
    hashtag1_score = models.IntegerField(default=0)
    hashtag2_score = models.IntegerField(default=0)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    updated_time = models.DateTimeField(null=True, blank=True)
    score = models.CharField(max_length=10, blank=True)
    winner = models.CharField(max_length=200, blank=True)
    ended = models.BooleanField(default=False)

    def __str__(self):
        return '%s vs %s' % (self.hashtag1, self.hashtag2)

    def save(self, *args, **kwargs):
        #define humanized score
        self.score = '%d:%d' % (self.hashtag1_score, self.hashtag2_score)
        
        #define humanized winner
        if self.hashtag1_score>self.hashtag2_score:
            self.winner = self.hashtag1
        elif self.hashtag1_score<self.hashtag2_score:
            self.winner =  self.hashtag2
        else:
            self.winner = 'None, Both or Tie'
        
        #fix if provided hashtag is not hashtagish
        if self.hashtag1[0]!='#':
            self.hashtag1 = '#' + self.hashtag1
        if self.hashtag2[0]!='#':
            self.hashtag2 = '#' + self.hashtag2
        #set if battle is ended
        if self.end_time <= pytz.utc.localize(datetime.now()):
            self.ended = True
        else:
            self.ended = False
        super(Battle, self).save(*args, **kwargs)
