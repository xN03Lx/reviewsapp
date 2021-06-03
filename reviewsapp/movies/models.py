from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator

from reviewsapp.celebrities.models import Celebrity
from reviewsapp.core.models import Review
from reviewsapp.core.behaviors import Filmable, TimestampableW


class Movie(Filmable, Timestampable, models.Model):
    crew = models.ManytoMany(Celebrity, related_name='movies', through='MovieCrew')
    cast = models.ManyToMany(Celebrity, related_name="cast_movie", related_query_name="movies")
    year_of_production = models.DateField()
    director = models.ForeignKey(
        Celebrity,
        on_delete=models.SET_NULL,
        null=True,
        related_name="movies"
    )


class MovieCrew(models.Model):
    JOBS = (
        ('director', 'DIRECTOR'),
        ('producer', 'PRODUCER'),
        ('actor', 'ACTOR'),
        ('writer', 'WRITER')
    )
    celebrity = models.ForeignKey(Celebrity, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    job = models.CharField(choices=JOBS, max_length=20)

class Review(models.Model):
    TYPE_OF_REVIEW = (
        ('by_critic' , 'by critic'),
        ('by_audience' , 'by audience'),
    )

    user = models.ForeignKey(get_user_model())
    comment = models.TextField()
    rating = models.FloatField(
        default=1, validators=[MaxValueValidator(5), MinValueValidator(1)]
    )
    type_of_review = models.CharField(choices=TYPE_OF_REVIEW, max_length=20)

    movie = models.ForeignKey(
        Movie, related_name="reviews", on_delete=models.CASCADE
    )
