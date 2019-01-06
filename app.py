import praw
import PyRSS2Gen as rss
import datetime as dt

from secrets import secret_params

def get_top(subreddit, r, limit):
    sub = r.subreddit(subreddit)
    return sub.top('week', limit=limit)


def post_to_rss(post):
    return rss.RSSItem(
        title=post.title,
        link=post.permalink,
        description=post.selftext,
        author=post.author.name,
        guid=post.id,
        pubDate=dt.datetime.utcfromtimestamp(post.created_utc),
    )


def top_rss(subreddit, r, limit=10):
    return rss.RSS2(
        title=f'Top /r/{subreddit} posts',
        link=f'https://reddit.com/r/{subreddit}/top',
        description=f'Top posts from /r/{subreddit}',
        lastBuildDate=dt.datetime.utcnow(),
        items=[
            post_to_rss(post) for post in
            get_top(subreddit, reddit, limit)
        ]
    )

if __name__ == '__main__':
    reddit = praw.Reddit(**secret_params)
    reddit.read_only = True

    print(top_rss('churning', reddit).to_xml())
