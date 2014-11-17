# -*- coding: utf-8 -*-
"""
Created on Mon Oct 27 13:31:03 2014

@author: Joachim
"""
from __future__ import division
import json
import urllib2 as ul
from nltk.tokenize import RegexpTokenizer


def get_lyrics(artist, title):
    """Find the lyrics to a song.
    Args:
        artist (str): Name of a music artist.
        title (str): Title of a song by a music artist.
    Returns:
        str: Lyrics to the specified song
    """
    artist = ul.quote(artist.encode('utf-8'))
    artist = artist.split('feat', 1)[0]  # Removes any featuring artists
    title = ul.quote(title.encode('utf-8'))
    address = {"http": "https://community.musixmatch.com/ws/1.1/track.lyrics" +
               ".get?app_id=community-app-v1.0&usertoken=db563b8c83b3347348b" +
               "13b2860e49f32a7461eb269ca19a1&format=json&part=lyrics_crowd%" +
               "2Cuser&commontrack_vanity_id="+artist+'%2F'+title}
    headers = {'User-agent': 'Mozilla/5.0'}
    prox = ul.ProxyHandler(address)
    opener = ul.build_opener(prox, ul.HTTPHandler(debuglevel=0))
    ul.install_opener(opener)
    req = ul.Request(address["http"], None, headers)
    data = ul.urlopen(req).read()
    json_data = json.loads(data)
    lyrics = json_data['message']['body']['lyrics']['lyrics_body']
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
    lyric = lyric.replace('f*ck', 'fuck')
    lyric = lyric.replace('\'', '')
    lyric = lyric.replace('\x92', '')
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(lyric)
    # Remove words of length 1 and make letters lower case
    words = []
    for token in tokens:
        if len(token) > 1:
            words.append(token.lower())
    return(words)


def open_libraries(moods):
    """Opens text files with name ending in 'WordLib.txt',
       for example 'angryWordLib.txt'.
    Args:
        moods (list of str): List with names of text files.
    Returns:
        List of list of str: List of lists with words from specified libraries.
    """
    word_lib = []
    for mood in moods:
        temp_lib = open(mood+'WordLib.txt', 'r')
        temp_read = temp_lib.read()
        word_lib.append(temp_read)
        temp_lib.close()
    return word_lib


def lyric_analyse(lyric_list, moods):
    """Counts the number of times a word in the lyrics is found in each
        word library
    Args:
        lyric_list (list of str): List of words from lyrics
        moods (list of str): List with names of word libraries
    Returns:
        int: Number of times a word from lyrics is found in each library.
    """
    word_lib = open_libraries(moods)
    # Tokenize word libraries
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = []
    for lib in word_lib:
        tokens.append(tokenizer.tokenize(lib))
    word_count = [0]*len(word_lib)
    # Count
    for i in range(0, len(word_lib)):
        for word in lyric_list:
            temp_count = tokens[i].count(word)
            word_count[i] = word_count[i]+(temp_count*1000)/len(lyric_list)
    return(word_count)
