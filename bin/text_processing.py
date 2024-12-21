from typing import AnyStr, List
from deep_translator import GoogleTranslator
import spacy
from collections import Counter

# Предзагрузка моделей для доступных языков
lang_models = {
    "en": "en_core_web_lg",
    "ru": "ru_core_news_lg",
}

def process_text(input_text: str, lang: str, top_n: int = 20) -> List[str]:
    """
    Обработка текста: определение модели языка или перевод на английский,
    извлечение ключевых слов и их перевод на русский.

    Args:
        input_text (str): Текст для обработки.
        lang (str): Код языка текста.
        top_n (int): Количество ключевых слов в итоговом списке.

    Returns:
        List[str]: Список ключевых слов на исходном языке и их переводов на русский.
    """
    # Переводчики
    translator_to_english = GoogleTranslator(source=lang, target="en")
    translator_to_russian = GoogleTranslator(source="en", target="ru")
    translator_to_original = GoogleTranslator(source="en", target=lang)

    # Проверяем, есть ли модель для указанного языка
    if lang in lang_models:
        nlp = spacy.load(lang_models[lang])
        doc = nlp(input_text)
    else:
        # Если модели нет, переводим текст на английский
        translated_text = translator_to_english.translate(input_text)
        nlp = spacy.load(lang_models["en"])
        doc = nlp(translated_text)

    # Извлечение существительных и прилагательных
    keywords = [token.lemma_ for token in doc if token.pos_ in {"NOUN", "ADJ", "VERB"} and not token.is_stop]

    # Подсчёт частот слов и выбор топ-N
    keyword_counts = Counter(keywords)
    most_common_keywords = [word for word, _ in keyword_counts.most_common(top_n)]

    # Перевод ключевых слов на русский
    translated_keywords = [translator_to_russian.translate(word) for word in most_common_keywords]

    # Если текст был переведён на английский, переводим ключевые слова обратно на исходный язык
    if lang not in lang_models:
        original_keywords = [translator_to_original.translate(word) for word in most_common_keywords]
    else:
        original_keywords = most_common_keywords

    # Возвращаем список ключевых слов на исходном языке и на русском
    return original_keywords + translated_keywords
