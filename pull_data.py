import json
import urllib2
import fuckit
import base64
import copy
#import numpy as np
#import cv2

keys = ""
with open("keys.txt") as f:
    keys = f.read()

keys = keys.splitlines()

ckey = keys[0]

history = 100
page = "feed"

postURL = "https://graph.facebook.com/v2.5/me/%s?limit=%d&access_token=%s" % (page, history, "%s")
objIDURL = "https://graph.facebook.com/v2.5/me/%s?fields=object_id&limit=%d&access_token=%s"% (page, history, "%s")
likeURL = "https://graph.facebook.com/v2.5/me/%s?fields=likes.limit(%d)&limit=%d&access_token=%s" % (page, history, history, "%s")
imageURL = "https://graph.facebook.com/v2.5/%s?fields=source&access_token=%s"

class Event(object):
    def __init__(self):
        self.likes = 0
        pass

    def __str__(self):
        return str(self.__dict__)

data_dict = dict()

def add_to_dict(d):

    global data_dict
    for sub in d:
        e = None

        if sub["id"] not in data_dict:
            e = Event()
            e.fbid = sub["id"]
        else:
            e = data_dict[sub["id"]]

        for key in sub:
            if key == "likes":
                e.__dict__["likes"] = len(sub[key]["data"])
            elif key != "id":
                e.__dict__[key] = sub[key]

        data_dict[sub["id"]] = e

def get(URL):
    response = urllib2.urlopen(URL % ckey).read()
    j = json.loads(response)
    add_to_dict(j.get("data", []))

def getImage():
    for key in data_dict:
        if "object_id" in data_dict[key].__dict__:
            URL = imageURL % (data_dict[key].object_id, ckey)
            src = ""
            with fuckit:
                resp = urllib2.urlopen(URL).read()
                j = json.loads(resp)
                src = j["source"]
                if ".jpg" in src:
                    data_dict[key].source = src
                    f = urllib2.urlopen(src).read()
                    """
                    arr = np.asarray(bytearray(f), dtype=np.uint8)
                    img = cv2.imdecode(arr, -1)
                    cv2.imshow("ha ha ha!", img)
                    if cv2.waitKey() & 0xFF == 27:
                        cv2.destroyAllWindows()
                    """

# Return date in integer format
# "2015-11-20T09:04:36+0000" (string) --> 20151120 (integer)
def getDate(time):
    time = time[:10]
    time = time.replace("-", "")
    time = int(time)
    return time

def getBlock(times, i):
    block = [times[i]]
    date = getDate(times[i].created_time)
    length = len(times)
    if (i == length - 1): return block

    nextDate = getDate(times[i+1].created_time)
    # Append to block only if dates are close to each other
    while (i != length - 1 and date + 3 > nextDate):
        i += 1
        block.append(times[i])
        nextDate = getDate(times[i].created_time)
    return block

def getTimeBlocks(times):
    length = len(times)
    timeBlocks = []
    i = 0
    while i < length:
        newBlock = getBlock(times, i)
        i += len(newBlock)
        timeBlocks.append(newBlock)
    return timeBlocks

def filterBlocks(blocks):
    newBlocks = []
    for block in blocks:
        if (len(block) != 1 or block[0].likes > 70):
            newBlocks.append(block)
    return newBlocks

def main():
    get(postURL)
    get(objIDURL)
    get(likeURL)
    getImage()

    times = [(data_dict[k].created_time,k) for k in data_dict]
    times.sort()

    sorted_times = [data_dict[k] for t,k in times]

    blocks = getTimeBlocks(sorted_times)
    blocks = filterBlocks(blocks)

    for block in blocks:
        print "-------"
        for time in block:
            print time
        print "-------"

main()
