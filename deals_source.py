import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

AMAZON_DEALS_URL = "https://www.amazon.in/gp/goldbox"


def fetch_real_deals():
    r = requests.get(AMAZON_DEALS_URL, headers=HEADERS, timeout=20)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")
    products = []

    for item in soup.select("div[data-asin]"):
        asin = item.get("data-asin")
        if asin and len(asin) == 10:
            products.append(asin)

    return list(dict.fromkeys(products))  # unique ASINs
