import tweepy
from TwitterData.TDKeys import TDKeys
from sentimentAnalyzer import SentimentAnalyzer


class Searcher():

    def search(self, keyword=None, coordinates=None, radius=5000):
        auth = tweepy.OAuthHandler(TDKeys.consumer_key, TDKeys.consumer_secret)
        auth.set_access_token(TDKeys.access_token, TDKeys.access_token_secret)
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

        return [(t.author.name, t.text, t.user.screen_name, '0', t.author.followers_count, t.author.profile_image_url, t.id, a.sentiment(t.text), a.relevance(t.text, keyword)) for t in tweets]


if __name__ == '__main__':
    s = Searcher()
    a = SentimentAnalyzer()
    #l = s.search('celtics', city='Boston', state='MA')
    l = s.search(coordinates={'lat': 42, 'lng': -71.89888888}, keyword=[''])
    for x in l:
        print x

    # a.analyze(l[0][1])