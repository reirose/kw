## Клиент для каталогизации текстовых документов по ключевым словам
### Основа - FastAPI, spaCy, MongoDB

#### Установка:
* Установить Python 3.11 ([Страница на официальном сайте](https://www.python.org/downloads/release/python-31111/))
* Установить MongoDB ([Ссылка на официальном сайте](https://www.mongodb.com/try/download/community))
> Для установки MongoDB может понадобиться VPN
* Скачать исходный код:
    ```bash
    git clone https://github.com/reirose/diplom-wrapper
    cd diplom-wrapper
    ```
* Установить необходимые библиотеки
    ```bash
    pip install requirements.txt
    ```

* Изменить ссылку для подключения к БД в файле `bin/db_init.py`:
    ```python
    client = MongoClient("mongodb://connection_string:port")
    db = client.get_database(%database_name%)
    kw_db = db.get_collection(%keywords_database_name%)
    ```

* Запустить клиент и перейти на `localhost:27015`:
    ```bash
    python main.py
    ```
![screenshot](./static/img.png "Client main page")
