import logging
import os
import codecs
import itertools

import chardet

LOG = logging.getLogger(__name__)

def standard_encoding_name(encoding):
    e = encoding
    try:
        if encoding:
            e = codecs.lookup(encoding).name
    except:
        pass
    return e

def iconv(text, from_encode="", to_encode="", error='replace'):
    if from_encode != "":    
        text = text.encode(from_encode, error)
    if to_encode != "":
        text = text.decode(to_encode, error)
    return text
    
def detect_encoding(tstr):
    if type(tstr) == str:
        e = chardet.detect(tstr)
        e["encoding"] = standard_encoding_name(e["encoding"])
        return e
    else:
        return {"encoding":"", "confidence":1}
