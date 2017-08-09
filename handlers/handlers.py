import json
import jinja2
import webapp2
from google.appengine.ext import db
from TwitterData.searcher import Searcher
from tweepy import TweepError
# from Sumo.sumo import Sumo

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader('./'),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class Score(db.Model):
    """Sub model for representing a score."""
    name = db.StringProperty()
    score = db.IntegerProperty()


class CapitalismHandler(webapp2.RequestHandler):

    def get(self):
        page = JINJA_ENVIRONMENT.get_template('Animations/Particles2.html')
        self.response.write(page.render())


class ColorPuzzleHandler(webapp2.RequestHandler):

    def get(self):
        page = JINJA_ENVIRONMENT.get_template('expiri.html')
        self.response.write(page.render())


class RecursiveTreeHandler(webapp2.RequestHandler):

    def get(self):
        page = JINJA_ENVIRONMENT.get_template('Animations/recursivetree.html')
        self.response.write(page.render())


class MarchHandler(webapp2.RequestHandler):

    def get(self):
        page = JINJA_ENVIRONMENT.get_template('MarchMad.html')
        self.response.write(page.render())


class MonteCarloPiHandler(webapp2.RequestHandler):

    def get(self):
        page = JINJA_ENVIRONMENT.get_template('MonteCarloApproxPi.html')
        self.response.write(page.render())


class HomeHandler(webapp2.RequestHandler):

    def get(self):
        page = JINJA_ENVIRONMENT.get_template('ftimesd_home.html')
        self.response.write(page.render())


class ProjectPageHandler(webapp2.RequestHandler):

    def get(self):
        page = JINJA_ENVIRONMENT.get_template('ftimesd_project_page.html')
        self.response.write(page.render())


class CastleHandler(webapp2.RequestHandler):
    def get(self):
        page = JINJA_ENVIRONMENT.get_template('castle+defense+ai.html')
        self.response.write(page.render())

class StarsHandler(webapp2.RequestHandler):

    def get(self):
        stars_page = JINJA_ENVIRONMENT.get_template('Starspace/Starspace.html')
        self.response.write(stars_page.render())


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


#################################################################################################
################ Twitter Data ###################################################################
#################################################################################################

class TwitterHomeHandler(webapp2.RequestHandler):

    def get(self):
        home_page = JINJA_ENVIRONMENT.get_template('TwitterData/TD_home_page.html')
        self.response.write(home_page.render())


class ResultsHandler(webapp2.RequestHandler):

    def get(self, mode):

        searcher = Searcher()

        k = self.request.get('keyword')
        lat = float(self.request.get('lat'))
        lng = float(self.request.get('lng'))
        coor = {'lat': lat, 'lng': lng}
        r = self.request.get('radius')
        try:
            # must pass keywords as list
            map_items = searcher.search(keyword=[k], coordinates=coor, radius=r)
            parameters = {'map_items': map_items}
            page = JINJA_ENVIRONMENT.get_template('TwitterData/TD_results_page.html')
        except TweepError, e:

            self.response.write(e)
            return

        self.response.write(page.render(parameters))


class MapHandler(webapp2.RequestHandler):

    def get(self):
        map_page = JINJA_ENVIRONMENT.get_template('TwitterData/TD_results_page.html')
        self.response.write(map_page.render())


