from __future__ import unicode_literals
from django.db import models

class TwittToken(models.Model):
    access_type = models.TextField(max_length = 8)
    csrf_token = models.TextField()
    utime = models.IntegerField()
    is_authorized = models.BooleanField(default=False)
    oauth_token = models.TextField()
    oauth_token_secret = models.TextField()

    def __unicode__(self):              # __unicode__ on Python 2
        return self.csrf_token

class secFollowersJson(models.Model):
    access_type = models.TextField(max_length = 8)
    csrf_token = models.TextField()
    screen_name = models.CharField(max_length = 20)
    json = models.TextField()

    def __unicode__(self):              # __unicode__ on Python 2
        return self.screen_name

