import feedparser
import requests
import json
import os
import re

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Feed RSS da monitorare
RSS_FEEDS = [
    "https://www.subito.it/annunci-italia/vendita/usato/?q=new+3ds&shp=true&rss=true",
    "https://www.subito.it/annunci-italia/vendita/usato/?q=new+3ds+xl&shp=true&rss=true",
    "https://www.subito.it/annunci-italia/vendita/usato/?q=2ds+xl&shp=true&rss=true",
    "https://www.subito.it/annunci-italia/vendita/usato/?q=dsi+xl&shp=true&rss=true",
    "https://www.subito.it/annunci-italia/vendita/usato/?q=ds+lite&shp=true&rss=true",
    "https://www.subito.it/annunci-italia/vendita/usato/?q=lotto+nintendo&shp=true&rss=true"
]

# Prezzi massimi per alert
MAX_PRICES = {
    "new 3ds": 130,
    "new 3ds xl": 140,
    "2ds xl": 120,
    "dsi xl": 70,
    "ds lite": 45,
    "lotto nintendo": 150
}

# Parole PREMIUM
PRIORITY_WORDS = [
    "pokemon",
    "zelda",
    "animal crossing",
    "fire emblem",
    "monster hunter",
    "limited",
    "edition"
]

# Parole da ignorare
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

SEEN_FILE = "seen.json"

# Carica annunci già visti
try:
    with open(SEEN_FILE, "r") as f:
        seen = json.load(f)
except:
    seen = []

new_seen = seen.copy()

# Funzione invio Telegram
def send_telegram(message):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": message
        }
    )

# Analizza feed
for feed_url in RSS_FEEDS:

    feed = feedparser.parse(feed_url)

    for entry in feed.entries[:10]:

        title = entry.title.lower()
        link = entry.link

        # Evita duplicati
        if link in seen:
            continue

        # Ignora parole inutili
        if any(word in title for word in IGNORE_WORDS):
            continue

        # Estrai prezzo
        price_match = re.search(r'(\d+)', title)

        if price_match:
            price = int(price_match.group(1))
        else:
            price = 9999

        should_send = False

        # Controllo prezzi
        for keyword, max_price in MAX_PRICES.items():

            if keyword in title and price <= max_price:
                should_send = True

        # Priority words = manda sempre
        if any(word in title for word in PRIORITY_WORDS):
            should_send = True

        if should_send:

            message = (
                f"🔥 OCCASIONE FLIPPING\n\n"
                f"{entry.title}\n\n"
                f"{link}"
            )

            send_telegram(message)

            new_seen.append(link)

# Salva ultimi annunci
with open(SEEN_FILE, "w") as f:
    json.dump(new_seen[-500:], f)
