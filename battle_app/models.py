
import uuid
import pytz

from django.utils import timezone
from datetime import datetime
from django.db import models


class Word(models.Model):
    id = models.UUIDField(primary_key=True, 
        default=uuid.uuid4, editable=False)
    word = models.CharField(max_length=140, unique=True)
    total_number = models.IntegerField(default=0)
    is_synonym = models.BooleanField(default=False)
    is_hashtag = models.BooleanField(default=False)
    last_tweet_id = models.CharField(max_length=50, default='0')
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('-updated_at',)

    def __str__(self):
        return self.word

    def save(self, *args, **kwargs):
        if self.word[0] == '#':
            self.is_hashtag = True
        self.word = self.word.lower()
        self.updated_at = timezone.now()
        super(Word, self).save(*args, **kwargs)
    
    def update_latest_id(self, tweet_id):
        if int(self.last_tweet_id) < tweet_id:
            self.last_tweet_id = str(tweet_id)
        self.save()

class Synonym(models.Model):
    synonym_to = models.ForeignKey(Word, related_name='synonyms')

class WordUsage(models.Model):
    word = models.ForeignKey(Word)
    retweets = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    timestamp = models.DateTimeField()

    def __str__(self):
        return self.word.word


class Setting(models.Model):
    key = models.CharField(max_length=200, unique=True)
    value = models.CharField(max_length=200)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.key

    def activate(self):
        self.active = True
        self.save()
        return 'Setting activated.'

    def deactivate(self):
        self.active = False
        self.save()
        return 'Setting deactivated.'







class Battle(models.Model):
    '''
    Other stuff
    '''
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
