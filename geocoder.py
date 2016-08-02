#import requests
import urllib
import json
import logging
import urllib2

class Geocoder():

    key = 'AIzaSyC05pL4bzG6Ynu9pucD4yFNSzFJpqOKq-Q'
    geo_url = 'https://maps.googleapis.com/maps/api/geocode/json?'

    def getCoordinates(self, city, state):
        loc_string = city + '+' + state
        url = Geocoder.geo_url + urllib.urlencode({'key': Geocoder.key, 'address': loc_string})
        logging.info('url='+url)
        response = urllib2.urlopen(url)
        result = response.read()
        #result = requests.get(url)
        j = json.loads(result)
        #print len(j['results'])

        return {'lat': j['results'][0]['geometry']['location']['lat'],
                'lng': j['results'][0]['geometry']['location']['lng']}


if __name__ == '__main__':

    g = Geocoder()

    print g.getCoordinates(('Sydney', 'Australia'))