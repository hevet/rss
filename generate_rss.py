import requests
import json
import re
from html import unescape

RSS_POLSKA = "https://www.polsatnews.pl/rss/polska.xml"
RSS_WORLD = "https://www.polsatnews.pl/rss/swiat.xml"

MAX_ITEMS = 5


def clean(text):

    text = unescape(text)

    text = re.sub(r'<.*?>', '', text)

    text = re.sub(r'\s+', ' ', text)

    return text.strip()


def fetch_feed(url):

    response = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0"
        },
        timeout=10
    )

    xml = response.text

    items = []

    matches = re.findall(
        r'<description><!\[CDATA\[(.*?)\]\]></description>',
        xml,
        re.DOTALL
    )

    for m in matches[:MAX_ITEMS]:

        text = clean(m)

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
