from django.db import models
from reviewsapp.celebrities.models import Celebrity
from reviewsapp.core.behaviors import Filmable, Timestampable



class Network(models.Model):
    name = models.CharField(max_length=100)


class TvShow(Filmable, Timestampable, models.Model):
    premiere_date = models.DateField()
    cast_crew = models.ManytoMany(Celebrity, related_name='tvshows', through='tvShowCastCrew')
    creators = models.ManytoMany(Celebrity)
    network = models.ForeignKey(Network, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

class Crew(models.Model):
    celebrity = models.ForeignKey(Celebrity, on_delete=models.CASCADE)
    tv_show = models.ForeignKey(TvShow, on_delete=models.CASCADE)

class TvSeason(models.Model):
    pass

class TvEpisode(models.Model):
    pass

