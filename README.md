# Парсер книг с сайта tululu.org

Скрипт позволяет скачивать книги с сайта [tululu.org](https://tululu.org/) в формате .txt с обложками и комментариями.

### Как установить

1. Предварительно должен быть установлен Python3.
2. Для установки зависимостей:
```console
$ pip install -r requirements.txt
```

## Скачивание книг по id
Для запуска скрипта:
```console
$ python parse_tululu.py
```

### Аргументы
Скрипт принимает на вход следующие аргументы:
- `--start_id`: с какой книги начинать скачивание (по умолчанию - 1);
- `--end_id`: по какую книгу скачивать (по умолчанию - 10);


## Скачивание книг жанра научной фантастики
Для запуска скрипта:
```console
$ python parse_tululu_category.py
```

### Аргументы
- `--start_page` - с какого номера страницы начинать скачивание (по умолчанию - 1);
- `--end_page` - по какую страницу скачивать (по умолчанию - 10);
- `--dest_folder` — путь к каталогу с результатами парсинга: картинкам, книгам (по умолчанию - каталог скрипта);
- `--skip_imgs` — не скачивать картинки;
- `--skip_txt` — не скачивать книги;
- `--json_path` — путь к каталогу с *.json файлом с результатами работы скрипта (по умолчанию - каталог скрипта);