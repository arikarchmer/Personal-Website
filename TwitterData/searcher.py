import tweepy
from TwitterData.TDkeys import TDkeys
from sentimentAnalyzer import SentimentAnalyzer
from TwitterData.geocoder import Geocoder
import requests
import httplib


class Searcher():

    def search(self, keyword=None, city=None, state=None, coordinates=None, radius='5mi'):
        auth = tweepy.OAuthHandler(TDkeys.consumer_key, TDkeys.consumer_secret)
        auth.set_access_token(TDkeys.access_token, TDkeys.access_token_secret)
        api = tweepy.API(auth)

        if coordinates is None:
            # geo = Geocoder()
            # coordinates = geo.getCoordinates(city, state)
            tweets = api.search(q=keyword)
        else:
            coordinate_str = '{lat},{lng},'.format(**coordinates) + radius
            tweets = api.search(q=keyword, geocode=coordinate_str, count=20, include_entities=True)

        tweets.sort(reverse=True, key=lambda x: x.author.followers_count)

        a = SentimentAnalyzer()

        return [(t.author.name, t.text, t.user.screen_name, t.entities, t.author.followers_count, t.author.profile_image_url, t.id, a.sentiment(t.text), a.relevance(t.text, keyword)) for t in tweets]


if __name__ == '__main__':
    s = Searcher()
    a = SentimentAnalyzer()
    #l = s.search('celtics', city='Boston', state='MA')
    l = s.search(coordinates={'lat': 42, 'lng': -71.89888888}, keyword=['soccer'])
    for x in l:
        print x

    # a.analyze(l[0][1])