
# -*- coding: utf-8 -*-
from .mutualImports import *

APP_KEY = 'dAKh0Y34DhR2QfeEQVZuCQQ3a'
APP_SECRET = 'hCDLRZ9uxtg8qnxZ80nIivvqcnY5ud9dYbAilMx3WTHVP5mXUV'

def logout(request):
    csrf_token = request.POST['csrfmiddlewaretoken']
    data = TwittToken.objects.filter(csrf_token = csrf_token, access_type = 'private')
    data.delete()

def getToken(request):
    try:
        return request.POST['csrfmiddlewaretoken'], 'POST'
    except:
        return request.COOKIES['csrftoken'], 'COOKIES'

'''
returns twitter handler if authorized token are available. 
I case no authorized token are avaiable the url for pin validation will be returned
'''
def getAuthHandlerStep1(request):

    csrf_token, origin =  getToken(request)    

    data = TwittToken.objects.filter(csrf_token = csrf_token, access_type = 'private')
    try:
        if len(data) == 0 and cmp(origin, 'COOKIES') == 0:
            return False
        if len(data) == 1:
            if data[0].is_authorized == True:

                twitter = Twython(
                            APP_KEY, APP_SECRET,
                            data[0].oauth_token,
                            data[0].oauth_token_secret
                        )
                
                # Checking if I have access to the account (probably unnecessary move)
                twitter.verify_credentials()
                
                return twitter

        raise TwythonError('Error during token exchanging / confirmation', -1)

    except TwythonError, TwythonAuthError:

        twitter = Twython(APP_KEY, APP_SECRET)

        auth = twitter.get_authentication_tokens()

        data.delete()
        data = TwittToken(
                access_type = 'private',
                csrf_token = csrf_token,
                utime = int(time.time()), 
                oauth_token = auth['oauth_token'],
                oauth_token_secret = auth['oauth_token_secret']
            )
        data.save()

        return {'auth_url' : auth['auth_url']}


def getAuthHandlerStep2(request):
    # 
    csrf_token = request.POST['csrfmiddlewaretoken']

    data = TwittToken.objects.filter(csrf_token = csrf_token, access_type = 'private')    
    
    if len(data) != 1:
        raise dbError('incorrect cursor rows count')

    twitter = Twython(
                APP_KEY, APP_SECRET,
                data[0].oauth_token,
                data[0].oauth_token_secret
            )

    final_step = twitter.get_authorized_tokens(request.POST['pin'])

    data[0].utime = int(time.time())
    data[0].is_authorized = True
    data[0].oauth_token = final_step['oauth_token']
    data[0].oauth_token_secret = final_step['oauth_token_secret']
    data[0].save()

    return True

def getTwitterHandle(csrf_token):

    # 1 get token from database
    data = TwittToken.objects.filter(csrf_token = csrf_token, access_type = 'public')

    if len(data) == 1:

        try:             
            twitter = Twython(APP_KEY, access_token=data[0].oauth_token)    
            return twitter
        
        except TwythonAuthError:
            pass

    data.delete()

    # 2 Generate new token if data is inconsistent
    twitter = Twython(APP_KEY, APP_SECRET, oauth_version=2)

    access_token = twitter.obtain_access_token()

    # 3 save token to DB
    data = TwittToken(
            access_type = 'public',
            csrf_token = csrf_token,
            utime = int(time.time()), 
            oauth_token = access_token,
            oauth_token_secret = 'brzdek'
        )
    data.save()

    # 4 generate Twitter handle.
    twitter = Twython(APP_KEY, access_token=access_token)
        
    # 7 return good twitter handle
    return twitter