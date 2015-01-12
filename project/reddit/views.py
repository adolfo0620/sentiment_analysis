from django.shortcuts import render, redirect
from django.views.generic import View
from sa_api.api import Score
from reddit.scraper import reddit_api
from django.contrib.auth.models import User

class Index( View ):
    def get( self, request ):
        r = reddit_api()
        results = r.get_info()
        score = Score()
        
        for post in results:
            score.eval( post )

        request.context_dict['pos'] = score.pos
        request.context_dict['neg'] = score.neg

        return render( request, 'reddit/results.html', request.context_dict)
