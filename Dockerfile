# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m spacy download en_core_web_lg
RUN python -m spacy download ru_core_news_lg
RUN python -m spacy download fr_core_news_lg
RUN python -m spacy download de_core_news_lg
RUN python -m spacy download it_core_news_lg
RUN python -m spacy download uk_core_news_lg

# Копируем исходный код
COPY . .

# Устанавливаем переменные окружения
ENV PYTHONUNBUFFERED=1

# Команда для запуска FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "27015", "--reload"]