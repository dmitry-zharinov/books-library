import os
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename

FOLDER_NAME = 'books'


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

    soup = BeautifulSoup(response.text, 'lxml')

    book_name = soup.find('td', class_='ow_px_td').find('h1').text.split('::')
    book_info = {
        'title': book_name[0].strip(),
        'author': book_name[1].strip()
    }
    return book_info


def main():

    for book_id in range(1, 11):
        payload = {
            'id': book_id,
        }
        url = 'https://tululu.org/txt.php'
        try:
            book_data = get_book_metadata(f'https://tululu.org/b{book_id}/')
            download_txt(url,
                         payload,
                         f'{book_id}. {book_data["title"]}',
                         FOLDER_NAME)
        except requests.exceptions.HTTPError as http_err:
            print(http_err)


main()
