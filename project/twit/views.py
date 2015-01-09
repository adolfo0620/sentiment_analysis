from django.shortcuts import render, redirect
from django.views.generic import View
from twit.keysecret import secrets
from django.contrib.auth.models import User, AnonymousUser
# from twit.models import User
from twython import Twython
from pprint import pprint

positives = ['love','loved','like','liked','awesome','amazing','good','great','excellent', 'nice', 'sweet']
negatives = ['hate','hated','dislike','disliked','awful','terrible','bad','painful','worst', 'disgraceful', 'horrible']


class Index( View ):
    def get(self, request):
        if "user_id" in request.session:
            return redirect('/twit/tweet')
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
        if User.objects.filter(username=final_step['screen_name']).exists():
            u = User.objects.get(username=final_step['screen_name'])
        else:
            u = User.objects.create(username=final_step['screen_name'])
        u.token = final_step['oauth_token']
        u.secret = final_step['oauth_token_secret']
        u.save()
        print(final_step['oauth_token'])
        print(final_step['oauth_token_secret'])
        request.session['user_id'] = u.id
        return redirect( '/twit/Eval')


class Eval( View ):
    def get(self, request):
        return render ( request, 'twit/evaluate.html')


class Results( View ):
    def get(self, request):
        u = User.objects.get(pk=request.session['user_id'])
        twitter = Twython(secrets['APP_KEY'], secrets['APP_SECRET'], u.token, u.secret)
        results = twitter.search(q=request.GET['query'], result_type='mixed', count=100)
        pos = 0
        neg = 0
        for result in results['statuses']:
            for word in positives:
                if word in result['text']:
                    pos += 1
            for word in negatives:
                if word in result['text']:
                    neg += 1
        return render(request, 'twit/results.html', {'hashtag':request.GET['query'], 'posi':pos, 'nega':neg})
       