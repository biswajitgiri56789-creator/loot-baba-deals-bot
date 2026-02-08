import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# Example: Mobile phones deals page (GitHub Actions friendly)
SEARCH_URL = "https://www.amazon.in/s?k=mobile+phones&rh=p_n_deal_type%3A26921226031"

def fetch_real_deals():
    """Fetch ASINs from Amazon search results."""
    r = requests.get(SEARCH_URL, headers=HEADERS, timeout=20)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")
    asins = []

    for div in soup.select("div[data-asin]"):
        asin = div.get("data-asin")
        if asin and len(asin) == 10:
            asins.append(asin)

    return list(dict.fromkeys(asins))  # Unique ASINs only
