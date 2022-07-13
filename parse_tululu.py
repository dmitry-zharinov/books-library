import argparse
import logging
from pathlib import Path

from download_books import download_book_with_image

logger = logging.getLogger(__file__)


def createParser():
    """Создание парсера аргументов"""
    parser = argparse.ArgumentParser(
        description='Скачивание книг по id'
    )
    parser.add_argument(
        '--start_id',
        help='С какой книги скачивать (по умолчанию - 1)',
        type=int,
        default=1)
    parser.add_argument(
        '--end_id',
        help='По какую книгу скачивать (по умолчанию - 10)',
        type=int,
        default=10)
    return parser


def main():
    logging.basicConfig(level=logging.ERROR)
    logger.setLevel(logging.DEBUG)

    parser = createParser()
    args = parser.parse_args()

    for book_id in range(args.start_id, args.end_id+1):
        book_data = download_book_with_image(
            book_id=book_id,
            dest_folder=Path.cwd(),
            skip_imgs=False,
            skip_txt=False)
        if book_data:
            logging.info(f'Заголовок: {book_data["title"]}')
            logging.info(book_data["genres"])


if __name__ == '__main__':
    main()
