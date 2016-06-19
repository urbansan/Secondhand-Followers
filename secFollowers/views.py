from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .backend import twitterAuth, twitterAPI
import twython
import pdb

#========================AUTHENTICATION PROCEDURE========================
def authenticate(urlFunc):
    def decoMorreno(request):
        auth = twitterAuth.getAuthHandlerStep1(request)
        appURL = request.path
        if isinstance(auth, twython.Twython):
            return urlFunc(request, auth)
        elif isinstance(auth, dict):
            auth.update({'appURL' : appURL})
            return render(request, 'secFollowers/verify.html', auth)
        else:
            return render(request, 'secFollowers/errorSite.html', {'mesg' : 'Middlware attack witnessed'})
    return decoMorreno

def authAppStep2(request):
    twitterAuth.getAuthHandlerStep2(request)
    # pdb.set_trace()    
    return HttpResponseRedirect(request.POST['appURL'])

#========================API REQUIRING AUTHENTICATION========================

@authenticate
def secFollowersAuth_somebody(request, twitter):
    data = twitterAPI.secFollowersList(request, request.POST['screen_name'], twitter)
    return render(request, 'secFollowers/secFollowers.html', data)

@authenticate
def login(request, twitter):
    return render(request, 'secFollowers/home.html',
                {'event' : 'you have logged in', 'log_status' : True}
            )


@authenticate
def secFollowersAuth(request, twitter):
    screen_name = twitter.verify_credentials()['screen_name']
    data = twitterAPI.secFollowersList(request, screen_name, twitter)
    return render(request, 'secFollowers/secFollowers.html', data)

@authenticate
def getUserInfoAuth(request, twitter):
    screen_name = twitter.verify_credentials()['screen_name']
    user_data = twitterAPI.basicUserData(request, screen_name, twitter)
    return render(request, 'secFollowers/userInfo.html', user_data)

@authenticate
def getUserInfoAuth_somebody(request, twitter):
    user_data = twitterAPI.basicUserData(request, request.POST['screen_name'], twitter)
    return render(request, 'secFollowers/userInfo.html', user_data)


def technicalAuth(request):
    data = twitterAPI.technical(request, 'private')
    return render(request, 'secFollowers/technical.html', {'technical' : data})

#========================PUBLIC API===========================================

def secFollowers(request):
    data = twitterAPI.secFollowersList(request, request.POST['screen_name'], None)
    return render(request, 'secFollowers/secFollowers.html', data)

def getUserInfo(request):
    user_data = twitterAPI.basicUserData(request, request.POST['screen_name'], None)
    return render(request, 'secFollowers/userInfo.html', user_data)

def technical(request):
    data = twitterAPI.technical(request, 'public')
    return render(request, 'secFollowers/technical.html', {'technical' : data})

#========================UTIL SITES===========================================

def index(request):
    return render(request, 'secFollowers/home.html')

def logout(request):
    twitterAuth.logout(request)
    return render(request, 'secFollowers/home.html',
             {'event' : 'you have logged out', 'log_status' : False})