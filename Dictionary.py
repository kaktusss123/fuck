from json import dump
from re import sub, search

from lxml.html import fromstring
from pymorphy2 import MorphAnalyzer
from requests import get

morph = MorphAnalyzer()


def russki_mat():
    url = 'http://www.russki-mat.net/e/mat_slovar.htm'
    resp = fromstring(get(url).content.decode('utf-8'))
    elems = resp.xpath("//span[@class='lem']/text()")
    elems = [sub(r'\W', r'', x.lower().replace('ё', 'е')) for x in elems if ' ' not in x and not search(r'\d', x)]
    return set(elems)


def cont_ws():
    url = 'https://cont.ws/@acorus/1218748'
    resp = fromstring(get(url).text)
    elems = resp.xpath("//article/p/b[contains(text(), 'ХУЙ')]/parent::p/following-sibling::p/text()")[:168]
    elems = [search(r'(\d*\.? ?)(\w+)', x).group(2).lower() for x in elems if search(r'(\d*\.? ?)(\w+)', x)]
    return set(elems)


def dict_3():
    with open('dict_3.txt', encoding='utf-8') as f:
        dct = set(filter(lambda x: len(x) < 10 and ' ' not in x and not search(r'\d', x),
                         map(lambda x: sub(r'\W', r'', x), f.read().strip().split(','))))
    return dct


with open('dict.json', 'w', encoding='utf-8') as f:
    s = cont_ws()
    s = s.union(russki_mat())
    s = s.union(dict_3())
    s -= {"без", "ни", "с", "святой", "сход"}
    dump(sorted(set(map(lambda x: morph.parse(x)[0].normal_form.replace('ё', 'е'), s))), f, ensure_ascii=False)
