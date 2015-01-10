from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, AuthenticationForm, UserChangeForm

from django.shortcuts import render, redirect
from django.views.generic import View

from pprint import pprint

class Index( View ):
    def get( self, request ):
        # if request.user.is_anonymous():
        #     request.context_dict['create_form'] = UserCreationForm()
        #     request.context_dict['login_form'] = AuthenticationForm()

        #     return render( request, 'users/index.html', request.context_dict )
        # else:
        return redirect( request.GET.get( 'next', '/twit' ) )

class Signup( View ):
    def get( self, request ):

        next_url = request.GET.get( 'next', False )
        if next_url:
            request.context_dict['next_url'] = next_url
            request.context_dict['next_string'] = '?next={}'.format( next_url )

        request.context_dict['form'] = UserCreationForm()

        return render( request, 'users/signup.html', request.context_dict )

    def post( self, request ):
        form = UserCreationForm( request.POST )
        if form.is_valid():
            form.save()

            next_url = request.POST.get( 'next', '' )
            if next_url:
                next_url = '&next={}'.format( next_url )

            return redirect( 
                '/users/login?message={}{}'.format( 
                    "Signup a success, please login",
                    next_url
                ) 
            )
        else:
            request.context_dict['form'] = form

            return render( request, 'users/signup.html', request.context_dict )

class Login( View ):
    def get( self, request ):

        next_url = request.GET.get( 'next', False )
        if next_url:
            request.context_dict['next_url'] = next_url
            request.context_dict['next_string'] = '?next={}'.format( next_url )

        request.context_dict['message'] = request.GET.get( 'message', '' )
        request.context_dict['form'] = AuthenticationForm()

        return render( request, 'users/login.html', request.context_dict )

    def post( self, request ):

        # odd that None is needed...
        # http://stackoverflow.com/a/21504550/3140931
        form = AuthenticationForm( None,request.POST )

        if form.is_valid():
            login( request, form.get_user() )
            
            return redirect( request.POST.get( 'next', '/twit' ) )
        else:
            request.context_dict[ 'form' ] = form

            return render( request, 'users/login.html', request.context_dict )

class Logout( View ):
    def get( self, request ):
        logout( request )

        return redirect( '/')

class Profile( View ):
    def get( self, request ):
        # user = User.objects.get( id=request.user.id )
        # pprint( **request.user )
        request.context_dict['form'] = UserChangeForm( None, instance=request.user )

        return render( request, 'users/profile.html', request.context_dict )

    def post( self, request ):
        form = UserChangeForm( request.POST, instance=request.user )
        if form.is_valid():
            form.save()

            return redirect( '/users/profile' )

        request.context_dict['form'] = form

        return render( request, 'users/profile.html', request.context_dict )


class ChangePassword( View ):
    def get( self, request ):
            request.context_dict['form'] = PasswordChangeForm( user=request.user )

            return render( request, 'users/changePassword.html', request.context_dict )

    def post( self, request ):
        form = PasswordChangeForm( user=request.user, data=request.POST )

        if form.is_valid():

            return redirect ( '/users/profile' )
        else:
            request.context_dict['form'] = form

            return render( request, 'users/changePassword.html', request.context_dict )
