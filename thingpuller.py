#!/usr/bin/env python

import requests
import string

def getSTLfile(keyphrase):
    things = findThings(keyPhrase)
    thing = things[1]
    return pullFile(thing)

def findThings(keyphrase):
    kp = keyphrase.replace(" ", "%20")
    baseURL = "http://www.thingiverse.com/search/relevant/things?q="
    url = baseURL + kp
    r = requests.get(url)
    thingList = list()
    rt = r.text
    while "/thing:" in rt:
        loc = rt.find("/thing:") + 7
        rt = rt[loc:]
        num = str()
        while rt[0] in string.digits:
            num += rt[0]
            rt = rt[1:]
        thingList.append(int(num))
    return thingList

def getLink(thingID):
    baseURL = "http://www.thingiverse.com/thing:"
    thingURL = baseURL + str(thingID)
    r = requests.get(thingURL)
    textify = r.text
    loc = textify.find("/download:") + len("/download:")
    textify = textify[loc:]
    num = str()
    while textify[0] in string.digits:
        num += textify[0]
    newrl = "http://www.thingiverse.com/download:" + num
    return num

def pullFile(thingID):
    link = getLink(thingID)
    with open((str(thingID) + ".stl"), 'wb') as handle:
        response = requests.get(link, stream=True)
    if not response.ok:
        return
    for block in response.iter_content(1024):
        handle.write(block)
        return (str(thingID) + ".stl")
