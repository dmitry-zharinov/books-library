from urllib.parse import urljoin

from bs4 import BeautifulSoup

HOST_NAME = 'https://tululu.org'


def extract_comments(soup):
    comments_serialized = soup.find_all('div', class_='texts')
    comments = [comment.find('span', class_='black').text
                for comment in comments_serialized]
    return comments


def extract_genres(soup):
    genres_serialized = soup.find('span', class_='d_book').find_all('a')
    genres = [genre.text for genre in genres_serialized]
    return genres


def parse_book_page(html_content):
    soup = BeautifulSoup(html_content, 'lxml')

    book_name = soup.find('td', class_='ow_px_td').find('h1').text.split('::')
    img_url = soup.find('div', class_='bookimage').find('img')['src']
    book_info = {
        'title': book_name[0].strip(),
        'author': book_name[1].strip(),
        'img': urljoin(HOST_NAME, img_url),
        'comments': extract_comments(soup),
        'genres': extract_genres(soup)
    }
    return book_info
