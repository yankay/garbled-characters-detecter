import os
import json
import codecs
import itertools

import detecter
import encoding_utils

ENCODINGS = ["utf_8", "gbk", "latin_1"]
LANGS = ["zh-CN"]

ENCODINGS = map(encoding_utils.standard_encoding_name, ENCODINGS)

def test_detecter(code_map, lang):
    sample_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                    "sample-" + lang + ".txt")
    with codecs.open(sample_path , 'r', encoding='UTF-8') as f:
        data = map(lambda line:{"from_text":line}, f.readlines())
    for i in data:
        i.update(code_map)
        i['to_text'] =encoding_utils.iconv(i['from_text'], i['from_encode'] , i['to_encode'])
        i['detect'] = detecter.detect(i['to_text'], encodings=ENCODINGS, lang=lang)
    print "========================"
    print "code_map:" + json.dumps(code_map)
    print "lang:" + json.dumps(lang)
    print "hit in 1: %s" % hit( data, 1)
    print "hit in 3: %s" % hit( data, 3)
    print "hit in 5: %s" % hit( data, 5)
    # print json.dumps(data[0])
    # print data[0]['org']

def hit( data, num):
    s = 0
    for item in data:
        for i in range(0, min(num, len(item['detect']))):
            if item['detect'][i]['from_encode'] == item['from_encode'] and item['detect'][i]['to_encode'] == item['to_encode']:
                s = s + 1
    return s


def main():
    code_maps = map(lambda x: {"from_encode":x[0], "to_encode":x[1]}, itertools.permutations(ENCODINGS, 2)) 
    code_maps.append({"from_encode":"", "to_encode":""})
    for code_map in code_maps:
        for lang in LANGS:
            test_detecter(code_map, lang)


if __name__ == '__main__':
    main()
