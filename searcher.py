import tweepy
from geocoder import Geocoder
from keys import Keys


class Searcher():

    def search(self, keyword=None, city=None, state=None, coordinates=None, radius='5mi'):
        auth = tweepy.OAuthHandler(Keys.twitter_oauth_key1, Keys.twitter_oauth_key2)
        auth.set_access_token(Keys.twitter_access_token1, Keys.twitter_access_token2)
        api = tweepy.API(auth)

        if coordinates is None:
            geo = Geocoder()
            coordinates = geo.getCoordinates(city, state)

        coordinate_str = '{lat},{lng},'.format(**coordinates) + radius

        tweets = api.search(keyword, count=100, geocode=coordinate_str)

        tweets.sort(reverse=True, key=lambda x: x.author.followers_count)

        return [(t.author.name, t.text, t.created_at, t.retweet_count, t.author.followers_count, t.author.profile_image_url, t.id) for t in tweets]

if __name__ == '__main__':
    s = Searcher()
    #l = s.search('warriors', city='Boston', state='MA')
    l = s.search(coordinates={'lat': 42, 'lng': -71.89888888})
    for x in l:
        print x