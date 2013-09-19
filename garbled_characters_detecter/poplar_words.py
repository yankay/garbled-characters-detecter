import logging
import os
import codecs
import itertools

import chardet

LOG = logging.getLogger(__name__)

POPLAR_WORDS_CACHE = {}
POPLAR_MULTI_WORDS_CACHE = {}

def __load_poplar_words(lang):
    if lang not in POPLAR_WORDS_CACHE:
        POPLAR_WORDS_CACHE[lang] = set()
        lang_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                    "popular-words-" + lang + ".txt")
        with codecs.open(lang_path , 'r', encoding='UTF-8') as f:
            POPLAR_WORDS_CACHE[lang] = f.readlines()
        POPLAR_WORDS_CACHE[lang] = map(lambda s:s.strip(), POPLAR_WORDS_CACHE[lang])
    return POPLAR_WORDS_CACHE[lang]


def load_poplar_words(langs):
    # load cache
    if len(langs) == 0:
        return set()
    elif len(langs) == 1:
        return __load_poplar_words(langs[0])
    else:
        langs = sorted(langs)
        langs_key = "_".join(langs)
        if langs_key not in POPLAR_MULTI_WORDS_CACHE:
            POPLAR_MULTI_WORDS_CACHE[langs_key] = set()
            for lang in langs:
                POPLAR_MULTI_WORDS_CACHE[langs_key] = POPLAR_MULTI_WORDS_CACHE[langs_key] | __load_poplar_words(lang)
        return POPLAR_MULTI_WORDS_CACHE[langs_key]

def poplar_words_rate(text, langs):
    if len(text) == 0:
        return 0
    else:
        poplar_words = load_poplar_words(langs)
        text_words = split_word(text,1) | split_word(text,2)
        return float(len(filter(lambda w: w in poplar_words ,
                text_words))) / len(text_words)

def split_word(text,num):
    w = set()
    if len(text) >= num:
        for i in range(0,len(text)-num+1):
            w.add(text[i:i+num])
    return w