import requests
from bs4 import BeautifulSoup
import json
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

SEARCH_URLS = [
    "https://www.subito.it/annunci-italia/vendita/usato/?q=new+3ds+xl",
    "https://www.subito.it/annunci-italia/vendita/usato/?q=new+3ds",
    "https://www.subito.it/annunci-italia/vendita/usato/?q=2ds+xl",
    "https://www.subito.it/annunci-italia/vendita/usato/?q=dsi+xl",
    "https://www.subito.it/annunci-italia/vendita/usato/?q=lotto+nintendo"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

SEEN_FILE = "seen.json"

IGNORE_WORDS = [
    "custodia",
    "cover",
    "case",
    "ricambi",
    "accessori"
]

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

for url in SEARCH_URLS:

    response = requests.get(url, headers=HEADERS)

    soup = BeautifulSoup(response.text, "html.parser")

    links = soup.find_all("a")

    for link in links:

        href = link.get("href")

        if not href:
            continue

        if "/videogiochi/" not in href:
            continue

        title = link.get_text(strip=True)

        if not title:
            continue

        title_lower = title.lower()

        if any(word in title_lower for word in IGNORE_WORDS):
            continue

        full_link = href

        if full_link in seen:
            continue

        message = f"🔥 NUOVO ANNUNCIO\n\n{title}\n\n{full_link}"

        send_telegram(message)

        new_seen.append(full_link)

with open(SEEN_FILE, "w") as f:
    json.dump(new_seen[-500:], f)
