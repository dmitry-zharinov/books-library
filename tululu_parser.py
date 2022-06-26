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


def parse_book_page(html_content, book_url):
    soup = BeautifulSoup(html_content, 'lxml')
    book_name = soup.find('td', class_='ow_px_td').find('h1').text.split('::')
    img_url = soup.find('div', class_='bookimage').find('img')['src']
    
    title, author = book_name
    print(img_url)
    book_info = {
        'title': title.strip(),
        'author': author.strip(),
        'img': urljoin(book_url, img_url),
        'comments': extract_comments(soup),
        'genres': extract_genres(soup)
    }

    return book_info
