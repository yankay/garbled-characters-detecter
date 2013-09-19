import os
import codecs
import itertools

from sklearn import svm

import detecter
import encoding_utils

SVMS = {}

#
# 0 is not fit
# 1 is fit
#

def svm_learn_data(lang, encodings):
    sample_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                "sample-" + lang + ".txt")
    encoding_maps = map(lambda x: {"from_encode":x[0], "to_encode":x[1]}, itertools.permutations(encodings, 2)) 
    encoding_maps.append({"from_encode":"", "to_encode":""})
    
    with codecs.open(sample_path , 'r', encoding='UTF-8') as f:
        data = map(lambda line:{"from_text":line}, f.readlines())
    
    X = []
    Y = []
    for d in data:
        for e in encoding_maps:
            detecte_infos = detecter.detect_info(encoding_utils.iconv(
                            d['from_text'], e['from_encode'], e['to_encode']), encodings, lang)
            for p in detecte_infos:
                X.append(svm_args(p))
                Y.append(svn_hit(p, e))
    return X , Y
                
    
def svm_args(p):
        return [
            p["to_str_detect_encoding"]["confidence"] * int(p["to_str_detect_encoding"]['encoding'] == p["from_encode"]),
            p['from_text_poplar_characters_rate'],
            p['to_text_poplar_characters_rate']]
        

def svn_hit(p, e):
    return int(p['from_encode'] == e['from_encode'] and p['to_encode'] == e['to_encode'])

def svm_classify(potential_infos, lang, encodings):
    svm_key = lang + "_" + "".join(sorted(encodings))
    if svm_key not in SVMS:
        SVMS[svm_key] = svm.SVC()
        X, Y = svm_learn_data(lang, encodings)
        SVMS[svm_key].fit(X, Y)
    return SVMS[svm_key].predict(map(svm_args, potential_infos))
