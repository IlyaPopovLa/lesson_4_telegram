import requests
from common_utils import download_image
import os
from pathlib import Path
from main import load_dotenv


def fetch_nasa_apod_photos():
    api_key = os.getenv("NASA_API_KEY")

    api_url = "https://api.nasa.gov/planetary/apod"
    params = {"api_key": api_key, "count": 30}

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        print(f"Ошибка при получении данных NASA APOD: {e}")
        return

    photo_urls = []
    if isinstance(data, list):
        for item in data:
            url = item.get("url")
            if url:
                photo_urls.append(url)
    else:
        url = data.get("url")
        if url:
            photo_urls.append(url)

    folder = Path("images")
    folder.mkdir(parents=True, exist_ok=True)

    for num, photo_url in enumerate(photo_urls):
        ext = os.path.splitext(photo_url)[1] or ".jpg"
        filename = folder / f"nasa_{num}{ext}"
        download_image(photo_url, filename)


if __name__ == "__main__":
    load_dotenv()
    fetch_nasa_apod_photos()
