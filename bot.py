import json
import random
import requests
import os
from config import CHANNEL_ID, AMAZON_STORE_ID
from deals_source import deals

# Telegram Bot Token (from GitHub Secrets)
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"


# ---------- Utility Functions ----------

def load_posted_deals():
    """Load already posted deal IDs"""
    try:
        with open("posted_deals.json", "r") as f:
            return json.load(f)
    except:
        return []


def save_posted_deals(data):
    """Save posted deal IDs"""
    with open("posted_deals.json", "w") as f:
        json.dump(data, f)


def generate_affiliate_link(link):
    """
    Convert any Amazon product link to clean, working affiliate link
    Supports /dp/ and /gp/product/
    """
    asin = None

    if "/dp/" in link:
        asin = link.split("/dp/")[1].split("/")[0]
    elif "/gp/product/" in link:
        asin = link.split("/gp/product/")[1].split("/")[0]

    if not asin:
        return link  # fallback (rare case)

    return f"https://www.amazon.in/dp/{asin}/?tag={AMAZON_STORE_ID}"


def format_post(deal):
    """Create a clean & attractive Telegram post"""
    aff_link = generate_affiliate_link(deal["link"])

    message = (
        "🔥 *Loot Deal Alert* 🔥\n\n"
        f"🛍️ *Product:* {deal['title']}\n"
        f"💰 *Price:* {deal['price']}\n"
        f"❌ *MRP:* {deal['mrp']}\n\n"
        f"👉 *Buy Now:* {aff_link}\n\n"
        "⏰ _Limited Time Offer_\n"
        "📦 _Deal may expire anytime_\n\n"
        "#LootDeals #AmazonDeals #PriceDrop"
    )
    return message


# ---------- Main Logic ----------

posted_deals = load_posted_deals()

# Filter new deals only
available_deals = [d for d in deals if d["id"] not in posted_deals]

if not available_deals:
    print("No new deals available to post.")
    exit()

# Pick one random new deal
deal = random.choice(available_deals)

post_text = format_post(deal)

response = requests.post(
    API_URL,
    data={
        "chat_id": CHANNEL_ID,
        "text": post_text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False
    }
)

if response.status_code == 200:
    posted_deals.append(deal["id"])
    save_posted_deals(posted_deals)
    print("✅ Deal posted successfully.")
else:
    print("❌ Failed to post deal:", response.text)
