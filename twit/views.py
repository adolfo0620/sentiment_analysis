from django.contrib.auth.models import User, AnonymousUser
from django.shortcuts import render, redirect
from twit.models import Twitter_access
from django.views.generic import View
from Query.models import Query
from sa_api.api import Score
from twython import Twython
from pprint import pprint
import json

from twit.keysecret import secrets

#don't delete these lines, they're for production
# import ast
# from os import environ

# secrets = environ.get('TWIT_SECRET')
# secrets = ast.literal_eval(secrets)

class Index( View ):
    def get(self, request):
        if Twitter_access.objects.filter(user=request.user.id).exists():
            return redirect('/twit/eval')
        twitter = Twython(secrets['APP_KEY'], secrets['APP_SECRET'])
        auth = twitter.get_authentication_tokens(callback_url='http://127.0.0.1:8000/twit/callback')
        request.session['OAUTH_TOKEN'] = auth['oauth_token']
        request.session['OAUTH_TOKEN_SECRET'] = auth['oauth_token_secret']
        url = auth['auth_url']
        return redirect( url )


class Callback( View ):
    def get(self, request):
        oauth_verifier = request.GET['oauth_verifier']
        twitter = Twython(secrets['APP_KEY'], secrets['APP_SECRET'], request.session['OAUTH_TOKEN'], request.session['OAUTH_TOKEN_SECRET'])
        final_step = twitter.get_authorized_tokens(oauth_verifier)

        Twitter_access.objects.create(token=final_step['oauth_token'],
                                    secret=final_step['oauth_token_secret'],
                                    user=request.user)
        
        return redirect( '/twit/eval')


class Eval( View ):
    def get(self, request):
        return render ( request, 'twit/evaluate.html', request.context_dict )


class Results( View ):
    def get(self, request):
        twitter_access = Twitter_access.objects.get(user=request.user)

        twitter = Twython(secrets['APP_KEY'], secrets['APP_SECRET'], twitter_access.token, twitter_access.secret)
        results = twitter.search(q=request.GET['query'], result_type='mixed', count=100,  lang='en')
        final = Score()

        #we should use these next lines to weigh sentiment at some point
        #results['retweet_count']
        #results['favourites_count']

        associated_hashtags = {}
        for twits in results['statuses']:
            final.eval( twits['text'] )
            for hashtag in twits['entities']['hashtags']:
                if hashtag["text"].lower() is not request.GET['query'][1:].lower():
                    if hashtag['text'] in associated_hashtags:
                        associated_hashtags[hashtag['text']] += 1
                    else:
                        associated_hashtags[hashtag['text']] = 1
        
        Query.objects.create(query_string=request.GET['query'],
                            negative_score=final.neg,
                            positive_score=final.pos,
                            user=request.user,
                            media_platform="Twitter"
                            )
        
        request.context_dict['hashtag'] = request.GET['query']
        request.context_dict['pos'] = final.pos
        request.context_dict['neg'] = final.neg
        request.context_dict['count'] = len(results['statuses'])
        request.context_dict['associated_hashtags'] = associated_hashtags

        return render(request, 'twit/results.html', request.context_dict)
