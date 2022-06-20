from pathlib import Path

import requests

FOLDER_NAME = 'books'


def download_book(url, payload, filename):
    response = requests.get(url, payload)
    response.raise_for_status()
    check_for_redirect(response)
    with open(Path(FOLDER_NAME) / filename, 'wb') as file:
        file.write(response.content)


def check_for_redirect(response):
    if response.history:
        raise requests.exceptions.HTTPError('Книга не найдена')


def main():
    Path(FOLDER_NAME).mkdir(parents=True, exist_ok=True)

    for book_id in range(1, 11):
        payload = {
            'id': book_id,
        }
        url = 'https://tululu.org/txt.php'
        try:
            download_book(url, payload, f'id{book_id}.txt')
        except requests.exceptions.HTTPError as http_err:
            print(http_err)


main()