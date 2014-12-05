# -*- coding: utf-8 -*-
r"""
test_script - Radiogaga.

This file belongs to Joachim Blom Hansen, Rasmus Jessen Aaskov and Soren
Trads Steen.
"""

from lyricanalysis import get_score
from gettempo import getbpm
from ml import EJ


def test_getscore():
    assert get_score('Metallica', 'One', 'mood_lib.csv') == [
        207.3170731707317, 85.36585365853658,
        158.53658536585365, 60.97560975609756]
    assert get_score(u'Mø', 'Pilgrim', 'mood_lib.csv') == [
        107.6923076923077, 107.6923076923077,
        153.84615384615384, 76.92307692307692]


def test_getbpm():
    assert getbpm('Metallica', 'One') == 123.911
    assert getbpm(u'Mø', 'Pilgrim') == 79.31


def test_EJ():
    assert EJ([1], [1]) == 1
    assert EJ([0], [0]) == 0
