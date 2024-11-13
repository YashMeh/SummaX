from email_service import get_gmail_service,get_latest_email
from x_service import get_x_client,post_tweets
from utils import get_essay,get_twitter_thread,get_tweet_summary
from dotenv import load_dotenv
import os

load_dotenv()

TOGETHER_API_KEY = os.getenv('TOGETHER_API_KEY')
CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

MAIL_QUERY="from:mehrotra.yash9@gmail.com newer_than:1d"
load_dotenv()

gmail_client = get_gmail_service()

def tweet_extract():
    email_content = get_latest_email(service=get_gmail_service(), q=MAIL_QUERY)
    if(email_content == None):
        return
    essay = get_essay(email_content,TOGETHER_API_KEY)
    twitter_thread = get_twitter_thread(essay=essay,api_key=TOGETHER_API_KEY)
    final_thread = []
    for tweet in twitter_thread.tweets:
        if(len(tweet)>260):
            final_thread.append(get_tweet_summary(tweet=tweet,charlen=260,api_key=TOGETHER_API_KEY))
        else:
            final_thread.append(tweet)
    return final_thread

all_tweets = tweet_extract()
x_client = get_x_client(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_TOKEN,ACCESS_TOKEN_SECRET)
post_tweets(x_client,all_tweets)