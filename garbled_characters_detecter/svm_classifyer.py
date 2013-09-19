#
# 0 is not fit
# 1 is fit
#
from sklearn import svm

SVMS = {}

def svm_args(p):
        return [
            p["detect_original"]["confidence"] * int(p["detect_original"] == p["from_encode"]),
            p['poplar_characters_rate_text'],
            p['poplar_characters_rate_original']]



def svm_learn(langs, potential):
    data = []
    for lang in langs:
        sample_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                        "sample-" + lang + ".txt")
        with codecs.open(sample_path , 'r', encoding='UTF-8') as f:
            data.extends(map(lambda line:{"org":line}, f.readlines()))
    for i in data:
        i['converted'] = convert(i['org'], potential['from_encode'] , potential['to_encode'])
        p = {"from_encode":potential['from_encode'], "to_encode":potential['to_encode']}
        i['potential'] = potential_encode(i['converted'], langs, p)
    
    pass

def svm_classify(langs, potential):
    key = potential["from_encode"] + "_" + potential["to_encode"] + "_" + json.dumps(sorted(langs)) 
    if key not in SVMS:
        SVMS[key] = svm.SVC()
        X, Y = svm_learn(langs, potential)
        SVMS[key].fit(X, Y)
    result = SVMS[key].predict([svm_args(potential)])
    if len(result) > 0:
        return result[0]
    else:
        return 0