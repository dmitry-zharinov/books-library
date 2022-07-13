import logging
import os
import time
from pathlib import Path
from urllib.parse import urljoin, urlsplit

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename

logger = logging.getLogger(__file__)

HOST_NAME = 'https://tululu.org'
FOLDER_NAME = 'books'
IMG_FOLDER_NAME = 'images'


def check_for_redirect(response):
    if response.history:
        raise requests.exceptions.HTTPError('Книга не найдена')


def download_book(url, payload, filename, folder):
    """Функция для скачивания текстовых файлов"""
    Path(folder).mkdir(parents=True, exist_ok=True)

    response = requests.get(url, payload)
    response.raise_for_status()
    check_for_redirect(response)

    filepath = os.path.join(folder, f'{sanitize_filename(filename)}.txt')
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(response.text)

    return filepath


def download_image(url, folder):
    """Функция для скачивания обложек"""
    Path(folder).mkdir(parents=True, exist_ok=True)
    filename = urlsplit(url).path.split('/')[-1]
    response = requests.get(url)
    response.raise_for_status()

    with open(Path(folder) / filename, 'wb') as file:
        file.write(response.content)


def extract_comments(soup):
    comments_selector = 'div.texts span.black'
    return [comment.text for comment in soup.select(comments_selector)]


def extract_genres(soup):
    genres_selector = 'span.d_book a'
    return [genre.text for genre in soup.select(genres_selector)]


def parse_book_page(html_content, book_url):
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
        'book_path': f'{FOLDER_NAME}/{title}.txt',
        'comments': extract_comments(soup),
        'genres': extract_genres(soup)
    }

    return book_info


def download_book_with_image(book_id):
    """Скачать книгу с обложкой"""
    payload = {
        'id': book_id,
    }
    try:
        book_url = f'https://tululu.org/b{book_id}/'
        response = requests.get(book_url)
        response.raise_for_status()
        check_for_redirect(response)
        book_metadata = parse_book_page(response.text, book_url)

        download_book(
            'https://tululu.org/txt.php',
            payload,
            f'{book_id}. {book_metadata["title"]}',
            FOLDER_NAME)
        download_image(
                book_metadata['img_src'],
                IMG_FOLDER_NAME)

        return book_metadata

    except requests.exceptions.HTTPError as http_err:
        logging.error(http_err)
    except requests.ConnectionError as e:
        logging.error(e)
        time.sleep(10)
