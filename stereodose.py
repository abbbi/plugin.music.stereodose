from bs4 import BeautifulSoup, SoupStrainer
#import requests
from json import loads as json_loads

import xbmcgui
import xbmcplugin
import urllib
import urlparse

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])
mode = args.get('mode', None)
#
xbmcplugin.setContent(addon_handle, 'movies')

BASE_URL = "https://www.stereodose.com"

def get_streams(drug, mood):
    ''' 
        parse streams from created java script code 
        tansform to python object by json

        TODO:
        1) parse var sc_client_id = "5a1f0425ba83c55eeb08b895d48eec9a";
        2) get stream_id from json
        3) construct URL:
         https://api.soundcloud.com/tracks/STREAM_ID/stream?client_id=sc_client_id
         -> this should be playable directly from KODI
    
    '''
    html = BeautifulSoup(urllib.urlopen(BASE_URL + '/playlist/' + drug + '/' + mood).read(), parse_only=SoupStrainer('script'))
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
    print "gretdrugs"
    html = BeautifulSoup(urllib.urlopen(BASE_URL).read(), parse_only=SoupStrainer('a'))
    drugs = dict()
    for link in html.find_all('a', {'class':"filter_option"} ,href=True):
        print "loop"
        linkdata = link.get('href')
        ''' only return official playlists for the moment '''
        if "playlist" in linkdata:
            start,dtype,drug,mood = linkdata.split('/')
            if not drugs.has_key(drug):
                drugs[drug]=[]

            drugs[drug].append(mood)

    if len(drugs) <= 0:
        return None

    print "returndrugs"
    return drugs

drugs = get_drugs()

if drugs != None:
    dialog = xbmcgui.Dialog()
    drug_list = drugs.keys()
    drug_choice = dialog.select('Select drug', drug_list)
    del dialog

    dialog = xbmcgui.Dialog()
    mood_list = drugs[drug_list[drug_choice]]
    print drug_choice
    print mood_list
    mood_choice = dialog.select('Select mood', mood_list)
    del dialog
    
    stream_mood = mood_list[mood_choice]
    stream_drug = drug_list[drug_choice]

    print "playlist/" + stream_drug + "/" + stream_mood

    streams = get_streams(stream_drug, stream_mood)

    l = 0
    for stream in streams:
        li = xbmcgui.ListItem("Stream ID: " + str(l), iconImage='DefaultVideo.png')
        l=l+1
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=stream, listitem=li)
 
    xbmcplugin.endOfDirectory(addon_handle)

xbmcplugin.endOfDirectory(addon_handle)
