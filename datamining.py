# -*- coding: utf-8 -*-
import json as js
import urllib2 as ul


class JsonResponse:
    """Search and return value in json file based on keywords.
    
    Args:
        json_url: the json address.\n
        keys: a list or tuble of keywords til go through
    Returns:
        answear: the string returned by the crawling process. If the crawling 
        algorithm did not found the string satisfying all of the keys, it 
        will return the array containing what have been found so far. 
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
        self.answer = js.loads(self.data)

    def crawl_page(self, level):
        if level != self.nkeys:
            try:
                element = self.keywords[level]
                self.answer = self.answer[element]
                self.level = self.level + 1
                self.crawl_page(self.level)
            except:
                self.answer = ''
