# -*- coding: utf-8 -*-

from django.conf import settings

import tweepy
import pytz
from datetime import datetime
from .models import WordUsage, Word
from .get_dictionary import exclude_by_type

def auth():
    auth = tweepy.OAuthHandler(settings.consumer_key, settings.consumer_secret)
    auth.set_access_token(settings.access_token, settings.access_token_secret)
    return auth

api = tweepy.API(auth())

def count_hash(hashtags, start_time, end_time, updated_time, count=100, result_type='recent'):
    '''
    q (required)
    A UTF-8,URL-encoded search query of 500 characters maximum, 
    including operators. Queries may additionally be limited by complexity.
    count (optional)
    The number of tweets to return per page, up to a maximum of 100. 
    Defaults to 15. This was formerly the “rpp” parameter in the old Search API.
    '''
    #this check will help avoid 100 max search results 
    if updated_time:    
        start_time=updated_time 

    hash_count = {}
    for hashtag in hashtags:
        tweets = api.search(q=hashtag, count=count, result_type=result_type)
        number = 0
        for tweet in tweets:
            print(tweet.text)
            tweet_created = pytz.utc.localize(tweet.created_at) #make a naive datetime timezone-aware
            if (tweet_created>=start_time) and (tweet_created<=end_time):
                number+=1
        hash_count[hashtag] = number   
    updated_time = pytz.utc.localize(datetime.now()) 
    return hash_count, updated_time
 
def get_word_statistics(search_word):
    '''
    get tweets with this word
    '''
    try:
        word = Word.objects.get(word=search_word)
        last_tweet_id = int(word.last_tweet_id)
        tweets = api.search(
            q=word.word,
            count=100,
            result_type='recent',
            since_id=last_tweet_id)
    except Exception:
        tweets = []

    for tweet in tweets:
        print(tweet.text)
        if last_tweet_id < tweet.id:
            last_tweet_id = tweet.id
        words = exclude_by_type(tweet.text)
        for tweet_word in words:
            try:
                word = Word.objects.get(word=tweet_word.lower())
            except Word.DoesNotExist:
                word = Word.objects.create(word=tweet_word, last_tweet_id=tweet.id)
            WordUsage.objects.create(
                word=word,
                retweets=tweet.retweet_count,
                likes=tweet.favorite_count,
                timestamp=pytz.utc.localize(tweet.created_at))

    word = Word.objects.get(word=search_word)
    word.update_latest_id(last_tweet_id)


