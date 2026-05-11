import feedparser
import json
from html import unescape
import re

RSS_POLSKA = "https://www.polsatnews.pl/rss/polska.xml"
RSS_WORLD = "https://www.polsatnews.pl/rss/swiat.xml"

MAX_ITEMS = 5


def clean(text):

    text = unescape(text)

    text = re.sub(r'<.*?>', '', text)

    text = re.sub(r'\s+', ' ', text)

    return text.strip()


def fetch_feed(url):

    feed = feedparser.parse(url)

    items = []

    for entry in feed.entries[:MAX_ITEMS]:

        text = entry.get("description", "")

        text = clean(text)

        if text:
            items.append(text)

    return items


result = {
    "polska": fetch_feed(RSS_POLSKA),
    "world": fetch_feed(RSS_WORLD)
}


with open("rss.json", "w", encoding="utf-8") as f:

    json.dump(
        result,
        f,
        ensure_ascii=False,
        indent=2
    )

print("rss.json generated")
