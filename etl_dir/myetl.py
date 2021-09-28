from time import time
import pymongo
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
# import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import logging
import traceback
import time

time.sleep(2)

s = SentimentIntensityAnalyzer()
client = pymongo.MongoClient(host='mongodb', port=27017, replicaset='my-replica-set')

def connect_db(databasename):
    dbconn = psycopg2.connect(
                host='mypg',
                port=5432,
                database=databasename,
                password=1234,
                user='postgres'
            )
    return dbconn

while True:
    try:
        dbconn = connect_db('twittereloncrypto')
        break
    except psycopg2.OperationalError:
        conn = connect_db('postgres')
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        thecur = conn.cursor()
        thecur.execute('create database twittereloncrypto;')

cur = dbconn.cursor()

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS tweets(
        id SERIAL PRIMARY KEY,
        tweet_text TEXT,
        username VARCHAR(100),
        followers_count INTEGER,
        tweet_id BIGINT,
        sentiment FLOAT
    );
    """
)
dbconn.commit()

db = client.twittereloncrypto
counter = 0
while True:
    try:
        with db.tweets.watch([{'$match': {'operationType': 'insert'}}]) as stream:
            for insert_change in stream:
                change = insert_change['fullDocument']
                result = s.polarity_scores(change['text'])
                compound = result['compound']
                sql = """
                INSERT INTO tweets (tweet_text, username, followers_count, tweet_id, sentiment) VALUES (%s, %s, %s, %s, %s);
                """
                cur.execute(sql, (change['text'],change['username'], change['followers_count'], change['id'], compound))
                dbconn.commit()
                logging.critical('new tweet inserted')
    except pymongo.errors.PyMongoError as e:
        logging.critical('PyMongoError happened')
        logging.critical(e)
        logging.critical(traceback.print_exc())
        client = pymongo.MongoClient(host='mongodb', port=27017)
        db = client.twittereloncrypto
        if counter >= 5:
            break
        else:
            time.sleep(1)
            counter += 1