# -*- coding: utf-8 -*-
import urllib2 as ul
import datamining as dm

def getbpm(artist, title):
    artist = artist.split(' feat', 1)[0]
    artist = ul.quote(artist.encode('utf-8'))
    title = ul.quote(title.encode('utf-8'))
    api_key = '6CQET4WZOPHVC3RCZ'

    url_str_id = "http://developer.echonest.com/api/v4/song/search?api_key={0}&artist={1}&title={2}"
    url_str_id = url_str_id.format(api_key, artist, title)

    keywords = ['response','songs',0,'id']

    try:
        jr = dm.JsonResponse(url_str_id, keywords)
        song_id = jr.answer

        url_str_bpm = "http://developer.echonest.com/api/v4/song/profile?api_key={0}&id={1}&bucket=audio_summary"
        url_str_bpm = url_str_bpm.format(api_key, song_id)    

        keywords = ['response', 'songs', 0, 'audio_summary', 'tempo']
        jr = dm.JsonResponse(url_str_bpm, keywords)
        song_tempo = jr.answer

        return(song_tempo)

    except:
        print('Error: track was not found in Echonest: ' + artist + ' ' + title)
        return(0)
