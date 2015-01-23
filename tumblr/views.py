from django.contrib.auth.models import User, AnonymousUser
from django.shortcuts import render, redirect 
from tumblr.models import Tumblr_access 
from django.views.generic import View
from sa_api.api import Score
from tumblpy import Tumblpy
from pprint import pprint

from tumblr.keysecret import tumsecret

#don't delete these lines, they're for production
# from os import environ
# import ast

# tumsecret = environ.get('TUM_SECRET')
# tumsecret = ast.literal_eval(tumsecret)


class Index( View ):
    def get(self, request):
        user = User.objects.get(id=request.user.id)
        if Tumblr_access.objects.filter(user=user).exists():
            return redirect('/tumblr/eval')
        
        tum = Tumblpy(tumsecret['APP_KEY'], tumsecret['APP_SECRET'])
        auth_props = tum.get_authentication_tokens(callback_url='http://127.0.0.1:8000/tumblr/callback/')
        url = auth_props['auth_url']

        OAUTH_TOKEN_SECRET = auth_props['oauth_token_secret']

        request.session['OAUTH_TOKEN'] = auth_props['auth_url']
        request.session['OAUTH_TOKEN_SECRET'] = auth_props['oauth_token_secret']

        t = Tumblpy(
            app_key=tumsecret['APP_KEY'], 
            app_secret=tumsecret['APP_SECRET']
        )

        auth_props = t.get_authentication_tokens( callback_url='http://127.0.0.1:8000/tumblr/callback' )

        request.session['tumblrOauthToken'] = auth_props['oauth_token']
        request.session['tumblrOauthTokenSecret'] = auth_props['oauth_token_secret']

        auth_url = auth_props['auth_url']

        return redirect( auth_url )

class Callback( View ):
    
    def get(self, request):
        # print( request.session['tumblrOauthToken'], request.session['tumblrOauthTokenSecret'] )
        oauth_verifier = request.GET['oauth_verifier']
        tum = Tumblpy(
            tumsecret['APP_KEY'],
            tumsecret['APP_SECRET'],
            request.session['tumblrOauthToken'],
            request.session['tumblrOauthTokenSecret']
        )
        oauth_verifier = request.GET['oauth_verifier']

        
        final_step = tum.get_authorized_tokens(oauth_verifier)

        
        # request.session['oauth_token'] = final_step['oauth_token']
        # request.session['oauth_token_secret'] = final_step['oauth_token_secret']
        
        Tumblr_access.objects.create(token=final_step['oauth_token'],
                                    secret=final_step['oauth_token_secret'],
                                    user=request.user)
        
        return redirect( '/tumblr/eval')

class Eval( View ):
    def get(self, request):

        return render ( request, 'tumblr/evaluate.html', request.context_dict )

class Results( View ):
    def get(self, request):
        
        blog_url = request.GET.get( 'blog_url', '' ) #'engineering.tumblr.com'
        tag = request.GET.get( 'tag', '' )

        tumblr_access = Tumblr_access.objects.get( user=request.user )

        tumblr = Tumblpy(
            tumsecret['APP_KEY'],
            tumsecret['APP_SECRET'],
            tumblr_access.token,
            tumblr_access.secret
        )
        
        tumblr = tumblr.get( 
            'posts',
            blog_url=blog_url,
            params={
                'type': 'text',
                'filter': 'text',
                'tag': tag
            }
        )

        score = Score()
        for posts in tumblr['posts']:
            score.eval( posts['body'] )

        request.context_dict['blog_url'] = blog_url
        request.context_dict['tag'] = tag
        request.context_dict['pos'] = score.pos
        request.context_dict['neg'] = score.neg

        return render( request, 'tumblr/results.html', request.context_dict )
