import json
import urllib2

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
    add_to_dict(j["data"])

def getImage():
    for key in data_dict:
        if "object_id" in data_dict[key].__dict__:
            URL = imageURL % (data_dict[key].object_id, ckey)
            resp = urllib2.urlopen(URL).read()
            j = json.loads(resp)
            print j

def main():
    get(postURL)
    get(objIDURL)
    get(likeURL)
    getImage()

    times = [(data_dict[k].created_time,k) for k in data_dict]
    for t,k in sorted(times)[::-1]:
        print data_dict[k]
main()
