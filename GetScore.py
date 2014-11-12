# -*- coding: utf-8 -*-
"""
Created on Mon Nov 03 13:25:50 2014

@author: Joachim
"""

# Get mood of a song

# Moods are for example angry, happy, relaxed and sad
import lyricAnalysis as LA


def GetScore(artist, title, moods):
    """Computes a score of how angry, happy, relaxed, sad, etc. a song is.
    Args:
        artist (str): Name of a music artist.
        title (str): Title of a song by a music artist.
        moods (list of str): List with moods to be used when computing score.
    Returns:
        int: Score that indicates how angry, happy, relaxed, sad, etc.
        the specified song is.
    Example:
        >>> lyricScore = GetScore('David Guetta featuring Kelly Rowland',
                                  'When Love Takes Over',
                                  ['angry', 'happy', 'relaxed', 'sad'])
        >>> lyricScore
        [35, 22, 32, 49]
    """
    try:
        lyrics = LA.getlyrics(artist, title)
        wordlist = LA.lyricTokens(lyrics)
        lyricScore = LA.lyricAnalyse(wordlist, moods)
    except:
        lyricScore = [-1, -1, -1, -1]
    return(lyricScore)

artist = 'David Guetta featuring Kelly Rowland'
title = 'When Love Takes Over'
moods = ['angry', 'happy', 'relaxed', 'sad']

lyricScore = GetScore(artist, title, moods)
