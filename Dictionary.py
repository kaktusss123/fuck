from re import sub

from lxml.html import fromstring
from requests import get


def russki_mat():
    url = 'http://www.russki-mat.net/e/mat_slovar.htm'
    resp = fromstring(get(url).content.decode('utf-8'))
    elems = resp.xpath("//span[@class='lem']/text()")
    elems = [sub(r'\W', r'', x.lower().replace('ё', 'е')) for x in elems]
    return set(elems)


def cont_ws():
    url = 'https://cont.ws/@acorus/1218748'
    resp = fromstring(get(url).text)
    elems = resp.xpath("//article/p/b[contains(text(), 'ХУЙ')]/parent::p/following-sibling::p/text()")
    elems = [sub(r'\W', r'', x.lower().split()[0]) for x in elems]
    return set(elems)


print(cont_ws())
