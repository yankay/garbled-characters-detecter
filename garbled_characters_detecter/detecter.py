import logging
import os
import codecs
import itertools

import chardet

LOG = logging.getLogger(__name__)

POPLAR_CHARACTERS_CACHE = {}

def load_poplar_characters(langs):
    #load cache
    langs = sorted(langs)
    langs_key = "_".join(langs)

    if langs_key not in POPLAR_CHARACTERS_CACHE:
        POPLAR_CHARACTERS_CACHE[langs_key] = set()
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
            POPLAR_CHARACTERS_CACHE[langs_key] = POPLAR_CHARACTERS_CACHE[langs_key] | POPLAR_CHARACTERS_CACHE[lang]
    return POPLAR_CHARACTERS_CACHE[langs_key]

def original_text(text,from_encode,to_encode):
    if from_encode == "" or to_encode == "":
        return text
    else:
        text =  text.encode(to_encode,'replace')
        return text.decode(from_encode,'replace')
     

def standard_encoding_name(encoding):
    if encoding:
        return codecs.lookup(encoding).name
    else:
        return encoding

def detect_encoding(utext,encode):
    e =  chardet.detect(utext.encode(encode,'replace'))
    e["encoding"] = standard_encoding_name(e["encoding"])

def poplar_characters_rate(text,langs):
    poplar_characters = load_poplar_characters(langs)
    return float(len(filter(lambda x: x in poplar_characters ,
            text))) / len(text)

#
# 0 is not fit
# 1 is fit
#
def svm_classify(list):
    pass
# 
# text is the garbled characters
#
def detect(text = u"", encodings = ["utf_8","gbk","big5","latin_1"],langs = ["zh-CN","zh-TW"]):
    encodings = map(standard_encoding_name, encodings)
    potentials = map(lambda x: {"from_encode":x[0],"to_encode":x[1]}, itertools.permutations(encodings, 2)) 
    potentials.append({"from_encode":"","to_encode":""})
    
    for potential in potentials:
        potential["original"] = original_text(text,potential["from_encode"],potential["to_encode"])

    for potential in potentials:
        potential["detect_text"] = detect_encoding(text,potential["to_encode"])
        potential["detect_original"] = detect_encoding(potential["original"],potential["from_encode"])

    for potential in potentials:
        potential['poplar_characters_rate_text'] =poplar_characters_rate(text,langs)
        potential['poplar_characters_rate_original'] = poplar_characters_rate(potential["original"] ,langs)

    for potential in potentials:
        potential['classify'] = svm_classify([
            potential["detect_original"]["confidence"]] * int(potential["detect_original"]==potential["from_encode"]),
            potential['poplar_characters_rate_text'],
            potential['poplar_characters_rate_original']
            )

    potentials = sorted(potentials, key=lambda potential: potential["rate"])
    potentials = sorted(potentials, key=lambda potential: potential["classify"])
    potentials.reverse()
    return potentials