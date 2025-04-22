import praw, os
import pandas as pd

from datetime import datetime, timezone
from dotenv import load_dotenv

def run_reddit_etl():

    """
    Function to extract data from Reddit and load it into a CSV file.
    """
    load_dotenv()

    client_id_reddit = os.getenv("CLIENT_ID_REDDIT")
    client_secret_reddit = os.getenv("CLIENT_SECRET_REDDIT")
    user_agent_reddit = os.getenv("USER_AGENT_REDDIT")

    reddit = praw.Reddit(
        client_id=client_id_reddit,
        client_secret=client_secret_reddit,
        user_agent= user_agent_reddit
    )

    subreddit = reddit.subreddit("espresso")

    reddit_posts = []
    for post in subreddit.hot(limit=10):

        new_post = {
            "title": post.title,
            "text": post.selftext,
            "created_at": datetime.fromtimestamp(post.created_utc, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S'),
            "id": post.id,
            "author": post.author.name if post.author else None,
            "link": post.url,
            "comments": post.num_comments,
            "upvotes": post.ups,
        }
        reddit_posts.append(new_post)

    reddit_df = pd.DataFrame(reddit_posts)
    reddit_df.to_csv("s3://reddit-airflow-bucket-otina/reddit_posts.csv", index=False)
