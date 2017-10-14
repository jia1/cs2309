from bs4 import BeautifulSoup
from time import time
from urllib.parse import urlparse
import requests

import math
import rake, random, re
rakeInstance = rake.Rake('./Resources/RAKE/SmartStoplist.txt')
specialString = ['//', '    ', '\\']

# kgr
# 2012, March 8
# Get Domain Name from URL
# http://stackoverflow.com/questions/9626535/get-domain-name-from-url
def getDomain(url):
    parsed = urlparse(url)
    domain = '{uri.scheme}://{uri.netloc}'.format(uri = parsed)
    return domain

def parseClass(className, url):
    def alphaOrSpace(string):
        return all(c.isalpha() or c.isspace() for c in string)
    resp = getResponse(url)
    html = resp.read()  
    soup = BeautifulSoup(html, 'lxml')
    elem = soup.select('.' + className)
    elem = map(lambda x: x.string, elem)
    elem = filter(lambda x: alphaOrSpace(x), elem)
    # return list(map(lambda x: x.replace(' ', '_'), elem))
    return list(map(lambda x: x.split(' '), elem))

# Adapted from Pieters M. (2014)
def parseLinks(resp):
    domain = getDomain(resp.url)
    soup = BeautifulSoup(resp.text, "lxml", from_encoding = resp.encoding)
    edges = set()

    for link in soup.find_all('a', href = True):
        u = link['href']
        if u and u[0] not in ['#', '?']:
            if u[0] == '/':
                u = domain + u
            edges.add(u)
    
    return edges

def parseKeywords(resp): return replaceSpace(parseRake(parseText(resp)))

# Adapted from Bochi, J. & Tugrul, K. (2016)
def parseText(resp):
    html = resp.text
    soup = BeautifulSoup(html, 'lxml')
    resultSetText = soup.findAll(text = True)
    tags = ['style', 'script', '[document]', 'head', 'title']
    
    def isVisible(doc):
        string = str(doc)
        return len(doc) >= 3 and \
            not (doc.parent.name in tags
                or re.match('<!--.*-->', string))

    def stripString(navigableString):
        stripped = navigableString.strip()
        encoded = stripped.encode('utf-8')
        string = str(encoded)
        finalString = ""
        for s in re.findall("'([^']*)'", string):
            if isShort(s):
                finalString = randomHash
            else:
                finalString += s
        return finalString

    def isReadable(string):
        return string != randomHash \
            and not any(special in string for special in specialString)

    def isShort(string): return len(string) < 3
    
    visible = filter(isVisible, resultSetText)
    randomHash = str(random.getrandbits(128))
    strippedStrings = map(stripString, visible)
    listText = filter(isReadable, strippedStrings)
    return ', '.join(listText)

def parseRake(string): return rakeInstance.run(string)

def replaceSpace(rakeOutput):
    return map(lambda w: w[0].split(' '), rakeOutput)

# TEST
def test():
    strt = time()
    example = "http://www.comp.nus.edu.sg/"
    resp = requests.get(example)
    text = parseText(resp)
    keywords = parseKeywords(resp)
    print("DOMAIN:\t%s\n" % getDomain(example))
    print("LINKS:\t%s\n" % (parseLinks(resp)))
    print("TEXT:\t%s\n" % text)
    print("WORDS:\t%s\n" % list(keywords))
    print("TIME:\t%f\t\n" % (time() - strt), end = '\n')

# test()
