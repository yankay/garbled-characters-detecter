import logging
import os
import codecs
import itertools

import chardet

import encoding_utils
import poplar_characters

LOG = logging.getLogger(__name__)


def potential_info( potential):
    potential["from_text"] = encoding_utils.iconv(potential["to_text"] , potential["to_encode"], potential["from_encode"])
    potential["from_text_ignore"] = encoding_utils.iconv(potential["to_text"] , potential["to_encode"], potential["from_encode"],error = "ignore")
    potential["to_str_ignore"] = encoding_utils.iconv(potential["to_text"] , potential["to_encode"], "",error = "ignore")

    potential["to_str_detect_encoding"] =encoding_utils.detect_encoding(potential["to_str_ignore"])

    potential['from_text_poplar_characters_rate'] =poplar_characters.poplar_characters_rate(potential["from_text_ignore"],[ potential["lang"] ])
    potential['to_text_poplar_characters_rate'] =poplar_characters.poplar_characters_rate(potential["from_text_ignore"],[ potential["lang"] ])
    return potential

# 
# text is the garbled characters
#
def detect(text=u"", encodings=["utf_8", "gbk", "big5", "latin_1"], lang="zh-CN"):
    encodings = map(encoding_utils.standard_encoding_name, encodings)
    
    potentials = map(lambda x: {"from_encode":x[0], "to_encode":x[1],"to_text": text, "lang":lang}, itertools.permutations(encodings, 2)) 
    potentials.append({"from_encode":"", "to_encode":"","to_text": text, "lang":lang})
    
    potentials = map(potential_info, potentials)

    potentials = sorted(potentials, key=lambda potential: potential["from_text_poplar_characters_rate"])
#     potentials = sorted(potentials, key=lambda potential: potential["classify"])
    potentials.reverse()
    return potentials
