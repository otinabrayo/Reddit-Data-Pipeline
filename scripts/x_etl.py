import tweepy, json, os
import s3fs
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv


load_dotenv()

bearer_token = os.getenv("BEARER_TOKEN")
access_key = os.getenv("ACCESS_KEY")
access_secret = os.getenv("ACCESS_SECRET")
consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")



'''

# Twitter API v1.1 Authentication Not free version

# X Authentication
auth = tweepy.OAuthHandler(access_key, access_secret)
auth.set_access_token(consumer_key, consumer_secret)

# Creating the API object
api = tweepy.API(auth, wait_on_rate_limit=True)

posts = api.user_timeline(screen_name='@elonmusk',
                          count=20,
                          include_rts=False,
                          tweet_mode='extended')

print(posts)

'''

# Twitter API v2 Authentication (Free version)
# X Authentication

if not bearer_token:
    raise ValueError("Missing Bearer Token!")

# Creating the API object
client = tweepy.Client(bearer_token=bearer_token)

user = client.get_user(username='elonmusk')
user_id = user.data.id

posts = client.get_users_tweets(id=user_id, max_results=100)

posts_list = []
for post in posts:
    posts_list.append(post.data)

