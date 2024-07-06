import tweepy
import datetime
import pandas as pd
import numpy as np
from datetime import timedelta
import os
from dotenv import load_dotenv

load_dotenv()
BEARER_TOKEN = os.getenv('BEARER_TOKEN')


def get_tweets():

    client = tweepy.Client(bearer_token=BEARER_TOKEN)

    # fetch previous day tweet
    date = datetime.datetime.now() - timedelta(days=1, hours=5.51)
    start_time = date.strftime('%Y-%m-%dT00:00:00Z')

    today = datetime.datetime.now() - timedelta(hours=5.51)
    end_time = today.strftime('%Y-%m-%dT%H:%M:%SZ')

    queries = ['mumbairains -is:retweet', 'mumbairain -is:retweet', 'mumbaiflood -is:retweet']

    all_tweets = []
    for query in queries :
        print(f"Fetching tweets for query: {query}---------------------------------------------------------")
        tweets = client.search_recent_tweets(query=query, tweet_fields=['conversation_id','created_at','text'], start_time=start_time, end_time=end_time, max_results=10)
        print(f"Total tweets fetched: {tweets.data}")
        if tweets.data:
            for tweet in tweets.data:
                print(f"{tweet} \n")
                all_tweets.append(tweet.text)

    return all_tweets

