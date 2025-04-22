import praw, os
import pandas as pd

from datetime import datetime, timezone
# from dotenv import load_dotenv

def run_reddit_etl():

    """
    Function to extract data from Reddit and load it into a CSV file.
    """

    reddit = praw.Reddit(
        client_id="Bi4xfiEOE9H8BS9YDmXZmw",
        client_secret="kdoUUfXYo3JyJjv_x8KvAquQ6yhNCA",
        user_agent="etl_redit"
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
