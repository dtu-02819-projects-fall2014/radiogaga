r"""
gettempo - Radiogaga.

This file belongs to Joachim Blom Hansen, Rasmus Jessen Aaskov and Soren
Trads Steen.
"""
import urllib2 as ul
import datamining as dm
from config import getfromconfig


def getbpm(artist, title):
    """Return the bpm for the song.

    Args:
        artist: artist name of song.
        title: title name of song.
    Returns:
        bpm: beats pr minute,
    """
    artist = artist.split(' feat', 1)[0]
    artist = ul.quote(artist.encode('utf-8'))
    title = ul.quote(title.encode('utf-8'))
    
    # Get the API key
    line = getfromconfig()
    api_key = line[4]

    url_str_id = """http://developer.echonest.com/api/v4/song/search?"""
    url_str_id = url_str_id + """api_key={0}&artist={1}&title={2}"""
    url_str_id = url_str_id.format(api_key, artist, title)

    keywords = ['response', 'songs', 0, 'id']

    try:
        jr = dm.JsonResponse(url_str_id, keywords)
        song_id = jr.answer

        url_bpm = """http://developer.echonest.com/api/v4/song/profile?"""
        url_bpm = url_bpm +"""api_key={0}&id={1}&bucket=audio_summary"""
        url_bpm = url_bpm.format(api_key, song_id)

        keywords = ['response', 'songs', 0, 'audio_summary', 'tempo']
        jr = dm.JsonResponse(url_bpm, keywords)
        song_tempo = jr.answer

        return(song_tempo)

    except:
        print('Error: track was not found in Echonest: ' + artist + title)
        return(0)
