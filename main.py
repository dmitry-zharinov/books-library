from pathlib import Path

import requests

FOLDER_NAME = 'books'


def download_book(url, filename):
    response = requests.get(url)
    response.raise_for_status()
    with open(Path(FOLDER_NAME) / filename, 'wb') as file:
        file.write(response.content)

Path(FOLDER_NAME).mkdir(parents=True, exist_ok=True)

for book_id in range(1, 10):
    url = f'https://tululu.org/txt.php?id={book_id}'
    download_book(url, f'id{book_id}.txt')
        