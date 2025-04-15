import requests
import time
import os
from bs4 import BeautifulSoup
from telegram import Bot

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "7513820233:AAEVLpUVvJqT-CUSUmkusLCYLWKv0NyDzWI")
TELEGRAM_CHANNEL = os.getenv("TELEGRAM_CHANNEL", "@BDT_HACEKR_RAFI")

bot = Bot(token=TELEGRAM_BOT_TOKEN)
previous_round = None

def get_latest_result():
    try:
        response = requests.get("https://hgzy.pages.dev/", timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        latest = soup.select_one(".records .record:nth-child(1)")
        round_text = latest.select_one(".issue").text.strip()
        number_text = latest.select_one(".number span").text.strip()
        return round_text, int(number_text)
    except Exception as e:
        print(f"[ERROR] Scraping failed: {e}")
        return None, None

def predict_color(number):
    if number in [0, 5, 10]:
        return "VIOLET"
    elif number < 5:
        return "GREEN"
    else:
        return "RED"

def send_signal(round_no, prediction):
    msg = f"""🎯 Wingo Prediction 🎯

Round: {round_no}
Signal: {prediction}"""

    bot.send_message(chat_id=TELEGRAM_CHANNEL, text=msg)

def send_result(round_no, prediction, actual_number):
    actual_color = predict_color(actual_number)
    result_msg = f"""📢 Result for Round {round_no}

Signal: {prediction}
Result: {actual_number} ({actual_color})"""

    if prediction == actual_color:
        final_msg = f"মধু মামা মধু!!! 🐝✅\n\n{result_msg}"
    else:
        final_msg = f"আহারে... গেম দিল ধোঁকা! ❌\n\n{result_msg}"

    bot.send_message(chat_id=TELEGRAM_CHANNEL, text=final_msg)

def run_bot():
    global previous_round
    while True:
        round_no, number = get_latest_result()
        if not round_no or not number:
            time.sleep(10)
            continue

        if round_no != previous_round:
            prediction = predict_color(number)
            send_signal(round_no, prediction)
            time.sleep(65)  # Wait for result
            _, actual_number = get_latest_result()
            if actual_number is not None:
                send_result(round_no, prediction, actual_number)
            previous_round = round_no
        else:
            time.sleep(10)

if __name__ == "__main__":
    run_bot()
