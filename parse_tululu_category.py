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
    parser_params = parser.parse_args()

    sci_fi_url = 'https://tululu.org/l55/'
    book_ids = get_book_ids(
        sci_fi_url,
        parser_params.start_page,
        parser_params.end_page)
    downloaded_books = [
        download_book_with_image(book_id) for book_id in book_ids]
    with open("books.json", "w", encoding="utf-8") as books_data_file:
        json.dump(
            downloaded_books,
            books_data_file,
            indent=4,
            ensure_ascii=False)


if __name__ == '__main__':
    main()
