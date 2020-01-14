import requests
import json

def decode_html(string):
    decoded = ['>', '<', '"', '&', '\'','{', '}']
    encoded = ['&gt;', '&lt;', '&quot;', '&amp;', '&#039;', '&#123;', '&#125;']
    for e, d in zip(encoded, decoded):
        string = string.replace(e, d)
    for e, d in zip(encoded[::-1], decoded[::-1]):
        string = string.replace(e, d)
    return string

def geoaddress(query, country=''):
    map_url = 'https://www.lyft.com/api/geocod?address={}+{}'
    headers = { 'Content-Type': 'text/html; charset=utf-8',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none','Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive','Content-Encoding': 'gzip' }

    parsed = {}
    query = query.replace(' ','+')
    map_url = map_url.format(query, country)
    response = requests.get(map_url, headers=headers)
    if response.status_code == 200:
        try:
            record = json.loads(response.content)
            data = {'display_address': record['display_address'],
                    'latitude': record.get('lat',''), 'longitude': record.get('lng',''),
                    'place_id':record.get('place_id',''), 'place_type': record.get('place_type',''),
                    'formated_address': record.get('routable_address'), 'error_flag': False}
            print(data)
        except Exception as e:
            return {'error_flag': True, 'Error': 'Interface Error with {}'.format(e)}
    else:
        return {'error_flag': True, 'Error': 'Interface Error with http code {}'.format(response.status_code)}

