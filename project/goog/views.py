from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.views.generic import View
from project.keysecret import hiddeninfo
from pyoauth2 import Client
import requests
import base64
from pprint import pprint as print
from goog.models import Google_access

API_KEY = hiddeninfo["API_KEY"]
CLIENT_ID = hiddeninfo["Client_ID"]
CLIENT_SECRET = hiddeninfo["Client_Secret"] 
REDIRECT_URL = 'http://127.0.0.1:8000/goog/callback'

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
client = Client(CLIENT_ID, CLIENT_SECRET,
                site='https://www.googleapis.com/oauth2/v1',
                authorize_url='https://accounts.google.com/o/oauth2/auth',
                token_url='https://accounts.google.com/o/oauth2/token')


class Index( View ):
    def get(self, request):
        if Google_access.objects.filter(user=request.user).exists():
            return redirect( '/goog/display')
        else:
            authorize_url = client.auth_code.authorize_url(redirect_uri=REDIRECT_URL, scope=SCOPE)
            return redirect( authorize_url )


class Callback( View ):
    def get(self, request):
        code = request.GET['code']
        access_token = client.auth_code.get_token(code, redirect_uri=REDIRECT_URL)
        ret = access_token.get('/userinfo')
        info = ret.parsed
        Google_access.objects.create(user=request.user,token= str(access_token.headers),secret="none")
        return redirect('/goog/display')


class Display( View ):
    def get(self, request):
        token_info = Google_access.objects.get(user=request.user)
        token = eval(token_info.token)
        token.update({'referer': '127.0.0.1:8000'})

        emails = requests.get('https://www.googleapis.com/gmail/v1/users/me/messages?includeSpamTrash=false&maxResults=50&key=' + API_KEY, headers = token)
        email_json = emails.json()['messages']
        email_html = []

        for em in email_json:
            reson = requests.get("https://www.googleapis.com/gmail/v1/users/me/messages/" + em['id']  + "?format=full&key=" + API_KEY, headers = token)            
            try:
                emails = reson.json()['payload']['parts']
                for email in emails:
                    incode = email['body']['data']
                    email_html.append(base64.urlsafe_b64decode(incode))
            except:
                pass
                
        return render(request,'goog/display.html')
