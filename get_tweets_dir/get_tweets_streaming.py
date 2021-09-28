import twitter_credentials as config
from tweepy import OAuthHandler, Stream
from tweepy.streaming import StreamListener
import logging
import pymongo
import time

time.sleep(2)

buzzwords = ['crypto', 'bitcoin', 'btc', 'dogecoin', 'doge']

def get_mongo():
    client = pymongo.MongoClient(host='mongodb', port=27017, replicaset='my-replica-set')
    return client

def authenticate():
    """Function for handling Twitter Authentication. Please note
       that this script assumes you have a file called config.py
       which stores the 4 required authentication tokens:

       1. API_KEY
       2. API_SECRET
       3. ACCESS_TOKEN
       4. ACCESS_TOKEN_SECRET

    See course material for instructions on getting your own Twitter credentials.
    """
    auth = OAuthHandler(config.api_key, config.api_secret)
    auth.set_access_token(config.access_token, config.access_token_secret)

    return auth

class MyTweetListener(StreamListener):

    def on_status(self, status):
        if hasattr(status, 'extended_tweet'):
            text = status.extended_tweet['full_text']
        else:
            text = status.text
        text = text.replace('\n', ' ')
        tweet = {
            'text': text,
            'username': status.user.screen_name,
            'followers_count': status.user.followers_count,
            'id': status.id
        }
        if any(word in text for word in buzzwords):
            while True:
                try:
                    db = client.twittereloncrypto
                    db.tweets.insert_one(tweet)
                    break
                except (pymongo.errors.PyMongoError, UnboundLocalError):
                    logging.critical('PyMongoError - Probably not Primary')
                    client = get_mongo()

    def on_error(self, status):
        print('error happened')
        print(status)
        if status == 420:
            print(f'Rate limit applies. Stop the stream.')
            return False

if __name__ == '__main__':
    auth = authenticate()
    listener = MyTweetListener()
    stream = Stream(auth, listener, tweet_mode='extended')
    # 44196397 is the twitter ID of Elon Musk
    stream.filter(follow=['44196397'], languages=['en'], is_async=False)