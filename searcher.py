import tweepy
from geocoder import Geocoder


class Searcher():

    def search(self, keyword=None, city=None, state=None, coordinates=None, radius='5mi'):
        auth = tweepy.OAuthHandler('GiF4dfJ2YHQIBwjvwOx7LiejC', 'lzMId2A8QG07ckHGJqT7jyeTkupbtmYOA6oUtLCh9Zdj5neY4t')
        auth.set_access_token('725448716392476672-wqkOEy6iTpSYqpkmexblvTgy05bt0Xq', '3kRMffTzYSVqbisO7BAkLUyzWbopJSgOMuQXIZX8jYpzu')
        api = tweepy.API(auth)

        if coordinates is None and (city is None or state is None):
            tweets = api.search(keyword, count=100)
        elif coordinates is None and city is not None and state is not None:
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