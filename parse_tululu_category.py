import argparse
import json
import logging

import requests
from bs4 import BeautifulSoup

from tululu_parser import download_book_with_image

logger = logging.getLogger(__file__)


def createParser():
    """Создать парсер аргументов"""
    parser = argparse.ArgumentParser()
    parser.add_argument('--start_page', type=int, default=1)
    parser.add_argument('--end_page', type=int, default=2)
    parser.add_argument('--dest_folder', default='')
    parser.add_argument('--skip_imgs', action='store_true', default=False)
    parser.add_argument('--skip_txt', action='store_true', default=False)
    parser.add_argument('--json_path', default='')

    return parser


def get_book_ids(genre_url: str, start_page: int, end_page: int):
    """Получить id книг по заданным страницам"""
    book_ids = []
    for page in range(start_page, end_page + 1):
        page_url = f'{genre_url}/{page}/'
        response = requests.get(page_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'lxml')
        books_selector = 'body table.d_book tr:nth-child(2) a'
        for book in soup.select(books_selector):
            book_ids.append(book['href'].strip('/b'))
    return book_ids


def main():
    logging.basicConfig(level=logging.ERROR)
    logger.setLevel(logging.DEBUG)

    parser = createParser()
    params = parser.parse_args()

    sci_fi_url = 'https://tululu.org/l55/'
    book_ids = get_book_ids(
        sci_fi_url,
        params.start_page,
        params.end_page)
    downloaded_books = [
        download_book_with_image(
            book_id=book_id,
            skip_imgs=params.skip_imgs,
            skip_txt=params.skip_txt)
        for book_id in book_ids]
    with open("books.json", "w", encoding="utf-8") as books_data_file:
        json.dump(
            downloaded_books,
            books_data_file,
            indent=4,
            ensure_ascii=False)


if __name__ == '__main__':
    main()
