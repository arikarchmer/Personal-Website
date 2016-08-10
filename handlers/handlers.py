import webapp2
import jinja2
import json
from searcher import Searcher

from google.appengine.ext import db

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader('./'),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class Score(db.Model):
    """Sub model for representing a score."""
    name = db.StringProperty()
    score = db.IntegerProperty()


class FireworksHandler(webapp2.RequestHandler):

    def get(self):
        page = JINJA_ENVIRONMENT.get_template('fireworks.html')
        self.response.write(page.render())


class BellCurveSimHandler(webapp2.RequestHandler):

    def get(self):
        page = JINJA_ENVIRONMENT.get_template('bellcurvesim.html')
        self.response.write(page.render())


class SpaceTravelHandler(webapp2.RequestHandler):

    def get(self):
        page = JINJA_ENVIRONMENT.get_template('space_travel.html')
        self.response.write(page.render())


class BouncingHandler(webapp2.RequestHandler):

    def get(self):
        page = JINJA_ENVIRONMENT.get_template('bouncingball.html')
        self.response.write(page.render())


class ParticleHandler(webapp2.RequestHandler):

    def get(self):
        page = JINJA_ENVIRONMENT.get_template('particles.html')
        self.response.write(page.render())


class DrawHandler(webapp2.RequestHandler):

    def get(self):
        draw_page = JINJA_ENVIRONMENT.get_template('draw_page.html')
        self.response.write(draw_page.render())


class AboutMeHandler(webapp2.RequestHandler):

    def get(self):
        page = JINJA_ENVIRONMENT.get_template('about_me.html')
        self.response.write(page.render())


class PlayersHandler(webapp2.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'application/json'

        new_player = {'name': self.request.get('name'), 'score': self.request.get('score')}
        if new_player['score'] != '':
            score = Score(name=new_player['name'], score=int(new_player['score']))
            score.put()

        query = db.Query(Score)
        query.order('-score')

        s = [{'name': x.name, 'score': x.score} for x in query.run(limit=100)]
        obj = {'leaderboard': s, 'latest': new_player}

        self.response.write(json.dumps(obj))


class StarsHandler(webapp2.RequestHandler):

    def get(self):
        stars_page = JINJA_ENVIRONMENT.get_template('stars_page.html')
        self.response.write(stars_page.render())


#################################################################################################
################ Twitter Data ###################################################################
#################################################################################################

class TwitterHomeHandler(webapp2.RequestHandler):

    def get(self):
        home_page = JINJA_ENVIRONMENT.get_template('home_page.html')
        self.response.write(home_page.render())


class SearchHandler(webapp2.RequestHandler):

    def get(self):
        search_page = JINJA_ENVIRONMENT.get_template('search_page.html')
        self.response.write(search_page.render())


class SearchTipsHandler(webapp2.RequestHandler):

    def get(self):
        search_tips_page = JINJA_ENVIRONMENT.get_template('search_tips_page.html')
        self.response.write(search_tips_page.render())


class ResultsHandler(webapp2.RequestHandler):

    def get(self, mode):

        searcher = Searcher()
        flag = True
        if mode == 'city_state':
            k = self.request.get('keyword')
            c = self.request.get('city')
            s = self.request.get('state')
            if k and c and s:
                items = searcher.search(keyword=k, city=c, state=s)
                info = [k, c, s]
            else:
                page = JINJA_ENVIRONMENT.get_template('search_page.html')
                parameters = {'invalid': True}
                print 'bad search'
                flag = False

        elif mode == 'coordinates':
            lat = self.request.get('lat')
            lng = self.request.get('lng')
            coor= {'lat': lat, 'lng': lng}
            r = self.request.get('radius')
            if lat is None or lng is None or r is None:
                page = JINJA_ENVIRONMENT.get_template('map_page.html')
                parameters = {'fail': True}
            else:
                items = searcher.search(coordinates=coor)
                info = [lat, lng, r]

        if flag:
            if len(items) == 0:
                if mode == 'city_state':
                    page = JINJA_ENVIRONMENT.get_template('search_page.html')
                    parameters = {'invalid': True}
                elif mode == 'coordinates':
                    page = JINJA_ENVIRONMENT.get_template('map_page.html')
                    parameters = {'len': len(items)}
            else:
                parameters = {'items': items, 'info': info}
                page = JINJA_ENVIRONMENT.get_template('results_page.html')

        self.response.write(page.render(parameters))


class MapHandler(webapp2.RequestHandler):

    def get(self):
        map_page = JINJA_ENVIRONMENT.get_template('map_page.html')
        self.response.write(map_page.render())