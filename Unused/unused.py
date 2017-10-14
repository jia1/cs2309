# Run the following command in the command line:
# python -V
# Python 3.5.2 :: Anaconda 4.1.1 (64-bit)

''' Unused Programs: crawl.py '''
'''
    A. Original bfsCrawl
        - urllib.request.urlopen -> HTTP Error 429: Too Many Requests
        - time.sleep() did not solve the error
        - The relevance dictionary cannot handle the memory load too
'''
'''
def bfsCrawl(frontier, iterations):
    i, frontier, relevance = 0, deque(frontier), {}
    while frontier and i < iterations:
        url = frontier.popleft()
        resp = requests.get(url)
        links = deque(parse.parseLinks(resp))
        topics = parse.parseKeywords(resp)
        for topic in topics:
            for search in searches:
                score = similarity.getSim(search, topic)
                relevance[str((search, topic))] = score
        frontier.extend(links)
        i += 1
    return (frontier, relevance)
'''

'''
    B. Code snippet for writing unvisited links to a file
        - Originally in bfsCrawl function
'''
'''
    with open('frontier.txt', 'w') as g:
        for url in frontier:
            g.write('%s\n' % url)
    g.close()
'''

'''
    C. Function call for initialising keywords and seeds
        - By crawling relevant websites containing such information
        - Originally in test function
'''
'''
    initSeeds("http://www.alexa.com/siteinfo/", \
        "http://www.alexa.com/topsites/countries/US")
    initTopics("keywords", \
        "http://www.pagetraffic.com/blog/most-popular-keywords-on-search-engines")
'''

''' Unused Programs: parse.py '''
'''
    A. Function which accepts a URL and returns a Response object
        - urllib.requests.urlopen
        - Encounters HTTP Error 429: Too Many Requests
'''
'''
from urllib.request import urlopen

def getResponse(url = "https://en.wikipedia.org/wiki/Main_Page"):
    return urlopen(url)
'''

'''
    B. Initialise a BeautifulSoup instance
        - Based on the Response object in (A)
        - Originally in parseLinks function
'''
# Retrieve links from web pages using Python and BeautifulSoup
# http://stackoverflow.com/questions/1080411/
# retrieve-links-from-web-page-using-python-and-beautifulsoup
'''
domn = getDomain(resp.geturl())
soup = BeautifulSoup(resp, "lxml", \
        from_encoding = resp.info().get_param('charset'))
'''

'''
    C. Data types in parseText function
        - resp data type is obsolete (replaced by requests library)
'''
# resp: <class 'http.client.HTTPResponse'>
# html: <class 'bytes'>
# soup: <class 'bs4.BeautifulSoup'>
# resultSetText: <class 'bs4.element.ResultSet'><class 'bs4.element.Doctype'>
# visible: <class 'filter'><class 'bs4.element.NavigableString'>
# strippedStrings: <class 'map'><class 'str'>
# listText: <class 'filter'><class 'str'>
'''
html = resp.read()
'''
