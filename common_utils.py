import os
import requests
from pathlib import Path
from urllib.parse import urlparse


def get_extension_from_url(url: str) -> str:
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    extension = os.path.splitext(filename)[1]
    return extension


def download_image(url: str, path: Path) -> None:
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
    print(f"Скачано: {path}")


def download_images_batch(urls: list[str], folder_name: str, prefix: str):
    folder_path = Path(folder_name)
    folder_path.mkdir(parents=True, exist_ok=True)

    for idx, url in enumerate(urls, start=1):
        ext = get_extension_from_url(url)
        filename = folder_path / f"{prefix}_{idx}{ext}"
        download_image(url, filename)


def main():
    urls = [
        "https://example.com/image1.jpg",
        "https://example.com/image2.png"
    ]
    folder = "images"
    prefix = "img"

    folder_path = Path(folder)
    folder_path.mkdir(parents=True, exist_ok=True)

    for idx, url in enumerate(urls, start=1):
        ext = get_extension_from_url(url)
        filename = folder_path / f"{prefix}_{idx}{ext}"
        try:
            download_image(url, filename)
        except requests.RequestException as e:
            print(f"Ошибка при скачивании изображения {url}: {e}")


if __name__ == "__main__":
    main()
