from typing import AnyStr
from string import punctuation


def process_text(text: AnyStr):
    text = text.decode("utf-8")
    seg = text.split(" ")
    n = len(seg)
    freq = {}

    for i, token in enumerate(seg):
        if any([token[-1] in x for x in punctuation]):
            seg[i] = token[:-1]

    for token in seg:
        freq[token] = seg.count(token) / n

    sorted_by_keys = dict(sorted(freq.items(), key=lambda item: item[0], reverse=True))
    print(list(sorted_by_keys.items())[:5])
