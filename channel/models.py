from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Channel(models.Model):

    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, blank=True, null=True,)
    content = models.ManyToManyField(
        'channel.Video',
        related_name = 'contenting',
        blank=True)

    def __str__(self):
        return '{}'.format(self.name)

class Series(models.Model):
    name = models.CharField(max_length=400)
    netflix_id = models.CharField(
        max_length=30,
        blank=True)
    wikipedia_url = models.CharField(
        max_length=300,
        blank=True)
    seasons_total = models.IntegerField(null=True, blank=True)
    episodes_total = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.name)

class Season(models.Model):
    name = models.CharField(max_length=20)
    series = models.ForeignKey('channel.Series')
    season_number = models.IntegerField(null=True, blank=True)


    def __str__(self):
        return '{}'.format(self.name)

class Video(models.Model):

    TYPE = (
        ("T","TV Episode"),
        ("M","Movie"),
    )

    name = models.CharField(max_length=200)
    netflix_id = models.CharField(
        max_length=20,
        blank=True)
    media_type = models.CharField(
        max_length=1,
        choices=TYPE)
    season = models.ForeignKey(
        'channel.Season',
        null=True)
    episodeNum =  models.IntegerField(
        null=True,
        blank=True)
    year = models.CharField(max_length=4,
        blank=True,
        null=True)
    runtime = models.IntegerField(default=0,
        blank=True,
        null=True)

    def __str__(self):
        return '{}'.format(self.name)
