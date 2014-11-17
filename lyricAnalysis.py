# -*- coding: utf-8 -*-
"""
Created on Mon Oct 27 13:31:03 2014

@author: Joachim
"""
from __future__ import division
import json
import urllib2 as ul
import csv
from numpy import multiply
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


def open_libraries(mood_lib):
    """Opens csv files with name ending in 'WordLib.csv',
       for example 'angryWordLib.csv'.
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
    """Counts the number of times a word in the lyrics is found in each
        word library
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
    word_count = word_count/len(lyric_list)
    word_count = word_count.tolist()
    return(word_count)
