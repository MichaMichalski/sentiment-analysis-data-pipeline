# Sentiment Analysis - Data Pipeline

Goal of this project is to extract tweets from twitter related to Elon Musk with keywords that are in relation to cryptocurrencies and perform sentiment analysis on it and do a HTTP request in order to send the results to slackbot or any kind of HTTP endpoint.

### Requirements

- Docker/ docker-compose

(This is the placeholder for a chart describing the infrastructure)

#### 1. Tweet stream

With help of the `tweepy` library I listen (via websocket integration) to certain tweets and insert them in mongodb.

#### 2. ETL (Extract, Transform, Load)

In order to create an action-based CDC (Change Data Capture) Strategy I decided to create a trigger inside mongodb in order to react to new inserts.
For mongodb to be able to perform such task it needs to instantiate a change log. This only happens when at least 3 instantiations of mongodb create a cluster and are assigned to the same replica-set.

As soon as a new tweet is inserted in mongodb. I perform sentiment Analysis on it with help of the `vaderSentiment` library.

After the sentimen Analysis I save the tweet with addition of the analysis result in a `PostgreSQL` database.

#### 3. Forward them to slackbot (or any kind of HTTP endpoint)

In this step it's all about retrieving all of the results an sending them to its destination.

##### 3.1 PostgreSQL listener

I decided to stick to the action-based CDC so I had to create a trigger function inside the `PostgreSQL` Server. This serves as a listener.

##### 3.2 PostgreSQL notifier

The notifier will be the action triggered after a listner has performed some action/ retrieved new data.

It's also the job of the notifier to send the HTTP request and therefore send the data to its destination.