import feedparser
import requests
import json
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

RSS_FEEDS = [
    "https://www.subito.it/annunci-italia/vendita/usato/?q=new+3ds&shp=true&rss=true",
    "https://www.subito.it/annunci-italia/vendita/usato/?q=new+3ds+xl&shp=true&rss=true",
    "https://www.subito.it/annunci-italia/vendita/usato/?q=2ds+xl&shp=true&rss=true",
    "https://www.subito.it/annunci-italia/vendita/usato/?q=dsi+xl&shp=true&rss=true",
    "https://www.subito.it/annunci-italia/vendita/usato/?q=ds+lite&shp=true&rss=true",
    "https://www.subito.it/annunci-italia/vendita/usato/?q=lotto+nintendo&shp=true&rss=true"
]

IGNORE_WORDS = [
    "custodia",
    "cover",
    "case",
    "ricambi",
    "accessori",
    "joystick",
    "guscio",
    "scocca"
]

PRIORITY_WORDS = [
    "pokemon",
    "zelda",
    "animal crossing",
    "fire emblem",
    "limited",
    "edition"
]

SEEN_FILE = "seen.json"

try:
    with open(SEEN_FILE, "r") as f:
        seen = json.load(f)
except:
    seen = []

new_seen = seen.copy()

def send_telegram(message):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": message
        }
    )

for feed_url in RSS_FEEDS:

    feed = feedparser.parse(feed_url)

    for entry in feed.entries[:10]:

        title = entry.title.lower()
        link = entry.link

        if link in seen:
            continue

        # Ignora spam
        if any(word in title for word in IGNORE_WORDS):
            continue

        priority = any(word in title for word in PRIORITY_WORDS)

        if priority:
            emoji = "⭐"
        else:
            emoji = "🔥"

        message = (
            f"{emoji} NUOVO ANNUNCIO\n\n"
            f"{entry.title}\n\n"
            f"{link}"
        )

        send_telegram(message)

        new_seen.append(link)

with open(SEEN_FILE, "w") as f:
    json.dump(new_seen[-500:], f)
