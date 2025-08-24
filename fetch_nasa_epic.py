import requests
from pathlib import Path
from datetime import datetime
from common_utils import download_image
from main import load_dotenv
import os


def fetch_nasa_epic_photos(apy_key: str):

    api_url = "https://api.nasa.gov/EPIC/api/natural/images"
    params = {"api_key": api_key}

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        epic_response = response.json()
    except requests.RequestException as e:
        print(f"Ошибка при получении данных NASA EPIC: {e}")
        return

    folder = Path("images")
    folder.mkdir(parents=True, exist_ok=True)

    for item in epic_response:
        date_str = item.get("date")
        image_name = item.get("image")

        if not date_str or not image_name:
            continue

        image_datetime = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")

        image_url = (
            f"https://epic.gsfc.nasa.gov/archive/natural/"
            f"{image_datetime.year}/{image_datetime.month:02}/{image_datetime.day:02}/png/{image_name}.png"
        )

        filename = folder / f"{image_name}.png"
        download_image(image_url, filename)


if __name__ == "__main__":
    load_dotenv()
    api_key = os.getenv("NASA_API_KEY")
    fetch_nasa_epic_photos(api_key)
