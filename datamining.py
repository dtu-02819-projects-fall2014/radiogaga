# -*- coding: utf-8 -*-
"""
Created on Wed Nov 12 00:00:45 2014

@author: Rasmus
"""
import json as js
import urllib2 as ul


class JsonResponse:
    """Search and return value in json file based on keywords.
    Args:
        json_url: the json address.\n
        keys: a list or tuble of keywords til go through
    Returns:
        the value returned by the crawling process.
    """
    def __init__(self, json_url, keywords):
        self.address = json_url
        self.keywords = keywords
        self.level = 0
        self.nkeys = len(keywords)
        if self.nkeys < 1:
            raise "Not enought input keywords"
        self.open_connection(self.address)
        self.crawl_page(self.level)

    def open_connection(self, url):
        request = ul.Request(url, headers={'User-agent': 'Mozilla/5.0'})
        self.data = ul.urlopen(request).read()
        self.answear = js.loads(self.data)

    def crawl_page(self, level):  
        if level != self.nkeys:
            try:
                element = self.keywords[level]
                self.answear = self.answear[element]
                self.level = self.level + 1
                self.crawl_page(self.level)
            except:
                print """No value found at keyword:
                      %s""" % (self.keywords[level])

# The following provide an example of calling the class on itunes music store
# searching for Pink Floyd's The Endless River.
url = """https://itunes.apple.com/search?term=
         Pink+Floyd+The+Endless+River&limit=1"""
keywords = ['results', 0, 'artworkUrl100']
info = JsonResponse(url, keywords)
print(info.answear)
