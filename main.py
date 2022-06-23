import os
from pathlib import Path
from urllib.parse import urlsplit

import requests
from pathvalidate import sanitize_filename

from tululu_parser import parse_book_page

FOLDER_NAME = 'books'
IMG_FOLDER_NAME = 'images'


def download_txt(url, payload, filename, folder):
    """Функция для скачивания текстовых файлов.

    Args:
        url (str): Cсылка на текст, который хочется скачать.
        payload (dict): Параметры запроса.
        filename (str): Имя файла, с которым сохранять.
        folder (str): Папка, куда сохранять.

    Raises:
        requests.exceptions.HTTPError: Ошибка HTTP.

    Returns:
        str: Путь до файла, куда сохранён текст.
    """
    Path(folder).mkdir(parents=True, exist_ok=True)

    response = requests.get(url, payload)
    response.raise_for_status()
    if not response.ok or response.history:
        raise requests.exceptions.HTTPError('Книга не найдена')

    fpath = os.path.join(folder, f'{sanitize_filename(filename)}.txt')
    with open(fpath, 'wb') as file:
        file.write(response.content)

    return fpath


def get_book_metadata(url):
    """Функция для извлечения данных о книге.

    Args:
        url (str): Cсылка на книгу на сайте tululu.org.

    Raises:
        requests.exceptions.HTTPError: Ошибка HTTP.

    Returns:
        dict: Словарь с данными о книге.
    """
    response = requests.get(url)
    response.raise_for_status()
    if not response.ok or response.history:
        raise requests.exceptions.HTTPError('Книга не найдена')
    return parse_book_page(response.text)


def download_image(url, folder):
    """Функция для скачивания обложек"""
    Path(folder).mkdir(parents=True, exist_ok=True)
    filename = urlsplit(url).path.split('/')[-1]
    response = requests.get(url)
    response.raise_for_status()
    with open(Path(folder) / filename, 'wb') as file:
        file.write(response.content)


def main():

    for book_id in range(1, 11):
        payload = {
            'id': book_id,
        }
        try:
            response = requests.get(f'https://tululu.org/b{book_id}/')
            response.raise_for_status()
            if not response.ok or response.history:
                raise requests.exceptions.HTTPError(
                    f'Книга {book_id} не найдена')
            book_metadata = parse_book_page(response.text)

            download_txt(
                'https://tululu.org/txt.php',
                payload,
                f'{book_id}. {book_metadata["title"]}',
                FOLDER_NAME
            )
            download_image(
                book_metadata['img'],
                IMG_FOLDER_NAME
            )
            print(f'Заголовок: {book_metadata["title"]}')
            print(book_metadata["genres"])

        except requests.exceptions.HTTPError as http_err:
            print(http_err)


main()
