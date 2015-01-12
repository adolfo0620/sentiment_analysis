from django.shortcuts import render, redirect
from django.views.generic import View
from twit.keysecret import secrets
from twit.models import Twitter_access
from django.contrib.auth.models import User, AnonymousUser
from sa_api.api import Score
from twython import Twython
from pprint import pprint
from Query.models import Query
import json


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

        #we should use this next line to weigh sentiment at some point
        #results['retweet_count']

        count_en = 0
        associated_hashtags = {}

        for twits in results['statuses']:
            final.eval( twits['text'] )
            for hashtag in twits['entities']['hashtags']:
                if hashtag["text"].lower() is not request.GET['query'][1:].lower():
                    if hashtag['text'] in associated_hashtags:
                        associated_hashtags[hashtag['text']] += 1
                    else:
                        associated_hashtags[hashtag['text']] = 1
            count_en += 1
        
        Query.objects.create(query_string=request.GET['query'],
                            negative_score=final.neg,
                            positive_score=final.pos,
                            user=request.user,
                            media_platform="Twitter"
                            )
        
        request.context_dict['hashtag'] = request.GET['query']
        request.context_dict['pos'] = final.pos
        request.context_dict['neg'] = final.neg
        request.context_dict['count_en'] = count_en
        request.context_dict['count'] = results['search_metadata']['count']
        request.context_dict['associated_hashtags'] = json.dumps(associated_hashtags)
        print(request.context_dict['associated_hashtags'])

        return render(request, 'twit/results.html', request.context_dict)
