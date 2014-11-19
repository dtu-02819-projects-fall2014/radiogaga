# -*- coding: utf-8 -*-
from __future__ import division
import urllib2 as ul
import csv
import math
from numpy import multiply
from nltk.tokenize import RegexpTokenizer
import datamining as dm


def get_score(artist, title, moods):
    """Computes a score of how angry, happy, relaxed, sad, etc. a song is.
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

    token = "db563b8c83b3347348b13b2860e49f32a7461eb269ca19a1"
    json_url = "https://community.musixmatch.com/ws/1.1/track.lyrics.get"
    json_url = json_url + "?app_id=community-app-v1.0&usertoken={0}&format="
    json_url = json_url + "json&part=lyrics_crowd%2Cuser&commontrack_vanity_id"
    json_url = json_url + "={1}%2F+{2}"
    json_url = json_url.format(token, artist, title)

    keywords = ['message', 'body', 'lyrics', 'lyrics_body']
    jr = dm.JsonResponse(json_url, keywords)
    lyrics = jr.answer
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
