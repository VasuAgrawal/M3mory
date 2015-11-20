import json
import urllib2
import fuckit
import base64
import numpy as np
import cv2
import block_parser as bp

keys = ""
with open("keys.txt") as f:
    keys = f.read()

keys = keys.splitlines()

ckey = keys[0]

history = 50
page = "feed"

postURL = "https://graph.facebook.com/v2.5/me/%s?limit=%d&access_token=%s" % (page, history, "%s")
objIDURL = "https://graph.facebook.com/v2.5/me/%s?fields=object_id&limit=%d&access_token=%s"% (page, history, "%s")
likeURL = "https://graph.facebook.com/v2.5/me/%s?fields=likes.limit(%d)&limit=%d&access_token=%s" % (page, history, history, "%s")
imageURL = "https://graph.facebook.com/v2.5/%s?fields=source&access_token=%s"

class Event(object):
    def __init__(self):
        self.likes = 0
        self.image = None
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
    try:
        response = urllib2.urlopen(URL % ckey).read()
        j = json.loads(response)
        add_to_dict(j.get("data", []))
    except:
        print URL % ckey

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
                    data_dict[key].image = base64.b64encode(f)

# Return date in integer format
# "2015-11-20T09:04:36+0000" (string) --> 20151120 (integer)
def getDate(time):
    time = time[:10]
    time = time.replace("-", "")
    time = int(time)
    print time
    return time

def getRunningAverage(times, i):
    PERIOD = 5
    total = 0
    for k in xrange(PERIOD):
        if (i - k < 0): return total/PERIOD
        time = times[i-k]
        try:
            total += getDate(time.created_time)
            break
        except AttributeError:
            pass
    return total/PERIOD

def getTimeBlocks(times):
    length = len(times)
    for i in xrange(length):
        runningAverage = getRunningAverage(times, i)
    return

def main():
    get(postURL)
    get(objIDURL)
    get(likeURL)
    getImage()

    times = [(data_dict[k].created_time,k) for k in data_dict]
    times.sort()

    sorted_times = [data_dict[k] for t,k in times]
    sorted_times = sorted_times[-11:-6]

    bp.process(sorted_times)

    # for s in sorted_times:
        # print s
        # if s.image != None:
            # f = base64.b64decode(s.image)
            # arr = np.asarray(bytearray(f), dtype = np.uint8)
            # img = cv2.imdecode(arr, -1)
            # cv2.imshow("lol", img)
            # if cv2.waitKey() & 0xFF == 27:
                # cv2.destroyWindows()

main()
