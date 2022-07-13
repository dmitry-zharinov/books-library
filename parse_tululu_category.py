import argparse
import json
import logging
from pathlib import Path

from download_books import download_book_with_image
from parser import get_book_ids

logger = logging.getLogger(__file__)


def createParser():
    """Создать парсер аргументов"""
    parser = argparse.ArgumentParser()
    parser.add_argument('--start_page', type=int, default=1)
    parser.add_argument('--end_page', type=int, default=2)
    parser.add_argument('--dest_folder', default=Path.cwd())
    parser.add_argument('--skip_imgs', action='store_true')
    parser.add_argument('--skip_txt', action='store_true')
    parser.add_argument('--json_path', default=Path.cwd())
    return parser


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
