'''
    Unused file: spider.py
    Unknown bug when word2vec model is imported
'''

from collections import deque

import data
import parse
# import similarity
import time

import scrapy

frontier = ["https://en.wikipedia.org/wiki/Main_Page"]
searches = data.searches

class BreadthSpider(scrapy.Spider):
    name = 'BFS'

    def start_requests(self):
        request = scrapy.Request(url = frontier[0], callback = self.parse)
        request.meta["frontier"] = frontier
        yield request
    
    def parse(self, response):
        frontier = response.meta["frontier"]
        links = parse.parseLinks(response)
        '''
        topics = parse.parseKeywords(response)
        for topic in topics:
            for search in searches:
                # s, t, score = similarity.getSim(search, topic)
                relevance[(s, t)] = score
        '''
        if links:
            frontier.extend(links)
        if frontier:
            request = scrapy.Request(url = frontier[0], callback = self.parse)
            request.meta["frontier"] = frontier[1:]
            yield request

# Run the following command in the command line:
# scrapy runspider spider.py
