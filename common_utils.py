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