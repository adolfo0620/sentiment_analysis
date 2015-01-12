from django.shortcuts import render, redirect
from django.views.generic import View
from sa_api.api import Score
from reddit.scraper import reddit_api
from django.contrib.auth.models import User
import requests
from pprint import pprint

class Index( View ):
    def get(self, request):
        bot = {"User-Agent": "sentiment bot by /u/adolfo0620"}
        json = requests.get('http://www.reddit.com/reddits.json?limit=1000',headers=bot).json()
        out = []
        for sub in json['data']['children']:
            out.append({
                'name': sub['data']['display_name'],
                'url': sub['data']['url']
                })
        pprint(out)
        request.context_dict['subs'] = out
        return render ( request, 'reddit/evaluate.html', request.context_dict )

class Eval( View ):
    def get( self, request ):

        subred = request.GET['query']
        print('here')
        print(subred)
        r = reddit_api(subred)
        results = r.get_info()
        score = Score()
        
        for post in results:
            score.eval( post )

        request.context_dict['pos'] = score.pos
        request.context_dict['neg'] = score.neg

        return render( request, 'reddit/results.html', request.context_dict)