import argparse
import requests
from pathlib import Path
from common_utils import download_image, load_env


def fetch_spacex_launch_photos(launch_id: str | None = None):
    if launch_id is None:
        url = "https://api.spacexdata.com/v5/launches/latest"
    else:
        url = f"https://api.spacexdata.com/v5/launches/{launch_id}"

    response = requests.get(url)
    response.raise_for_status()

    data = response.json()
    photos = data.get("links", {}).get("flickr", {}).get("original", [])
    folder = Path("images")

    for num, photo_url in enumerate(photos):
        filename = folder / f"spacex_{num}.jpg"
        download_image(photo_url, filename)


if __name__ == "__main__":
    load_env()

    parser = argparse.ArgumentParser(description="Скачать фото запуска SpaceX по ID или последний запуск")
    parser.add_argument("--id", type=str, help="ID запуска SpaceX")
    args = parser.parse_args()

    fetch_spacex_launch_photos(args.id)
