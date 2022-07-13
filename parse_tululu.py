import argparse
import logging

from download_books import download_book_with_image


logger = logging.getLogger(__file__)


def createParser():
    """Создание парсера аргументов"""
    parser = argparse.ArgumentParser()
    parser.add_argument('--start_id', type=int, default=1)
    parser.add_argument('--end_id', type=int, default=11)
    return parser


def main():
    logging.basicConfig(level=logging.ERROR)
    logger.setLevel(logging.DEBUG)

    parser = createParser()
    parser_params = parser.parse_args()

    for book_id in range(parser_params.start_id, parser_params.end_id+1):
        book_data = download_book_with_image(book_id)
        if book_data:
            logging.info(f'Заголовок: {book_data["title"]}')
            logging.info(book_data["genres"])


if __name__ == '__main__':
    main()
