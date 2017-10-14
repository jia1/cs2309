from collections import deque

import data
import parse
import requests
import similarity
import time

seeds = deque(["https://en.wikipedia.org/wiki/Main_Page"])
searches = data.searches

def initSeeds(root, url):
    length = len(root)
    def isSite(link):
        return link != root and root in link
    def sliceLink(link):
        return link[length:]
    seeds = filter(isSite, parse.parseLinks(url))
    seeds = deque(map(sliceLink, seeds))
    print(seeds)

def initTopics(selector, url):
    topics = parse.parseClass(selector, url)
    print(topics)

def bfsCrawlWrite(frontier, iterations):
    frontier = deque(frontier)
    relevant, threshold = [], 2/3
    indent1 = 0, ' ' * 2
    indent2, indent3 = indent1 * 2, indent1 * 3
    indent4 = indent2 * 2
    i = 0
    with open('similarity.json', 'w') as f:
        f.write('[\n%s[\n%s""' % (indent1, indent2))
        while frontier and i < iterations:
            f.write(',\n%s{\n' % (indent2))
            url = frontier.popleft()
            resp = requests.get(url)
            topics = parse.parseKeywords(resp)
            f.write('%s"": ""' % (indent3))
            for topic in topics:
                relevant = False
                stringBuilder = []
                stringBuilder.append(',\n%s"%s": [\n' % (indent3, topic))
                for search in searches:
                    try:
                        score = similarity.getSim(search, topic)
                        if score >= threshold:
                            relevant = True
                            stringBuilder.append('%s"(%s, %s)",\n' % (indent4, \
                                search, score))
                    except:
                        continue
                if relevant:
                    stringBuilder[-1] = stringBuilder[-1].rstrip()[:-1]
                    stringBuilder.append('\n')
                    f.write(''.join(stringBuilder))
                    f.write('%s]' % (indent3))
            frontier.extend(deque(parse.parseLinks(resp)))
            f.write('\n%s}\n%s]' % (indent2, indent1))
            if frontier and i < iterations:
                f.write(',')
            else:
                break
            i += 1
        f.write('\n]')
    f.close()

def bfsCrawl(frontier, iterations):
    frontier = deque(frontier)
    lowLim, uppLim = 3/5, 4/5
    i, numVisited, urlVisited = 0, 0, set()
    while frontier and i < iterations:
        url = frontier.popleft()
        urlVisited.add(url)
        host = parse.getDomain(url)
        resp = requests.get(url)
        topics = parse.parseKeywords(resp)
        for topic in topics:
            for search in searches:
                try:
                    score = similarity.getSim(search, topic)
                    if lowLim < score < highLim:
                        print(str((score, search, topic, url)))
                except:
                    continue
        frontier.extend(deque(parse.parseLinks(resp) - urlVisited))
        numVisited += 1
        i += 1
    return (len(frontier), numVisited)

def dfsCrawl(stack, iterations):
    stack = deque(stack)
    lowLim, uppLim = 3/5, 4/5
    depthMax, lastHost = 3, ""
    depthLeft = depthMax
    i, numVisited, urlVisited = 0, 0, set()
    while stack and i < iterations:
        url = stack.pop()
        urlVisited.add(url)
        resp = requests.get(url)
        topics = parse.parseKeywords(resp)
        for topic in topics:
            for search in searches:
                try:
                    score = similarity.getSim(search, topic)
                    if lowLim < score < highLim:
                        print(str((score, search, topic, url)))
                except:
                    continue
        host = parse.getDomain(url)
        if host == lastHost:
            if depthLeft:
                depthLeft -= 1
                stack.extend(deque(parse.parseLinks(resp)))
            else:
                depthLeft = depthMax
        else:
            depthLeft = depthMax
            stack.extend(deque(parse.parseLinks(resp) - urlVisited))
        numVisited += 1
        i += 1
    return (len(stack), numVisited)

# TEST
def test():
    iterations = 100
    print("Iterations: %d" % iterations)
    print()
    start = time.time()
    queueSize, bfsnumVisited = bfsCrawl(seeds, iterations)
    print("Size of Queue: %d" % queueSize)
    print("Number of numVisited: %d" % bfsnumVisited)
    print("Time Taken: %f" % (time.time() - start))
    print()
    start = time.time()
    stackSize, dfsnumVisited = dfsCrawl(seeds, iterations)
    print("Size of Stack: %d" % queueSize)
    print("Number of numVisited: %d" % dfsnumVisited)
    print("Time Taken: %f" % (time.time() - start))
    print()

# test()
