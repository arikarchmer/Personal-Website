import tweepy
from TwitterData.TDkeys import TDkeys
from TwitterData.geocoder import Geocoder
import requests
import httplib


class Searcher():

    def search(self, keyword=None, city=None, state=None, coordinates=None, radius='5mi'):
        auth = tweepy.OAuthHandler(TDkeys.consumer_key, TDkeys.consumer_secret)
        auth.set_access_token(TDkeys.access_token, TDkeys.access_token_secret)
        api = tweepy.API(auth)

        # api.update_status(status="hello, world")

        if coordinates is None:
            # geo = Geocoder()
            # coordinates = geo.getCoordinates(city, state)
            tweets = api.search(q=keyword)
        else:
            coordinate_str = '{lat},{lng},'.format(**coordinates) + radius
            tweets = api.search(geocode=coordinate_str, count=20, include_entities=True)

        tweets.sort(reverse=True, key=lambda x: x.author.followers_count)

        a = Analyzer()
        # return [t.entities for t in tweets]
        return [(t.author.name, t.text, t.user.screen_name, t.entities, t.author.followers_count, t.author.profile_image_url, t.id, a.analyze(t.text)) for t in tweets]


class Analyzer():

    def analyze(self, t):

        url = 'http://text-processing.com/api/sentiment/'
        r = requests.post(url, data={'text': t, 'language': 'english'})
        res = r.content.split(':')
        print res
        return str(res[2].split(',')[0][1:]) + ',' + str(res[3].split(',')[0][1:]) + ',' + str(res[4].split(',')[0][1:-2])

if __name__ == '__main__':
    s = Searcher()
    a = Analyzer()
    #l = s.search('celtics', city='Boston', state='MA')
    l = s.search(coordinates={'lat': 42, 'lng': -71.89888888})
    for x in l:
        print x

    # a.analyze(l[0][1])