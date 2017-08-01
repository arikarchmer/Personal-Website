import tweepy
from TwitterData.TDkeys import TDkeys
from sentimentAnalyzer import SentimentAnalyzer
from TwitterData.geocoder import Geocoder
import requests
import httplib
import json
import collections


class Searcher():

    def convert(self, data):
        if isinstance(data, basestring):
            return data.encode('utf-8')
        elif isinstance(data, collections.Mapping):
            return dict(map(self.convert, data.iteritems()))
        elif isinstance(data, collections.Iterable):
            return type(data)(map(self.convert, data))
        else:
            return data

    def search(self, keyword=None, city=None, state=None, coordinates=None, radius=5000):
        auth = tweepy.OAuthHandler(TDkeys.consumer_key, TDkeys.consumer_secret)
        auth.set_access_token(TDkeys.access_token, TDkeys.access_token_secret)
        api = tweepy.API(auth)

        if coordinates is None:
            # geo = Geocoder()
            # coordinates = geo.getCoordinates(city, state)
            tweets = api.search(q=keyword)
        else:
            coordinate_str = '{lat},{lng},'.format(**coordinates) + str(float(radius) / 1600) + 'mi'
            tweets = api.search(q=keyword, geocode=coordinate_str, count=20)

        tweets.sort(reverse=True, key=lambda x: x.author.followers_count)

        a = SentimentAnalyzer()
        # print self.convert(tweets[0].entities)['urls'][0]['url']

        return [(t.author.name, t.text, t.user.screen_name, '0', t.author.followers_count, t.author.profile_image_url, t.id, a.sentiment(t.text), a.relevance(t.text, keyword)) for t in tweets]


if __name__ == '__main__':
    s = Searcher()
    a = SentimentAnalyzer()
    #l = s.search('celtics', city='Boston', state='MA')
    l = s.search(coordinates={'lat': 42, 'lng': -71.89888888}, keyword=['the'])
    for x in l:
        print x

    # a.analyze(l[0][1])