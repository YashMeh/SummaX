import tweepy
import time
import random

def get_x_client(consumer_key,consumer_secret,access_token,access_token_secret):
    client = tweepy.Client(
        consumer_key=consumer_key, consumer_secret=consumer_secret,
        access_token=access_token, access_token_secret=access_token_secret
    )
    return client


def post_tweets(client,tweets):
    try:
        prevTweetId = None
        for currentTweet in tweets:
            time.sleep(random.randrange(1,10))
            if(prevTweetId != None):
                currentTweet = client.create_tweet(text=currentTweet, in_reply_to_tweet_id=prevTweetId)
            else:
                print("b")
                currentTweet = client.create_tweet(text=currentTweet)
            print("Posted : {0}".format(currentTweet))    
            prevTweetId = currentTweet.data['id']
        print("Posted all tweets")
    except Exception as e:
        print("Exception occured while posting ",e)    


# post_tweet(get_x_client(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_TOKEN,ACCESS_TOKEN_SECRET),['test1','base1','set1','math1'])    
