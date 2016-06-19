from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^authApp$', views.authAppStep2, name='authAppStep2'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^login$', views.login, name='login'),

    url(r'^followers/followers$', views.secFollowersAuth, name='secFollowers'),
    url(r'^someone/followers/followers.auth$', views.secFollowersAuth_somebody, name='secFollowers'),
    url(r'^someone/followers/followers$', views.secFollowers, name='secFollowersNoAuth'),

    url(r'^followers/followers/technical$', views.technicalAuth, name='technical'),
    url(r'^someone/followers/followers/technical$', views.technical, name='technical'),

    url(r'^userInfo$', views.getUserInfoAuth, name='getUserInfo'),
    url(r'^someone/userInfo.auth$', views.getUserInfoAuth_somebody, name='getUserInfo'),
    url(r'^someone/userInfo$', views.getUserInfo, name='getUserInfo')
]