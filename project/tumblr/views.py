from django.shortcuts import render, redirect 
from django.views.generic import View
from tumblr.models import Tumblr_access 
from tumblpy import Tumblpy
from project.keysecret import tumsecret
from django.contrib.auth.models import User, AnonymousUser


# Create your views here.

class Index( View ):
    def get(self, request):
        user = User.objects.get(id=request.user.id)
        if Tumblr_access.objects.filter(user=user).exists():
            return redirect('/tumblr/eval')
        
        tum = Tumblpy(tumsecret['APP_KEY'], tumsecret['APP_SECRET'])
        auth_props = tum.get_authentication_tokens(callback_url='http://127.0.0.1:8000/tumblr/callback')
        print('wtf')
        url = auth_props['auth_url']
        
        request.session['OAUTH_TOKEN'] = auth_props['auth_url']
        request.session['OAUTH_TOKEN_SECRET'] = auth_props['oauth_token_secret']

        return redirect( url )

class Callback( View ):
    
    def get(self, request):
        tum = Tumblpy(tumsecret['APP_KEY'], tumsecret['APP_SECRET'], request.session['OAUTH_TOKEN'], request.session['OAUTH_TOKEN_SECRET'])
        oauth_verifier = request.GET['oauth_verifier']

        
        final_step = tum.get_authorized_tokens(oauth_verifier)

        
        request.session['oauth_token'] = final_step['oauth_token']
        request.session['oauth_token_secret'] = final_step['oauth_token_secret']
        
        Tumblr_access.objects.create(token=final_step['oauth_token'],
                                    secret=final_step['oauth_token_secret'],
                                    user=request.user)
        
        return redirect( '/tumblr/eval')

class Eval( View ):
    def get(self, request):
    	pass
        # return render ( request, 'tumblr/evaluate.html', request.context_dict )

class Results( View ):
    def get(self, request):
        # u = User.objects.get(pk=request.session['user_id'])
        tumblr_access = Tumblr_access.objects.get(user=request.user)

        tum = Tumblpy(tumsecret['APP_KEY'], tumsecret['APP_SECRET'], tumblr_access.token, tumblr_access.secret)
        
        final = Score()
        # saving to db
        # twitter = Twython(secrets['APP_KEY'], secrets['APP_SECRET'], request.session['oauth_token'], request.session['oauth_token_secret'])
        # results = twitter.search(q=request.GET['query'], result_type='mixed', count=1000000)

        count_en = 0
        for twits in results['statuses']:
            final.eval( twits['text'] )
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

        return render(request, 'twit/results.html', request.context_dict)
