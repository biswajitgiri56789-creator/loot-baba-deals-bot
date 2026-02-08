import os
import json
import requests
from datetime import datetime
from deals_source import fetch_real_deals

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
AMAZON_STORE_ID = os.getenv("AMAZON_STORE_ID")

POSTED_FILE = "posted.json"


def load_posted():
    if not os.path.exists(POSTED_FILE):
        return []
    with open(POSTED_FILE, "r") as f:
        return json.load(f)


def save_posted(data):
    with open(POSTED_FILE, "w") as f:
        json.dump(data, f)


def build_affiliate_link(asin):
    return f"https://www.amazon.in/gp/product/{asin}?tag={AMAZON_STORE_ID}"


def is_valid_product(asin):
    url = f"https://www.amazon.in/dp/{asin}"
    r = requests.get(url, allow_redirects=True, timeout=15)
    return r.status_code == 200 and "dog" not in r.url.lower()


def format_message(asin, link):
    return (
        "🔥 *Loot Baba New Deal!* 🔥\n\n"
        f"🛒 Amazon Product ASIN: `{asin}`\n\n"
        f"👉 *Buy Now:*\n{link}\n\n"
        "⚡ Limited Time Deal\n"
        "📦 Amazon Verified"
    )


def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHANNEL_ID,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False
    }
    requests.post(url, json=payload, timeout=20).raise_for_status()


def main():
    posted = load_posted()
    asins = fetch_real_deals()

    for asin in asins:
        if asin in posted:
            continue

        if not is_valid_product(asin):
            continue

        link = build_affiliate_link(asin)
        message = format_message(asin, link)
        send_to_telegram(message)

        posted.append(asin)
        save_posted(posted)

        print("Posted:", asin, datetime.now())
        break


if __name__ == "__main__":
    main()
