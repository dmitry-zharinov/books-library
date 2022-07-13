import logging
from urllib.parse import urljoin

from bs4 import BeautifulSoup

logger = logging.getLogger(__file__)


def extract_comments(soup: BeautifulSoup):
    """Извлечь список комментариев"""
    comments_selector = 'div.texts span.black'
    return [comment.text for comment in soup.select(comments_selector)]


def extract_genres(soup: BeautifulSoup):
    """Извлечь список жанров"""
    genres_selector = 'span.d_book a'
    return [genre.text for genre in soup.select(genres_selector)]


def parse_book_page(html_content: str, book_url: str, books_folder: str):
    """Парсинг страницы книги"""
    soup = BeautifulSoup(html_content, 'lxml')

    book_name_selector = 'td.ow_px_td h1'
    book_name = soup.select_one(book_name_selector).text.split('::')

    img_selector = 'div.bookimage img'
    img_src = soup.select_one(img_selector)['src']

    title, author = book_name
    title = title.strip()
    book_info = {
        'title': title,
        'author': author.strip(),
        'img_src': urljoin(book_url, str(img_src)),
        'book_path': f'{books_folder}/{title}.txt',
        'comments': extract_comments(soup),
        'genres': extract_genres(soup)
    }
    return book_info
