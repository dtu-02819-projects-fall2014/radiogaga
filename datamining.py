r"""
datamining - Radiogaga.

This file belongs to Joachim Blom Hansen, Rasmus Jessen Aaskov and Soren
Trads Steen.
"""
import json as js
import urllib2 as ul


class JsonResponse:
    
    r"""Search and return value in json file based on keywords.
    
    Args:
        json_url: the json address.
        keys: a list or tuble of keywords til go through.
    Returns:
        answear: the string returned by the crawling process. If the crawling 
        algorithm did not found the string satisfying all of the keys, it 
        will return the array containing what have been found so far. 
    """
    
    def __init__(self, json_url, keywords):
        """Initialize the JsonResponse class."""
        self.address = json_url
        self.keywords = keywords
        self.level = 0
        self.nkeys = len(keywords)
        if self.nkeys < 1:
            raise "Not enought input keywords"
        self.open_connection(self.address)
        self.crawl_page(self.level)

    def open_connection(self, url):
        """Open a connection to the page."""
        request = ul.Request(url, headers={'User-agent': 'Mozilla/5.0'})
        self.data = ul.urlopen(request).read()
        self.answer = js.loads(self.data)

    def crawl_page(self, level):
        """Crawling algorithm. Search through the json page."""
        if level != self.nkeys:
            try:
                element = self.keywords[level]
                self.answer = self.answer[element]
                self.level = self.level + 1
                self.crawl_page(self.level)
            except:
                self.answer = ''


class JsonMultiResponse:
    
    r"""Search and return value in json file based on keywords [BETA].
    
    Args:
        json_url: the json address.
        keys: a tuble with lists. Each list is then used in the crawlprocess.
    Returns:
        answear: the string returned by the crawling process. If the crawling 
        algorithm did not found the string satisfying all of the keys, it 
        will return the array containing what have been found so far. 
    """
    
    def __init__(self, json_url, keywords):
        """Initializing the JsonResponse class."""
        self.address = json_url
        self.open_connection(self.address)
        self.nset = len(keywords)
        
        self.returnthis = list()
        for keyset in keywords:
            self.level = 0
            self.nkeys = len(keyset)
            self.keyset = keyset
            self.temp_ans = self.answer
            
            self.crawl_page(self.keyset, self.level)
            self.returnthis.append(self.temp_ans)

    def open_connection(self, url):
        """Open a connection to the page."""
        request = ul.Request(url, headers={'User-agent': 'Mozilla/5.0'})
        self.data = ul.urlopen(request).read()
        self.answer = js.loads(self.data)

    def crawl_page(self, keyset, level):
        """Crawling algorithm. Search through the json page."""
        if level != self.nkeys:
            try:
                segment = self.keyset[level]
                self.temp_ans = self.temp_ans[segment]
                self.level = self.level + 1
                self.crawl_page(keyset, self.level)
            except:
                self.answer = ''
