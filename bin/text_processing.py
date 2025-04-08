from typing import List
from deep_translator import GoogleTranslator
# import spacy
# from collections import Counter

from itertools import groupby
import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer

tokenizer, model = None, None

async def initialize_model(model_name="0x7194633/keyt5-large"):
    global tokenizer, model
    print("Загрузка токенизатора...")
    tokenizer = T5Tokenizer.from_pretrained(model_name, legacy=False)
    print("Токенизатор инициализирован")
    print(f"Загрузка модели {model_name}")
    model = T5ForConditionalGeneration.from_pretrained(model_name)
    print(f"Модель {model_name} инициализирована")

# Предзагрузка моделей для доступных языков
lang_models = {
    "en": "en_core_web_lg",
    "ru": "ru_core_news_lg",
}


# noinspection PyCallingNonCallable
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

    if lang != "ru":
        text = GoogleTranslator(source=lang, target="ru").translate(input_text)
        print("Translated text")
    else:
        text = input_text
        print("Loaded text")

    inputs = tokenizer(text, return_tensors='pt', truncation=True, max_length=4096)
    print("Tokenized text")
    with torch.no_grad():
        print("Doing something with text")
        hypotheses = model.generate(**inputs, num_beams=5, top_p=.5, max_length=64)
        print("Finished doing something with text")
    s = tokenizer.decode(hypotheses[0], skip_special_tokens=True)
    print("S:", s)
    print("Extracted keywords")
    s = s.replace('; ', ';').replace(' ;', ';').lower().split(';')[:-1]
    s = [el for el, _ in groupby(s)]
    print("Returning keywords")

    return s
