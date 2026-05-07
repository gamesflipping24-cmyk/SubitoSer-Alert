import feedparser
import requests
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

RSS_FEED = "https://www.subito.it/annunci-italia/vendita/usato/?q=new+3ds+xl&rss=true"

feed = feedparser.parse(RSS_FEED)

message = f"Trovati {len(feed.entries)} annunci"

requests.post(
    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
    data={
        "chat_id": CHAT_ID,
        "text": message
    }
)
