# -*- coding: utf-8 -*-
"""
Created on Mon Sep 29 16:12:48 2014

@author: Søren bærbar
"""

import json
import urllib2 as ul

def getbpm(artist,title):
    artist = artist.split(' feat',1)[0]
    
    artist = ul.quote(artist.encode('utf-8'))
    title = ul.quote(title.encode('utf-8'))
    #unicode(title,'utf-8')
    url_str_id = 'http://developer.echonest.com/api/v4/song/search?api_key=KEY&artist='+artist+'&title='+title
    headers = {'User-agent':'Mozilla/5.0'}
    
    ul_req_id = ul.Request(url_str_id,None, headers)
    json_str_id = ul.urlopen(ul_req_id).read()
    json_data_id = json.loads(json_str_id)
    
    try:
        song_id = json_data_id['response']['songs'][0]['id']
    except:
        print('ERROR: NOT IN ECHONEST?!?' + artist + title)
        return(0)
    url_str_bpm = 'http://developer.echonest.com/api/v4/song/profile?api_key=KEY&id=' + song_id +'&bucket=audio_summary'
    ul_req_bpm = ul.Request(url_str_bpm)
    json_str_bpm = ul.urlopen(ul_req_bpm).read()
    json_data_bpm = json.loads(json_str_bpm)
    
    song_tempo = json_data_bpm['response']['songs'][0]['audio_summary']['tempo']
    return(song_tempo)
