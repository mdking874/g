import requests
from bs4 import BeautifulSoup

def fetch_latest_result():
    try:
        url = 'https://hgzy.pages.dev/'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # ঠিক HTML structure অনুযায়ী সিলেক্ট করো
        history_box = soup.select_one('.list .row')
        if not history_box:
            raise ValueError("Couldn't find result box.")

        number = history_box.select_one('.num').text.strip()
        color = history_box.select_one('.color').text.strip().lower()

        return int(number), color
    except Exception as e:
        print(f"[ERROR] Scraping failed: {e}")
        return None, None
