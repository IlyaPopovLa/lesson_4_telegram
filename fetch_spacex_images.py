import argparse
import requests
from pathlib import Path
from common_utils import download_image
from main import load_dotenv


def fetch_spacex_launch_photos(launch_id: Optional[str] = None) -> None:
    base_url = "https://api.spacexdata.com/v5/launches/"
    url = f"{base_url}{launch_id}" if launch_id else f"{base_url}latest"

    response = requests.get(url)
    response.raise_for_status()

    data = response.json()
    photos = data.get("links", {}).get("flickr", {}).get("original", [])
    folder = Path("images")

    for num, photo_url in enumerate(photos):
        filename = folder / f"spacex_{num}.jpg"
        download_image(photo_url, filename)


if __name__ == "__main__":
    load_dotenv()

    parser = argparse.ArgumentParser(description="Скачать фото запуска SpaceX по ID или последний запуск")
    parser.add_argument("--id", type=str, help="ID запуска SpaceX", default=None)
    args = parser.parse_args()

    fetch_spacex_launch_photos(args.id)
