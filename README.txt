
Author: Krzysztof Urbańczyk
email: urbansanek@gmail.com

SecFolloers: Twitter second level followers searcher application

API used: Django, utilized Twitter API via Twython module, Python 2.7

Modules:
Backend:
	- twitterAPI.py: API feeding data from Twitter REST API.
	- twitterAuth.py: API providing authentication to Twitter accounts

exceptions.py: custom exception

Database solution:
- TwittToken table contains valid Twitter token or these which still need to be authorized. 
	constaints: There should be 1 row for 1 csrf token for every OAuth method (max 2)
- secFollowersJson table contains json's of the last data feeding from Twitter API per method (max 2)
- Any DB insert is based on csrf token recieved via POST method

Usability:
- Check your / somones second hand followers (OAuth1, OAuth2)
- Check your / someones basic user info (OAuth1, OAuth2)

- OAuth1 is a authorization method requiring user logon. For mobiles and desktop app requires a 2 step logging in with fetching a token or authorization with a callback. A token version has been chosen.
- OAuth2 is a authorization method which doesn't requiring logging in but will not have access to e.g. twitting for specific users.

views.py:
- @authenticate decorator requires a POST request with variable verified == 0 or 1.
	verified == 0: determines that the first step of OAuth1 is taking place.
	verified == 1: determines that the second step of OAuth1 is taking place.