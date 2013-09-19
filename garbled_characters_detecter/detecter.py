import logging
import itertools

import encoding_utils
import poplar_characters
import poplar_words


LOG = logging.getLogger(__name__)


def potential_info(potential):
    potential["from_text"] = encoding_utils.iconv(potential["to_text"] , potential["to_encode"], potential["from_encode"])
    potential["from_text_ignore"] = encoding_utils.iconv(potential["to_text"] , potential["to_encode"], potential["from_encode"],error = "ignore")
    potential["to_str_ignore"] = encoding_utils.iconv(potential["to_text"] , potential["to_encode"], "",error = "ignore")

    potential["to_str_detect_encoding"] =encoding_utils.detect_encoding(potential["to_str_ignore"])

    potential['from_text_poplar_characters_rate'] =poplar_characters.poplar_characters_rate(potential["from_text_ignore"],[ potential["lang"] ])
    potential['to_text_poplar_characters_rate'] =poplar_characters.poplar_characters_rate(potential["to_text"],[ potential["lang"] ])

    potential['from_text_poplar_words_rate'] =poplar_words.poplar_words_rate(potential["from_text_ignore"],[ potential["lang"] ])
    potential['to_text_poplar_words_rate'] =poplar_words.poplar_words_rate(potential["to_text"],[ potential["lang"] ])

    return potential

# 
# text is the garbled characters
#
def detect_info(text, encodings, lang):
    encodings = map(encoding_utils.standard_encoding_name, encodings)
    
    potentials = map(lambda x: {"from_encode":x[0], "to_encode":x[1],"to_text": text, "lang":lang}, itertools.permutations(encodings, 2)) 
    potentials.append({"from_encode":"", "to_encode":"","to_text": text, "lang":lang})
    
    return map(potential_info, potentials)

    

def detect(text=u"", encodings=["utf_8", "gbk", "big5", "latin_1"], lang="zh-CN"):
    potentials = detect_info(text, encodings, lang)
    
    potentials = sorted(potentials, key=lambda potential: potential["from_text_poplar_characters_rate"])
    potentials = sorted(potentials, key=lambda potential: potential["from_text_poplar_words_rate"])
#     try:
#     import svm_classifyer
#     svm_classify = svm_classifyer.svm_classify(potentials, lang, encodings)
#     for i in range(0,min(len(svm_classify),len(potentials))):
#         potentials[i]['classify'] = svm_classify[i]
# 
#     potentials = sorted(potentials, key=lambda potential: potential["classify"])
#     except:
#         LOG.warn("cannot load svm_classifyer")
    potentials.reverse()
    return potentials