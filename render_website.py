import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
from more_itertools import chunked
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server

BOOKS_FOLDER = 'books'
IMG_FOLDER = 'images'


def init_template():
    env = Environment(
        loader=FileSystemLoader('templates'),
        autoescape=select_autoescape(['html'])
    )
    return env.get_template('template.html')


def load_books_from_json():
    with open("books.json", "r", encoding='utf8') as my_file:
        books_json = my_file.read()
        return list(chunked(json.loads(books_json), 2))


def run_server():
    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


def on_reload():
    book_items = load_books_from_json()
    template = init_template()

    rendered_page = template.render(
        books=book_items,
        books_folder=BOOKS_FOLDER,
        img_folder=IMG_FOLDER,
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)


def main():
    # run_server()
    server = Server()
    on_reload()
    server.watch('templates/*.html', on_reload)
    server.serve(root='.')


if __name__ == '__main__':
    main()
