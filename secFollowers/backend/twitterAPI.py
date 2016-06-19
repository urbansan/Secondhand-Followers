
# -*- coding: utf-8 -*-
from .mutualImports import *
from .twitterAuth import getTwitterHandle

def basicUserData(request, screenName, twitter = None):
    if twitter is None:
        twitter = getTwitterHandle(request.POST['csrfmiddlewaretoken'])

    try:
        user_data = twitter.lookup_user(screen_name = screenName)
        user_data = [[key + ':', user_data[0][key]] for key in ['name', 'screen_name', 'id_str', 'followers_count', 'friends_count', 'statuses_count']]
    except TwythonError:
        user_data = [['No data found for this user']]

    return {'user_data' : user_data}


def secFollowersList(request, screenName, twitter = None):
    # 1. getting followers Ifrom collections import Counter
    if twitter is None:
        twitter = getTwitterHandle(request.POST['csrfmiddlewaretoken'])

    data = {'screen_name' : screenName}
    validSecFollowers_id = []

    try:
        limits = twitter.get_application_rate_limit_status()
        if limits['resources']['followers']['/followers/ids']['remaining'] == 0:
            raise TwythonRateLimitError('Followers ID limist exceeded', -1)

        followers_id = twitter.get_followers_ids(
                    screen_name = screenName,
                    cursor = -1,
                    count = 5000
                )

        #2. get second level followers excluding first level followers if occur

        for follower in followers_id['ids']:
            try:
                secFollowers_id = twitter.get_followers_list(
                            user_id = follower,
                            skip_status = True,
                            count = 200
                        )
                
                for secFollower in secFollowers_id['users']:
                    if secFollower['id'] not in followers_id['ids']:
                        validSecFollowers_id.append(secFollower['screen_name'])
            except TwythonAuthError:
                pass #omitting users which require additional authorization
        
    except TwythonRateLimitError:
        timeRemaining = int(limits['resources']['followers']['/followers/ids']['reset'] - time.time())
        data.update({'limits' : 'Data limit reached. ' + str(timeRemaining / 60) + ' minutes remaining'})
        
    except TwythonError:
        pass #validSecFollowers_id.append('No data found for this user')

    screenNameCounter = Counter(validSecFollowers_id)
    data.update({'users' : sorted(screenNameCounter.items(), key=lambda x: x[1], reverse = True)})

    # save data to database as json
    if twitter.oauth_version == 1:
        access_type = 'private'
    else:
        access_type = 'public'

    json_h = secFollowersJson.objects.filter(
                csrf_token = request.POST['csrfmiddlewaretoken'], 
                access_type = access_type
            )

    json_h.delete()

    json_h = secFollowersJson(
            screen_name = screenName,
            access_type = access_type,
            csrf_token = request.POST['csrfmiddlewaretoken'], 
            json = json.dumps(data['users'], ensure_ascii=False)
        )
    json_h.save()

    return data


def technical(request, access_type):

    json_h = secFollowersJson.objects.filter(
                csrf_token = request.POST['csrfmiddlewaretoken'], 
                access_type = access_type
            )

    if len(json_h) == 1:
        data = json_h[0].json
    else:
        data = 'No data'

    return {'users' : data}

