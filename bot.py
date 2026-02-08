import os
import requests
from deals_source import deals

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
AMAZON_STORE_ID = os.getenv("AMAZON_STORE_ID")

POSTED_FILE = "posted_asins.txt"


def load_posted_asins():
    if not os.path.exists(POSTED_FILE):
        return set()
    with open(POSTED_FILE, "r") as f:
        return set(line.strip() for line in f.readlines())


def save_posted_asin(asin):
    with open(POSTED_FILE, "a") as f:
        f.write(asin + "\n")


def generate_amazon_link(asin):
    # PERFECT canonical affiliate link
    return f"https://www.amazon.in/dp/{asin}?tag={AMAZON_STORE_ID}"


def format_message(deal, link):
    discount = ""
    try:
        mrp = int(deal["mrp"].replace("₹", "").replace(",", ""))
        price = int(deal["price"].replace("₹", "").replace(",", ""))
        discount = f"{int(((mrp - price) / mrp) * 100)}% OFF"
    except:
        pass

    return f"""
🔥 *Loot Baba Deal Alert!* 🔥

🛍️ *{deal["title"]}*

💰 Price: *{deal["price"}*
❌ MRP: {deal["mrp"]}
🎯 Discount: *{discount}*

👉 *Buy Now:*
{link}

⚡ Limited Time Deal
📦 Amazon Verified
""".strip()


def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHANNEL_ID,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False
    }
    r = requests.post(url, json=payload)
    return r.status_code == 200


def main():
    posted_asins = load_posted_asins()

    for deal in deals:
        asin = deal.get("asin")

        # Safety checks
        if not asin or len(asin) != 10:
            continue

        if asin in posted_asins:
            continue  # already posted

        link = generate_amazon_link(asin)
        message = format_message(deal, link)

        success = send_telegram_message(message)

        if success:
            save_posted_asin(asin)
            print(f"✅ Posted: {asin}")
            break  # only ONE post per run
        else:
            print("❌ Telegram error")
            break


if __name__ == "__main__":
    main()
