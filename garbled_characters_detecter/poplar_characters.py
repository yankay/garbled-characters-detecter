import logging
import os
import codecs
import itertools

import chardet

LOG = logging.getLogger(__name__)

POPLAR_CHARACTERS_CACHE = {}
POPLAR_MULTI_CHARACTERS_CACHE = {}

def __load_poplar_characters(lang):
    if lang not in POPLAR_CHARACTERS_CACHE:
        POPLAR_CHARACTERS_CACHE[lang] = set()
        lang_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                    "popular-characters-" + lang + ".txt")
        with codecs.open(lang_path , 'r', encoding='UTF-8') as f:
            while True:
                c = f.read(1)
                if len(c) <= 0:
                    break
                POPLAR_CHARACTERS_CACHE[lang].add(c)
    return POPLAR_CHARACTERS_CACHE[lang]


def load_poplar_characters(langs):
    # load cache
    if len(langs) == 0:
        return set()
    elif len(langs) == 1:
        return __load_poplar_characters(langs[0])
    else:
        langs = sorted(langs)
        langs_key = "_".join(langs)
        if langs_key not in POPLAR_MULTI_CHARACTERS_CACHE:
            POPLAR_MULTI_CHARACTERS_CACHE[langs_key] = set()
            for lang in langs:
                POPLAR_MULTI_CHARACTERS_CACHE[langs_key] = POPLAR_MULTI_CHARACTERS_CACHE[langs_key] | __load_poplar_characters(lang)
        return POPLAR_MULTI_CHARACTERS_CACHE[langs_key]

def poplar_characters_rate(text, langs):
    if len(text) == 0:
        return 0
    else:
        poplar_characters = load_poplar_characters(langs)
        return float(len(filter(lambda x: x in poplar_characters ,
                text))) / len(text)
