import requests
from pathlib import Path
from urllib.parse import urlparse


def get_extension_from_url(url: str) -> str:
    parsed_url = urlparse(url)
    path = parsed_url.path
    ext = Path(path).suffix
    return ext if ext else '.jpg'


def download_image(url: str, filename: Path):
    response = requests.get(url)
    response.raise_for_status()

    with open(filename, 'wb') as file:
        file.write(response.content)


def download_images_batch(urls: list[str], folder_name: str, prefix: str):
    folder_path = Path(folder_name)
    folder_path.mkdir(parents=True, exist_ok=True)

    for idx, url in enumerate(urls, start=1):
        ext = get_extension_from_url(url)
        filename = folder_path / f"{prefix}_{idx}{ext}"
        try:
            download_image(url, filename)
            print(f"Успешно скачано: {filename}")
        except requests.RequestException as e:
            print(f"Ошибка при скачивании изображения {url}: {e}")


def main():
    urls = [
        "https://example.com/image1.jpg",
        "https://example.com/image2.png"
    ]
    folder = "images"
    prefix = "img"

    download_images_batch(urls, folder, prefix)


if __name__ == "__main__":
    main()