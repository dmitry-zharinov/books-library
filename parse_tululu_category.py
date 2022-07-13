import json
import logging

import requests
from bs4 import BeautifulSoup

from tululu_parser import download_book_with_image


logger = logging.getLogger(__file__)


def get_book_ids(genre_url, start_page, end_page):
    book_ids = []
    for page in range(start_page, end_page + 1):
        page_url = f'{genre_url}/{page}/'
        response = requests.get(page_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')
        for link in soup.find('body').find_all('table', class_='d_book'):
            book_ids.append(link.find('a')['href'].strip('/b'))
        # books_selector = 'body table.d_book a'
        # book_ids_ = soup.select(books_selector)
        # book_list = [link.strip('/b') for link in book_ids_.find_all('href')]
        # print(book_list)

    return book_ids


def main():
    logging.basicConfig(level=logging.ERROR)
    logger.setLevel(logging.DEBUG)

    sci_fi_url = 'https://tululu.org/l55/'
    book_ids = get_book_ids(sci_fi_url, 1, 2)
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
