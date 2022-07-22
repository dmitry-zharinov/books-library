import json
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked

BOOKS_FOLDER = 'books'
IMG_FOLDER = 'images'
PAGES_FOLDER = 'pages'
STATIC_URL = '../static'
MEDIA_FOLDER = 'media'
BOOKS_ON_PAGE = 10


def init_template():
    env = Environment(
        loader=FileSystemLoader('templates'),
        autoescape=select_autoescape(['html'])
    )
    return env.get_template('template.html')


def load_books_from_json():
    books_json_path = Path(MEDIA_FOLDER) / 'books.json'
    with open(books_json_path, 'r', encoding='utf8') as books_file:
        return chunked(json.load(books_file), 2)


def run_server():
    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


def on_reload():
    book_items = load_books_from_json()
    template = init_template()
    chunked_books = list(chunked(book_items, BOOKS_ON_PAGE))
    num_of_pages = len(chunked_books)

    for page_num, books in enumerate(chunked_books):
        rendered_page = template.render(
            books=books,
            books_folder=BOOKS_FOLDER,
            img_folder=IMG_FOLDER,
            media_folder=MEDIA_FOLDER,
            num_of_pages=num_of_pages,
            page_num=page_num+1,
            static_url=STATIC_URL
        )
        index_filepath = os.path.join(PAGES_FOLDER, f'index{page_num+1}.html')

        with open(index_filepath, 'w', encoding="utf8") as file:
            file.write(rendered_page)


def main():
    Path(PAGES_FOLDER).mkdir(parents=True, exist_ok=True)
    server = Server()
    on_reload()
    server.watch('templates/*.html', on_reload)
    server.serve(root='.')


if __name__ == '__main__':
    main()
