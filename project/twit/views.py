from django.shortcuts import render, redirect
from django.views.generic import View
from twit.keysecret import secrets

from django.contrib.auth.models import User, AnonymousUser

from sa_api.views import Score

from twython import Twython
from pprint import pprint


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
        # if User.objects.filter(username=final_step['screen_name']).exists():
        #     u = User.objects.get(username=final_step['screen_name'])
        # else:
        #     u = User.objects.create(username=final_step['screen_name'])
        # u.token = final_step['oauth_token']
        # u.secret = final_step['oauth_token_secret']
        # u.save()
        # request.session['user_id'] = u.id
        request.session['oauth_token'] = final_step['oauth_token']
        request.session['oauth_token_secret'] = final_step['oauth_token_secret']
        return redirect( '/twit/eval')


class Eval( View ):
    def get(self, request):
        return render ( request, 'twit/evaluate.html', request.context_dict )


class Results( View ):
    def get(self, request):
        # u = User.objects.get(pk=request.session['user_id'])
        twitter = Twython(secrets['APP_KEY'], secrets['APP_SECRET'], request.session['oauth_token'], request.session['oauth_token_secret'])
        results = twitter.search(q=request.GET['query'], result_type='mixed', count=1000000)

        final = Score()

        count_en = 0
        for twits in results['statuses']:
            if twits['lang'] != 'en':
                continue
            final.eval( twits['text'] )
            count_en += 1
        
        request.context_dict['hashtag'] = request.GET['query']
        request.context_dict['pos'] = final.pos
        request.context_dict['neg'] = final.neg
        request.context_dict['count_en'] = count_en
        request.context_dict['count'] = results['search_metadata']['count']

        return render(request, 'twit/results.html', request.context_dict)

       