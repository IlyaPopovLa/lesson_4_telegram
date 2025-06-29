from dotenv import load_dotenv
import os
from telegram import Bot

def send_text_to_channel(token: str, channel_id: str, text: str) -> None:
    bot = Bot(token=token)
    bot.send_message(chat_id=channel_id, text=text)

if __name__ == "__main__":
    load_dotenv()
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    CHANNEL_ID = os.getenv("CHANNEL_ID")
    MESSAGE = "Привет! Скоро выложу новые фото космоса"
    send_text_to_channel(TELEGRAM_TOKEN, CHANNEL_ID, MESSAGE)