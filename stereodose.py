from bs4 import BeautifulSoup, SoupStrainer
from requests import get as http_get
from json import loads as json_loads

def get_streams():
    html = BeautifulSoup(http_get('https://www.stereodose.com/playlist/weed/chill').content, parse_only=SoupStrainer('script'))
    stream_script = str(html('script')[1])
    script_parse = stream_script.split('[{', 1)[1].rsplit('}];', 1)[0]
    streamdata = '[{' + script_parse + '}]'
    jsondata = json_loads(streamdata)
    for stream in jsondata:
        print stream['soundurl']

def get_drugs():
    html = BeautifulSoup(http_get('https://www.stereodose.com/').content, parse_only=SoupStrainer('a'))
    drugs = dict()
    for link in html.find_all('a', {'class':"filter_option"} ,href=True):
        linkdata = link.get('href')
        if "playlist" in linkdata:
            start,dtype,drug,mood = linkdata.split('/')
            if not drugs.has_key(drug):
                drugs[drug]=[]

            drugs[drug].append(mood)

    return drugs

get_streams()
print get_drugs()
