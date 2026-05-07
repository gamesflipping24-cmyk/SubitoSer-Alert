import feedparser
import requests
import json
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

RSS_FEEDS = [
    "https://www.subito.it/annunci-italia/vendita/usato/?q=new+3ds+xl&shp=true&rss=true"
]

SEEN_FILE = "seen.json"

# TEST TELEGRAM IMMEDIATO
requests.post(
    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
    data={
        "chat_id": CHAT_ID,
        "text": "✅ TEST TELEGRAM OK"
    }
)

try:
    with open(SEEN_FILE, "r") as f:
        seen = json.load(f)
except:
    seen = []

new_seen = seen.copy()

for feed_url in RSS_FEEDS:
    feed = feedparser.parse(feed_url)

    for entry in feed.entries[:10]:
        link = entry.link

        if link not in seen:
            title = entry.title

            message = f"🔥 Nuovo annuncio\n\n{title}\n\n{link}"

            requests.post(
                f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                data={
                    "chat_id": CHAT_ID,
                    "text": message
                }
            )

            new_seen.append(link)

with open(SEEN_FILE, "w") as f:
    json.dump(new_seen[-200:], f)
