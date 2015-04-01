from bs4 import BeautifulSoup, SoupStrainer
from requests import get as http_get
from json import loads as json_loads


BASE_URL = "https://www.stereodose.com"

def get_streams(drug, mood):
    ''' 
        parse streams from created java script code 
        tansform to python object by json
    '''
    html = BeautifulSoup(http_get(BASE_URL + '/playlist/' + drug + '/' + mood).content, parse_only=SoupStrainer('script'))
    stream_script = str(html('script')[1])
    script_parse = stream_script.split('[{', 1)[1].rsplit('}];', 1)[0]
    streamdata = '[{' + script_parse + '}]'
    jsondata = json_loads(streamdata)
    streams = []
    for stream in jsondata:
        streams.append(stream['soundurl'])

    if len(streams) <= 0:
        return None

    return streams

def get_drugs():
    '''
        return list of possible drugs and moods 
        to choose
    '''
    html = BeautifulSoup(http_get(BASE_URL).content, parse_only=SoupStrainer('a'))
    drugs = dict()
    for link in html.find_all('a', {'class':"filter_option"} ,href=True):
        linkdata = link.get('href')
        ''' only return official playlists for the moment '''
        if "playlist" in linkdata:
            start,dtype,drug,mood = linkdata.split('/')
            if not drugs.has_key(drug):
                drugs[drug]=[]

            drugs[drug].append(mood)

    if len(drugs) <= 0:
        return None

    return drugs

drugs =  get_drugs()

for drug in drugs:
    print drug
    for mood in drugs[drug]:
        print mood
        print get_streams(drug,mood)
