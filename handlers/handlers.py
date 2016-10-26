import json

import jinja2
import webapp2
from google.appengine.ext import db
from google.appengine.api import users
from flask import Markup

from searcher import Searcher

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader('./'),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class Score(db.Model):
    """Sub model for representing a score."""
    name = db.StringProperty()
    score = db.IntegerProperty()


class ColorPuzzleHandler(webapp2.RequestHandler):

    def get(self):
        page = JINJA_ENVIRONMENT.get_template('expiri.html')
        self.response.write(page.render())


class ScramblerHandler(webapp2.RequestHandler):

    def get(self):
        page = JINJA_ENVIRONMENT.get_template('sentence_scrambler.html')
        self.response.write(page.render())


class FireworksHandler(webapp2.RequestHandler):

    def get(self):
        page = JINJA_ENVIRONMENT.get_template('fireworks.html')
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

class RepellantOrbHandler(webapp2.RequestHandler):

    def get(self):
        page = JINJA_ENVIRONMENT.get_template('repellantOrb.html')
        self.response.write(page.render())


class ConnectingPartsHandler(webapp2.RequestHandler):

    def get(self):
        page = JINJA_ENVIRONMENT.get_template('ConnectingParts.html')
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


class StarsHandler(webapp2.RequestHandler):

    def get(self):
        stars_page = JINJA_ENVIRONMENT.get_template('Starspace.html')
        self.response.write(stars_page.render())


#################################################################################################
################ Twitter Data ###################################################################
#################################################################################################

class TwitterHomeHandler(webapp2.RequestHandler):

    def get(self):
        home_page = JINJA_ENVIRONMENT.get_template('TD_home_page.html')
        self.response.write(home_page.render())


class SearchHandler(webapp2.RequestHandler):

    def get(self):
        search_page = JINJA_ENVIRONMENT.get_template('TD_search_page.html')
        self.response.write(search_page.render())


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
                page = JINJA_ENVIRONMENT.get_template('TD_search_page.html')
                parameters = {'invalid': True}
                print 'bad search'
                flag = False

        elif mode == 'coordinates':
            lat = self.request.get('lat')
            lng = self.request.get('lng')
            coor= {'lat': lat, 'lng': lng}
            r = self.request.get('radius')
            if lat is None or lng is None or r is None:
                page = JINJA_ENVIRONMENT.get_template('TD_map_page.html')
                parameters = {'fail': True}
            else:
                items = searcher.search(coordinates=coor)
                info = [lat, lng, r]

        if flag:
            if len(items) == 0:
                if mode == 'city_state':
                    page = JINJA_ENVIRONMENT.get_template('TD_search_page.html')
                    parameters = {'invalid': True}
                elif mode == 'coordinates':
                    page = JINJA_ENVIRONMENT.get_template('TD_map_page.html')
                    parameters = {'len': len(items)}
            else:
                parameters = {'items': items, 'info': info}
                page = JINJA_ENVIRONMENT.get_template('TD_results_page.html')

        self.response.write(page.render(parameters))


class MapHandler(webapp2.RequestHandler):

    def get(self):
        map_page = JINJA_ENVIRONMENT.get_template('TD_map_page.html')
        self.response.write(map_page.render())


#########################################BOARDS################################################

class User(db.Model):
    """Sub model for representing a score."""
    username = db.StringProperty()
    password = db.StringProperty()


# class BoardHandler(webapp2.RequestHandler):
#
#     def get(self):
#         # user = users.get_current_user()
#         # if user:
#         #     nickname = user.nickname()
#         #     logout_url = users.create_logout_url('/')
#         #     greeting = 'Welcome, {}! (<a href="{}">sign out</a>)'.format(
#         #         nickname, logout_url)
#         # else:
#         #     login_url = users.create_login_url('/')
#         #     greeting = '<a href="{}">Sign in</a>'.format(login_url)
#
#         self.response.write(JINJA_ENVIRONMENT.get_template('Boards.html').render())


class BoardsAccountsHandler(webapp2.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'application/json'

        flag = True
        new_account = {'username': self.request.get('username'), 'password': self.request.get('password')}
        if new_account['password'] != '':
            username_query = User.all()
            username_query.filter("username =", new_account['username'])
            if username_query.get() is None:
                user = User(username=new_account['username'], password=new_account['password'])
                user.put()
            else:
                page = JINJA_ENVIRONMENT.get_template('Boards.html')
                parameters = {'user_taken': 'true'}
                flag = False

        if flag:
            query = db.Query(User)

            s = [{'username': x.username, 'password': x.password} for x in query.run(limit=100)]
            obj = {'accounts': s, 'latest': new_account}

            self.response.write(json.dumps(obj))
        else:
            self.response.write(page.render(parameters))


class BoardHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            # url = users.create_logout_url(self.request.uri)
            nickname = user.nickname()
            url_linktext = 'Logout'
            user_status = False
            login_url = Markup(users.create_logout_url('/boards'))
        else:
            # url = users.create_login_url(self.request.uri)
            nickname = ''
            url_linktext = 'Login'
            user_status = True
            login_url = Markup(users.create_login_url('/boards'))

        parameters = {
            'user': user,
            'name': nickname,
            'url': login_url,
            'url_linktext': url_linktext,
            'user_status': user_status
        }

        template = JINJA_ENVIRONMENT.get_template('Boards.html')
        self.response.write(template.render(parameters))


class BoardSignHandler(webapp2.RequestHandler):
    def get(self):
        Boards_page = JINJA_ENVIRONMENT.get_template('BoardsHome.html')
        self.response.write(Boards_page.render())