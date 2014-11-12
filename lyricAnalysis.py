# -*- coding: utf-8 -*-
"""
Created on Mon Oct 27 13:31:03 2014

@author: Joachim
"""
import json
import urllib2 as ul
from nltk.tokenize import RegexpTokenizer


def getlyrics(artist, title):
    """Find the lyrics to a song.
    Args:
        artist (str): Name of a music artist.
        title (str): Title of a song by a music artist.
    Returns:
        str: Lyrics to the specified song
    Example:
        >>> lyrics = getlyrics('David Guetta featuring Kelly Rowland',
                               'When Love Takes Over')
        >>> lyrics
        'It's complicated It always is That’s just the way...' etc.
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


def lyricTokens(lyric):
    """Tokenization of lyrics.
    Args:
        lyric (str): String of lyrics to a song.
    Returns:
        List of str: List of tokenized words from song lyric.
    Example:
        >>> words = lyricTokens('''It's complicated It always is That’s...''')
        >>> words
        ['its', 'complicated', 'it', 'always', 'is', 'that']
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
    for i in tokens:
        if len(i) > 1:
            words.append(i.lower())
    return(words)


def openLibraries(moods):
    """Opens text files with name ending in 'WordLib.txt',
       for example 'angryWordLib.txt'.
    Args:
        moods (list of str): List with names of text files.
    Returns:
        List of list of str: List of lists with words from specified libraries.
    Example:
        >>> wordLib = openLibraries(['angry','happy','relaxed','sad'])
        >>> wordLib
        ['angry, love, could, heart, death, ...] etc.
    """
    wordLib = []
    for i in moods:
        tempLib = open(i+'WordLib.txt', 'r')
        tempRead = tempLib.read()
        wordLib.append(tempRead)
        tempLib.close()
    return wordLib


def lyricAnalyse(lyriclist, moods):
    """Counts the number of times a word in the lyrics is found in each
        word library
    Args:
        lyriclist (list of str): List of words from lyrics
        moods (list of str): List with names of word libraries
    Returns:
        int: Number of times a word from lyrics is found in each library.
    Example:
        >>> wordCount = lyricAnalyse([u'its', u'complicated',
                                      u'it', u'always',...],
                                      ['angry','happy','relaxed','sad'])
        >>> wordCount
        [35, 22, 32, 49]
    """
    wordLib = openLibraries(moods)
    # Tokenize word libraries
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = []
    for lib in wordLib:
        tokens.append(tokenizer.tokenize(lib))
    wordCount = [0]*len(wordLib)
    # Count
    for i in range(0, len(wordLib)):
        for word in lyriclist:
            tempcount = tokens[i].count(word)
            wordCount[i] = wordCount[i]+(float(tempcount)*1000)/len(lyriclist)
    return(wordCount)
