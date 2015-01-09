from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from users.models import User
from django.shortcuts import render, redirect
from django.views.generic import View


class Index(View):
    def get(self, request):
        if request.user.is_anonymous():
            return render( request, 'users/index.html', {'create_form':UserCreationForm(), 'login_form': AuthenticationForm() } )
        else:
            return redirect('/twit')


class Signup(View):
    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            a = User.objects.create_user( username=cd.get('username'), password=cd.get('password1'))
            return redirect('/?error={}'.format("signup a success! now please login") )
        else:
            return render( request, 'users/index.html', {'create_form':UserCreationForm(), 'login_form': AuthenticationForm() } )


class Login(View):
    def post(self, request):

        # odd that None is needed...
        # http://stackoverflow.com/a/21504550/3140931
        form = AuthenticationForm( None,request.POST )

        if form.is_valid():
            login(request, form.get_user())
            return redirect('/twit/tweet')
        else:
            return render( request, 'users/index.html', {'create_form':UserCreationForm(), 'login_form': AuthenticationForm() } )

class Logout(View):
    def get(self, request):
        logout(request)
        return redirect( '/')


class Profile(View):
    def get(self, request):
        if request.user.is_anonymous():
            return redirect( '/')
        else:
            return render( request, 'users/profile.html', {'form':PasswordChangeForm(request.user)})


class ChangePass(View):
    def post(self, request):
        user = authenticate(username=request.user.username, password=request.POST["old_password"])
        if request.POST['new_password1'] != request.POST['new_password2']:
            return redirect ('/users/profile/?error={}'.format("new passwords don't match"))
        if user is not None:
            user.set_password(request.POST['new_password1'])
            user.save()
            return redirect ('/users/profile')
        else:
            return redirect ('/users/profile/?error={}'.format("incorrect password"))
