import requests
from bs4 import BeautifulSoup

def fetch_latest_result():
    try:
        url = 'https://hgzy.pages.dev/'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # প্রথম .list div এর সব .row এলিমেন্ট বের করো
        rows = soup.select('.list .row')
        if not rows or len(rows) == 0:
            raise ValueError("No result rows found on the page.")

        latest_row = rows[0]  # প্রথম (সর্বশেষ) row

        number_elem = latest_row.select_one('.num')
        color_elem = latest_row.select_one('.color')

        if number_elem is None or color_elem is None:
            raise ValueError("Number or Color element missing.")

        number = number_elem.text.strip()
        color = color_elem.text.strip().lower()

        return int(number), color
    except Exception as e:
        print(f"[ERROR] Scraping failed: {e}")
        return None, None
