import logging
import os
import codecs
import itertools

import chardet

LOG = logging.getLogger(__name__)

POPLAR_CHARACTERS_CACHE = {}

def load_poplar_characters(langs):
    #load cache
    poplar_characters = set()
    for lang in langs:
        if lang not in POPLAR_CHARACTERS_CACHE:
            POPLAR_CHARACTERS_CACHE[lang] = set()
            lang_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                "popular-characters-"+lang+".txt")
            with codecs.open( lang_path ,'r',encoding = 'UTF-8') as f:
                while True:
                    c = f.read(1)
                    if len(c) <= 0:
                        break
                    POPLAR_CHARACTERS_CACHE[lang].add(c)
        poplar_characters = poplar_characters | POPLAR_CHARACTERS_CACHE[lang]
    return poplar_characters


def original_text(text,from_encode,to_encode):
    text =  text.encode(to_encode,'replace')
    return text.decode(from_encode,'replace')
     

def standard_encoding_name(encoding):
    if encoding:
        return codecs.lookup(encoding).name
    else:
        return encoding

# 
# text is the garbled characters
#
def detect(text = u"", encodings = ["utf_8","gbk","gb2312","big5","latin_1"],langs = ["en","zh-CN","zh-TW"]):
    poplar_characters = load_poplar_characters(langs)
    encodings = map(standard_encoding_name, encodings)
    potentials = map(lambda x: {"mapping" : x}, itertools.product(encodings, repeat=2)   ) 
    for potential in potentials:
        potential["original"] = original_text(text,potential["mapping"][0],potential["mapping"][1])

        potential["detect_text"] = chardet.detect(text.encode(potential["mapping"][1],'replace'))
        potential["detect_text"]["encoding"] = standard_encoding_name(potential["detect_text"]["encoding"])
        potential["detect_original"] = chardet.detect(potential["original"].encode(potential["mapping"][0],'replace'))
        potential["detect_original"]["encoding"] = standard_encoding_name(potential["detect_original"]["encoding"])

        potential['poplar_characters_rate_text'] = float(len(filter(lambda x: x in poplar_characters ,
            text))) / len(text)
        potential['poplar_characters_rate_original'] = float(len(filter(lambda x: x in poplar_characters ,
            potential["original"]))) / len(potential["original"])

        potential['rate']= potential['poplar_characters_rate_original'] * 0.8 + 0.2
        if potential["detect_original"]["confidence"] < 0.9 or not potential["mapping"][0] == potential["detect_original"]["encoding"]:
            potential['rate'] = potential['rate'] /2
        if potential['poplar_characters_rate_text'] > potential['poplar_characters_rate_original']:
            potential['rate'] = potential['rate'] /2

    
    potentials = sorted(potentials, key=lambda potential: potential["rate"], reverse = True)
    return potentials