from .tweet.process_tweets import process_tweet
from .tweet.fetch_tweets import get_tweets
import datetime

from .models import Tweet

def store_tweets():
    tweets = get_tweets()

    new_tweets = []
    for tweet in tweets:
        processed_tweet = process_tweet(tweet)

        for location in processed_tweet["locations"]:
            new_tweets.append(
                Tweet.objects.create(
                    text=processed_tweet["text"],
                    date=datetime.datet.today(),
                    sentiment=processed_tweet["sentiment"]=="POSITIVE",
                    latitude=location[0],
                    longitude=location[1]
                )
            )
    
    return new_tweets
