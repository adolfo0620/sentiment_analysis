from django.shortcuts import render, redirect
from django.views.generic import View
from project.keysecret import facesercets
from facebook.models import Facebook_access
from django.contrib.auth.models import User, AnonymousUser

import FacebookAPI

from sa_api.api import Score
from twython import Twython
from pprint import pprint
from Query.models import Query


class Index( View ):
    def get(self, request):
        if Facebook_access.objects.filter(user=request.user).exists():
            return redirect('/facebook/eval')

        f = FacebookAPI(facesercets["appId"], facesercets["APP_SECRET"], 'http://127.0.0.1:8000/facebook/callback')
        auth_url = f.get_auth_url(scope=['publish_stream', 'user_photos', 'user_status'])
        print(auth_url)
        return redirect( auth_url )
# ended here

        # twitter = Twython(secrets['APP_KEY'], secrets['APP_SECRET'])
        # auth = twitter.get_authentication_tokens(callback_url='http://127.0.0.1:8000/twit/callback')
        # request.session['OAUTH_TOKEN'] = auth['oauth_token']
        # request.session['OAUTH_TOKEN_SECRET'] = auth['oauth_token_secret']
        # url = auth['auth_url']
        # return redirect( url )

class Callback( View ):
    def get(self, request):
        
        code = request.GET.get('code')
        access_token = f.get_access_token(code)
        final_access_token = access_token['oauth_token']
        Facebook_access.objects.create(token=final_access_token,
                                        user=request.user,
                                        secret="none")

        return redirect( '/facebook/eval')

class Eval( View ):
    def get(self, request):
        return render ( request, 'facebook/evaluate.html', request.context_dict )

class Results( View ):
    def get(self, request):
        # u = User.objects.get(pk=request.session['user_id'])
        facebook_access = Facebook_access.objects.get(user=request.user)

        
        final = Score()
        # saving to db
        # twitter = Twython(secrets['APP_KEY'], secrets['APP_SECRET'], request.session['oauth_token'], request.session['oauth_token_secret'])
        # results = twitter.search(q=request.GET['query'], result_type='mixed', count=1000000)

        # Query.objects.create(query_string=request.GET['query'],
        #                     negative_score=final.neg,
        #                     positive_score=final.pos,
        #                     user=request.user,
        #                     media_platform="Twitter"
        #                     )
        
        # request.context_dict['hashtag'] = request.GET['query']
        # request.context_dict['pos'] = final.pos
        # request.context_dict['neg'] = final.neg
        # request.context_dict['count_en'] = count_en
        # request.context_dict['count'] = results['search_metadata']['count']

        return render(request, 'facebook/results.html', request.context_dict)
