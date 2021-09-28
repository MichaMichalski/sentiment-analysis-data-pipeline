import psycopg2
import select
import logging
import requests

# this could be any kind of slack webhook
slackurl = 'https://hooks.slack.com/services/xxxxx/xxxxx'

# dbname should be the same for the listening process
conn = psycopg2.connect(host="mypg", dbname="twittereloncrypto", user="postgres", password=1234)

cur = conn.cursor()
conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

cur.execute("LISTEN new_id;")
logging.critical("Waiting for notifications on channel 'new_id'")

while True:
    if select.select([conn], [], [], 10) == ([], [], []):
        logging.critical("More than 10 seconds passed...")
    else:
        conn.poll()
        while conn.notifies:
            notify = conn.notifies.pop(0)
            logging.critical(f"Got NOTIFY: {notify.channel} - {notify.payload}")
            cur.execute(
                """
                SELECT * FROM tweets WHERE id = %s
                """
            , (notify.payload,))
            result = cur.fetchone()
            postbody = {'text': result[1] + ' - sentiment: ' + str(result[5])}
            res = requests.post(slackurl, json=postbody)
