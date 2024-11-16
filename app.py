from email_service import get_gmail_service,get_latest_email
from x_service import get_x_client,post_tweets
from utils import get_essay,get_twitter_thread,get_tweet_summary
from dotenv import load_dotenv
import os
import schedule
import time
import datetime

load_dotenv()

TOGETHER_API_KEY = os.getenv('TOGETHER_API_KEY')
CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

MAIL_QUERY="from:morning@finshots.in is:unread newer_than:1d"
load_dotenv()

gmail_client = get_gmail_service()

def tweet_extract(source):
    try:
        email_content = get_latest_email(service=get_gmail_service(), q=MAIL_QUERY)
        if(email_content == None):
            return
        essay = get_essay(email_content,TOGETHER_API_KEY)
        twitter_thread = get_twitter_thread(essay=essay,source=source, api_key=TOGETHER_API_KEY)
        final_thread = []
        for tweet in twitter_thread.tweets:
            if(len(tweet)>260):
                final_thread.append(get_tweet_summary(tweet=tweet,charlen=260,api_key=TOGETHER_API_KEY))
            else:
                final_thread.append(tweet)
        return final_thread        
    except Exception as e:
        print("Excpetion occured ",e)

def post_summary_x(source):
    # Post only on weekdays
    current_day = datetime.datetime.now().strftime("%A")
    if(current_day == 'Saturday' or current_day == 'Sunday'):
        return
    all_tweets = tweet_extract(source)
    if (all_tweets!=None):
        x_client = get_x_client(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_TOKEN,ACCESS_TOKEN_SECRET)
        post_tweets(x_client,all_tweets)

# Run everyday at 18:00 IST
schedule.every().day.at("18:00", "Asia/Calcutta").do(post_summary_x, source="Finshots")

while True:
    schedule.run_pending()
    time.sleep(1)