from textblob import TextBlob
from textblob import Word
import fuckit
from difflib import SequenceMatcher

class UserEvent(object):
    # This class stores all of the data we can try to garner about a user from
    # the things on their feed.
    def __init__(self):
        self.location = dict()
        self.phrases = dict()

    def toadd(self, likes):
        return .25 * likes

    # we assume the story is always relevant to the event
    def parse_story(self, story, likes):
        loc = ""
        if "at" in story:
            loc = story[story.rfind("at") + 1:]
        else:
            return

        if len(self.location.keys()) == 0:
            self.location[loc] = self.toadd(likes)
        else:
            sims = [(SequenceMatcher(None, key, loc).ratio(),key) for key in self.location]
            m = max(sims)
            if m[0] > 0.5:
                self.location[m[1]] += self.toadd(likes)
            else:
                self.location[loc] = self.toadd(likes)

    def parse_message(self, message, likes):
        m = TextBlob(message)
        for noun in m.noun_phrases:
            if len(self.phrases.keys()) == 0:
                self.phrases[noun] = self.toadd(likes)
            else:
                sims = [(SequenceMatcher(None, key, noun).ratio(),key) for key in self.phrases]
                m = max(sims)
                if m[0] > 0.5:
                    self.phrases[m[1]] += self.toadd(likes)
                else:
                    self.phrases[noun] = self.toadd(likes)

def process(events):
    # takes in a list of events and returns a list of keywords with some
    # probability. loads of cool things that can happen here to try to classify
    # and add interesting keywords.
    ue = UserEvent()

    for event in events:
        if "message" in event.__dict__:
            print event.likes, event.message
            ue.parse_message(event.message, event.likes)
        if "story" in event.__dict__:
            print event.likes, event.story
            ue.parse_story(event.story, event.likes)

    print ue.location
    print ue.phrases

def counts(s):
    count = dict()
    for word in s:
        if word in count:
            count[word] += 1
        else:
            count[word] = 1
    return count

def main():

    s1 = """PennApps added a new photo -- with Vasu Agrawal and 3 others at Wells
    Fargo Center."""
    s2 = """PennApps added a new photo -- with Rajat Mehndiratta and 3 others at
    Wells Fargo Center."""

    m1 ="""Okay, well it is finally now my turn to make a post about PennApps.

PennApps was my first hackathon and I had a blast with my teammates Cyrus, Vasu
and Rajat.  We developed an assistive device for the visually impaired. It
allows people to send and receive information in braille through six buttons,
all encased in a single, ergonomic, 3D-printed figure. Through Bluetooth, this
device connects to an Android app that runs a virtual assistant in the
background. Users can therefore send queries and receive answers to those
queries in braille (almost like Siri talking in braille).

This device helped us win the Best AlphaLab Gear Hardware Hack, the PennApps
Best Hardware Hack, and most importantly the PennApps Grand Prize. I'm honestly
still trying to comprehend what just happened. Nonetheless, I am very, very
happy to have experienced something so memorable. A year ago I didn't even know
what a hackathon was, and had never touched hardware before. Now, I realize that
I have finally discovered my true passion: building cool things."""
    s3 = """Edward Ahn updated his profile picture."""
    m2 = """PennApps XII in a nutshell and Edward Ahn's Grand Prize
    moments."""
    s4 = "Joseph Kim and 55 others wrote on your timeline."

    ue = UserEvent()

    ue.parse_story(" ".join(s1.split()), 10)
    ue.parse_story(" ".join(s2.split()), 10)
    ue.parse_story(" ".join(s3.split()), 10)
    ue.parse_story(" ".join(s4.split()), 10)

    ue.parse_message(m1, 10)
    ue.parse_message(m2, 10)

    print ue.phrases
    print ue.location

    # print "1?"
    # tb = TextBlob(testString)
    # print tb.noun_phrases

    # print "2"
    # testString = testString.lower()
    # tb = TextBlob(testString)
    # print tb.noun_phrases

if __name__ == "__main__":
    main()
