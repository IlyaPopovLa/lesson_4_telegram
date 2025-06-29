import requests
from pathlib import Path
from datetime import datetime
from common_utils import download_image, load_env
import os


def fetch_nasa_epic_photos():
    api_key = os.getenv("NASA_API_KEY")

    api_url = "https://api.nasa.gov/EPIC/api/natural/images"
    params = {"api_key": api_key}

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        print(f"Ошибка при получении данных NASA EPIC: {e}")
        return

    folder = Path("images")
    folder.mkdir(parents=True, exist_ok=True)

    for item in data:
        date_str = item.get("date")
        image_name = item.get("image")

        if not date_str or not image_name:
            continue

        dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")

        image_url = (
            f"https://epic.gsfc.nasa.gov/archive/natural/"
            f"{dt.year}/{dt.month:02}/{dt.day:02}/png/{image_name}.png"
        )

        filename = folder / f"{image_name}.png"
        download_image(image_url, filename)


if __name__ == "__main__":
    load_env()
    fetch_nasa_epic_photos()
