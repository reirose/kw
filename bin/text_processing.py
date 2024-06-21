import json
from typing import AnyStr

import spacy


def process_text(text: AnyStr):
    nlp = spacy.load('en_core_web_md')
    used_tokens = []
    used_ents = []
    used_pos = ["ADJ", "NOUN", "PROPN"]  # "VERB", "ADV",

    doc = nlp(text)

    for token in doc:
        if token.pos_ in used_pos:
            used_tokens.append(token)

    for ent in doc.ents:
        used_ents.append(ent.text)

    freq = {}
    n = len(used_tokens)
    for x in used_tokens:
        freq[x.lemma_] = used_tokens.count(x) / n

    freq = dict(sorted(freq.items(), key=lambda item: item[0], reverse=True))

    kws = list(freq.keys())[:int(len(list(freq.items()))/2)] + [x.lower() for x in used_ents]
    kws.sort()

    return kws
