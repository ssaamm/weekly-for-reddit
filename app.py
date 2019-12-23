import datetime as dt

import praw
import PyRSS2Gen as rss
from flask import Flask, request
from markdown import markdown

from secrets import secret_params

app = Flask(__name__)
reddit = praw.Reddit(**secret_params)
reddit.read_only = True


def get_top(subreddit, r, limit):
    sub = r.subreddit(subreddit)
    return sub.top("week", limit=limit)


def render_description(selftext, link):
    if selftext:
        return markdown(selftext)
    if any(link.endswith(suffix) for suffix in ("jpg", "png", "gif")):
        return f'<img src="{link}">'
    return f'<a href="{link}">Link</a>'


def post_to_rss(post):
    return rss.RSSItem(
        title=post.title,
        link=post.permalink,
        description=render_description(post.selftext, post.url),
        author=post.author.name,
        guid=post.id,
        pubDate=dt.datetime.utcfromtimestamp(post.created_utc),
    )


def top_rss(subreddit, r, limit=10):
    return rss.RSS2(
        title=f"Top /r/{subreddit} posts",
        link=f"https://reddit.com/r/{subreddit}/top",
        description=f"Top {limit} posts from /r/{subreddit}",
        lastBuildDate=dt.datetime.utcnow(),
        items=[post_to_rss(post) for post in get_top(subreddit, reddit, limit)],
    )


@app.route("/sub/<name>")
def create_feed(name):
    try:
        limit = int(request.args.get("limit", "10"))
    except ValueError:
        limit = 10
    return top_rss(name, reddit, limit).to_xml()


if __name__ == "__main__":
    app.run(debug=True)
