r"""
Lyricanalysis - Radiogaga.

This file belongs to Joachim Blom Hansen, Rasmus Jessen Aaskov and Soren
Trads Steen.
"""
from __future__ import division
import urllib2 as ul
import csv
import math
from numpy import multiply
from nltk.tokenize import RegexpTokenizer
import datamining as dm


def get_score(artist, title, moods):
    """Compute a score of how angry, happy, relaxed, sad, etc. a song is.
    
    Args:
        artist (str): Name of a music artist.
        title (str): Title of a song by a music artist.
        moods (list of str): List with moods to be used when computing score.
    Returns:
        int: Score that indicates how angry, happy, relaxed, sad, etc.
        the specified song is.
    """
    # Search for lyrics
    lyrics = get_lyrics(artist, title)

    # Tokenize
    word_list = lyric_tokens(lyrics)

    # Calculate the lyric score
    lyric_score = lyric_analyse(word_list, moods)

    # Check for nan
    for t in range(len(lyric_score)):
        if math.isnan(lyric_score[t]):
            lyric_score[t] = 0

    # Print result
    print(lyric_score)
    return(lyric_score)


def get_lyrics(artist, track):
    """Find the lyrics to a song.
    
    Args:
        artist (str): Name of a music artist.
        title (str): Title of a song by a music artist.
    Returns:
        str: Lyrics to the specified song.
    """
    artist = ul.quote(artist.encode('utf-8'))
    #artist = artist.split('feat', 1)[0]  # Removes any featuring artists
    track = ul.quote(track.encode('utf-8'))


    # Start by getting the track id
    api = 'apikey=e09c71c88ce173e2f2a05f9fec97fa4b'
    base = 'http://api.musixmatch.com/ws/1.1/'
    search_url = 'track.search?'
    track_url = """&q_track={0}""".format(track)
    artist_url = """&q_artist={0}""".format(artist)
    option = '&f_has_lyrics=1'
    call = base + search_url + api + track_url + artist_url + option
    an = dm.JsonResponse(call, ['message','body','track_list',0,'track','track_id'])
    track_id = an.answer
    
    # Then get the lyric with the found track id
    lyric_url = 'track.lyrics.get?'
    id_url = """&track_id={0}""".format(track_id)
    call = base + lyric_url + api + id_url
    an = dm.JsonResponse(call, ['message','body','lyrics','lyrics_body'])

    lyrics = an.answer
    
    lyrics = lyrics.replace('******* This Lyrics is NOT for Commercial use *******','')

    return(lyrics)


def lyric_tokens(lyric):
    """Tokenization of lyrics.
    
    Args:
        lyric (str): String of lyrics to a song.
    Returns:
        List of str: List of tokenized words from song lyric.
    """
    # Formatting of words to remove unnecessary new line chars,
    # censorship and apostrophes
    lyric = lyric.replace('\n', ' ')
    lyric = lyric.replace('\r', ' ')
    lyric = lyric.replace('f*ck', 'fuck')
    lyric = lyric.replace('\'', '')
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(lyric)
    # Remove words of length 1 and make letters lower case
    words = []
    for token in tokens:
        if len(token) > 1:
            words.append(token.lower())
    return(words)


def open_libraries(mood_lib):
    """Open a csv files with name ending in 'WordLib.csv'.
       
    Args:
        moods (list of str): List with names of text files.
    Returns:
        List of list of str: List of lists with words from specified libraries.
    """
    mood_list = []
    with open(mood_lib, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            mood_list.append(row)
    return(mood_list)


def lyric_analyse(lyric_list, mood_lib):
    """Count the number of times a word is in the mood library.
        
    Args:
        lyric_list (list of str): List of words from lyrics
        moods (list of str): List with names of word libraries
    Returns:
        int: Number of times a word from lyrics is found in each library.
    """
    mood_list = open_libraries(mood_lib)
    word_count = [0]*len(mood_list)
    # Count
    for i in range(len(mood_list)):
        for word in lyric_list:
            temp_count = mood_list[i].count(word)
            word_count[i] = word_count[i]+temp_count
    # Scaling and division by length of song
    word_count = multiply(1000, word_count)

    if len(lyric_list) > 0:
        word_count = word_count/len(lyric_list)

    word_count = word_count.tolist()
    return(word_count)
