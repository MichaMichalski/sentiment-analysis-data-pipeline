import twitter_credentials as config
from tweepy import OAuthHandler, Cursor, API
from tweepy.streaming import StreamListener
import logging
import json
from pprint import pprint

def authenticate():
    """Function for handling Twitter Authentication. Please note
       that this script assumes you have a file called config.py
       which stores the 2 required authentication tokens:

       1. API_KEY
       2. API_SECRET
     

    See course material for instructions on getting your own Twitter credentials.
    """
    auth = OAuthHandler(config.api_key, config.api_secret)
    return auth

if __name__ == '__main__':
    auth = authenticate()
    api = API(auth)

    # cursor = Cursor(
    #     api.user_timeline,
    #     id = 'elonmusk',
    #     tweet_mode = 'extended'
    # )

    user = api.get_user('@elonmusk')
    # pprint(user._json)
    for status in user.timeline(count=100):
        text = status.text
        if 'extended_tweet' in dir(status):
            text =  status.extended_tweet.full_text
        if 'retweeted_status' in dir(status):
            r = status.retweeted_status
            if 'extended_tweet' in dir(r):
                text =  r.extended_tweet.full_text
        tweet = {
            'text': text,
            'username': status.user.screen_name,
            'followers_count': status.user.followers_count
        }
        print(tweet['text'])

    # for status in cursor.items(10):
    #     text = status.full_text
    #     print(status)

    #     # take extended tweets into account
    #     # TODO: CHECK
    #     if 'extended_tweet' in dir(status):
    #         text =  status.extended_tweet.full_text
    #     if 'retweeted_status' in dir(status):
    #         r = status.retweeted_status
    #         if 'extended_tweet' in dir(r):
    #             text =  r.extended_tweet.full_text

    #     tweet = {
    #         'text': text,
    #         'username': status.user.screen_name,
    #         'followers_count': status.user.followers_count
    #     }
    #     print(tweet)

