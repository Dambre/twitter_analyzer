
from hashbattle.local_settings import *

import tweepy
import pytz
from datetime import datetime


def auth():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
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
 
