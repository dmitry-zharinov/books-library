import argparse

from tululu_parser import download_book_with_image


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--start_id', type=int, default=1)
    parser.add_argument('--end_id', type=int, default=11)
    return parser


def main():
    parser = createParser()
    parser_params = parser.parse_args()

    for book_id in range(parser_params.start_id, parser_params.end_id+1):
        book_data = download_book_with_image(book_id)
        if book_data:
            print(f'Заголовок: {book_data["title"]}')
            print(book_data["genres"])


if __name__ == '__main__':
    main()
