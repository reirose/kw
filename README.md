## Клиент для каталогизации текстовых документов по ключевым словам
### Основа - FastAPI, spaCy, MongoDB

#### Установка:
* Установить MongoDBCompass
* Скачать исходный код:
    ```bash
    git clone https://github.com/reirose/diplom-wrapper
    cd diplom-wrapper
    ```
* Установить необходимые библиотеки
    ```bash
    pip install spacy pymongo fastapi
    ```

* Изменить ссылку для подключения к БД в файле `bin/db_init.py`:
    ```python
    client = MongoClient("mongodb://connection_string:port")
    db = client.get_database("database_name")
    kw_db = db.get_collection("keywords_database")
    ```

* Запустить клиент и перейти на `localhost:27015`:
    ```bash
    python main.py
    ```
![screenshot](./static/img.png "Client main page")
