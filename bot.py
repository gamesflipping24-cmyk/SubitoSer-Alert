from playwright.sync_api import sync_playwright
import requests
import json
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

URL = "https://www.subito.it/annunci-italia/vendita/usato/?q=new+3ds+xl"

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

with sync_playwright() as p:

    browser = p.chromium.launch(headless=True)

    page = browser.new_page()

    page.goto(URL, timeout=60000)

    page.wait_for_timeout(7000)

    links = page.locator("a").evaluate_all("""
        elements => elements.map(el => ({
            href: el.href,
            text: el.innerText
        }))
    """)

    found = 0

    for item in links:

        href = item.get("href", "")
        title = item.get("text", "").strip()

        # Ignora link vuoti
        if not href:
            continue

        # SOLO link subito reali
        if "subito.it" not in href:
            continue

        # Evita roba inutile
        if len(title) < 10:
            continue

        # Evita duplicati
        if href in seen:
            continue

        found += 1

        message = f"🔥 NUOVO ANNUNCIO\n\n{title}\n\n{href}"

        send_telegram(message)

        new_seen.append(href)

    browser.close()

send_telegram(f"✅ Scan completato - trovati {found} annunci")

with open(SEEN_FILE, "w") as f:
    json.dump(new_seen[-500:], f)
