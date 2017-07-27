# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 11:42:53 2017

@author: akarchmer
"""

import requests

class SentimentAnalyzer():

    def sentiment(self, t):
        url = 'https://apiv2.indico.io/sentiment'
        r = requests.post(url, data={'data': t}, headers={'X-ApiKey': 'f8847868d65bae789cfdc8d35c11470e'})
        return r.content.split(':')[1][1:-1]


    def relevance(self, t, keywords):
        url = 'https://apiv2.indico.io/relevance'
        r = requests.post(url, data={'data': t, 'queries': keywords}, headers={'X-ApiKey': 'f8847868d65bae789cfdc8d35c11470e'})
        print r.content
        return r.content.split(':')[1][2:-2]