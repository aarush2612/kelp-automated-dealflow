import requests
from bs4 import BeautifulSoup


def scrape_homepage_summary(url: str) -> str:
    """
    Extracts a short descriptive paragraph from company website.
    Used only for enrichment, not core facts.
    """
    try:
        r = requests.get(url, timeout=8)
        soup = BeautifulSoup(r.text, "html.parser")

        p = soup.find("p")
        return p.get_text(strip=True) if p else ""
    except Exception:
        return ""
