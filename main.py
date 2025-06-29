import os
import requests
from pathlib import Path
from urllib.parse import urlparse
from dotenv import load_dotenv
from datetime import datetime


def get_extension_from_url(url: str) -> str:
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    extension = os.path.splitext(filename)[1]
    return extension


def download_images_spacex(url: str, path: Path) -> None:
    headers = {
        'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/91.0.4472.124 Safari/537.36')
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, 'wb') as file:
        file.write(response.content)


def download_images_nasa(urls: list[str], folder_name: str):
    folder_path = Path(folder_name)
    folder_path.mkdir(parents=True, exist_ok=True)

    for num, image_url in enumerate(urls):
        ext = get_extension_from_url(image_url)
        filename = folder_path / f"nasa_{num + 1}{ext}"
        download_images_spacex(image_url, filename)


def fetch_spacex_last_launch():
    url = "https://api.spacexdata.com/v5/launches/5eb87d47ffd86e000604b38a"
    response = requests.get(url)
    response.raise_for_status()

    data = response.json()
    flickr_photos = data.get("links", {}).get("flickr", {}).get("original", [])

    folder = Path("spacex_images")
    for num, photo_url in enumerate(flickr_photos):
        filename = folder / f"spacex_{num}.jpg"
        download_images_spacex(photo_url, filename)


def fetch_nasa_apod_photos():
    api_key = os.getenv("NASA_API_KEY")

    api_url = "https://api.nasa.gov/planetary/apod"
    params = {"api_key": api_key}

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        data = response.json()
    except (requests.RequestException, ValueError) as e:
        print(f"Ошибка при получении данных NASA: {e}")
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

    if photo_urls:
        download_images_nasa(photo_urls, "nasa_images")


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

    folder = Path("epic_images")
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
        download_images_spacex(image_url, filename)


if __name__ == "__main__":
    load_dotenv()
    fetch_spacex_last_launch()
    fetch_nasa_apod_photos()
    fetch_nasa_epic_photos()
