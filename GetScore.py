# -*- coding: utf-8 -*-
"""
Created on Mon Nov 03 13:25:50 2014

@author: Joachim
"""

# Get mood of a song

# Moods are for example angry, happy, relaxed and sad
import lyricAnalysis as LA


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
    try:
        lyrics = LA.get_lyrics(artist, title)
        word_list = LA.lyric_tokens(lyrics)
        lyric_score = LA.lyric_analyse(word_list, moods)
    except:
        lyric_score = [-1, -1, -1, -1]
    return(lyric_score)

artist = 'David Guetta featuring Kelly Rowland'
title = 'When Love Takes Over'
moods = 'mood_lib.csv'

lyric_score = get_score(artist, title, moods)
