import re
import requests
from urllib.parse import quote_plus as url_encode
from bs4 import BeautifulSoup

def decode_html(string):
    decoded = ['>', '<', '"', '&', '\'','{', '}']
    encoded = ['&gt;', '&lt;', '&quot;', '&amp;', '&#039;', '&#123;', '&#125;']
    for e, d in zip(encoded, decoded):
        string = string.replace(e, d)
    for e, d in zip(encoded[::-1], decoded[::-1]):
        string = string.replace(e, d)
    return string

def gaddress(query, country, cookie):
    facebook_url = 'https://developers.facebook.com/tools/debug/echo/?q=%s'
    map_url = 'https://www.lyft.com/api/geocode?address=%s+%s'
    headers  = {
    'Host': 'developers.facebook.com',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5','Accept-Encoding': 'deflate',
    'Connection': 'keep-alive', 'Cookie': cookie,
    'Upgrade-Insecure-Requests': '1','Cache-Control': 'max-age=0',
    'TE': 'Trailers'}
    parsed = {}
    query = query.replace('\s+','+')
    escaped = url_encode(map_url % (url_encode(query), url_encode(country)))
    response = requests.get(facebook_url % escaped, headers=headers)
    string = decode_html(response.text)
    pattern = r'''({"display_address".+"google"})'''
    matches = re.finditer(pattern, string)
    num = 0
    for match in matches:
        parsed[num] = {'address' : match.group(1)}
        num += 1
    return parsed
