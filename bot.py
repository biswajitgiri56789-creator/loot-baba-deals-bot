import json
import random
import requests
import os
from config import CHANNEL_ID, AMAZON_STORE_ID
from deals_source import deals

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

def load_posted():
    with open("posted_deals.json", "r") as f:
        return json.load(f)

def save_posted(data):
    with open("posted_deals.json", "w") as f:
        json.dump(data, f)

def add_affiliate(link):
    if "?" in link:
        return f"{link}&tag={AMAZON_STORE_ID}"
    return f"{link}?tag={AMAZON_STORE_ID}"

posted = load_posted()
available = [d for d in deals if d["id"] not in posted]

if not available:
    print("No new deals available.")
    exit()

deal = random.choice(available)

message = f"""🔥 Loot Deal Alert 🔥

🛒 Product: {deal['title']}
💰 Price: {deal['price']}
❌ MRP: {deal['mrp']}

👉 Buy Now: {add_affiliate(deal['link'])}

⏰ Limited Time Offer
"""

requests.post(API_URL, data={
    "chat_id": CHANNEL_ID,
    "text": message
})

posted.append(deal["id"])
save_posted(posted)

print("Deal posted successfully")