from django.shortcuts import render, redirect
from requests_oauthlib import OAuth2Session
from django.contrib.auth import login
from django.views.generic import View
from goog.models import Google_access
from pprint import pprint as print
from sa_api.api import Score
import requests
import base64
# from goog.keysecret import hiddeninfo

#don't delete these lines, they're for production

from os import environ
import ast

hiddeninfo = environ.get('GOOG_SECRET')
hiddeninfo = ast.literal_eval(hiddeninfo)

API_KEY = hiddeninfo["API_KEY"]
CLIENT_ID = hiddeninfo["Client_ID"]
CLIENT_SECRET = hiddeninfo["Client_Secret"] 
REDIRECT_URL = ' http://bytesenti.herokuapp.com/goog/callback'

SCOPE = [ 'profile', 
          'https://www.googleapis.com/auth/plus.login',
          'email',
          'https://www.googleapis.com/auth/plus.profile.emails.read',
          'openid',
          'https://www.googleapis.com/auth/plus.me',
          'https://www.googleapis.com/auth/gmail.compose',
          'https://www.googleapis.com/auth/gmail.readonly',
          'https://mail.google.com/',
          ]

SCOPE = ' '.join(SCOPE)
oath = OAuth2Session(CLIENT_ID, CLIENT_SECRET, redirect_uri=REDIRECT_URL, scope=SCOPE)
                # site='https://www.googleapis.com/oauth2/v1',
                # authorize_url=,
                # token_url='https://accounts.google.com/o/oauth2/token'


class Index( View ):
    def get(self, request):
        if Google_access.objects.filter(user=request.user).exists():
            return redirect( '/goog/display')
        else:
            authorize_url, state = oath.authorization_url('https://accounts.google.com/o/oauth2/auth', access_type="offline", approval_prompt="force")
            return redirect( authorize_url )


class Callback( View ):
    def get(self, request):
        code = request.GET['code']
#think the authorization response is wrong here
        access_token = oath.fetch_token('https://accounts.google.com/o/oauth2/token', authorization_response=code, client_secret=CLIENT_SECRET)
        ret = oath.get('https://www.googleapis.com/oauth2/v1/userinfo')
        info = ret.parsed
        Google_access.objects.create(user=request.user,token= str(access_token.headers),secret="none")
        return redirect('/goog/display')


class Display( View ):
    def get(self, request):
        token_info = Google_access.objects.get(user=request.user)
        token = eval(token_info.token)
        token.update({'referer': '127.0.0.1:8000'})

        emails = requests.get('https://www.googleapis.com/gmail/v1/users/me/messages?includeSpamTrash=false&maxResults=30&key=' + API_KEY, headers = token)
        if 'messages' in emails.json():
            email_json = emails.json()['messages']
        
            email_html = []

            final = Score()
            for em in email_json:
                reson = requests.get("https://www.googleapis.com/gmail/v1/users/me/messages/" + em['id']  + "?format=full&key=" + API_KEY, headers = token)            
                try:
                    emails = reson.json()['payload']['parts']
                    for email in emails:
                        incode = email['body']['data']
                        email_html.append(base64.urlsafe_b64decode(incode))
                except:
                    pass
            
            for email in email_html:
                final.eval(email.decode('utf-8'))
            
            request.context_dict['pos'] = final.pos
            request.context_dict['neg'] = final.neg
        else:
            Google_access.objects.filter(user=request.user).delete()
            return redirect('/goog')

        return render(request, 'goog/results.html',request.context_dict)
