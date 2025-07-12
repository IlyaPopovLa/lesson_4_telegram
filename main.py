import argparse
import os
import random
import time
from pathlib import Path
from dotenv import load_dotenv
from telegram import Bot


def publish_photos_loop(token: str, channel_id: str, folder: Path, delay_seconds: int):
    bot = Bot(token=token)
    photos = list(folder.glob("*.*"))
    if not photos:
        print(f"В папке {folder} нет фотографий для публикации.")
        return

    while True:
        random.shuffle(photos)
        for photo_path in photos:
            try:
                with open(photo_path, "rb") as photo_file:
                    bot.send_photo(chat_id=channel_id, photo=photo_file)
                print(f"Опубликовано фото: {photo_path.name}")
            except Exception as e:
                print(f"Ошибка при публикации {photo_path.name}: {e}")
            time.sleep(delay_seconds)


def main():
    load_dotenv()

    parser = argparse.ArgumentParser(description="Автопубликация фото в Telegram из папки с интервалом.")
    parser.add_argument(
        "-t", "--token", type=str, default=os.getenv("TELEGRAM_TOKEN"),
        help="Telegram Bot Token (по умолчанию из переменной окружения TELEGRAM_TOKEN)"
    )
    parser.add_argument(
        "-c", "--channel", type=str, default=os.getenv("CHANNEL_ID"),
        help="ID Telegram канала (по умолчанию из переменной окружения CHANNEL_ID)"
    )
    parser.add_argument(
        "-d", "--directory", type=str, default="images",
        help="Путь к директории с фото (по умолчанию 'images')"
    )
    parser.add_argument(
        "-i", "--interval", type=int, default=4,
        help="Интервал публикации в часах (по умолчанию 4)"
    )

    args = parser.parse_args()

    if not args.token or not args.channel:
        print("Ошибка: необходимо указать Telegram токен и ID канала.")
        return

    folder = Path(args.directory)
    delay_seconds = args.interval * 3600

    print(f"Запуск публикации из папки '{folder}', интервал: {args.interval} час(а).")
    publish_photos_loop(args.token, args.channel, folder, delay_seconds)


if __name__ == "__main__":
    main()
