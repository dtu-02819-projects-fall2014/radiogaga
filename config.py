# -*- coding: utf-8 -*-
"""
Created on Mon Nov 17 14:35:51 2014

@author: Søren bærbar
"""
import csv


def getfromconfig():
    """
    Return fields from a single line csv file.
    """
    with open('configuration.csv') as f:
        r = csv.reader(f)
        line = r.next()
    return(line)
