import logging
from pathlib import Path
from time import sleep
from urllib.parse import urljoin, urlsplit

import requests
from bs4 import BeautifulSoup


logger = logging.getLogger(__file__)


def check_for_redirect(response: requests.Response):
    if response.history:
        raise requests.exceptions.HTTPError('Книга не найдена')


def extract_comments(soup: BeautifulSoup):
    """Извлечь список комментариев"""
    comments_selector = 'div.texts span.black'
    return [comment.text for comment in soup.select(comments_selector)]


def extract_genres(soup: BeautifulSoup):
    """Извлечь список жанров"""
    genres_selector = 'span.d_book a'
    return [genre.text for genre in soup.select(genres_selector)]


def parse_book_page(html_content: str, book_url: str):
    """Парсинг страницы книги"""
    soup = BeautifulSoup(html_content, 'lxml')

    book_name_selector = 'td.ow_px_td h1'
    book_name = soup.select_one(book_name_selector).text.split('::')

    img_selector = 'div.bookimage img'
    img_src = soup.select_one(img_selector)['src']

    title, author = book_name
    title = title.strip()
    book_metadata = {
        'title': title,
        'author': author.strip(),
        'img_src': urljoin(book_url, str(img_src)),
        'img_filename': str(urlsplit(img_src).path.split('/')[-1]),
        'book_filename': f'{title}.txt',
        'comments': extract_comments(soup),
        'genres': extract_genres(soup)
    }
    return book_metadata


def extract_book_ids(soup: BeautifulSoup):
    """Извлечь id книг на странице"""
    book_ids = []
    books_selector = 'body table.d_book tr:nth-child(2) a'
    for book in soup.select(books_selector):
        book_ids.append(book['href'].strip('/b'))
    return book_ids


def get_book_ids(genre_url: str, start_page: int, end_page: int):
    """Получить id книг по заданным страницам"""
    book_ids = []
    for page in range(start_page, end_page + 1):
        page_url = f'{genre_url}/{page}/'
        try:
            response = requests.get(page_url)
            response.raise_for_status()
            check_for_redirect(response)
            soup = BeautifulSoup(response.text, 'lxml')
            book_ids.extend(extract_book_ids(soup))
        except requests.exceptions.ConnectionError as connect_err:
            logging.error(connect_err)
            sleep(10)
        except requests.exceptions.HTTPError as http_err:
            logging.error(http_err)
            continue
    return book_ids
