import requests
from common_utils import download_image
import os
from pathlib import Path
from main import load_dotenv


PHOTOS_COUNT = 30

def fetch_nasa_apod_photos(api_key: str, photos_count: int = PHOTOS_COUNT):

    api_url = "https://api.nasa.gov/planetary/apod"
    params = {
        "api_key": api_key,
        "count": photos_count
    }

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        apod_response = response.json()
    except requests.RequestException as e:
        print(f"Ошибка при получении данных NASA APOD: {e}")
        return

    photo_urls = []
    if isinstance(apod_response, list):
        for item in apod_response:
            url = item.get("url")
            if url:
                photo_urls.append(url)
    else:
        url = apod_response.get("url")
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
    api_key = os.getenv("NASA_API_KEY")
    fetch_nasa_apod_photos(api_key)
