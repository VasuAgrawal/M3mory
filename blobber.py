#!/usr/bin/env python

from textblob import TextBlob, Word
from outfile import *

def getTags(string):
  tb = TextBlob(string)
  # tb = TextBlob(str(tb.correct()))
  nouns = tb.noun_phrases
  real_nouns_of_NY = list()
  sentiment = tb.sentiment.polarity
  for noun in nouns:
    n = Word(noun)
    real_nouns_of_NY.append(n.lemmatize())
  return sentiment, real_nouns_of_NY

def testGetTags():
  str1 = "nigga nigga niga i'm 100% nigga"
  str2 = "communism is the only objectively true philosophy"
  str3 = "usa bitches"
  str4 = "it is now five thirty a m it's morning time bitches"
  str5 = "we are raffling off some hookers and blow"
  str6 = "one of which is a facebook mug and tumblr set bitches"
  str7 = "suck my dick bitches"
  str8 = "every sentence in here ends in bitches"
  str9 = "Back in the bay for Global Hackathon Finals @ Facebook HQ! Let's go CMU!! smile emoticon"
  str10 = "my heart goes out to all the people who died in paris last night. fuck isis"
  str11 = "fuck obama!"
  str12 = "9/11 boom boom plane fly into building me so sad"
  str13 = "my bitch of a grandmother just died yesterday after swallowing too much horse semen"
  str14 = "penis bitches!!!!!!!!!!!!!!!!"
  str15 = "so I'm seeing a lot of porn"
  str16 = "my dog was actually adopted into the family"
  str17 = "so your mom went surfing on my dick last night. surfing surfing surfing"
  strings = [str1, str2, str3, str4, str5, str6, str7, str8, str9, str10, str11, str12, str13, str14, str15, str16, str17]
  for big_black_dict in bunch_of_dicts:
    if 'message' in big_black_dict:
      strings.append(big_black_dict.get('message'))
  for string in strings:
    print getTags(string)

testGetTags()
