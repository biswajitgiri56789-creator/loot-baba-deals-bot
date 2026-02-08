import os
import json
import requests
from datetime import datetime

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


def fetch_deal():
    # Demo static deal (stable – no broken link)
    return {
        "title": "Bluetooth Wireless Earbuds",
        "price": "₹999",
        "mrp": "₹1,999",
        "asin": "B0C9J8RZ5M"
    }


def build_affiliate_link(asin):
    return f"https://www.amazon.in/dp/{asin}?tag={AMAZON_STORE_ID}"


def format_message(deal, link):
    discount = ""
    try:
        mrp = int(deal["mrp"].replace("₹", "").replace(",", ""))
        price = int(deal["price"].replace("₹", "").replace(",", ""))
        discount = f"{int(((mrp - price) / mrp) * 100)}% OFF"
    except:
        pass

    return (
        "🔥 *Loot Baba Deal Alert!* 🔥\n\n"
        f"🛍️ *{deal['title']}*\n\n"
        f"💰 *Price:* {deal['price']}\n"
        f"❌ *MRP:* {deal['mrp']}\n"
        f"🎯 *Discount:* {discount}\n\n"
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
    r = requests.post(url, json=payload, timeout=20)
    r.raise_for_status()


def main():
    posted = load_posted()
    deal = fetch_deal()

    if deal["asin"] in posted:
        print("Already posted. Skipping.")
        return

    link = build_affiliate_link(deal["asin"])
    message = format_message(deal, link)
    send_to_telegram(message)

    posted.append(deal["asin"])
    save_posted(posted)

    print("Posted successfully at", datetime.now())


if __name__ == "__main__":
    main()
