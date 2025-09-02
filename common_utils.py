import requests
from pathlib import Path
from urllib.parse import urlparse


def get_extension_from_url(url):
    parsed_url = urlparse(url)
    path = parsed_url.path
    extension = Path(path).suffix
    return extension


def download_image(url, filename):
    response = requests.get(url)
    response.raise_for_status()

    with open(filename, 'wb') as file:
        file.write(response.content)


def download_images_batch(urls, folder_name, prefix):
    folder_path = Path(folder_name)
    folder_path.mkdir(parents=True, exist_ok=True)

    for idx, url in enumerate(urls, start=1):
        ext = get_extension_from_url(url)
        filename = folder_path / f"{prefix}_{idx}{ext}"
        download_image(url, filename)
        print(f"Успешно скачано: {filename}")