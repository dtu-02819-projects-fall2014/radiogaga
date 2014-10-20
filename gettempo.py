import json
import urllib2 as ul

def getbpm(artist,title):
    artist = artist.split(' feat',1)[0]
    artist = ul.quote(unicode(artist,'utf-8').encode('utf-8'))
    title = ul.quote(unicode(title,'utf-8').encode('utf-8'))
    
    url_str_id = 'http://developer.echonest.com/api/v4/song/search?api_key=6CQET4WZOPHVC3RCZ&artist='+artist+'&title='+title
    
    ul_req_id = ul.Request(url_str_id)
    json_str_id = ul.urlopen(ul_req_id).read()
    json_data_id = json.loads(json_str_id)
    
    #json_output = json.dumps(json_data,indent=True)
    
    #with open(artist + '_' + title + '.json','w') as jf:
     #   jf.write(json_output)
    song_id = json_data_id['response']['songs'][0]['id']
    
    url_str_bpm = 'http://developer.echonest.com/api/v4/song/profile?api_key=6CQET4WZOPHVC3RCZ&id=' + song_id +'&bucket=audio_summary'
    ul_req_bpm = ul.Request(url_str_bpm)
    json_str_bpm = ul.urlopen(ul_req_bpm).read()
    json_data_bpm = json.loads(json_str_bpm)
    
    #json_output = json.dumps(json_data_bpm,indent=True)
    
    #with open(artist + '_' + title + '.json','w') as jf:
    #    jf.write(json_output)
    
    song_tempo = json_data_bpm['response']['songs'][0]['audio_summary']['tempo']
    print(song_tempo)
